#!/usr/bin/env python3
"""
Fix The Bloodied extraction - the Bloodied Bone Ring was incorrectly filtered out
"""

import sqlite3
import subprocess
import json
import re

def extract_real_items_from_json(content, mob_name):
    """Extract real items from the JSON embedded in the page - FIXED FILTERING"""
    items = []
    
    try:
        # Find the JSON data in the script tag
        json_match = re.search(r'"body":"({.*?})"', content)
        if not json_match:
            return items
            
        # Decode the JSON string (it's double-encoded)
        json_str = json_match.group(1)
        # Unescape the JSON
        json_str = json_str.replace('\\"', '"').replace('\\\\', '\\')
        
        data = json.loads(json_str)
        
        if 'data' not in data or '_loot' not in data['data']:
            return items
            
        # Look through loot tables for _Named items
        for loot_table in data['data']['_loot']:
            table_name = loot_table.get('name', '')
            
            # Look for _Named pattern
            if '_Named' in table_name:
                print(f"    🎯 Found _Named table: {table_name}")
                
                # Extract items from reward containers
                if 'rewardDefContainers' in loot_table:
                    for container in loot_table['rewardDefContainers']:
                        if 'rewards' in container:
                            # Get weights for drop chance calculation
                            weights = container.get('weightsPerReward', [])
                            total_weight = sum(weights) if weights else 0
                            
                            for i, reward in enumerate(container['rewards']):
                                if 'itemRewards' in reward:
                                    for item_reward in reward['itemRewards']:
                                        if 'item' in item_reward and item_reward['item']:
                                            item = item_reward['item']
                                            item_name = item.get('itemName', 'Unknown')
                                            item_code = item.get('name', '')
                                            min_rarity = int(item.get('minRarity', '1'))
                                            
                                            # FIXED FILTERING: Only exclude based on item_code, not item_name
                                            # This allows "Bloodied Bone Ring" (Gear_Accessory_Ring_Bloodied) to pass through
                                            if (item_code.startswith('Resource_') or
                                                item_code.startswith('Consumable_Recipe_')):
                                                continue
                                            
                                            # ONLY include actual gear (weapons, armor, accessories)
                                            if not (item_code.startswith('Gear_Weapon_') or 
                                                   item_code.startswith('Gear_Armor_') or 
                                                   item_code.startswith('Gear_Accessory_')):
                                                continue
                                                
                                            item_url = f"https://ashescodex.com/db/item/{item_code}"
                                            
                                            # Determine item type
                                            item_type = "Unknown"
                                            if "Gear_Weapon_" in item_code:
                                                item_type = "Weapon"
                                            elif "Gear_Accessory_" in item_code:
                                                item_type = "Accessory"
                                            elif "Gear_Armor_" in item_code:
                                                item_type = "Armor"
                                            
                                            # Calculate drop chance from weights
                                            drop_chance = "Unknown"
                                            if weights and i < len(weights) and total_weight > 0:
                                                chance_percent = (weights[i] / total_weight) * 100
                                                drop_chance = f"{chance_percent:.1f}%"
                                            
                                            items.append({
                                                'name': item_name,
                                                'url': item_url,
                                                'rarity': 'Uncommon' if min_rarity >= 2 else 'Common',
                                                'type': item_type,
                                                'drop_chance': drop_chance
                                            })
                                            
                                            print(f"      ✅ {item_name} ({drop_chance}) - {item_type}")
        
    except Exception as e:
        print(f"    ❌ Error parsing JSON: {e}")
    
    return items

def fix_bloodied():
    """Fix The Bloodied specifically"""
    db_path = '/app/database/db/mydb.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get The Bloodied mob ID
    cursor.execute("SELECT id FROM named_mobs WHERE name = ?", ('The Bloodied',))
    result = cursor.fetchone()
    if not result:
        print("❌ The Bloodied not found in database")
        return
        
    mob_id = result[0]
    print(f"📍 Fixing The Bloodied (ID: {mob_id})")
    
    # Fetch real items from Codex
    try:
        url = "https://ashescodex.com/db/mob/the-bloodied"
        result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            print("❌ Failed to fetch Codex page")
            return
            
        content = result.stdout
        real_items = extract_real_items_from_json(content, "The Bloodied")
        
        if real_items:
            # Clear existing items
            cursor.execute("DELETE FROM named_mob_items WHERE named_mob_id = ?", (mob_id,))
            
            # Add real items
            for i, item in enumerate(real_items, 1):
                cursor.execute("""
                    INSERT INTO named_mob_items 
                    (named_mob_id, item_name, item_url, item_rarity, item_type, drop_order, drop_chance)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (mob_id, item['name'], item['url'], item['rarity'], item['type'], i, item['drop_chance']))
            
            conn.commit()
            print(f"    💾 Added {len(real_items)} items")
            
            # Verify
            cursor.execute("""
                SELECT item_name, drop_chance, item_type 
                FROM named_mob_items 
                WHERE named_mob_id = ?
                ORDER BY drop_order
            """, (mob_id,))
            
            print(f"    ✅ Verification:")
            for row in cursor.fetchall():
                item_name, drop_chance, item_type = row
                print(f"      - {item_name} ({drop_chance}) - {item_type}")
        else:
            print("    ⚠️  No items found")
            
    except Exception as e:
        print(f"    ❌ Error: {e}")
    finally:
        conn.close()

def main():
    print("🔧 Fixing The Bloodied Item Extraction")
    print("=" * 40)
    
    fix_bloodied()

if __name__ == "__main__":
    main()
