# AOC Timer Map Service

This service provides the interactive resource map and named mob timer functionality for InvictaWeb.

## Features

- ✅ **Interactive Resource Map**: Click-to-place resource markers with respawn timers
- ✅ **Named Mob Timers**: Track 230+ named mobs with automatic respawn calculations  
- ✅ **Real-time Updates**: Live timer updates and spawn notifications
- ✅ **Export/Import**: Save and load marker configurations
- ✅ **Multi-user Support**: Shared guild resource tracking

## Technology Stack

- **Frontend**: Angular 17+ (dev/src/)
- **Backend**: PHP 8+ with SQLite database
- **Container**: Docker with PHP-FPM + Nginx
- **Database**: SQLite with automatic schema migration

## API Endpoints

### Resource Markers
- `GET /api.php` - Get all markers
- `POST /api.php` - Create new marker
- `PUT /api.php` - Update marker  
- `DELETE /api.php` - Remove marker

### Named Mobs
- `GET /named_mobs_api.php` - Get all named mob timers
- `POST /named_mobs_api.php` - Create timer entry
- `PUT /named_mobs_api.php` - Update timer
- `DELETE /named_mobs_api.php` - Remove timer
- `POST /named_mobs_api.php/import` - Import named mobs data

## Development

```bash
# Run development server
cd dev && npm start

# Build for production  
cd dev && npm run build

# Run in Docker
docker-compose up
```

## Database Schema

### markers table
- `id` - Primary key
- `x`, `y` - Map coordinates  
- `type` - Resource type (iron, wood, etc.)
- `respawn_time` - Seconds until respawn
- `missing` - Time until available (default 1800s)
- `rarity` - Resource rarity (common, uncommon, rare)

### named_mobs table  
- `id` - Primary key
- `mob_id` - Reference to static mob data
- `killed_at` - Timestamp of kill
- `respawn_at` - Calculated respawn time
- `notes` - User notes
- `created_at` - Record creation time

### named_mobs_static table
- `id` - Primary key  
- `name` - Display name
- `respawn_time` - Base respawn time in minutes
- `slug` - URL slug
- `location` - Spawn location
- `level_range` - Level requirement

## Integration

This service integrates with the main InvictaWeb portal:

- **Route**: `/map/*` → AOC Timer Map
- **Authentication**: Shared HTTP Basic Auth
- **Theme**: Consistent guild branding
- **Navigation**: Back to main portal

## Deployment

The service runs as part of the InvictaWeb monolith via Docker Compose with nginx routing.
