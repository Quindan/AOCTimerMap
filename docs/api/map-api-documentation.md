# AOC Timer Map API Documentation

## Overview

The AOC Timer Map API provides endpoints for managing map markers and named mob timers in Age of Conan. The API is built with PHP and uses SQLite for data persistence, offering both RESTful endpoints for marker management and specialized endpoints for named mob tracking.

## Base URL

```
http://84.247.141.193:80/map/
```

## Authentication

Currently, no authentication is required for API access. CORS headers are configured to allow cross-origin requests.

## Response Format

All API responses are returned in JSON format with the following structure:

**Success Response:**
```json
{
  "success": true,
  "data": [...],
  "message": "Optional success message"
}
```

**Error Response:**
```json
{
  "error": "Error description"
}
```

---

## Map Markers API

### Database Schema

The `markers` table contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | INTEGER | Primary key, auto-increment |
| `label` | TEXT | Display name for the marker |
| `lat` | REAL | Latitude coordinate |
| `lng` | REAL | Longitude coordinate |
| `startTime` | INTEGER | Start time in milliseconds (timestamp) |
| `alarmAfter` | INTEGER | Alarm delay in seconds (default: 1800) |
| `inGameCoord` | TEXT | In-game coordinate string |
| `type` | TEXT | Marker type (resource, mob, etc.) |
| `missing` | INTEGER | Missing duration in seconds |
| `rarity` | TEXT | Rarity level (default: 'common') |

### Endpoints

#### GET `/api.php`
**Description:** Retrieve all map markers

**Response:**
```json
[
  {
    "id": 1,
    "label": "Iron Ore Vein",
    "lat": 1234.56,
    "lng": 7890.12,
    "startTime": 1640995200000,
    "alarmAfter": 1800,
    "inGameCoord": "1234, 5678",
    "type": "resource",
    "missing": 1800,
    "rarity": "common"
  }
]
```

#### POST `/api.php?action=create`
**Description:** Create a new map marker

**Request Body:**
```json
{
  "label": "Gold Vein",
  "lat": 1234.56,
  "lng": 7890.12,
  "startTime": 1640995200000,
  "alarmAfter": 1800,
  "inGameCoord": "1234, 5678",
  "type": "resource",
  "rarity": "rare",
  "missing": 1800
}
```

**Response:**
```json
{
  "success": true,
  "marker": {
    "id": 2,
    "label": "Gold Vein",
    "lat": 1234.56,
    "lng": 7890.12,
    "startTime": 1640995200000,
    "alarmAfter": 1800,
    "inGameCoord": "1234, 5678",
    "type": "resource",
    "rarity": "rare",
    "missing": 1800
  }
}
```

#### POST `/api.php?action=update`
**Description:** Update an existing map marker

**Request Body:**
```json
{
  "id": 1,
  "label": "Updated Iron Ore Vein",
  "lat": 1234.56,
  "lng": 7890.12,
  "startTime": 1640995200000,
  "alarmAfter": 3600,
  "inGameCoord": "1234, 5678",
  "type": "resource",
  "rarity": "uncommon",
  "missing": 1800
}
```

**Response:**
```json
{
  "success": true
}
```

#### POST `/api.php?action=delete`
**Description:** Delete a map marker

**Request Body:**
```json
{
  "id": 1
}
```

**Response:**
```json
{
  "success": true
}
```

---

## Named Mobs API

### Database Schema

#### `named_mobs` Table
| Field | Type | Description |
|-------|------|-------------|
| `id` | INTEGER | Primary key, auto-increment |
| `name` | TEXT | Mob name |
| `slug` | TEXT | URL-friendly identifier |
| `level` | INTEGER | Mob level |
| `level_range` | TEXT | Level range description |
| `respawn_time` | TEXT | Respawn time description |
| `respawn_minutes` | INTEGER | Respawn time in minutes |
| `codex_url` | TEXT | Link to Ashes of Codex |
| `location_x` | REAL | X coordinate |
| `location_y` | REAL | Y coordinate |
| `location_z` | REAL | Z coordinate |
| `type` | TEXT | Mob type (default: 'named_mob') |

#### `named_mob_timers` Table
| Field | Type | Description |
|-------|------|-------------|
| `id` | INTEGER | Primary key, auto-increment |
| `named_mob_id` | INTEGER | Foreign key to named_mobs |
| `marker_id` | INTEGER | Optional link to map marker |
| `last_killed_at` | DATETIME | When the mob was last killed |
| `respawn_at` | DATETIME | When the mob will respawn |
| `server_name` | TEXT | Server identifier (default: 'default') |
| `notes` | TEXT | Additional notes |
| `player_name` | TEXT | Player who killed the mob |

### Endpoints

#### GET `/named_mobs_api.php`
**Description:** Retrieve all named mobs with optional filtering

