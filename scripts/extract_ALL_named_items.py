#!/usr/bin/env python3
"""
Extract ALL items from _Named categories except recipes and materials
Includes: Gear, Bags, Artisan Tools, Artisan Clothing, and any other special items
"""

import sqlite3
import subprocess
import json
import re
import time

def extract_all_items_from_named(content, mob_name):
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
                                            
                                            # ONLY exclude recipes and materials - KEEP EVERYTHING ELSE
                                            if (item_code.startswith('Resource_') or
                                                item_code.startswith('Consumable_Recipe_') or
                                                item_code.startswith('Certificate_')):
                                                continue
                                            
                                            # Skip empty items
                                            if not item_name or item_name == 'Unknown':
                                                continue
                                                
                                            item_url = f"https://ashescodex.com/db/item/{item_code}"
                                            
                                            # Determine item type from code - COMPREHENSIVE
                                            item_type = "Special"  # Default for unknown types
                                            if item_code.startswith('Gear_Weapon_'):
                                                item_type = "Weapon"
                                            elif item_code.startswith('Gear_Accessory_'):
                                                item_type = "Accessory"
                                            elif item_code.startswith('Gear_Armor_'):
                                                item_type = "Armor"
                                            elif item_code.startswith('Gear_Artisan_'):
                                                item_type = "Artisan Tool"
                                            elif item_code.startswith('Bag_'):
                                                item_type = "Bag"
                                            elif item_code.startswith('Artisan_'):
                                                item_type = "Artisan"
                                            elif item_code.startswith('Tool_'):
                                                item_type = "Tool"
                                            else:
                                                # Guess from name patterns
                                                name_lower = item_name.lower()
                                                if any(word in name_lower for word in ['bag', 'satchel', 'pouch', 'handbag']):
                                                    item_type = "Bag"
                                                elif any(word in name_lower for word in ['apron', 'clothing', 'outfit', 'garb']):
                                                    item_type = "Artisan"
                                                elif any(word in name_lower for word in ['tool', 'hammer', 'pick', 'axe', 'saw']):
                                                    item_type = "Tool"
                                                elif any(word in name_lower for word in ['mount', 'pet', 'companion']):
                                                    item_type = "Mount/Pet"
                                                else:
                                                    print(f"        🤔 Unknown type for: {item_name} ({item_code})")
                                            
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

def process_remaining_mobs():
    """Process the remaining visible mobs with comprehensive extraction"""
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
    
    print(f"🔍 Processing {len(mobs)} remaining mobs with COMPREHENSIVE extraction...")
    
    found_new_items = 0
    newly_hidden = 0
    
    for mob in mobs:
        mob_id, name, slug = mob
        
        print(f"\n📍 Processing: {name} ({slug})")
        
        # Fetch items from Codex
        try:
            url = f"https://ashescodex.com/db/mob/{slug}"
            result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, timeout=15)
            if result.returncode != 0:
                print("    ❌ Failed to fetch page")
                continue
                
            content = result.stdout
            items = extract_all_items_from_named(content, name)
            
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
                newly_hidden += 1
            else:
                print(f"    ⚠️  Still no items found")
        
        except Exception as e:
            print(f"    ❌ Error: {e}")
        
        # Rate limiting
        time.sleep(1)
    
    print(f"\n✅ Comprehensive extraction complete!")
    print(f"📊 Stats:")
    print(f"  - New items found: {found_new_items}")
    print(f"  - Newly hidden mobs: {newly_hidden}")

def show_final_results():
    """Show final results"""
    db_path = '/app/database/db/mydb.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Total counts
    cursor.execute("SELECT COUNT(*) FROM named_mobs WHERE is_hidden = 1")
    hidden_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM named_mobs WHERE is_hidden = 0 AND name != 'Test Mob'")
    visible_count = cursor.fetchone()[0]
    
    # Total items
    cursor.execute("SELECT COUNT(*) FROM named_mob_items")
    total_items = cursor.fetchone()[0]
    
    print(f"\n📊 FINAL COMPREHENSIVE Results:")
    print(f"  - Hidden mobs (with special items): {hidden_count}")
    print(f"  - Visible mobs (no special items): {visible_count}")
    print(f"  - Total special items extracted: {total_items}")
    
    if visible_count > 0:
        print(f"\n👁️ Remaining visible mobs (truly no special items):")
        cursor.execute("SELECT name FROM named_mobs WHERE is_hidden = 0 AND name != 'Test Mob' ORDER BY name")
        for row in cursor.fetchall():
            print(f"    - {row[0]}")
    
    # Show item type distribution
    print(f"\n📋 Item types found:")
    cursor.execute("""
        SELECT item_type, COUNT(*) as count 
        FROM named_mob_items 
        GROUP BY item_type 
        ORDER BY count DESC
    """)
    for row in cursor.fetchall():
        item_type, count = row
        print(f"    - {item_type}: {count} items")
    
    conn.close()

def main():
    print("🎯 COMPREHENSIVE _Named Items Extraction")
    print("🎯 (ALL items except recipes and materials)")
    print("=" * 50)
    
    process_remaining_mobs()
    show_final_results()
    
    print(f"\n🌐 Test at: http://localhost:9090")
    print(f"Should now include ALL special items: gear, bags, artisan tools, clothing, etc!")

if __name__ == "__main__":
    main()
