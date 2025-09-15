# InvictaWeb Migration Plan

## Phase 1: Setup Main Portal (Week 1)

### 1.1 Create Main Portal Service
```bash
# In InvictaWeb repository
mkdir -p services/main-portal/src
cd services/main-portal
ng new . --routing --style=scss
```

### 1.2 Main Portal Features
- **Landing Page**: Guild branding, news, announcements
- **Navigation Hub**: Cards/links to all services
- **User Authentication**: Single sign-on for all tools
- **Service Status**: Health checks for all services

### 1.3 Main Portal Structure
```
services/main-portal/
├── src/app/
│   ├── landing/              # Welcome page
│   ├── navigation/           # Service directory
│   ├── auth/                 # Login/logout
│   └── shared/               # Common components
├── dockerfile
└── package.json
```

## Phase 2: Migrate AOC Timer Map (Week 2)

### 2.1 Move Current Project
```bash
# Copy AOCTimerMap to InvictaWeb
cp -r AOCTimerMap/ InvictaWeb/services/aoc-timer-map/
```

### 2.2 Update Routing
- Configure nginx to route `/map/*` → aoc-timer-map service
- Update API endpoints to `/api/map/*`
- Maintain existing functionality

### 2.3 Integration Points
- Use shared authentication from main portal
- Apply consistent guild theming
- Add navigation back to main portal

## Phase 3: Add Guild Sheets Service (Week 3)

### 3.1 Create Guild Management Service
```
services/guild-sheets/
├── src/
│   ├── member-management/     # Guild roster
│   ├── raids/                 # Raid planning
│   ├── resources/             # Resource tracking
│   └── reports/               # Guild statistics
├── api/                       # Backend for guild data
└── dockerfile
```

### 3.2 Features
- Guild member roster and roles
- Raid signup and planning
- Resource contribution tracking
- Performance analytics

## Phase 4: Infrastructure & Deployment (Week 4)

### 4.1 Docker Compose Orchestration
```yaml
# docker-compose.yml
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports: ["80:80", "443:443"]
    volumes: ["./infrastructure/nginx:/etc/nginx"]
  
  main-portal:
    build: ./services/main-portal
    expose: ["4200"]
  
  aoc-timer-map:
    build: ./services/aoc-timer-map
    expose: ["80"]
    volumes: ["./shared/database:/var/www/db"]
  
  guild-sheets:
    build: ./services/guild-sheets
    expose: ["3000"]
```

### 4.2 Nginx Reverse Proxy
```nginx
# Route traffic to appropriate services
location / {
    proxy_pass http://main-portal:4200;
}
location /map/ {
    proxy_pass http://aoc-timer-map:80/;
}
location /guild/ {
    proxy_pass http://guild-sheets:3000/;
}
```

## Phase 5: Shared Services (Ongoing)

### 5.1 Shared Authentication
```
shared/auth/
├── jwt-service.ts            # Token management
├── auth-guard.ts             # Route protection
└── user-service.ts           # User data
```

### 5.2 Shared UI Components
```
shared/ui-components/
├── guild-header/             # Common header
├── navigation-menu/          # Service navigation
├── user-profile/             # User dropdown
└── invicta-theme/            # Guild styling
```

### 5.3 Shared Database Utilities
```
shared/database/
├── migrations/               # Database schema
├── seeders/                  # Initial data
└── backup-scripts/           # Data backup
```

## Deployment Commands

### Development
```bash
docker-compose -f deployment/development.yml up -d
```

### Production
```bash
docker-compose -f deployment/production.yml up -d
```

### Service-Specific Development
```bash
# Work on just the map
docker-compose up aoc-timer-map

# Work on just the guild sheets
docker-compose up guild-sheets
```

## Benefits Summary

### 🎯 **For Development (Cursor Context)**
- Single repository with all related code
- Cross-service refactoring and search
- Shared dependencies and configurations
- Unified development environment

### 🎯 **For Production (Easy Deployment)**
- Single docker-compose deployment
- Shared SSL certificates and domains
- Unified monitoring and logging
- Consistent backup strategies

### 🎯 **For Maintenance (Modularity)**
- Independent service development
- Clear service boundaries
- Technology flexibility per service
- Independent scaling and updates

## Migration Risks & Mitigation

### Risk: Disruption to Current Map
**Mitigation**: 
- Keep current deployment running
- Migrate incrementally
- Test thoroughly in development

### Risk: Complexity Increase
**Mitigation**:
- Start simple with basic routing
- Add features incrementally
- Document everything clearly

### Risk: Performance Impact
**Mitigation**:
- Use nginx caching
- Optimize Docker images
- Monitor performance metrics

