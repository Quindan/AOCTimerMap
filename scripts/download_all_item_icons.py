#!/usr/bin/env python3
"""
Download ALL item icons for special items from Ashes Codex CDN
"""
import sqlite3
import requests
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_icon(item_data):
    item_name, item_url, item_type = item_data
    icons_dir = "app/frontend-dev/src/assets/icons/items"
    
    try:
        # Extract item code from URL
        if '/item/' not in item_url:
            return f"❌ {item_name}: Invalid URL"
            
        item_code = item_url.split('/item/')[1].split('?')[0]
        
        # Generate filename
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', item_name.lower())
        filename = f"{safe_name}.webp"
        filepath = os.path.join(icons_dir, filename)
        
        # Skip if already exists
        if os.path.exists(filepath):
            return f"⏭️  {item_name}: Already exists"
        
        # Try different icon URL patterns based on item code
        icon_urls = []
        
        if item_code.startswith('Gear_Weapon_'):
            icon_urls.append(f"https://cdn.ashescodex.com/UI/Icons/Items/Gear/Weapons/TUI_Icon_{item_code}_64.webp")
        elif item_code.startswith('Gear_Accessory_'):
            icon_urls.append(f"https://cdn.ashescodex.com/UI/Icons/Items/Gear/Jewelry/TUI_Icon_{item_code}_64.webp")
        elif item_code.startswith('Gear_Armor_'):
            icon_urls.append(f"https://cdn.ashescodex.com/UI/Icons/Items/Gear/Armor/TUI_Icon_{item_code}_64.webp")
        elif item_code.startswith('Bag_'):
            icon_urls.append(f"https://cdn.ashescodex.com/UI/Icons/Items/Gear/Bags/TUI_Icon_{item_code}_64.webp")
        elif item_code.startswith('Gear_Artisan_'):
            icon_urls.append(f"https://cdn.ashescodex.com/UI/Icons/Items/Gear/Artisan/TUI_Icon_{item_code}_64.webp")
        
        # Also try generic patterns
        icon_urls.extend([
            f"https://cdn.ashescodex.com/UI/Icons/Items/TUI_Icon_{item_code}_64.webp",
            f"https://cdn.ashescodex.com/UI/Icons/Items/Gear/TUI_Icon_{item_code}_64.webp",
            f"https://cdn.ashescodex.com/UI/Icons/Gear/TUI_Icon_{item_code}_64.webp"
        ])
        
        # Try each URL
        for icon_url in icon_urls:
            try:
                response = requests.get(icon_url, timeout=15)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    return f"✅ {item_name}: Downloaded from {icon_url.split('/')[-2]}"
            except:
                continue
        
        return f"❌ {item_name}: All URLs failed"
        
    except Exception as e:
        return f"❌ {item_name}: Error - {e}"

def download_all_item_icons():
    print("📥 Downloading ALL item icons from Ashes Codex CDN...")
    
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
    
    # Get ALL special items
    cursor.execute("""
        SELECT DISTINCT item_name, item_url, item_type 
        FROM named_mob_items 
        WHERE item_url IS NOT NULL AND item_url != ''
        ORDER BY item_type, item_name
    """)
    
    items = cursor.fetchall()
    print(f"Found {len(items)} items to download...")
    
    # Download in parallel (but be nice to the server)
    downloaded = 0
    failed = 0
    
    # Process in batches to be nice to the server
    batch_size = 10
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(download_icon, item) for item in batch]
            
            for future in as_completed(futures):
                result = future.result()
                print(f"  {result}")
                if "✅" in result:
                    downloaded += 1
                else:
                    failed += 1
        
        # Pause between batches
        if i + batch_size < len(items):
            print(f"  💤 Pausing between batches... ({i+batch_size}/{len(items)})")
            time.sleep(2)
    
    conn.close()
    print(f"\n📊 Results:")
    print(f"✅ Downloaded: {downloaded}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Icons saved to: {icons_dir}")

if __name__ == "__main__":
    download_all_item_icons()
