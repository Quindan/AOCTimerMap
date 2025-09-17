# AOC Timer Map - API Documentation

## Overview

The AOC Timer Map provides RESTful APIs for managing resource markers and named mob timers. All endpoints require HTTP Basic Authentication using your guild credentials.

### Base Information
- **Base URL**: `https://your-domain.com/`
- **Authentication**: HTTP Basic Authentication
- **Content-Type**: `application/json`
- **Rate Limiting**: 100 requests per minute per user

### Response Format
All API responses follow a consistent JSON format:
```json
{
  "success": true,
  "data": {...},
  "message": "Operation completed successfully"
}
```

## Resource Markers API (`api.php`)

The Resource Markers API manages map markers for resources, mining nodes, and other points of interest.

### Database Schema
```sql
CREATE TABLE markers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  label TEXT,
  lat REAL,
  lng REAL,
  startTime INTEGER,
  alarmAfter INTEGER,
  inGameCoord TEXT,
  type TEXT,
  missing INTEGER,
  rarity TEXT DEFAULT 'common'
)
```

### Endpoints

#### Get All Markers
- **Method**: `GET`
- **Endpoint**: `/api.php`
- **Description**: Retrieves all resource markers from the database
- **Authentication**: Required

**Response Example**:
```json
[
  {
    "id": 1,
    "label": "Iron Ore Deposit",
    "lat": 45.123,
    "lng": -73.456,
    "startTime": 1640995200000,
    "alarmAfter": 1800,
    "inGameCoord": "X: 1234, Y: 5678",
    "type": "iron",
    "missing": 1800,
    "rarity": "common"
  }
]
```

#### Create Marker
- **Method**: `POST`
- **Endpoint**: `/api.php?action=create`
- **Description**: Creates a new resource marker
- **Authentication**: Required

**Request Body**:
```json
{
  "label": "Iron Ore Deposit",
  "lat": 45.123,
  "lng": -73.456,
  "startTime": 1640995200000,
  "alarmAfter": 1800,
  "inGameCoord": "X: 1234, Y: 5678",
  "type": "iron",
  "missing": 1800,
  "rarity": "common"
}
```

**Parameters**:
- `label` (string, optional): Descriptive label for the marker
- `lat` (float, required): Latitude coordinate
- `lng` (float, required): Longitude coordinate
- `startTime` (integer, optional): Timestamp when timer starts (defaults to current time)
- `alarmAfter` (integer, optional): Seconds until alarm (default: 1800)
- `inGameCoord` (string, optional): In-game coordinate representation
- `type` (string, optional): Resource type identifier
- `missing` (integer, optional): Missing time in seconds (default: 1800)
- `rarity` (string, optional): Resource rarity level (default: "common")

**Response Example**:
```json
{
  "success": true,
  "marker": {
    "id": 123,
    "label": "Iron Ore Deposit",
    "lat": 45.123,
    "lng": -73.456,
    "startTime": 1640995200000,
    "alarmAfter": 1800,
    "inGameCoord": "X: 1234, Y: 5678",
    "type": "iron",
    "missing": 1800,
    "rarity": "common"
  }
}
```

#### Update Marker
- **Method**: `POST`
- **Endpoint**: `/api.php?action=update`
- **Description**: Updates an existing resource marker
- **Authentication**: Required

**Request Body**:
```json
{
  "id": 123,
  "label": "Updated Iron Ore Deposit",
  "lat": 45.123,
  "lng": -73.456,
  "startTime": 1640995200000,
  "alarmAfter": 3600,
  "inGameCoord": "X: 1234, Y: 5678",
  "type": "iron",
  "missing": 3600,
  "rarity": "rare"
}
```

**Parameters**:
- `id` (integer, required): ID of the marker to update
- All other parameters are optional and will update the corresponding fields

**Response Example**:
```json
{
  "success": true
}
```

#### Delete Marker
- **Method**: `POST`
- **Endpoint**: `/api.php?action=delete`
- **Description**: Deletes a resource marker
- **Authentication**: Required

**Request Body**:
```json
{
  "id": 123
}
```

**Parameters**:
- `id` (integer, required): ID of the marker to delete

**Response Example**:
```json
{
  "success": true
}
```

## Named Mobs API (`named_mobs_api.php`)

The Named Mobs API manages named mob timers and tracking for boss spawns and special creatures.

### Database Schema

