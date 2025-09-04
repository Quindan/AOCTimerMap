#!/bin/bash

# Branch Deployment Script for AOC Timer Map
# Usage: ./scripts/branch-deploy.sh [branch-name] [environment]
# Example: ./scripts/branch-deploy.sh feature/named-timers feature

set -e

# Configuration
REPO_URL="https://github.com/Quindan/AOCTimerMap.git"
PROJECT_DIR="/var/www/aoctimermap"
BACKUP_DIR="/var/backups/aoctimermap"

# Default values
BRANCH=${1:-"main"}
ENVIRONMENT=${2:-"development"}
PORT=${3:-"8080"}

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

# Function to validate environment
validate_environment() {
    case "$ENVIRONMENT" in
        "production"|"development"|"testing"|"feature")
            log "Environment: $ENVIRONMENT"
            ;;
        *)
            error "Invalid environment: $ENVIRONMENT. Use: production, development, testing, or feature"
            ;;
    esac
}

# Function to backup current deployment
backup_deployment() {
    if [ -d "$PROJECT_DIR" ]; then
        log "Creating backup of current deployment..."
        mkdir -p "$BACKUP_DIR"
        BACKUP_NAME="backup-$(date +%Y%m%d-%H%M%S)"
        cp -r "$PROJECT_DIR" "$BACKUP_DIR/$BACKUP_NAME"
        success "Backup created: $BACKUP_DIR/$BACKUP_NAME"
    fi
}

# Function to deploy branch
deploy_branch() {
    log "Deploying branch: $BRANCH to environment: $ENVIRONMENT"
    
    # Create project directory if it doesn't exist
    mkdir -p "$PROJECT_DIR"
    cd "$PROJECT_DIR"
    
    # Clone or update repository
    if [ -d ".git" ]; then
        log "Updating existing repository..."
        git fetch origin
        git checkout "$BRANCH" || error "Branch '$BRANCH' not found"
        git pull origin "$BRANCH"
    else
        log "Cloning repository..."
        git clone -b "$BRANCH" "$REPO_URL" .
    fi
    
    success "Code deployment completed"
}

# Function to setup environment
setup_environment() {
    log "Setting up environment for $ENVIRONMENT..."
    
    # Create environment-specific database directory
    DB_DIR="db"
    if [ "$ENVIRONMENT" != "production" ]; then
        DB_DIR="db-$ENVIRONMENT"
    fi
    
    mkdir -p "$DB_DIR"
    touch "$DB_DIR/mydb.sqlite"
    
    # Set permissions
    sudo chown -R www-data:www-data src "$DB_DIR"
    sudo chmod -R ug+rw src "$DB_DIR"
    
    # Create .htpasswd if it doesn't exist
    if [ ! -f "docker/nginx/.htpasswd" ]; then
        mkdir -p docker/nginx
        htpasswd -cb docker/nginx/.htpasswd invicta invicta
        success "Created default .htpasswd (invicta:invicta)"
    fi
    
    success "Environment setup completed"
}

# Function to deploy with docker-compose
deploy_docker_compose() {
    log "Deploying with docker-compose..."
    
    # Determine service name and profile
    SERVICE_NAME="aoctimermap-main"
    PROFILE=""
    
    case "$ENVIRONMENT" in
        "development")
            SERVICE_NAME="aoctimermap-dev"
            PROFILE="--profile dev"
            PORT="8080"
            ;;
        "testing"|"feature")
            SERVICE_NAME="aoctimermap-feature"
            PROFILE="--profile feature"
            PORT="8081"
            ;;
        "production")
            SERVICE_NAME="aoctimermap-main"
            PORT="80"
            ;;
    esac
    
    # Stop existing service
    docker-compose stop "$SERVICE_NAME" 2>/dev/null || true
    docker-compose rm -f "$SERVICE_NAME" 2>/dev/null || true
    
    # Build and start service
    docker-compose build "$SERVICE_NAME"
    docker-compose up -d $PROFILE "$SERVICE_NAME"
    
    success "Docker service '$SERVICE_NAME' deployed on port $PORT"
}

# Function to import named mobs data
import_named_mobs() {
    if [ -f "scripts/fetch_named_mobs.php" ]; then
        log "Importing named mobs data..."
        php scripts/fetch_named_mobs.php
        
        if [ -f "data/named_mobs.sql" ]; then
            DB_FILE="db/mydb.sqlite"
            if [ "$ENVIRONMENT" != "production" ]; then
                DB_FILE="db-$ENVIRONMENT/mydb.sqlite"
            fi
            
            sqlite3 "$DB_FILE" < data/named_mobs.sql
            success "Named mobs data imported"
        fi
    fi
}

# Function to run tests
run_tests() {
    log "Running basic health checks..."
    
    # Wait for service to be ready
    sleep 5
    
    # Test HTTP response
    HEALTH_URL="http://localhost:$PORT"
    if curl -f -s "$HEALTH_URL" > /dev/null; then
        success "Service is responding on port $PORT"
    else
        warning "Service may not be ready yet on port $PORT"
    fi
    
    # Test API endpoint
    API_URL="http://localhost:$PORT/api.php"
    if curl -f -s "$API_URL" > /dev/null; then
        success "API endpoint is accessible"
    else
        warning "API endpoint may not be ready"
    fi
}

# Function to show deployment summary
show_summary() {
    echo ""
    echo "================================================"
    echo "🚀 Deployment Summary"
    echo "================================================"
    echo "Branch: $BRANCH"
    echo "Environment: $ENVIRONMENT"
    echo "Port: $PORT"
    echo "Service: $SERVICE_NAME"
    echo "URL: http://$(hostname -I | awk '{print $1}'):$PORT"
    echo "API: http://$(hostname -I | awk '{print $1}'):$PORT/api.php"
    echo "Named Mobs: http://$(hostname -I | awk '{print $1}'):$PORT/named_mobs_api.php"
    echo "================================================"
    echo ""
    echo "🔧 Useful commands:"
    echo "  docker-compose logs $SERVICE_NAME     # View logs"
    echo "  docker-compose stop $SERVICE_NAME     # Stop service"
    echo "  docker-compose restart $SERVICE_NAME  # Restart service"
    echo "================================================"
}

# Main execution
main() {
    log "Starting branch deployment script..."
    log "Branch: $BRANCH, Environment: $ENVIRONMENT, Port: $PORT"
    
    validate_environment
    backup_deployment
    deploy_branch
    setup_environment
    deploy_docker_compose
    import_named_mobs
    run_tests
    show_summary
    
    success "Deployment completed successfully! 🎉"
}

# Show usage if no arguments provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 [branch-name] [environment] [port]"
    echo ""
    echo "Arguments:"
    echo "  branch-name   Git branch to deploy (default: main)"
    echo "  environment   Deployment environment: production, development, testing, feature (default: development)"
    echo "  port         Port to run on (default: 8080)"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Deploy main branch in development"
    echo "  $0 feature/named-timers feature      # Deploy feature branch for testing"
    echo "  $0 main production                   # Deploy main branch in production"
    echo "  $0 develop development 8082          # Deploy develop branch on port 8082"
    exit 1
fi

# Run main function
main
