#!/usr/bin/env python3
"""
Extract special items from Codex _Named categories
Works with the 4 test mobs: Bloodmage Triune, Waterlogged Liffy, Forgelord Zammer, Crunch Trunk
"""

import sqlite3
import subprocess
import json
import re

def fetch_and_extract_named_data(mob_slug, mob_name):
    """Fetch mob page and extract _Named item data"""
    try:
        url = f"https://ashescodex.com/db/mob/{mob_slug}"
        result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            return []
            
        content = result.stdout
        
        # Look for the _Named pattern specific to this mob
        expected_pattern = f"{mob_name.replace(' ', '_').replace('Bloodmage', 'Cultist_Mage')}_Named"
        if 'Waterlogged' in mob_name:
            expected_pattern = f"Waterlogged_Liffy_Named"
        elif 'Forgelord' in mob_name:
            expected_pattern = f"Forgelord_Zammer_Named"
        elif 'Crunch' in mob_name:
            expected_pattern = f"Crunch_Trunk_Named"
        elif 'Bloodmage' in mob_name:
            expected_pattern = f"Cultist_Mage_Triune1_Named"
            
        print(f"  🔍 Looking for pattern: {expected_pattern}")
        
        # Check if the pattern exists in the content
        if expected_pattern not in content:
            print(f"  ⚠️  Pattern not found in page")
            return []
            
        print(f"  ✅ Found _Named pattern in page!")
        
        # For now, let's extract some sample data based on what we know works
        # We'll look for items in the general loot structure and filter for special ones
        items = []
        
        # Look for gear items that might be special drops
        gear_patterns = [
            r'"itemName":"([^"]+(?:Axe|Sword|Mace|Bow|Staff|Shield|Ring|Earring|Necklace)[^"]*)"[^}]*"name":"(Gear_[^"]+)"',
            r'"itemName":"([^"]+)"[^}]*"name":"(Gear_Weapon_[^"]+)"[^}]*"minRarity":"([1-6])"',
            r'"itemName":"([^"]+)"[^}]*"name":"(Gear_Accessory_[^"]+)"[^}]*"minRarity":"([1-6])"'
        ]
        
        for pattern in gear_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if len(match) >= 2:
                    item_name = match[0]
                    item_code = match[1]
                    rarity = match[2] if len(match) > 2 else "2"
                    
                    # Filter for likely special items (avoid common/generic names)
                    if any(skip in item_name.lower() for skip in ['recipe', 'fragment', 'essence', 'emblem']):
                        continue
                        
                    # Look for items that might be special (tier 2+ rarity, or specific naming patterns)
                    if (int(rarity) >= 2 or 
                        any(special in item_name for special in ['Steelbloom', 'Nightreaver', 'Dreadwake', 'Shadowfang']) or
                        mob_name.replace(' ', '') in item_name.replace(' ', '')):
                        
                        item_url = f"https://ashescodex.com/db/item/{item_code}"
                        
                        # Determine item type
                        item_type = "Unknown"
                        if "Weapon_" in item_code:
                            item_type = "Weapon"
                        elif "Accessory_" in item_code:
                            item_type = "Accessory"
                        elif "Armor_" in item_code:
                            item_type = "Armor"
                        
                        # Estimate drop chance (placeholder - would need more parsing)
                        drop_chance = "Unknown"
                        
                        items.append({
                            'name': item_name,
                            'url': item_url,
                            'rarity': 'Uncommon',  # Default for special items
                            'type': item_type,
                            'drop_chance': drop_chance
                        })
                        
                        print(f"    🎁 Found potential special item: {item_name}")
        
        # Remove duplicates
        seen = set()
        unique_items = []
        for item in items:
            if item['name'] not in seen:
                seen.add(item['name'])
                unique_items.append(item)
        
        return unique_items[:3]  # Limit to 3 items per mob for testing
        
    except Exception as e:
        print(f"  ❌ Error processing {mob_slug}: {e}")
        return []

def test_named_extraction():
    """Test with the 4 specific mobs"""
    test_mobs = [
        ('bloodmage-triune', 'Bloodmage Triune'),
        ('waterlogged-liffy', 'Waterlogged Liffy'),
        ('forgelord-zammer', 'Forgelord Zammer'),
        ('crunch-trunk', 'Crunch Trunk')
    ]
    
    all_results = {}
    
    for slug, name in test_mobs:
        print(f"\n📍 Testing: {name} ({slug})")
        items = fetch_and_extract_named_data(slug, name)
        all_results[name] = items
        
        if items:
            print(f"  🎁 Found {len(items)} potential special items:")
            for item in items:
                print(f"    - {item['name']} ({item['type']})")
        else:
            print(f"  ⚠️  No special items extracted")
    
    return all_results

def update_database_with_items(results):
    """Update the database with extracted items (for confirmed working mobs)"""
    db_path = 'data/database/db/mydb.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get mob IDs
    cursor.execute("SELECT id, name FROM named_mobs WHERE name IN (?, ?, ?, ?)", 
                  ('Bloodmage Triune', 'Waterlogged Liffy', 'Forgelord Zammer', 'Crunch Trunk'))
    mobs = {row[1]: row[0] for row in cursor.fetchall()}
    
    for mob_name, items in results.items():
        if mob_name in mobs and items:
            mob_id = mobs[mob_name]
            print(f"\n📝 Updating database for {mob_name} (ID: {mob_id})")
            
            # Clear existing _Named items
            cursor.execute("DELETE FROM named_mob_items WHERE named_mob_id = ? AND item_name LIKE '%Named%'", (mob_id,))
            
            # Add new items
            for i, item in enumerate(items, 1):
                cursor.execute("""
                    INSERT INTO named_mob_items 
                    (named_mob_id, item_name, item_url, item_rarity, item_type, drop_order, drop_chance)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (mob_id, item['name'], item['url'], item['rarity'], item['type'], i, item['drop_chance']))
                
                print(f"    ✅ Added: {item['name']}")
    
    conn.commit()
    conn.close()
    print(f"\n💾 Database updated successfully!")

def main():
    print("🎯 Testing _Named Items Extraction")
    print("=" * 40)
    
    results = test_named_extraction()
    
    print(f"\n📊 Summary:")
    total_items = sum(len(items) for items in results.values())
    print(f"Total special items found: {total_items}")
    
    if total_items > 0:
        print(f"\n❓ Update database with these items? (y/n)")
        # For testing, we'll skip the interactive prompt
        print("Skipping database update for testing phase.")
        # update_database_with_items(results)

if __name__ == "__main__":
    main()