#### Named Mobs Table
```sql
CREATE TABLE named_mobs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  slug TEXT UNIQUE,
  level INTEGER,
  level_range TEXT,
  respawn_time TEXT,
  respawn_minutes INTEGER,
  codex_url TEXT,
  location_x REAL,
  location_y REAL,
  location_z REAL,
  type TEXT DEFAULT 'named_mob',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

#### Named Mob Timers Table
```sql
CREATE TABLE named_mob_timers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  named_mob_id INTEGER NOT NULL,
  marker_id INTEGER,
  last_killed_at DATETIME,
  respawn_at DATETIME,
  server_name TEXT DEFAULT 'default',
  notes TEXT,
  player_name TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (named_mob_id) REFERENCES named_mobs(id),
  FOREIGN KEY (marker_id) REFERENCES markers(id)
)
```

### Endpoints

#### Get All Named Mobs
- **Method**: `GET`
- **Endpoint**: `/named_mobs_api.php`
- **Description**: Retrieves all named mobs with optional filtering
- **Authentication**: Required

**Query Parameters**:
- `level` (integer, optional): Filter by mob level
- `search` (string, optional): Search by name or slug

**Response Example**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Ancient Dragon",
      "slug": "ancient-dragon",
      "level": 60,
      "level_range": "58-62",
      "respawn_time": "4 hours",
      "respawn_minutes": 240,
      "codex_url": "https://example.com/codex/ancient-dragon",
      "location_x": 1234.5,
      "location_y": 5678.9,
      "location_z": 100.0,
      "type": "named_mob",
      "created_at": "2024-01-01 12:00:00",
      "updated_at": "2024-01-01 12:00:00"
    }
  ],
  "total": 1
}
```

#### Search Named Mobs
- **Method**: `GET`
- **Endpoint**: `/named_mobs_api.php/search`
- **Description**: Search named mobs by query
- **Authentication**: Required

**Query Parameters**:
- `q` (string, required): Search query
- `level` (integer, optional): Filter by level

**Response Example**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Ancient Dragon",
      "slug": "ancient-dragon",
      "level": 60,
      "respawn_minutes": 240
    }
  ]
}
```

#### Get Single Named Mob
- **Method**: `GET`
- **Endpoint**: `/named_mobs_api.php/{id_or_slug}`
- **Description**: Get details of a specific named mob by ID or slug
- **Authentication**: Required

**Response Example**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Ancient Dragon",
    "slug": "ancient-dragon",
    "level": 60,
    "level_range": "58-62",
    "respawn_time": "4 hours",
    "respawn_minutes": 240,
    "codex_url": "https://example.com/codex/ancient-dragon",
    "location_x": 1234.5,
    "location_y": 5678.9,
    "location_z": 100.0,
    "type": "named_mob"
  }
}
```

#### Get Active Timers
- **Method**: `GET`
- **Endpoint**: `/named_mobs_api.php/timers`
- **Description**: Get all active named mob timers
- **Authentication**: Required

**Query Parameters**:
- `server` (string, optional): Filter by server name (default: "default")

