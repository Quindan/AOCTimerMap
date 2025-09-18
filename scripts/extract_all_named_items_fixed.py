#!/usr/bin/env python3
"""
Extract ALL items from _Named categories EXCEPT recipes and materials
Includes: Gear (weapons/armor/accessories), Bags, Artisan Clothing, Tools, etc.
"""

import sqlite3
import subprocess
import json
import re
import time

def extract_all_named_items(content, mob_name):
    """Extract ALL items from _Named categories except recipes and materials"""
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
                                            
                                            # SIMPLE FILTERING: ONLY exclude recipes and materials
                                            # Keep EVERYTHING else from _Named categories
                                            if (item_code.startswith('Resource_') or
                                                item_code.startswith('Consumable_Recipe_') or
                                                item_code.startswith('Certificate_')):
                                                continue
                                            
                                            # Skip empty items
                                            if not item_name or item_name == 'Unknown':
                                                continue
                                                
                                            item_url = f"https://ashescodex.com/db/item/{item_code}"
                                            
                                            # Determine item type from code
                                            item_type = "Unknown"
                                            if item_code.startswith('Gear_Weapon_'):
                                                item_type = "Weapon"
                                            elif item_code.startswith('Gear_Accessory_'):
                                                item_type = "Accessory"
                                            elif item_code.startswith('Gear_Armor_'):
                                                item_type = "Armor"
                                            elif item_code.startswith('Bag_'):
                                                item_type = "Bag"
                                            elif item_code.startswith('Artisan_'):
                                                item_type = "Artisan"
                                            elif item_code.startswith('Tool_'):
                                                item_type = "Tool"
                                            else:
                                                # For unknown types, try to guess from name
                                                if any(word in item_name.lower() for word in ['bag', 'satchel', 'pouch']):
                                                    item_type = "Bag"
                                                elif any(word in item_name.lower() for word in ['apron', 'clothing', 'outfit']):
                                                    item_type = "Artisan"
                                                elif any(word in item_name.lower() for word in ['tool', 'hammer', 'pick']):
                                                    item_type = "Tool"
                                                else:
                                                    item_type = "Special"
                                            
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

def fix_all_remaining_mobs():
    """Re-process the remaining visible mobs with the fixed filtering"""
    db_path = '/app/database/db/mydb.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get the remaining visible mobs (excluding Test Mob)
    cursor.execute("""
        SELECT id, name, slug 
        FROM named_mobs 
        WHERE is_hidden = 0 AND name != 'Test Mob' AND codex_url IS NOT NULL
        ORDER BY name
    """)
    
    mobs = cursor.fetchall()
    conn.close()
    
    print(f"🔍 Re-processing {len(mobs)} remaining mobs with FIXED filtering...")
    
    found_new_items = 0
    
    for mob in mobs:
        mob_id, name, slug = mob
        
        print(f"\n📍 Re-processing: {name} ({slug})")
        
        # Fetch items from Codex with fixed filtering
        try:
            url = f"https://ashescodex.com/db/mob/{slug}"
            result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, timeout=15)
            if result.returncode != 0:
                print("    ❌ Failed to fetch page")
                continue
                
            content = result.stdout
            items = extract_all_named_items(content, name)
            
            if items:
                # Update database
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Clear existing items
                cursor.execute("DELETE FROM named_mob_items WHERE named_mob_id = ?", (mob_id,))
                
                # Add new items
                for i, item in enumerate(items, 1):
                    cursor.execute("""
                        INSERT INTO named_mob_items 
                        (named_mob_id, item_name, item_url, item_rarity, item_type, drop_order, drop_chance)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (mob_id, item['name'], item['url'], item['rarity'], item['type'], i, item['drop_chance']))
                
                # Hide this mob since it now has items
                cursor.execute("UPDATE named_mobs SET is_hidden = 1 WHERE id = ?", (mob_id,))
                
                conn.commit()
                conn.close()
                
                print(f"    💾 Added {len(items)} items and hid mob")
                found_new_items += len(items)
            else:
                print(f"    ⚠️  Still no items found")
        
        except Exception as e:
            print(f"    ❌ Error: {e}")
        
        # Rate limiting
        time.sleep(1)
    
    print(f"\n✅ Re-processing complete!")
    print(f"📊 Found {found_new_items} new items with fixed filtering")

def show_final_status():
    """Show final status after re-processing"""
    db_path = '/app/database/db/mydb.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"\n📊 FINAL Status:")
    
    # Count mobs with items
    cursor.execute("SELECT COUNT(*) FROM named_mobs WHERE is_hidden = 1")
    hidden_count = cursor.fetchone()[0]
    
    # Count mobs without items
    cursor.execute("SELECT COUNT(*) FROM named_mobs WHERE is_hidden = 0 AND name != 'Test Mob'")
    visible_count = cursor.fetchone()[0]
    
    print(f"- Hidden (with items): {hidden_count}")
    print(f"- Visible (no items): {visible_count}")
    
    if visible_count > 0:
        print(f"\n👁️ Still visible (no special items found):")
        cursor.execute("SELECT name FROM named_mobs WHERE is_hidden = 0 AND name != 'Test Mob' ORDER BY name")
        for row in cursor.fetchall():
            print(f"  - {row[0]}")
    
    conn.close()

def main():
    print("🎯 Re-extracting with FIXED Filtering (ALL _Named items except recipes/materials)")
    print("=" * 80)
    
    fix_all_remaining_mobs()
    show_final_status()
    
    print(f"\n🌐 Check results at: http://localhost:9090")
    print(f"Now includes: Gear, Bags, Artisan Clothing, Tools, and any other special items!")

if __name__ == "__main__":
    main()
