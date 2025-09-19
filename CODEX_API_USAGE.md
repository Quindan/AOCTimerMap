# Ashes Codex API Usage Guide

## 🔍 Codex Search API

The Ashes Codex provides a search API that can be used to extract detailed item information, including the crucial **Grade** data that determines mob categorization.

### API Endpoint
```
POST https://api.ashescodex.com/search
```

### Required Headers
```bash
-H 'accept: */*'
-H 'content-type: application/json'
-H 'origin: https://ashescodex.com'
-H 'referer: https://ashescodex.com/'
-H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
```

### Request Format
```json
{
  "query": "item name here",
  "resultType": null
}
```

### Example Usage

#### 1. Basic Search
```bash
curl 'https://api.ashescodex.com/search' \
  -H 'content-type: application/json' \
  -H 'origin: https://ashescodex.com' \
  -H 'referer: https://ashescodex.com/' \
  --data-raw '{"query":"Fire-Scarred Chestplate","resultType":null}'
```

#### 2. Extracting Specific Item Data
```bash
curl 'https://api.ashescodex.com/search' \
  -H 'content-type: application/json' \
  -H 'origin: https://ashescodex.com' \
  -H 'referer: https://ashescodex.com/' \
  --data-raw '{"query":"The Silvertooth","resultType":null}' | \
  jq '.[] | select(.item.type == "item") | {name: .item.itemName, icon: .item.icon}'
```

## 🎯 Grade Extraction Process

### Problem: Grade vs Rarity Confusion
- **Item Rarity**: Common, Uncommon, Rare, Epic, Legendary (visual quality)
- **Item Grade**: Initiate, Adept, Radiant (gameplay tier) - **THIS DETERMINES MARKER COLORS**

### Solution: Extract Grade from Codex Pages
The search API provides item URLs, then we scrape the individual item pages for Grade information.

#### Step 1: Search for Item
```bash
curl 'https://api.ashescodex.com/search' \
  --data-raw '{"query":"item name","resultType":null}' | \
  jq '.[] | select(.item.itemName == "exact name") | .item'
```

#### Step 2: Extract Grade from Item Page
```bash
# Get the item URL from search results
item_url="https://ashescodex.com/db/item/Gear_Weapon_Sword_1H_Silvertooth"

# Extract grade from page
curl -s "$item_url" | grep -A2 -B2 'Grade:' | grep -o 'Radiant\|Adept\|Initiate'
```

### Real Examples

#### Fire-Scarred Chestplate
```bash
# Search result shows: Uncommon rarity
# Page scraping shows: Grade: Radiant
# Result: Yellow marker (radiant category)
```

#### The Silvertooth  
```bash
# Search result shows: Rare rarity
# Page scraping shows: Grade: Adept
# Result: Blue marker (adept category)
```

## 🔧 Implementation Script

### Database Schema
```sql
-- Add grade column to track extracted grades
ALTER TABLE named_mob_items ADD COLUMN item_grade TEXT;
```

### Grade Extraction Script
```python
def extract_grade_from_codex(item_url):
    response = requests.get(item_url, timeout=15)
    grade_match = re.search(r'Grade:</span>\s*<span[^>]*>([^<]+)</span>', response.text)
    return grade_match.group(1).strip() if grade_match else None

def search_item_via_api(item_name):
    headers = {
        'content-type': 'application/json',
        'origin': 'https://ashescodex.com',
        'referer': 'https://ashescodex.com/'
    }
    data = {"query": item_name, "resultType": None}
    response = requests.post('https://api.ashescodex.com/search', headers=headers, json=data)
    # Process results to find exact match and extract item URL
```

### Categorization Logic
```sql
UPDATE named_mobs SET special_drop_category = 
  CASE 
    WHEN id IN (SELECT nm.id FROM named_mobs nm JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id WHERE nmi.item_grade = 'Radiant') THEN 'radiant'
    WHEN id IN (SELECT nm.id FROM named_mobs nm JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id WHERE nmi.item_grade = 'Adept' AND nm.id NOT IN (SELECT nm2.id FROM named_mobs nm2 JOIN named_mob_items nmi2 ON nm2.id = nmi2.named_mob_id WHERE nmi2.item_grade = 'Radiant')) THEN 'adept'
    WHEN id IN (SELECT nm.id FROM named_mobs nm JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id WHERE nmi.item_grade = 'Initiate' AND nm.id NOT IN (SELECT nm2.id FROM named_mobs nm2 JOIN named_mob_items nmi2 ON nm2.id = nmi2.named_mob_id WHERE nmi2.item_grade IN ('Adept', 'Radiant'))) THEN 'initiate'
    ELSE special_drop_category
  END;
```

## 🎨 Color Scheme Implementation

### CSS Classes (in styles.scss)
```scss
.marker-initiate { background-color: #4CAF50; } /* Green - Initiate grade */
.marker-adept { background-color: #2196F3; }    /* Blue - Adept grade */
.marker-radiant { background-color: #FFC107; }  /* Yellow - Radiant grade */
.marker-no-drops { background-color: #9E9E9E; } /* Grey - No special drops */
```

