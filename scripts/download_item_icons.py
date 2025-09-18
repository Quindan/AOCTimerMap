#!/usr/bin/env python3
"""
Download item icons from Ashes Codex for special items
"""
import sqlite3
import requests
import os
import re
from urllib.parse import urlparse
import time

def download_item_icons():
    print("📥 Downloading item icons from Ashes Codex...")
    
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
    
    # Get all special items
    cursor.execute("""
        SELECT DISTINCT item_name, item_url, item_type 
        FROM named_mob_items 
        WHERE item_url IS NOT NULL AND item_url != ''
        ORDER BY item_name
    """)
    
    items = cursor.fetchall()
    print(f"Found {len(items)} items to download icons for")
    
    downloaded = 0
    for item_name, item_url, item_type in items:
        try:
            # Extract item code from URL
            # Example: https://ashescodex.com/db/item/Gear_Weapon_Sword_2H_T2_Jannus?rarity=1
            if '/item/' in item_url:
                item_code = item_url.split('/item/')[1].split('?')[0]
                
                # Generate icon URL
                icon_url = f"https://ashescodex.com/images/items/{item_code}.png"
                
                # Generate filename
                safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', item_name.lower())
                filename = f"{safe_name}.png"
                filepath = os.path.join(icons_dir, filename)
                
                # Skip if already exists
                if os.path.exists(filepath):
                    print(f"  ⏭️  {item_name}: Already exists")
                    continue
                
                # Download icon
                print(f"  📥 {item_name}: {icon_url}")
                response = requests.get(icon_url, timeout=10)
                
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"    ✅ Downloaded: {filename}")
                    downloaded += 1
                else:
                    print(f"    ❌ Failed: {response.status_code}")
                
                # Be nice to the server
                time.sleep(0.5)
                
        except Exception as e:
            print(f"    ❌ Error downloading {item_name}: {e}")
    
    conn.close()
    print(f"\n✅ Downloaded {downloaded} item icons")
    print(f"📁 Icons saved to: {icons_dir}")
    
    # Update Angular assets configuration
    print("\n📝 Updating Angular assets...")
    angular_json_path = "app/frontend-dev/angular.json"
    try:
        with open(angular_json_path, 'r') as f:
            content = f.read()
        
        # Check if items icons are already in assets
        if '"src/assets/icons/items"' not in content:
            # Add to assets array
            content = content.replace(
                '"src/assets"',
                '"src/assets",\n              {\n                "glob": "**/*",\n                "input": "src/assets/icons/items",\n                "output": "/assets/icons/items"\n              }'
            )
            
            with open(angular_json_path, 'w') as f:
                f.write(content)
            print("✅ Angular assets updated")
        else:
            print("✅ Angular assets already configured")
            
    except Exception as e:
        print(f"❌ Error updating Angular config: {e}")

if __name__ == "__main__":
    download_item_icons()
