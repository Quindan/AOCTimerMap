#!/usr/bin/env python3
"""
Download item icons by scraping the actual Codex item pages to get real icon URLs
"""
import sqlite3
import requests
import os
import re
import time
from bs4 import BeautifulSoup

def get_icon_from_page(item_url):
    """Get the actual icon URL from the Codex item page"""
    try:
        response = requests.get(item_url, timeout=15)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for the item icon image
        # Pattern: <img src="https://cdn.ashescodex.com/UI/Icons/Items/..."
        icon_imgs = soup.find_all('img', src=lambda x: x and 'cdn.ashescodex.com/UI/Icons/Items' in x)
        
        for img in icon_imgs:
            src = img.get('src')
            if src and '_64.webp' in src:
                return src
                
        return None
        
    except Exception as e:
        print(f"    Error scraping page: {e}")
        return None

def download_icons_from_pages():
    print("📥 Downloading item icons by scraping Codex pages...")
    
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
    
    # Get items that failed in previous attempts (no existing icons)
    cursor.execute("""
        SELECT DISTINCT item_name, item_url, item_type 
        FROM named_mob_items 
        WHERE item_url IS NOT NULL AND item_url != ''
        ORDER BY item_type, item_name
        LIMIT 20
    """)
    
    items = cursor.fetchall()
    print(f"Testing with {len(items)} items...")
    
    downloaded = 0
    for item_name, item_url, item_type in items:
        try:
            # Generate filename
            safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', item_name.lower())
            filename = f"{safe_name}.webp"
            filepath = os.path.join(icons_dir, filename)
            
            # Skip if already exists
            if os.path.exists(filepath):
                print(f"  ⏭️  {item_name}: Already exists")
                continue
            
            print(f"  📥 {item_name}: Scraping {item_url}")
            
            # Get the real icon URL from the page
            icon_url = get_icon_from_page(item_url)
            
            if icon_url:
                print(f"    🔗 Found icon: {icon_url}")
                
                # Download the icon
                icon_response = requests.get(icon_url, timeout=15)
                if icon_response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(icon_response.content)
                    print(f"    ✅ Downloaded: {filename}")
                    downloaded += 1
                else:
                    print(f"    ❌ Download failed: {icon_response.status_code}")
            else:
                print(f"    ❌ No icon found on page")
            
            # Be nice to the server
            time.sleep(1)
            
        except Exception as e:
            print(f"    ❌ Error processing {item_name}: {e}")
    
    conn.close()
    print(f"\n✅ Downloaded {downloaded} additional icons using page scraping")
    print(f"📁 Icons saved to: {icons_dir}")

if __name__ == "__main__":
    download_icons_from_pages()
