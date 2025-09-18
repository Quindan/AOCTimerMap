#!/usr/bin/env python3
"""
Fetch special items from Codex embed pages
Parses the "Possible Drops" table to find uncommon items and their drop rates
"""

import sqlite3
import requests
import re
import time
from urllib.parse import urljoin, unquote

def parse_codex_embed_page(mob_slug):
    """Parse the Codex embed page for a mob to extract special items"""
    try:
        url = f"https://ashescodex.com/db/mob/{mob_slug}?embed=true"
        print(f"📡 Fetching: {url}")
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content = response.text
        
        # Parse the "Possible Drops" table
        items = []
        
        # Look for table rows with item links and drop rates
        # Pattern: [Item Name ](/db/item/item-url) | | | Drop Rate
        pattern = r'\[([^]]+)\s+\]\(/db/item/([^)]+)\).*?(\d+(?:\.\d+)?%)'
        
        matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            item_name = match[0].strip()
            item_url_encoded = match[1]
            drop_rate = match[2]
            
            # Decode URL encoding
            item_url = unquote(item_url_encoded)
            full_item_url = f"https://ashescodex.com/db/item/{item_url}"
            
            # Determine item type and rarity based on patterns
            item_type = "Unknown"
            rarity = "Uncommon"  # Default for special drops
            
            if "Recipe" in item_name:
                item_type = "Recipe"
                rarity = "Common"
            elif "Fragment" in item_name or "Bone" in item_name:
                item_type = "Material"
                rarity = "Common"
            elif "Gear_Weapon" in item_url:
                item_type = "Weapon"
                rarity = "Uncommon"
            elif "Gear_Accessory" in item_url:
                item_type = "Accessory" 
                rarity = "Uncommon"
            elif "Gear_Armor" in item_url:
                item_type = "Armor"
                rarity = "Uncommon"
            
            # Only include uncommon items (the special drops)
            if rarity == "Uncommon":
                items.append({
                    'name': item_name,
                    'url': full_item_url,
                    'rarity': rarity,
                    'type': item_type,
                    'drop_chance': drop_rate
                })
                print(f"  ✅ Found special item: {item_name} ({drop_rate})")
        
        return items
        
    except Exception as e:
        print(f"  ❌ Error parsing {mob_slug}: {e}")
        return []

def update_mob_items(mob_id, mob_name, items):
    """Update the database with special items for a mob"""
    if not items:
        return
        
    db_path = '/app/database/db/mydb.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Clear existing items for this mob
    cursor.execute("DELETE FROM named_mob_items WHERE named_mob_id = ?", (mob_id,))
    
    # Add new items
    for i, item in enumerate(items, 1):
        cursor.execute("""
            INSERT INTO named_mob_items 
            (named_mob_id, item_name, item_url, item_rarity, item_type, drop_order, drop_chance)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (mob_id, item['name'], item['url'], item['rarity'], item['type'], i, item['drop_chance']))
        
        print(f"    ✅ Added: {item['name']} ({item['drop_chance']})")
    
    conn.commit()
    conn.close()

def process_named_mobs():
    """Process named mobs to fetch their special items"""
    db_path = '/app/database/db/mydb.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get named mobs with codex URLs (limit to test first)
    cursor.execute("""
        SELECT id, name, slug, codex_url 
        FROM named_mobs 
        WHERE codex_url IS NOT NULL 
        ORDER BY name
        LIMIT 10
    """)
    
    mobs = cursor.fetchall()
    conn.close()
    
    print(f"🔍 Processing {len(mobs)} named mobs...")
    
    processed = 0
    for mob in mobs:
        mob_id, name, slug, codex_url = mob
        
        print(f"\n📍 Processing: {name}")
        
        # Extract slug from codex URL
        if '/db/mob/' in codex_url:
            mob_slug = codex_url.split('/db/mob/')[-1]
            
            # Fetch items from Codex
            items = parse_codex_embed_page(mob_slug)
            
            if items:
                update_mob_items(mob_id, name, items)
                processed += 1
            else:
                print(f"  ⚠️  No special items found")
        
        # Rate limiting
        time.sleep(1)
    
    print(f"\n✅ Processed {processed} mobs with special items")

def main():
    print("🎯 Fetching Special Items from Codex")
    print("=" * 40)
    
    process_named_mobs()

if __name__ == "__main__":
    main()