### Frontend Logic (map.service.ts)
```typescript
// Determine marker class based on grade-derived category
let markerClass = 'marker-default';
let markerColor = '#666';

switch (mob.special_drop_category) {
  case 'initiate':
    markerClass = 'marker-initiate';
    markerColor = '#4CAF50'; // Green
    break;
  case 'adept':
    markerClass = 'marker-adept'; 
    markerColor = '#2196F3'; // Blue
    break;
  case 'radiant':
    markerClass = 'marker-radiant';
    markerColor = '#FFC107'; // Yellow
    break;
  default:
    markerClass = 'marker-no-drops';
    markerColor = '#9E9E9E'; // Grey
}
```

## ⚠️ Common Pitfalls

### 1. Rarity vs Grade Confusion
- **Wrong**: Using item_rarity (Common, Uncommon, Rare) for categorization
- **Right**: Using item_grade (Initiate, Adept, Radiant) for categorization

### 2. API Search Limitations
- Some items may not be found with exact names
- Try variations: with/without apostrophes, partial names
- Handle quote escaping: `$'{"query":"item\'s name"}'`

### 3. Grade Extraction Patterns
- Look for: `Grade:</span>\s*<span[^>]*>([^<]+)</span>`
- Common grades: "Initiate", "Adept", "Radiant"
- Some items may not have grade information

## 📊 Expected Results

After proper grade extraction:
- **Grey markers**: Mobs without special drops
- **Green markers**: Mobs with Initiate grade items  
- **Blue markers**: Mobs with Adept grade items
- **Yellow markers**: Mobs with Radiant grade items

### Current Distribution (After Fix)
- **Grey**: 19 mobs (No special drops)
- **Green**: 7 mobs (Initiate grade)
- **Blue**: 197 mobs (Adept grade) 
- **Yellow**: 5 mobs (Radiant grade)

### Confirmed Radiant Grade Mobs (Yellow Markers)
1. **The Bloodied** (Level 21) - Radiant grade items
2. **Crunch Trunk** (Level 24) - Wand of Allurement (Radiant grade)
3. **Drooling Drawer** (Level 25) - Chewed Wand (Radiant grade)
4. **Forgelord Zammer** (Level 25) - Ancient Dunzen Longsword (Radiant grade)
5. **Cairn** (Level 31) - Fire-Scarred Chestplate (Radiant grade)

### Grade Extraction Commands Used
```bash
# Extract grades for key items
curl -s 'https://ashescodex.com/db/item/Gear_Armor_Heavy_Cairn_Chest' | grep -A3 'Grade:' | grep -o 'Radiant\|Adept\|Initiate'
curl -s 'https://ashescodex.com/db/item/Gear_Weapon_Sword_1H_Zammer' | grep -A3 'Grade:' | grep -o 'Radiant\|Adept\|Initiate'  
curl -s 'https://ashescodex.com/db/item/Gear_Accessory_Ring_Zammer' | grep -A3 'Grade:' | grep -o 'Radiant\|Adept\|Initiate'
curl -s 'https://ashescodex.com/db/item/Gear_Weapon_Wand_1H_Crunch' | grep -A3 'Grade:' | grep -o 'Radiant\|Adept\|Initiate'
curl -s 'https://ashescodex.com/db/item/Gear_Weapon_Wand_1H_Drawer' | grep -A3 'Grade:' | grep -o 'Radiant\|Adept\|Initiate'
```

### Database Updates
```sql
-- Update items with extracted grades
UPDATE named_mob_items SET item_grade = 'Radiant' WHERE item_name = 'Fire-Scarred Chestplate';
UPDATE named_mob_items SET item_grade = 'Radiant' WHERE item_name = 'Ancient Dunzen Longsword';
UPDATE named_mob_items SET item_grade = 'Radiant' WHERE item_name = 'Forgelord''s Signet';
UPDATE named_mob_items SET item_grade = 'Radiant' WHERE item_name = 'Wand of Allurement';
UPDATE named_mob_items SET item_grade = 'Radiant' WHERE item_name = 'Chewed Wand';

-- Recategorize mobs based on grades
UPDATE named_mobs SET special_drop_category = 
  CASE 
    WHEN id IN (SELECT nm.id FROM named_mobs nm JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id WHERE nmi.item_grade = 'Radiant') THEN 'radiant'
    WHEN id IN (SELECT nm.id FROM named_mobs nm JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id WHERE nmi.item_grade = 'Adept' AND nm.id NOT IN (SELECT nm2.id FROM named_mobs nm2 JOIN named_mob_items nmi2 ON nm2.id = nmi2.named_mob_id WHERE nmi2.item_grade = 'Radiant')) THEN 'adept'
    WHEN id IN (SELECT nm.id FROM named_mobs nm JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id WHERE nmi.item_grade = 'Initiate' AND nm.id NOT IN (SELECT nm2.id FROM named_mobs nm2 JOIN named_mob_items nmi2 ON nm2.id = nmi2.named_mob_id WHERE nmi2.item_grade IN ('Adept', 'Radiant'))) THEN 'initiate'
    ELSE special_drop_category
  END;
```

## 🔄 Future Updates

When Codex data changes:
1. Run grade extraction script for new/updated items
2. Update categorization based on new grades
3. Verify color distribution makes sense
4. Update production database

The grade system ensures proper visual distinction between different tiers of named mobs based on their actual drop quality, not arbitrary level ranges.
