#!/usr/bin/env python3
"""
Parse Codex JSON data embedded in mob pages to extract special items
Looks for the _Named pattern in loot table names and extracts associated items
"""

import sqlite3
import subprocess
import json
import re
from urllib.parse import unquote

def fetch_mob_page_json(mob_slug):
    """Fetch mob page and extract embedded JSON data"""
    try:
        url = f"https://ashescodex.com/db/mob/{mob_slug}"
        result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            return None
            
        content = result.stdout
        
        # Look for the embedded JSON data in script tags
        # Pattern: __sveltekit_... = {...}
        json_pattern = r'__sveltekit_[^=]+=\s*({.*?});'
        matches = re.findall(json_pattern, content, re.DOTALL)
        
        for match in matches:
            try:
                data = json.loads(match)
                # Check if this contains mob/loot data
                if 'nodes' in data and isinstance(data['nodes'], list):
                    for node in data['nodes']:
                        if isinstance(node, dict) and 'data' in node:
                            return node['data']
                            
                # Alternative structure check
                if 'data' in data:
                    return data['data']
                    
            except json.JSONDecodeError:
                continue
                
        return None
        
    except Exception as e:
        print(f"Error fetching {mob_slug}: {e}")
        return None

def extract_named_items(json_data, mob_name):
    """Extract items from _Named loot tables"""
    if not json_data:
        return []
        
    items = []
    
    def search_for_named_items(obj, path=""):
        """Recursively search for _Named patterns and associated items"""
        if isinstance(obj, dict):
            # Check if this is a loot table with _Named pattern
            name = obj.get('name', '')
            if '_Named' in name or f'{mob_name.replace(" ", "_")}_Named' in name:
                print(f"  🎯 Found _Named table: {name}")
                
                # Extract items from this table
                if 'rewardDefContainers' in obj:
                    for container in obj['rewardDefContainers']:
                        if 'rewards' in container:
                            for reward in container['rewards']:
                                if 'itemRewards' in reward:
                                    for item_reward in reward['itemRewards']:
                                        if 'item' in item_reward:
                                            item = item_reward['item']
                                            item_name = item.get('itemName', 'Unknown')
                                            item_guid = item.get('guid', '')
                                            
                                            # Skip recipes and common materials
                                            if 'Recipe:' in item_name or 'Fragment' in item_name:
                                                continue
                                                
                                            # Build item URL
                                            item_url_name = item.get('name', '')
                                            item_url = f"https://ashescodex.com/db/item/{item_url_name}" if item_url_name else ""
                                            
                                            # Determine item type and rarity
                                            item_type = "Unknown"
                                            rarity = "Uncommon"  # Default for special drops
                                            
                                            if "Gear_Weapon" in item_url_name:
                                                item_type = "Weapon"
                                            elif "Gear_Accessory" in item_url_name or "Earring" in item_name or "Ring" in item_name:
                                                item_type = "Accessory"
                                            elif "Gear_Armor" in item_url_name:
                                                item_type = "Armor"
                                            
                                            # Try to get drop chance from inherited chances
                                            drop_chance = "Unknown"
                                            if 'inheritedSubTableChance' in obj:
                                                chances = obj['inheritedSubTableChance']
                                                if '0' in chances:
                                                    chance_val = float(chances['0']) * 100
                                                    drop_chance = f"{chance_val:.1f}%"
                                            
                                            items.append({
                                                'name': item_name,
                                                'url': item_url,
                                                'rarity': rarity,
                                                'type': item_type,
                                                'drop_chance': drop_chance,
                                                'guid': item_guid,
                                                'table_name': name
                                            })
                                            
                                            print(f"    ✅ {item_name} ({drop_chance}) - {item_type}")
            
            # Recursively search in nested objects
            for key, value in obj.items():
                search_for_named_items(value, f"{path}.{key}")
                
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                search_for_named_items(item, f"{path}[{i}]")
    
    search_for_named_items(json_data)
    return items

def update_mob_items(mob_id, mob_name, items):
    """Update the database with special items for a mob"""
    if not items:
        print(f"    ⚠️  No special items found for {mob_name}")
        return
        
    db_path = 'data/database/db/mydb.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Clear existing items for this mob (only _Named items to preserve manual entries)
    cursor.execute("DELETE FROM named_mob_items WHERE named_mob_id = ? AND item_name LIKE '%Named%'", (mob_id,))
    
    # Add new items
    for i, item in enumerate(items, 1):
        cursor.execute("""
            INSERT INTO named_mob_items 
            (named_mob_id, item_name, item_url, item_rarity, item_type, drop_order, drop_chance)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (mob_id, item['name'], item['url'], item['rarity'], item['type'], i, item['drop_chance']))
        
        print(f"    ✅ Added: {item['name']} ({item['drop_chance']})")
    
    conn.commit()
    conn.close()

def test_specific_mobs():
    """Test with the 4 specific mobs mentioned by user"""
    test_mobs = [
        ('bloodmage-triune', 'Bloodmage Triune'),
        ('waterlogged-liffy', 'Waterlogged Liffy'),
        ('forgelord-zammer', 'Forgelord Zammer'),
        ('crunch-trunk', 'Crunch Trunk')
    ]
    
    for slug, name in test_mobs:
        print(f"\n📍 Testing: {name} ({slug})")
        
        # Fetch JSON data from page
        json_data = fetch_mob_page_json(slug)
        
        if json_data:
            print(f"  📄 JSON data extracted")
            items = extract_named_items(json_data, name)
            
            if items:
                print(f"  🎁 Found {len(items)} special items:")
                for item in items:
                    print(f"    - {item['name']} ({item['drop_chance']}) from table: {item['table_name']}")
                    
                # For testing, we won't update the database yet
                # update_mob_items(mob_id, name, items)
            else:
                print(f"  ⚠️  No _Named items found")
        else:
            print(f"  ❌ Failed to extract JSON data")

def main():
    print("🎯 Testing Codex JSON Parsing for _Named Items")
    print("=" * 50)
    
    test_specific_mobs()

if __name__ == "__main__":
    main()
