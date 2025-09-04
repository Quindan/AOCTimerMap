# Docker Compose Deployment Guide

This document explains how to use the docker-compose setup for testing different branches on the server.

## 🏗️ Architecture Overview

The docker-compose setup provides **3 separate environments**:

| Environment | Service Name | Port | Database | Use Case |
|-------------|--------------|------|----------|----------|
| **Production** | `aoctimermap-main` | 80 | `db/` | Main production deployment |
| **Development** | `aoctimermap-dev` | 8080 | `db-dev/` | Development testing |
| **Feature** | `aoctimermap-feature` | 8081 | `db-feature/` | Feature branch testing |

## 🚀 Quick Start Commands

### Basic Operations

```bash
# Start production service
make compose-up

# Start development service (port 8080)
make compose-dev

# Start feature testing service (port 8081)
make compose-feature

# Stop all services
make compose-down
```

### Branch Deployment

```bash
# Deploy main branch to development
make deploy-branch BRANCH=main ENV=development

# Deploy feature branch for testing
make deploy-branch BRANCH=feature/named-timers ENV=feature

# Deploy to production
make deploy-branch BRANCH=main ENV=production
```

## 📁 File Structure

```
AOCTimerMap/
├── docker-compose.yml          # Main compose configuration
├── docker-compose.override.yml # Local development overrides
├── scripts/
│   └── branch-deploy.sh        # Automated branch deployment
├── db/                         # Production database
├── db-dev/                     # Development database
├── db-feature/                 # Feature testing database
└── src/                        # Application source code
```

## 🔧 Advanced Usage

### Manual Docker Compose Commands

```bash
# Build all images
docker-compose build

# Start specific service
docker-compose up -d aoctimermap-dev

# View logs
docker-compose logs aoctimermap-dev
docker-compose logs -f aoctimermap-feature  # Follow logs

# Stop specific service
docker-compose stop aoctimermap-dev

# Remove service
docker-compose rm aoctimermap-dev

# Start with specific profile
docker-compose --profile dev up -d
docker-compose --profile feature up -d
```

### Environment Variables

Services support environment variables:

- `BRANCH`: Git branch name
- `ENVIRONMENT`: deployment environment (production/development/testing/feature)
- `DEBUG`: Enable debug mode (true/false)
- `LOG_LEVEL`: Logging level (debug/info/warn/error)

## 🌐 Service URLs

After deployment, services are available at:

- **Production**: `http://your-server-ip/`
- **Development**: `http://your-server-ip:8080/`
- **Feature**: `http://your-server-ip:8081/`

### API Endpoints

Each service exposes the same API endpoints:

- **Main API**: `/api.php`
- **Named Mobs API**: `/named_mobs_api.php`
- **Health Check**: `/` (basic HTTP response)

## 🔄 Branch Testing Workflow

### 1. Testing a New Feature Branch

```bash
# 1. Deploy the feature branch
make deploy-branch BRANCH=feature/named-timers ENV=feature

# 2. Service will be available on port 8081
# 3. Test the feature at http://your-server:8081

# 4. View logs if needed
docker-compose logs aoctimermap-feature

# 5. Stop when testing is complete
docker-compose stop aoctimermap-feature
```

### 2. Development Testing

```bash
# 1. Start development service
make compose-dev

# 2. Test at http://your-server:8080

# 3. Deploy different branches as needed
make deploy-branch BRANCH=develop ENV=development
```

### 3. Production Deployment

```bash
# 1. Test in development first
make deploy-branch BRANCH=main ENV=development

# 2. If tests pass, deploy to production
make deploy-branch BRANCH=main ENV=production

# 3. Service available on port 80
```

## 🗄️ Database Management

Each environment has its own database:

```bash
# Access production database
sqlite3 db/mydb.sqlite

# Access development database
sqlite3 db-dev/mydb.sqlite

# Access feature database
sqlite3 db-feature/mydb.sqlite

# Import named mobs to specific database
sqlite3 db-feature/mydb.sqlite < data/named_mobs.sql
```

## 🔒 Authentication

All services use the same `.htpasswd` file:

```bash
# Create/update authentication
make addUser USER=username

# Default credentials: invicta:invicta
```

## 📋 Monitoring & Debugging

### View Service Status

```bash
# List running containers
docker-compose ps

# Check service health
curl -I http://localhost:8080/
curl -I http://localhost:8081/
```

### Logs and Debugging

```bash
# View all logs
docker-compose logs

# Follow specific service logs
docker-compose logs -f aoctimermap-dev

# Execute commands in container
docker-compose exec aoctimermap-dev bash

# Check nginx status
docker-compose exec aoctimermap-dev nginx -t
```

### Troubleshooting

Common issues and solutions:

1. **Port conflicts**: Check if ports are already in use
   ```bash
   netstat -tlnp | grep :8080
   ```

2. **Permission issues**: Ensure database directories have correct permissions
   ```bash
   sudo chown -R www-data:www-data db-dev/
   sudo chmod -R ug+rw db-dev/
   ```

3. **Service won't start**: Check logs for errors
   ```bash
   docker-compose logs aoctimermap-dev
   ```

## 🚨 Production Considerations

### Security

- Use strong authentication credentials
- Limit access to development/testing ports (8080, 8081)
- Consider using SSL/TLS for production

### Performance

- Monitor resource usage with multiple services
- Use separate databases for isolation
- Consider container resource limits for production

### Backup

```bash
# Backup production database
cp db/mydb.sqlite backups/mydb-$(date +%Y%m%d).sqlite

# Backup entire project
tar -czf aoctimermap-backup-$(date +%Y%m%d).tar.gz .
```

## 📝 Branch Deployment Script Features

The `scripts/branch-deploy.sh` script provides:

- ✅ Automatic git branch switching
- ✅ Environment-specific database setup
- ✅ Docker service management
- ✅ Named mobs data import
- ✅ Health checks
- ✅ Deployment summary
- ✅ Backup creation
- ✅ Permission management

### Script Usage

```bash
# Basic usage
./scripts/branch-deploy.sh [branch-name] [environment] [port]

# Examples
./scripts/branch-deploy.sh feature/named-timers feature
./scripts/branch-deploy.sh main production
./scripts/branch-deploy.sh develop development 8082
```

## 🎯 Best Practices

1. **Always test in development** before production deployment
2. **Use feature environment** for feature branch testing
3. **Monitor logs** during deployment
4. **Backup databases** before major changes
5. **Use consistent naming** for branches and environments
6. **Clean up** unused services to save resources

This setup allows you to safely test multiple branches simultaneously without affecting production! 🚀
