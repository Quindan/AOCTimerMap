# AOC Timer Map - Production Deployment Guide

## 🚀 Deployment Process

### Prerequisites
- SSH access to production server: `84.247.141.193`
- Docker installed on production server
- Git repository access

### Production Server Details
- **IP**: 84.247.141.193
- **User**: root
- **Project Path**: `/root/AOCTimerMap`
- **Port**: 80 (HTTP)
- **Authentication**: Basic Auth (invicta/invicta)

### Deployment Steps

#### 1. Connect to Production Server
```bash
ssh root@84.247.141.193
cd /root/AOCTimerMap
```

#### 2. Pull Latest Changes
```bash
git pull origin main
```

#### 3. Build and Deploy
```bash
# Stop existing container
docker stop aoc-timer-map 2>/dev/null
docker rm aoc-timer-map 2>/dev/null

# Build new image
docker build -t aoctimermap_timer-map .

# Start production container
docker run -d --name aoc-timer-map -p 80:80 -v /root/AOCTimerMap/data:/app/database aoctimermap_timer-map
```

#### 4. Fix Authentication (if needed)
```bash
# Create/update .htpasswd file
htpasswd -bc .htpasswd invicta invicta

# Copy to container
docker cp .htpasswd aoc-timer-map:/app/.htpasswd

# Reload nginx
docker exec aoc-timer-map nginx -s reload
```

#### 5. Verify Deployment
```bash
# Test main page
curl -u "invicta:invicta" -s -I "http://84.247.141.193/" | head -3

# Test API
curl -u "invicta:invicta" -s "http://84.247.141.193/named_mobs_api.php" | head -5

# Test assets
curl -u "invicta:invicta" -s -I "http://84.247.141.193/assets/invicta-logo.png" | head -3
```

## 🔧 Common Issues and Solutions

### Issue: 403 Forbidden
**Cause**: Missing `.htpasswd` file in container
**Solution**: 
```bash
htpasswd -bc .htpasswd invicta invicta
docker cp .htpasswd aoc-timer-map:/app/.htpasswd
docker exec aoc-timer-map nginx -s reload
```

### Issue: Port 80 Already in Use
**Cause**: Another container using port 80
**Solution**:
```bash
docker stop $(docker ps -q)  # Stop all containers
# Or specifically:
docker stop aoctimermap_main_production
```

### Issue: JavaScript Files 404
**Cause**: Angular build generates different filenames each time
**Solution**: Check actual filenames in container:
```bash
docker exec aoc-timer-map ls -la /app/frontend/ | grep '\.js'
```

### Issue: Database Permissions
**Cause**: UID/GID mismatch between host and container
**Solution**: Already fixed in Dockerfile with UID 33:33 mapping

## 📊 Deployment Verification Checklist

- [ ] Main page loads (200 OK with auth)
- [ ] Assets load (invicta-logo.png, icons)
- [ ] API endpoints respond (named_mobs_api.php)
- [ ] Map displays with markers
- [ ] Item icons visible on markers and cards
- [ ] Timer system functional
- [ ] Dark theme applied
- [ ] Landing page accessible

## 🎯 Current Production Features

### Icon System
- **310 item icons** from Ashes Codex CDN
- **Dual filename support** (frontend compatible)
- **100% coverage** for all named mob items

### UI Enhancements
- **Dark theme** throughout
- **Boss icons** replacing trophy emojis
- **Visual timer overlays** with clock-hand shadows
- **Enhanced notifications** with audio alerts

### Assets
- **New Invicta logo** (4-menu design, 65KB)
- **Updated Guild Sheet URL** to actual spreadsheet
- **Interactive map icon** (276KB fantasy design)

### Timer System
- **Reset timer** functionality
- **Spawn tracking** (Last Spawn, Next Spawn)
- **Notification system** ("Bip when ready")
- **Visual countdown** on map markers

## 📝 Last Deployment
- **Date**: September 18, 2025
- **Commit**: b4d7603 (Complete icon system with 310 item icons and UI enhancements)
- **Files Changed**: 669 files (6289 insertions, 2778 deletions)
- **Database**: ✅ Complete database uploaded (230 named mobs, 256 items)
- **Status**: ✅ Successfully deployed and verified

### Database Upload Process
```bash
# 1. Create directory structure on production
ssh root@84.247.141.193 "mkdir -p /root/AOCTimerMap/data/database/db"

# 2. Upload complete database
scp data/database/db/mydb.sqlite root@84.247.141.193:/root/AOCTimerMap/data/database/db/mydb.sqlite

# 3. Set permissions and restart
ssh root@84.247.141.193 "
  chown www-data:www-data /root/AOCTimerMap/data/database/db/mydb.sqlite
  chmod 664 /root/AOCTimerMap/data/database/db/mydb.sqlite
  docker restart aoc-timer-map
"
```

### Production Database Status
- **Named Mobs**: 230 entries
- **Special Items**: 256 entries  
- **API Response**: 228 visible mobs
- **Categorization**: Based on item grades (not mob levels)
  - **Initiate**: 7 mobs (Common items) - Grey markers
  - **Adept**: 202 mobs (Uncommon items) - Blue markers  
  - **Radiant**: 0 mobs (Rare+ items) - Yellow markers
  - **No Special Drop**: 19 mobs - Grey markers

### Mob Categorization Logic

**IMPORTANT**: Mobs are categorized by their **item GRADE**, not item rarity or mob level.

#### Grade vs Rarity Distinction
- **Rarity**: Visual quality (Common, Uncommon, Rare, Epic, Legendary) - shown as item border color
- **Grade**: Gameplay tier (Initiate, Adept, Radiant) - determines marker color and categorization

#### Color Scheme (Based on Item Grades)
- **Grey**: No special drops (19 mobs)
- **Green**: Initiate grade items (7 mobs) - "uncommon-like color for initiate"  
- **Blue**: Adept grade items (203 mobs) - "rare-like color for adept"
- **Yellow**: Radiant grade items (1 mob) - "heroic-like color for radiant"

#### Categorization Process
1. Extract **Grade** from Codex item pages (not rarity)
2. Categorize mob by **highest grade** of their special items
3. Apply color scheme based on grade tier

#### Grade Extraction Examples
```bash
# Fire-Scarred Chestplate: Uncommon rarity BUT Radiant grade
curl -s "https://ashescodex.com/db/item/Gear_Armor_Heavy_Cairn_Chest" | grep -A2 "Grade:" 
# Returns: "Radiant" → Yellow marker

# The Silvertooth: Rare rarity BUT Adept grade  
curl -s "https://ashescodex.com/db/item/Gear_Weapon_Sword_1H_Silvertooth" | grep -A2 "Grade:"
# Returns: "Adept" → Blue marker
```

### Example Corrections
- **Warlord Silvertooth**: Level 14, drops "The Silvertooth" (Rare rarity, **Adept grade**) → Blue marker
- **Cairn**: Drops "Fire-Scarred Chestplate" (Uncommon rarity, **Radiant grade**) → Yellow marker
- **Common items**: Usually Initiate grade → Green markers

## 🌐 Access Information
- **URL**: http://84.247.141.193
- **Credentials**: invicta / invicta
- **Local Dev**: http://localhost:9090 (same credentials)