**Query Parameters:**
- `level` (optional): Filter by mob level
- `search` (optional): Search by name or slug

**Example:** `/named_mobs_api.php?level=80&search=dragon`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Ancient Dragon",
      "slug": "ancient-dragon",
      "level": 80,
      "level_range": "80-80",
      "respawn_time": "2 hours",
      "respawn_minutes": 120,
      "codex_url": "https://ashes.codex.gg/...",
      "location_x": 1234.56,
      "location_y": 7890.12,
      "location_z": 100.0,
      "type": "named_mob"
    }
  ],
  "total": 1
}
```

#### GET `/named_mobs_api.php/named-mobs/search`
**Description:** Search named mobs with autocomplete support

**Query Parameters:**
- `q` (required): Search query
- `level` (optional): Filter by level

**Example:** `/named_mobs_api.php/named-mobs/search?q=dragon&level=80`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Ancient Dragon",
      "slug": "ancient-dragon",
      "level": 80,
      "respawn_minutes": 120
    }
  ]
}
```

#### GET `/named_mobs_api.php/named-mobs/timers`
**Description:** Get active timers for named mobs

**Query Parameters:**
- `server` (optional): Server name (default: 'default')

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "named_mob_id": 1,
      "mob_name": "Ancient Dragon",
      "level": 80,
      "respawn_minutes": 120,
      "last_killed_at": "2024-01-15 14:30:00",
      "respawn_at": "2024-01-15 16:30:00",
      "server_name": "default",
      "minutes_remaining": 45,
      "notes": "Killed by guild group"
    }
  ],
  "server": "default"
}
```

#### POST `/named_mobs_api.php/named-mobs/timer`
**Description:** Start a timer for a named mob

**Request Body:**
```json
{
  "named_mob_id": 1,
  "killed_at": "2024-01-15 14:30:00",
  "server": "default",
  "player_name": "PlayerName",
  "notes": "Killed by guild group"
}
```

**Response:**
```json
{
  "success": true,
  "timer_id": 1,
  "respawn_at": "2024-01-15 16:30:00",
  "minutes_until_respawn": 120
}
```

#### PUT `/named_mobs_api.php/named-mobs/timer`
**Description:** Update an active timer

**Request Body:**
```json
{
  "timer_id": 1,
  "notes": "Updated notes",
  "player_name": "NewPlayerName"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Timer updated successfully"
}
```

#### DELETE `/named_mobs_api.php/named-mobs/timer`
**Description:** Delete an active timer

**Query Parameters:**
- `timer_id` (required): Timer ID to delete

**Example:** `/named_mobs_api.php/named-mobs/timer?timer_id=1`

**Response:**
```json
{
  "success": true,
  "message": "Timer deleted successfully"
}
```

#### POST `/named_mobs_api.php/named-mobs/import`
**Description:** Import named mobs from JSON data file

**Response:**
```json
{
  "success": true,
  "imported": 150,
  "total_mobs": 150,
  "message": "Imported 150 named mobs successfully"
}
```

---

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful request
- `400 Bad Request`: Invalid request data or missing required parameters
- `404 Not Found`: Resource not found
- `405 Method Not Allowed`: Invalid HTTP method
- `500 Internal Server Error`: Server-side error

## CORS Support

The API includes CORS headers to support cross-origin requests:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

## Usage Examples

### JavaScript/Fetch API

```javascript
// Get all markers
const markers = await fetch('http://84.247.141.193:80/map/api.php')
  .then(response => response.json());

// Create a new marker
const newMarker = await fetch('http://84.247.141.193:80/map/api.php?action=create', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    label: 'Iron Ore Vein',
    lat: 1234.56,
    lng: 7890.12,
    type: 'resource',
    rarity: 'common'
  })
}).then(response => response.json());

// Start a named mob timer
const timer = await fetch('http://84.247.141.193:80/map/named_mobs_api.php/named-mobs/timer', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    named_mob_id: 1,
    killed_at: new Date().toISOString(),
    server: 'default',
    player_name: 'MyCharacter'
  })
}).then(response => response.json());
```

### cURL Examples

```bash
# Get all markers
curl -X GET "http://84.247.141.193:80/map/api.php"

# Create a marker
curl -X POST "http://84.247.141.193:80/map/api.php?action=create" \
  -H "Content-Type: application/json" \
  -d '{"label":"Iron Ore","lat":1234.56,"lng":7890.12,"type":"resource"}'

# Get active timers
curl -X GET "http://84.247.141.193:80/map/named_mobs_api.php/named-mobs/timers?server=default"
```

---

## Integration Notes

- The API is designed to work seamlessly with the AOC Timer Map Angular application
- Named mob data is synchronized with the Ashes of Codex database
- Timer calculations are performed server-side for accuracy
- The API supports multiple servers through the `server_name` parameter
- All timestamps are handled in UTC and converted as needed for display
