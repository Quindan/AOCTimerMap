#!/usr/bin/env python3
"""
Extract icon URLs from Codex item pages and store them in database for future use
"""
import sqlite3
import requests
import re
import time

def extract_icon_from_page(item_url):
    """Extract the icon URL from a Codex item page"""
    try:
        print(f"    🔍 Scraping: {item_url}")
        response = requests.get(item_url, timeout=15)
        if response.status_code != 200:
            return None
        
        # Look for the icon URL in the HTML
        # Pattern: src="https://cdn.ashescodex.com/UI/Icons/Items/...64.webp"
        icon_matches = re.findall(r'src="(https://cdn\.ashescodex\.com/UI/Icons/Items/[^"]*64\.webp)"', response.text)
        
        if icon_matches:
            icon_url = icon_matches[0]
            print(f"    ✅ Found icon: {icon_url}")
            return icon_url
        else:
            print(f"    ❌ No icon found")
            return None
            
    except Exception as e:
        print(f"    ❌ Error scraping: {e}")
        return None

def extract_all_icon_urls():
    print("🔍 Extracting icon URLs from Codex pages...")
    
    # Connect to database
    db_path = "data/database/db/mydb.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Add icon_url column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE named_mob_items ADD COLUMN icon_url TEXT")
        print("✅ Added icon_url column to database")
    except:
        print("✅ icon_url column already exists")
    
    # Get items without icon URLs
    cursor.execute("""
        SELECT id, item_name, item_url 
        FROM named_mob_items 
        WHERE item_url IS NOT NULL AND item_url != ''
        AND (icon_url IS NULL OR icon_url = '')
        ORDER BY item_name
        LIMIT 10
    """)
    
    items = cursor.fetchall()
    print(f"Processing {len(items)} items...")
    
    updated = 0
    for item_id, item_name, item_url in items:
        print(f"📥 {item_name}")
        
        icon_url = extract_icon_from_page(item_url)
        
        if icon_url:
            # Update database with icon URL
            cursor.execute("UPDATE named_mob_items SET icon_url = ? WHERE id = ?", (icon_url, item_id))
            updated += 1
        
        # Be nice to the server
        time.sleep(1)
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Updated {updated} items with icon URLs")
    print("📊 Now you can download icons using the exact URLs from the database!")

if __name__ == "__main__":
    extract_all_icon_urls()
