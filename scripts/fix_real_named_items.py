#!/usr/bin/env python3
"""
Fix the test items with the REAL items from Codex JSON data
"""

import sqlite3
import subprocess
import json
import re

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
                                            
                                            # Skip recipes and common materials (but include the special items)
                                            if 'Recipe:' in item_name:
                                                continue
                                            
                                            # Only include items with rarity 2+ (uncommon+) or specific special items
                                            if (min_rarity >= 2 or 
                                                any(special in item_name for special in ['Waterlogged Gloves', 'Wand of Allurement', 'Silkwind Leggings'])):
                                                
                                                item_url = f"https://ashescodex.com/db/item/{item_code}"
                                                
                                                # Determine item type
                                                item_type = "Unknown"
                                                if "Weapon_" in item_code:
                                                    item_type = "Weapon"
                                                elif "Accessory_" in item_code:
                                                    item_type = "Accessory"
                                                elif "Armor_" in item_code:
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

def fix_real_items():
    """Replace fake items with real ones from Codex"""
    db_path = '/app/database/db/mydb.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Test mobs to fix
    test_mobs = [
        ('bloodmage-triune', 'Bloodmage Triune'),
        ('waterlogged-liffy', 'Waterlogged Liffy'),
        ('crunch-trunk', 'Crunch Trunk')
        # Skip Forgelord Zammer as it already has correct items
    ]
    
    # Get mob IDs
    cursor.execute("SELECT id, name FROM named_mobs WHERE name IN (?, ?, ?)", 
                  ('Bloodmage Triune', 'Waterlogged Liffy', 'Crunch Trunk'))
    mobs = {row[1]: row[0] for row in cursor.fetchall()}
    
    print("🔧 Fixing items with REAL Codex data...")
    
    for slug, name in test_mobs:
        if name in mobs:
            mob_id = mobs[name]
            print(f"\n📍 {name} ({slug})")
            
            # Fetch real items
            real_items = fetch_real_items(slug, name)
            
            if real_items:
                # Clear fake items
                cursor.execute("DELETE FROM named_mob_items WHERE named_mob_id = ?", (mob_id,))
                
                # Add real items
                for i, item in enumerate(real_items, 1):
                    cursor.execute("""
                        INSERT INTO named_mob_items 
                        (named_mob_id, item_name, item_url, item_rarity, item_type, drop_order, drop_chance)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (mob_id, item['name'], item['url'], item['rarity'], item['type'], i, item['drop_chance']))
                
                print(f"    💾 Added {len(real_items)} real items")
            else:
                print(f"    ⚠️  No real items found - keeping existing")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Real items updated successfully!")

def verify_real_items():
    """Verify the real items were added correctly"""
    db_path = '/app/database/db/mydb.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"\n🔍 Verifying REAL items...")
    cursor.execute("""
        SELECT nm.name, nmi.item_name, nmi.drop_chance, nmi.item_type 
        FROM named_mobs nm 
        JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id 
        WHERE nm.name IN ('Bloodmage Triune', 'Waterlogged Liffy', 'Forgelord Zammer', 'Crunch Trunk') 
        ORDER BY nm.name, nmi.drop_order
    """)
    
    current_mob = None
    for row in cursor.fetchall():
        mob_name, item_name, drop_chance, item_type = row
        if mob_name != current_mob:
            print(f"\n📍 {mob_name}:")
            current_mob = mob_name
        print(f"    - {item_name} ({drop_chance}) - {item_type}")
    
    conn.close()

def main():
    print("🎯 Fixing Items with REAL Codex Data")
    print("=" * 40)
    
    fix_real_items()
    verify_real_items()
    
    print(f"\n🌐 Test at: http://localhost:9090")
    print(f"Real items should now appear:")
    print(f"  - Waterlogged Liffy: Waterlogged Gloves")
    print(f"  - Crunch Trunk: Wand of Allurement + Silkwind Leggings")

if __name__ == "__main__":
    main()
