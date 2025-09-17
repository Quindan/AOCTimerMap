# Ashes Codex API Analysis for Named Timers

## API Endpoints

### Named Mobs List
- **URL**: `https://api.ashescodex.com/mobs?page={page}&per_page=30&sortColumn=name&sortDir=asc&namedMobs=true`
- **Purpose**: Get paginated list of named mobs
- **Pagination**: 30 items per page, 230 total named mobs

### Individual Mob Details
- **URL**: `https://api.ashescodex.com/mob?populationInstanceId={id}`
- **Purpose**: Get detailed information for specific mob
- **Example ID**: `6064632025523879945`

## Data Structure Analysis

### From the API Response Example:

**Named Mob: "Byer, The Last Sentinel"**

```json
{
  "_id": "68b85a5f463d3d630edff3c4",
  "_displayName": "Byer, The Last Sentinel",
  "_slug": "byer-the-last-sentinel",
  "_levelRange": "27",
  "_location": {
    "x": -965201.8619764735,
    "y": 758601.6304653264,
    "z": 14166.402212446985
  },
  "populationInstances": [{
    "respawnTime": "1200 seconds",
    "nPCLevelMin": 27,
    "nPCLevelMax": 27,
    "guid": "6064631663104688146",
    "_isNamed": true,
    "_displayName": "Byer, The Last Sentinel"
  }]
}
```

## Key Data Points for Named Timers

1. **Name**: `_displayName` - "Byer, The Last Sentinel"
2. **Respawn Time**: `populationInstances[0].respawnTime` - "1200 seconds" (20 minutes)
3. **Level**: `_levelRange` or `nPCLevelMin`/`nPCLevelMax`
4. **Location**: `_location` coordinates (x, y, z)
5. **Codex Link**: Can be constructed from `_slug` or `_id`
6. **Population Instance ID**: For detailed API calls

## Implementation Plan

### Data Structure for Named Timers
```javascript
{
  id: "mob_id_or_slug",
  name: "Display Name",
  respawnTime: 1200, // seconds
  level: 27,
  location: {
    x: -965201.86,
    y: 758601.63,
    z: 14166.40
  },
  codexLink: "https://ashescodex.com/mobs/byer-the-last-sentinel",
  populationInstanceId: "6064631663104688146",
  lastKilled: null, // timestamp when killed
  nextSpawn: null   // calculated next spawn time
}
```

### API Integration Strategy
1. Fetch all pages of named mobs
2. Store in local database/cache
3. Provide timer functionality
4. Link to Ashes Codex for detailed info

### Timer Features
- Track last kill time
- Calculate next spawn time
- Alert system for spawns
- Map integration with spawn locations
