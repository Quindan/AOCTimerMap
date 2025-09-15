# InvictaWeb Architecture Proposal

## 🏗️ **Hybrid Monorepo Architecture**

This architecture provides monolith benefits (single repo, easy deployment) with modular maintenance (independent services).

## 📋 **Service Directory**

### **Core Services**

| Service | URL Route | Technology | Purpose |
|---------|-----------|------------|---------|
| **Main Portal** | `/` | Angular | Landing page, navigation hub |
| **AOC Timer Map** | `/map/` | Angular + PHP | Resource map, named mob timers |
| **Guild Sheets** | `/guild/` | Angular + Node.js | Member management, raids |
| **API Gateway** | `/api/` | Nginx + PHP | Centralized API routing |

### **Shared Services**

| Component | Purpose | Used By |
|-----------|---------|---------|
| **Authentication** | Single sign-on, JWT tokens | All services |
| **UI Components** | Guild theming, common widgets | Frontend services |
| **Database Utils** | Shared database access, migrations | Backend services |
| **Monitoring** | Logging, health checks, metrics | All services |

## 🌐 **URL Structure**

```
https://invicta.your-domain.com/
├── /                          # Main portal (landing page)
├── /map/                      # AOC Timer Map
│   ├── /map/resources         # Resource map view
│   ├── /map/named-mobs        # Named mob timers
│   └── /map/api/              # Map-specific APIs
├── /guild/                    # Guild management
│   ├── /guild/roster          # Member roster
│   ├── /guild/raids           # Raid planning
│   └── /guild/resources       # Resource tracking
├── /api/                      # Centralized API gateway
│   ├── /api/auth/             # Authentication
│   ├── /api/map/              # Map APIs
│   └── /api/guild/            # Guild APIs
└── /admin/                    # Administrative tools
```

## 🐳 **Docker Architecture**

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Reverse proxy and SSL termination
  nginx:
    image: nginx:alpine
    ports: ["80:80", "443:443"]
    volumes:
      - ./infrastructure/nginx:/etc/nginx/conf.d
      - ./infrastructure/ssl:/etc/ssl
    depends_on: [main-portal, aoc-timer-map, guild-sheets]

  # Main landing page and navigation
  main-portal:
    build: ./services/main-portal
    expose: ["4200"]
    environment:
      - NODE_ENV=production
      - API_URL=http://nginx/api

  # Your current AOC Timer Map project
  aoc-timer-map:
    build: ./services/aoc-timer-map
    expose: ["80"]
    volumes:
      - ./shared/database/map:/var/www/db
      - ./shared/uploads:/var/www/uploads
    environment:
      - PHP_ENV=production
      - DB_PATH=/var/www/db/mydb.sqlite

  # Guild management tools
  guild-sheets:
    build: ./services/guild-sheets
    expose: ["3000"]
    volumes:
      - ./shared/database/guild:/app/data
    environment:
      - NODE_ENV=production
      - DATABASE_URL=sqlite:///app/data/guild.sqlite

  # Shared database service (optional)
  database:
    image: postgres:15
    volumes:
      - ./shared/database/postgres:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=invictaweb
      - POSTGRES_USER=invicta
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
```

## 🔧 **Development Workflow**

### **Option 1: Full Stack Development**
```bash
# Start all services for full integration testing
docker-compose up

# Access services:
# http://localhost/         → Main portal
# http://localhost/map/     → AOC Timer Map
# http://localhost/guild/   → Guild Sheets
```

### **Option 2: Single Service Development**
```bash
# Work on just the map (current workflow)
docker-compose up aoc-timer-map

# Work on just the guild tools
docker-compose up guild-sheets main-portal
```

### **Option 3: Hybrid Development**
```bash
# Run services you're not working on
docker-compose up nginx main-portal guild-sheets

# Run map locally for development
cd services/aoc-timer-map
make compose-dev  # Your existing workflow
```

## 📂 **File Organization**

```
InvictaWeb/
├── README.md                 # Main project overview
├── docker-compose.yml        # Development environment
├── docker-compose.prod.yml   # Production environment
├── .env.example              # Environment template
├── .gitignore                # Global ignore patterns
│
├── services/                 # Individual applications
│   ├── main-portal/          # Landing page & navigation
│   │   ├── src/app/
│   │   ├── dockerfile
│   │   ├── package.json
│   │   └── README.md
│   ├── aoc-timer-map/        # Your current project (moved)
│   │   ├── src/              # PHP API + Angular build
│   │   ├── dev/              # Angular development
│   │   ├── docker/           # Existing docker config
│   │   ├── dockerfile        # Existing dockerfile
│   │   ├── makefile          # Existing makefile
│   │   └── README.md
│   └── guild-sheets/         # Guild management
│       ├── frontend/         # Angular app
│       ├── backend/          # Node.js API
│       ├── dockerfile
│       └── README.md
│
├── shared/                   # Shared components
│   ├── auth/                 # Authentication utilities
│   │   ├── jwt-service.ts
│   │   ├── auth-guard.ts
│   │   └── user.interface.ts
│   ├── ui-components/        # Angular shared components
│   │   ├── guild-header/
│   │   ├── navigation-menu/
│   │   └── invicta-theme/
│   ├── database/             # Database utilities
│   │   ├── migrations/
│   │   ├── seeders/
│   │   └── backup-scripts/
│   └── utils/                # Common utilities
│       ├── logger.ts
│       ├── config.ts
│       └── validators.ts
│
├── infrastructure/           # Deployment & operations
│   ├── nginx/                # Reverse proxy configuration
│   │   ├── default.conf
│   │   ├── ssl.conf
│   │   └── routes.conf
│   ├── ssl/                  # SSL certificates
│   ├── monitoring/           # Logging & monitoring
│   │   ├── prometheus/
│   │   ├── grafana/
│   │   └── loki/
│   └── backup/               # Backup scripts
│
├── deployment/               # Deployment configurations
│   ├── development.yml       # Dev environment
│   ├── staging.yml           # Staging environment
│   ├── production.yml        # Production environment
│   └── scripts/              # Deployment automation
│       ├── deploy.sh
│       ├── backup.sh
│       └── health-check.sh
│
└── docs/                     # Documentation
    ├── architecture/         # System design docs
    ├── api/                  # API documentation
    ├── deployment/           # Deployment guides
    └── development/          # Development guides
```

## 🎯 **Key Benefits for Your Use Case**

### **Cursor AI Context**
- ✅ Single repository for better code understanding
- ✅ Cross-service refactoring and search
- ✅ Shared types and interfaces
- ✅ Unified development environment

### **Easy Production**
- ✅ Single `docker-compose up` for full deployment
- ✅ Shared SSL certificates and domain
- ✅ Unified monitoring and logging
- ✅ Consistent backup and disaster recovery

### **Modular Maintenance**
- ✅ Independent service development
- ✅ Technology flexibility (PHP, Node.js, Python, etc.)
- ✅ Clear service boundaries
- ✅ Independent scaling and updates

## 🚀 **Next Steps**

1. **Immediate**: Test the named mobs feature in current deployment
2. **Week 1**: Create the main portal structure in InvictaWeb
3. **Week 2**: Migrate AOCTimerMap as first service
4. **Week 3**: Add guild management service
5. **Week 4**: Polish and production deployment

This architecture gives you the **monolith benefits** you want for development and deployment while maintaining the **modular flexibility** for long-term maintenance and growth.

