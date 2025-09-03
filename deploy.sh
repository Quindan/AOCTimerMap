#!/bin/bash

# AOCTimerMap Deployment Script
# This script sets up the server and deploys the application

SERVER="root@84.247.141.193"
DEPLOY_PATH="/var/www/aoctimermap"

echo "🚀 Starting AOCTimerMap deployment..."

# Function to run commands on server
run_on_server() {
    echo "Running on server: $1"
    ssh $SERVER "$1"
}

# Function to check if command succeeded
check_success() {
    if [ $? -eq 0 ]; then
        echo "✅ $1"
    else
        echo "❌ $1 failed"
        exit 1
    fi
}

echo "📡 Testing SSH connection..."
ssh -o ConnectTimeout=5 $SERVER "echo 'SSH connection successful'"
check_success "SSH connection test"

echo "📦 Setting up server environment..."
run_on_server "apt update -y"
check_success "System update"

run_on_server "command -v docker >/dev/null 2>&1 || (curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh)"
check_success "Docker installation"

run_on_server "apt install -y make git"
check_success "Essential tools installation"

run_on_server "mkdir -p $DEPLOY_PATH"
check_success "Directory creation"

echo "📁 Copying project files..."
scp -r . $SERVER:$DEPLOY_PATH/
check_success "File transfer"

echo "🏗️ Building and starting application..."
run_on_server "cd $DEPLOY_PATH && make install"
check_success "Make install"

run_on_server "cd $DEPLOY_PATH && make build"
check_success "Docker build"

run_on_server "cd $DEPLOY_PATH && make run"
check_success "Application start"

echo "🔍 Checking application status..."
run_on_server "docker ps | grep aoctimermap"
check_success "Container status check"

echo ""
echo "🎉 Deployment completed successfully!"
echo "📍 Your application should be available at: http://84.247.141.193"
echo ""
echo "📊 To check logs: ssh $SERVER 'docker logs aoctimermap_container'"
echo "🔄 To restart: ssh $SERVER 'cd $DEPLOY_PATH && make restart'"
echo "⏹️  To stop: ssh $SERVER 'cd $DEPLOY_PATH && make stop'"

