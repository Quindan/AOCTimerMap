# InvictaWeb - Guild Hub

A comprehensive platform for Ashes of Creation guild management, featuring an interactive resource timer map, guild sheets, vendor optimization tools, and more.

## 🏗️ **Platform Architecture**

InvictaWeb combines multiple guild services in a single, easy-to-deploy platform:

- **🌐 Main Portal**: Landing page and navigation hub  
- **🗺️ AOC Timer Map**: Interactive resource map with 230+ named mob timers
- **👥 Guild Sheets**: Member management and raid planning *(coming soon)*
- **💰 Vendor Optimizer**: Trade route and pricing tools *(planned)*
- **📚 API Documentation**: Complete API reference

### **Service Routing**
- `/` → Main portal (landing page)
- `/map/` → AOC Timer Map  
- `/guild/` → Guild management *(beta)*
- `/vendor/` → Vendor tools *(planned)*
- `/api-docs/` → API documentation

## 🚀 **Quick Start**

### **Full Platform Deployment (Recommended)**

```bash
# 1. Initialize database and directories
make create

# 2. Build the platform
make hub-build

# 3. Start all services
make start

# 4. Access services
# Portal: http://localhost:9090/
# Map: http://localhost:9090/map/
# API Docs: http://localhost:9090/api-docs/
# Health: http://localhost:9090/health
```

**Default Login**: `invicta` / `password`

### **Individual Service Development**

```bash
# Start just the timer map (legacy mode)
make run

# Start with Docker Compose profiles
make compose-dev    # Development environment
make compose-feature # Feature testing
```

## 📁 **Project Structure**

```
InvictaWeb/
├── services/                 # Individual applications
│   ├── main-portal/          # Landing page & navigation
│   ├── aoc-timer-map/        # Timer map (your current project)
│   ├── guild-sheets/         # Guild management (planned)
│   └── vendor-trash/         # Vendor optimization (planned)
├── shared/                   # Shared components
│   ├── auth/                 # Common authentication
│   ├── ui-components/        # Shared Angular components
│   ├── database/             # Database utilities
│   └── utils/                # Common utilities
├── infrastructure/           # Deployment & operations
│   ├── nginx/                # Reverse proxy configs
│   ├── supervisor/           # Process management
│   └── ssl/                  # SSL certificates
├── deployment/               # Environment configs
├── src/                      # Built application files
└── docs/                     # Documentation
```

## 🎯 **AOC Timer Map Features**

### **Interactive Resource Map**
- Click-to-place resource markers with respawn timers
- Real-time updates shared across all guild members
- Visual timer states: blue (available), red (cooldown), yellow (missing)
- Custom resource types with icons
- Export/import marker configurations

### **Named Mob Timers** 
- Track 230+ named mobs from Ashes Codex API
- Automatic respawn time calculations
- Kill tracking and timer management
- Search and filter by mob name/location
- Notes and guild coordination features

### **Controls**
- **R**: Reset timer (when you kill/harvest)
- **M**: Mark as missing (when someone else got it)
- **Click**: View details and manage timers

## 🔧 **Development Commands**

### **Platform Commands**
```bash
make hub-build         # Build platform container
make start             # Start all services (alias for hub-start)
make logs              # View logs (alias for hub-logs)  
make stop              # Stop all services (alias for hub-stop)
```

### **Database Management**
```bash
make create            # Initialize database
make import-named-mobs # Import named mobs data
make fetch-named-mobs  # Update named mobs from API
```

### **Legacy Single Service**
```bash
make install           # Install dependencies
make build            # Build containers
make run              # Start timer map only
make logs             # View container logs
make error-logs       # Detailed error debugging
```

### **Docker Compose Profiles**
```bash
make compose-dev       # Development environment (port 8080)
make compose-feature   # Feature testing (port 8081)
make deploy-branch     # Deploy specific branch
```

## 🔐 **Authentication**

All services use HTTP Basic Authentication:

- **Username**: `invicta`
- **Password**: `invicta` (default)

To change the password:
```bash
# Generate new .htpasswd
htpasswd -c .htpasswd invicta

# Or update in container
make addUser
```

## 🗄️ **Database**

- **Type**: SQLite
- **Location**: `./db/mydb.sqlite`
- **Backup**: Automatic with Docker volumes
- **Schema**: Auto-migration on startup

### **Tables**
- `markers`: Resource markers and timers
- `named_mobs`: Named mob timer entries  
- `named_mobs_static`: Static mob data from Ashes Codex

## 🌐 **API Endpoints**

### **Resource Markers**
- `GET /api.php` - Get all markers
- `POST /api.php` - Create marker
- `PUT /api.php` - Update marker
- `DELETE /api.php` - Remove marker

### **Named Mobs**
- `GET /named_mobs_api.php` - Get timers
- `POST /named_mobs_api.php` - Create timer
- `PUT /named_mobs_api.php` - Update timer
- `DELETE /named_mobs_api.php` - Remove timer
- `POST /named_mobs_api.php/import` - Import mob data

### **Health & Status**
- `GET /health` - Service health check
- Returns JSON with service status and timestamp

## 📊 **Monitoring**

- **Health Checks**: `/health` endpoint
- **Logs**: Nginx + PHP logs via Docker
- **Metrics**: Container resource usage
- **Uptime**: Supervisor process management

## 🚧 **Roadmap**

### **Phase 1: Current (Completed)**
- ✅ Monolith architecture setup
- ✅ Main portal with service navigation
- ✅ AOC Timer Map integration
- ✅ Named mobs feature (230+ mobs)
- ✅ API documentation
- ✅ Docker deployment

### **Phase 2: Guild Management (In Progress)**
- 🚧 Guild member roster
- 🚧 Raid planning and signups
- 🚧 Resource contribution tracking
- 🚧 Performance analytics

### **Phase 3: Vendor Optimization (Planned)**
- 📋 Real-time vendor pricing
- 📋 Trade route calculation
- 📋 Profit optimization tools
- 📋 Market trend analysis

### **Phase 4: Enhanced Features (Future)**
- 📋 Mobile app
- 📋 Discord integration
- 📋 Advanced analytics
- 📋 Multi-guild support

## 🤝 **Contributing**

This is built for the Invicta guild, but contributions are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📜 **License**

Built for the Ashes of Creation community. Use freely for your guild's needs.

---

**Made with ⚔️ by the Invicta Guild for the AOC community**