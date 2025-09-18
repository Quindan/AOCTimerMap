#!/usr/bin/env python3
"""
Extract REAL _Named items from Codex for ALL named mobs
Excludes recipes and materials, only keeps weapons/armor/accessories
"""

import sqlite3
import subprocess
import json
import re
import time

def extract_real_items_from_json(content, mob_name):
    """Extract real items from the JSON embedded in the page"""
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
                                            
                                            # EXCLUDE recipes and materials - ONLY keep gear
                                            if ('Recipe:' in item_name or 
                                                'Fragment' in item_name or 
                                                'Spool' in item_name or
                                                'Stick' in item_name or
                                                'Hide' in item_name or
                                                'Bone' in item_name or
                                                'Setting' in item_name or
                                                'Gem' in item_name or
                                                'Essence' in item_name or
                                                'Emblem' in item_name or
                                                item_code.startswith('Resource_') or
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

def fetch_real_items(mob_slug, mob_name):
    """Fetch and extract real items from Codex"""
    try:
        url = f"https://ashescodex.com/db/mob/{mob_slug}"
        result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            return []
            
        content = result.stdout
        return extract_real_items_from_json(content, mob_name)
        
    except Exception as e:
        print(f"  ❌ Error fetching {mob_slug}: {e}")
        return []

def process_all_named_mobs():
    """Process ALL named mobs in the database"""
    db_path = '/app/database/db/mydb.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all named mobs with codex URLs
    cursor.execute("""
        SELECT id, name, slug, codex_url 
        FROM named_mobs 
        WHERE codex_url IS NOT NULL 
        ORDER BY name
    """)
    
    mobs = cursor.fetchall()
    conn.close()
    
    print(f"🔍 Processing {len(mobs)} named mobs...")
    
    processed = 0
    found_items = 0
    
    for mob in mobs:
        mob_id, name, slug, codex_url = mob
        
        print(f"\n📍 Processing: {name} ({slug})")
        
        # Fetch real items from Codex
        real_items = fetch_real_items(slug, name)
        
        if real_items:
            # Update database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Clear existing items for this mob
            cursor.execute("DELETE FROM named_mob_items WHERE named_mob_id = ?", (mob_id,))
            
            # Add real items
            for i, item in enumerate(real_items, 1):
                cursor.execute("""
                    INSERT INTO named_mob_items 
                    (named_mob_id, item_name, item_url, item_rarity, item_type, drop_order, drop_chance)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (mob_id, item['name'], item['url'], item['rarity'], item['type'], i, item['drop_chance']))
            
            conn.commit()
            conn.close()
            
            print(f"    💾 Added {len(real_items)} special items")
            processed += 1
            found_items += len(real_items)
        else:
            print(f"    ⚠️  No special items found")
        
        # Rate limiting to be nice to Codex
        time.sleep(1)
    
    print(f"\n✅ Processing complete!")
    print(f"📊 Stats:")
    print(f"  - Processed: {processed} mobs")
    print(f"  - Total special items: {found_items}")

def verify_results():
    """Show summary of extracted items"""
    db_path = '/app/database/db/mydb.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"\n📊 Summary of extracted special items:")
    cursor.execute("""
        SELECT nm.name, COUNT(nmi.id) as item_count
        FROM named_mobs nm 
        LEFT JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id 
        GROUP BY nm.id, nm.name
        HAVING item_count > 0
        ORDER BY item_count DESC, nm.name
        LIMIT 20
    """)
    
    for row in cursor.fetchall():
        mob_name, item_count = row
        print(f"  - {mob_name}: {item_count} items")
    
    conn.close()

def main():
    print("🎯 Extracting ALL Real _Named Items")
    print("=" * 40)
    
    process_all_named_mobs()
    verify_results()
    
    print(f"\n🌐 Test results at: http://localhost:9090")
    print(f"All named mobs with special items will now show them in their popups!")

if __name__ == "__main__":
    main()