**Response Example**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "named_mob_id": 1,
      "marker_id": null,
      "last_killed_at": "2024-01-01 12:00:00",
      "respawn_at": "2024-01-01 16:00:00",
      "server_name": "default",
      "notes": "Killed by guild raid",
      "player_name": "PlayerName",
      "mob_name": "Ancient Dragon",
      "level": 60,
      "respawn_minutes": 240,
      "codex_url": "https://example.com/codex/ancient-dragon",
      "location_x": 1234.5,
      "location_y": 5678.9,
      "minutes_remaining": 180
    }
  ],
  "server": "default"
}
```

#### Start Timer
- **Method**: `POST`
- **Endpoint**: `/named_mobs_api.php/timer`
- **Description**: Start a timer for a named mob after it's killed
- **Authentication**: Required

**Request Body**:
```json
{
  "named_mob_id": 1,
  "killed_at": "2024-01-01 12:00:00",
  "server": "default",
  "player_name": "PlayerName",
  "notes": "Killed by guild raid"
}
```

**Parameters**:
- `named_mob_id` (integer, required): ID of the named mob
- `killed_at` (string, optional): Timestamp when killed (defaults to now)
- `server` (string, optional): Server name (default: "default")
- `player_name` (string, optional): Name of the player who killed it
- `notes` (string, optional): Additional notes

**Response Example**:
```json
{
  "success": true,
  "timer_id": 123,
  "respawn_at": "2024-01-01 16:00:00",
  "minutes_until_respawn": 240
}
```

#### Update Timer
- **Method**: `PUT`
- **Endpoint**: `/named_mobs_api.php/timer`
- **Description**: Update an existing timer
- **Authentication**: Required

**Request Body**:
```json
{
  "timer_id": 123,
  "notes": "Updated notes",
  "player_name": "UpdatedPlayerName"
}
```

**Parameters**:
- `timer_id` (integer, required): ID of the timer to update
- `notes` (string, optional): Updated notes
- `player_name` (string, optional): Updated player name

**Response Example**:
```json
{
  "success": true,
  "message": "Timer updated successfully"
}
```

#### Delete Timer
- **Method**: `DELETE`
- **Endpoint**: `/named_mobs_api.php/timer?timer_id={id}`
- **Description**: Delete a timer
- **Authentication**: Required

**Query Parameters**:
- `timer_id` (integer, required): ID of the timer to delete

**Response Example**:
```json
{
  "success": true,
  "message": "Timer deleted successfully"
}
```

#### Create Named Mob
- **Method**: `POST`
- **Endpoint**: `/named_mobs_api.php`
- **Description**: Create a new named mob entry
- **Authentication**: Required

**Request Body**:
```json
{
  "name": "New Boss",
  "slug": "new-boss",
  "level": 50,
  "level_range": "48-52",
  "respawn_time": "2 hours",
  "respawn_minutes": 120,
  "codex_url": "https://example.com/codex/new-boss",
  "location_x": 1000.0,
  "location_y": 2000.0,
  "location_z": 50.0,
  "type": "named_mob"
}
```

#### Import Named Mobs
- **Method**: `POST`
- **Endpoint**: `/named_mobs_api.php/import`
- **Description**: Import named mobs from JSON data file
- **Authentication**: Required

**Response Example**:
```json
{
  "success": true,
  "imported": 25,
  "total_mobs": 25,
  "message": "Imported 25 named mobs successfully"
}
```

## Error Handling

All endpoints return appropriate HTTP status codes and error messages:

### Common HTTP Status Codes
- `200 OK`: Request successful
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required
- `404 Not Found`: Resource not found
- `405 Method Not Allowed`: HTTP method not supported
- `500 Internal Server Error`: Server error

### Error Response Format
```json
{
  "error": "Error message describing what went wrong"
}
```

## Authentication

All API endpoints require HTTP Basic Authentication. Include your credentials in the Authorization header:

```bash
curl -u username:password https://your-domain.com/api.php
```

Or using base64 encoding:
```bash
curl -H "Authorization: Basic $(echo -n username:password | base64)" https://your-domain.com/api.php
```

## Rate Limiting

API requests are rate-limited to prevent abuse:
- **General endpoints**: 30 requests per second, burst up to 20
- **API endpoints**: 10 requests per second, burst up to 5

Rate limit headers are included in responses:
- `X-RateLimit-Remaining`: Number of requests remaining
- `X-RateLimit-Reset`: Time when the rate limit resets

## Examples

### cURL Examples

#### Get all markers
```bash
curl -u username:password https://your-domain.com/api.php
```

#### Create a new marker
```bash
curl -X POST -u username:password \
  -H "Content-Type: application/json" \
  -d '{
    "label": "Iron Deposit",
    "lat": 45.123,
    "lng": -73.456,
    "type": "iron",
    "rarity": "common"
  }' \
  "https://your-domain.com/api.php?action=create"
```

#### Get active named mob timers
```bash
curl -u username:password https://your-domain.com/named_mobs_api.php/timers
```

#### Start a named mob timer
```bash
curl -X POST -u username:password \
  -H "Content-Type: application/json" \
  -d '{
    "named_mob_id": 1,
    "player_name": "GuildMember",
    "notes": "Killed during evening raid"
  }' \
  "https://your-domain.com/named_mobs_api.php/timer"
```

### JavaScript Examples

#### Using Fetch API
```javascript
// Get all markers
const response = await fetch('/api.php', {
  headers: {
    'Authorization': 'Basic ' + btoa('username:password')
  }
});
const markers = await response.json();

// Create a new marker
const newMarker = await fetch('/api.php?action=create', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Basic ' + btoa('username:password')
  },
  body: JSON.stringify({
    label: 'Silver Ore',
    lat: 45.123,
    lng: -73.456,
    type: 'silver',
    rarity: 'uncommon'
  })
});
```

## Integration Notes

- The APIs use SQLite database for data persistence
- All timestamps are stored in ISO 8601 format
- Location coordinates use the game's coordinate system
- The system automatically creates database tables if they don't exist
- Named mob timers are automatically calculated based on respawn_minutes
- Timers are server-specific to support multiple game servers

## Changelog

### Version 1.0
- Initial API implementation
- Resource markers CRUD operations
- Named mob timer management
- Basic authentication and rate limiting
