#!/usr/bin/env python3
"""
Download missing item icons using the complex Codex URL patterns
Based on the example: /Light/Meshes/TUI_Icon_Gear_Armor_Light_Meshes_WoefulSlippers_64.webp
"""
import sqlite3
import requests
import os
import re
import time

def try_complex_patterns(item_code, item_name):
    """Try various complex URL patterns for Codex icons"""
    base_url = "https://cdn.ashescodex.com/UI/Icons/Items/"
    
    patterns = []
    
    if item_code.startswith('Gear_Armor_'):
        parts = item_code.split('_')
        if len(parts) >= 4:
            # Gear_Armor_Light_Bootshredder_Feet
            armor_type = parts[2]  # Light, Medium, Heavy
            
            # Try different mesh/material patterns
            patterns.extend([
                f"{base_url}Gear/Armor/{armor_type}/Meshes/TUI_Icon_Gear_Armor_{armor_type}_Meshes_{item_name.replace(' ', '').replace(''s', '')}_64.webp",
                f"{base_url}Gear/Armor/{armor_type}/Leather/TUI_Icon_Gear_Armor_{armor_type}_Leather_{item_name.replace(' ', '').replace(''s', '')}_64.webp",
                f"{base_url}Gear/Armor/{armor_type}/Plate/TUI_Icon_Gear_Armor_{armor_type}_Plate_{item_name.replace(' ', '').replace(''s', '')}_64.webp",
                f"{base_url}Gear/Armor/{armor_type}/Mail/TUI_Icon_Gear_Armor_{armor_type}_Mail_{item_name.replace(' ', '').replace(''s', '')}_64.webp",
                f"{base_url}Gear/Armor/{armor_type}/TUI_Icon_{item_code}_64.webp",
            ])
    
    elif item_code.startswith('Gear_Weapon_'):
        parts = item_code.split('_')
        if len(parts) >= 3:
            weapon_type = parts[2]  # Sword, Mace, etc.
            patterns.extend([
                f"{base_url}Gear/Weapons/{weapon_type}/TUI_Icon_{item_code}_64.webp",
                f"{base_url}Gear/Weapons/TUI_Icon_{item_code}_64.webp",
            ])
    
    # Also try the patterns we know work
    patterns.extend([
        f"{base_url}Gear/Jewelry/TUI_Icon_{item_code}_64.webp",
        f"{base_url}Gear/Bags/TUI_Icon_{item_code}_64.webp",
        f"{base_url}TUI_Icon_{item_code}_64.webp",
    ])
    
    return patterns

def download_missing_icons():
    print("📥 Downloading missing item icons with complex patterns...")
    
    # Connect to database
    db_path = "data/database/db/mydb.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create icons directory
    icons_dir = "app/frontend-dev/src/assets/icons/items"
    os.makedirs(icons_dir, exist_ok=True)
    
    # Get items that don't have icons yet
    cursor.execute("""
        SELECT DISTINCT item_name, item_url, item_type 
        FROM named_mob_items 
        WHERE item_url IS NOT NULL AND item_url != ''
        AND item_name IN ('Mismatched Bloody Boots', 'Ancient Dunzen Longsword', 'Wand of Allurement', 'Waterlogged Gloves', 'Breaching Pickaxe')
        ORDER BY item_name
    """)
    
    items = cursor.fetchall()
    print(f"Testing with {len(items)} problematic items...")
    
    downloaded = 0
    for item_name, item_url, item_type in items:
        try:
            # Extract item code
            item_code = item_url.split('/item/')[1].split('?')[0]
            
            # Generate filename
            safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', item_name.lower())
            filename = f"{safe_name}.webp"
            filepath = os.path.join(icons_dir, filename)
            
            if os.path.exists(filepath):
                print(f"  ⏭️  {item_name}: Already exists")
                continue
            
            print(f"  📥 {item_name} ({item_code})")
            
            # Try complex patterns
            patterns = try_complex_patterns(item_code, item_name)
            
            success = False
            for pattern in patterns:
                try:
                    response = requests.get(pattern, timeout=10)
                    if response.status_code == 200:
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        print(f"    ✅ Downloaded from: {pattern.split('/')[-2]}")
                        downloaded += 1
                        success = True
                        break
                    else:
                        print(f"    ❌ {pattern.split('/')[-2]}: {response.status_code}")
                except:
                    print(f"    ❌ {pattern.split('/')[-2]}: Error")
            
            if not success:
                print(f"    ❌ All patterns failed for {item_name}")
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"    ❌ Error processing {item_name}: {e}")
    
    conn.close()
    print(f"\n✅ Downloaded {downloaded} additional icons")

if __name__ == "__main__":
    download_missing_icons()
