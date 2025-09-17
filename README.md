# AOC Timer Map

Interactive resource map and named mob timer for Ashes of Creation guilds.

## 🚀 Quick Start

### Local Development
```bash
make local
```
**Access**: http://localhost:9090  
**Login**: `invicta` / `invicta`

### Production Deployment
```bash
make prod-deploy
```

## 🎯 Features

- ✅ **Interactive Map** - Click-to-place resource markers with timers
- ✅ **Named Mob Timers** - Track 208+ named mobs with precise positioning  
- ✅ **API Documentation** - Comprehensive API docs at `/api-docs/`
- ✅ **Database Persistence** - SQLite with automatic backups
- ✅ **Bookstack Integration** - Documentation system

## 🔧 Commands

| Command | Description |
|---------|-------------|
| `make local` | Start local development |
| `make prod-deploy` | Deploy to production |
| `make db-backup` | Backup database |
| `make logs` | View container logs |
| `make reset` | Reset containers |

## 📁 Structure

```
AOCTimerMap/
├── app/
│   ├── frontend-built/   # Built Angular app
│   ├── api/              # PHP APIs  
│   └── frontend-src/     # Angular source code
├── scripts/              # Temporary utility scripts (easy cleanup)
├── data/
│   ├── database/         # SQLite database
│   ├── named-mobs/       # Named mob data
│   └── backups/          # Database backups
├── bookstack/
│   ├── data/             # Bookstack application data
│   ├── database/         # Bookstack MySQL database
│   └── backups/          # Bookstack backups
├── docs/
│   ├── api/              # API documentation
│   ├── guidelines/       # Project guidelines
│   └── architecture/     # Technical documentation
├── infrastructure/       # Deployment configs
├── docker/               # Docker configuration
├── Dockerfile            # Production image
├── docker-compose.yml    # Container orchestration
└── Makefile             # Build/deploy commands
```

## 🌐 API Endpoints

- `GET /api.php` - Resource markers
- `GET /named_mobs_api.php` - Named mob timers  
- `GET /api-docs/` - API documentation
- `GET /health` - Health check

## 💾 Database Management

### Backup
```bash
make db-backup
```

### Restore
```bash
make db-restore FILE=backup_20240101_120000.sqlite
```

## 🔐 Authentication

Default credentials: `invicta` / `invicta`

## 📊 Named Mob Triangulation

The system uses 3 reference points for precise mob positioning:
- **Wormwig**: (-235.619, 137.396)
- **Ysshokk**: (-239.000, 144.375)  
- **Olive Bootshredder**: (-246.830, 110.336)

All 208+ named mobs are positioned relative to these reference points.