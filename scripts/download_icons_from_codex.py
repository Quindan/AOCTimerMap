#!/usr/bin/env python3
"""
Download icons directly from Codex pages using our database URLs
This approach uses the exact item URLs we already have in the database
"""
import sqlite3
import requests
import re
import os
import time

def extract_icon_from_codex_page(codex_url):
    """Extract icon URL from a Codex item page"""
    try:
        print(f"    🔍 Scraping: {codex_url}")
        response = requests.get(codex_url, timeout=15)
        if response.status_code != 200:
            print(f"    ❌ HTTP {response.status_code}")
            return None
        
        # Look for the icon URL in the HTML
        # Pattern: src="https://cdn.ashescodex.com/UI/Icons/Items/...64.webp"
        icon_matches = re.findall(r'cdn\.ashescodex\.com[^"]*64\.webp', response.text)
        
        if icon_matches:
            icon_url = f"https://{icon_matches[0]}"
            print(f"    ✅ Found: {icon_url}")
            return icon_url
        else:
            print(f"    ❌ No 64.webp icon found")
            return None
            
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return None

def download_icon(icon_url, filepath):
    """Download an icon to a file"""
    try:
        response = requests.get(icon_url, timeout=10)
        if response.status_code == 200 and len(response.content) > 100:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True
        else:
            print(f"    ❌ Download failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"    ❌ Download error: {e}")
        return False

def download_all_missing_icons():
    """Download icons for all items in database that don't have icons yet"""
    print("🔍 Downloading icons from Codex pages...")
    
    # Connect to database
    db_path = "data/database/db/mydb.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all items with Codex URLs
    cursor.execute("""
        SELECT DISTINCT item_name, item_url 
        FROM named_mob_items 
        WHERE item_url IS NOT NULL AND item_url != ''
        ORDER BY item_name
    """)
    
    items = cursor.fetchall()
    conn.close()
    
    icons_dir = "app/frontend-built/assets/icons/items/"
    dev_icons_dir = "app/frontend-dev/src/assets/icons/items/"
    downloaded = 0
    
    print(f"Processing {len(items)} items...")
    
    for item_name, item_url in items:
        # Create safe filename
        safe_name = item_name.lower().replace(' ', '_').replace("'", '').replace('-', '_')
        safe_name = ''.join(c for c in safe_name if c.isalnum() or c == '_')
        
        icon_path = os.path.join(icons_dir, f"{safe_name}.webp")
        dev_icon_path = os.path.join(dev_icons_dir, f"{safe_name}.webp")
        
        # Skip if already exists
        if os.path.exists(icon_path):
            print(f"⏭️  {item_name} (already exists)")
            continue
        
        print(f"📥 {item_name}")
        
        # Get icon URL from Codex page
        icon_url = extract_icon_from_codex_page(item_url)
        
        if icon_url:
            # Download to both directories
            if download_icon(icon_url, icon_path):
                # Copy to dev directory
                try:
                    with open(icon_path, 'rb') as src:
                        with open(dev_icon_path, 'wb') as dst:
                            dst.write(src.read())
                    print(f"    ✅ Downloaded and copied to dev")
                    downloaded += 1
                except Exception as e:
                    print(f"    ⚠️  Downloaded but failed to copy to dev: {e}")
                    downloaded += 1
            else:
                print(f"    ❌ Download failed")
        else:
            print(f"    ❌ No icon URL found")
        
        # Be nice to the server
        time.sleep(0.5)
    
    print(f"\n✅ Downloaded {downloaded} new icons")
    print(f"📊 Total icons now: {len(os.listdir(icons_dir))}")

if __name__ == "__main__":
    download_all_missing_icons()
