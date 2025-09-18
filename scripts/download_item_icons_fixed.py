#!/usr/bin/env python3
"""
Download item icons from Ashes Codex CDN using correct URL pattern
"""
import sqlite3
import requests
import os
import re
import time

def download_item_icons():
    print("📥 Downloading item icons from Ashes Codex CDN...")
    
    # Connect to database
    db_path = "data/database/db/mydb.sqlite"
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create icons directory
    icons_dir = "app/frontend-dev/src/assets/icons/items"
    os.makedirs(icons_dir, exist_ok=True)
    
    # Get sample items to test the URL pattern
    cursor.execute("""
        SELECT DISTINCT item_name, item_url, item_type 
        FROM named_mob_items 
        WHERE item_url IS NOT NULL AND item_url != ''
        AND item_name IN ('Forgelord''s Signet', 'Ancient Dunzen Longsword', 'Wand of Allurement', 'Bloodied Bone Ring', 'Waterlogged Gloves')
        ORDER BY item_name
    """)
    
    items = cursor.fetchall()
    print(f"Testing with {len(items)} sample items...")
    
    downloaded = 0
    for item_name, item_url, item_type in items:
        try:
            # Extract item code from URL
            if '/item/' in item_url:
                item_code = item_url.split('/item/')[1].split('?')[0]
                
                # Determine icon path based on item type and code
                icon_paths = []
                
                # Try different icon URL patterns based on item code
                if item_code.startswith('Gear_Weapon_'):
                    # Weapons: /UI/Icons/Items/Gear/Weapons/
                    weapon_type = item_code.split('_')[2]  # Sword, Mace, etc.
                    icon_paths.append(f"https://cdn.ashescodex.com/UI/Icons/Items/Gear/Weapons/TUI_Icon_{item_code}_64.webp")
                elif item_code.startswith('Gear_Accessory_'):
                    # Accessories: /UI/Icons/Items/Gear/Jewelry/
                    icon_paths.append(f"https://cdn.ashescodex.com/UI/Icons/Items/Gear/Jewelry/TUI_Icon_{item_code}_64.webp")
                elif item_code.startswith('Gear_Armor_'):
                    # Armor: /UI/Icons/Items/Gear/Armor/
                    icon_paths.append(f"https://cdn.ashescodex.com/UI/Icons/Items/Gear/Armor/TUI_Icon_{item_code}_64.webp")
                elif item_code.startswith('Bag_'):
                    # Bags: /UI/Icons/Items/Gear/Bags/
                    icon_paths.append(f"https://cdn.ashescodex.com/UI/Icons/Items/Gear/Bags/TUI_Icon_{item_code}_64.webp")
                
                # Also try generic pattern
                icon_paths.append(f"https://cdn.ashescodex.com/UI/Icons/Items/TUI_Icon_{item_code}_64.webp")
                
                # Generate filename
                safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', item_name.lower())
                filename = f"{safe_name}.webp"
                filepath = os.path.join(icons_dir, filename)
                
                # Skip if already exists
                if os.path.exists(filepath):
                    print(f"  ⏭️  {item_name}: Already exists")
                    continue
                
                # Try each icon URL
                success = False
                for icon_url in icon_paths:
                    print(f"  📥 {item_name}: {icon_url}")
                    try:
                        response = requests.get(icon_url, timeout=10)
                        
                        if response.status_code == 200:
                            with open(filepath, 'wb') as f:
                                f.write(response.content)
                            print(f"    ✅ Downloaded: {filename}")
                            downloaded += 1
                            success = True
                            break
                        else:
                            print(f"    ❌ Failed: {response.status_code}")
                    except Exception as e:
                        print(f"    ❌ Error: {e}")
                
                if not success:
                    print(f"    ❌ All URLs failed for {item_name}")
                
                # Be nice to the server
                time.sleep(0.5)
                
        except Exception as e:
            print(f"    ❌ Error processing {item_name}: {e}")
    
    conn.close()
    print(f"\n✅ Downloaded {downloaded} item icons")
    print(f"📁 Icons saved to: {icons_dir}")

if __name__ == "__main__":
    download_item_icons()
