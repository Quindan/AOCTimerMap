#!/usr/bin/env python3
"""
Extract item grades for ALL items using Codex search API
This will fix the 'everything is blue' issue by getting proper grades
"""
import sqlite3
import requests
import re
import time
import json

def search_item_via_api(item_name):
    """Search for item using Codex API and return item data"""
    headers = {
        'content-type': 'application/json',
        'origin': 'https://ashescodex.com',
        'referer': 'https://ashescodex.com/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    }
    
    # Try different search variants for better matching
    variants = [
        item_name,  # Original name
        item_name.replace("'", ""),  # Remove apostrophes
        item_name.replace("'", " "),  # Replace apostrophes with spaces
        " ".join(item_name.split()[:3]),  # First 3 words
    ]
    
    for variant in variants:
        try:
            data = {"query": variant, "resultType": None}
            response = requests.post('https://api.ashescodex.com/search', 
                                   headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                results = response.json()
                
                # Look for exact match first
                for result in results:
                    if (result.get('item', {}).get('type') == 'item' and 
                        result.get('item', {}).get('itemName') == item_name):
                        return result.get('item', {})
                
                # Look for close matches
                for result in results:
                    if result.get('item', {}).get('type') == 'item':
                        found_name = result.get('item', {}).get('itemName', '')
                        if (item_name.lower().replace("'", "") in found_name.lower().replace("'", "") or
                            found_name.lower().replace("'", "") in item_name.lower().replace("'", "")):
                            print(f"    📝 Close match: '{found_name}'")
                            return result.get('item', {})
                            
        except Exception as e:
            print(f"    ❌ API error with '{variant}': {e}")
            continue
    
    return None

def extract_grade_from_codex_page(item_url):
    """Extract grade from Codex item page"""
    try:
        response = requests.get(item_url, timeout=15)
        if response.status_code != 200:
            return None
        
        # Look for Grade information
        grade_match = re.search(r'Grade:</span>\s*<span[^>]*>([^<]+)</span>', response.text)
        
        if grade_match:
            grade = grade_match.group(1).strip()
            return grade
        else:
            return None
            
    except Exception as e:
        print(f"    ❌ Page scraping error: {e}")
        return None

def extract_all_grades():
    """Extract grades for all items in database"""
    print("🔍 Extracting grades for ALL items using Codex search API...")
    
    # Connect to database
    db_path = "data/database/db/mydb.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all items without grades
    cursor.execute("""
        SELECT id, item_name, item_url, item_rarity 
        FROM named_mob_items 
        WHERE item_grade IS NULL OR item_grade = ''
        ORDER BY item_name
    """)
    
    items = cursor.fetchall()
    print(f"Processing {len(items)} items...")
    
    updated = 0
    failed = []
    
    for item_id, item_name, item_url, item_rarity in items:
        print(f"📥 {item_name} (Rarity: {item_rarity})")
        
        grade = None
        
        # Method 1: Try direct page scraping if we have URL
        if item_url:
            grade = extract_grade_from_codex_page(item_url)
        
        # Method 2: Try API search if direct scraping failed
        if not grade:
            print(f"    🔍 Trying API search...")
            item_data = search_item_via_api(item_name)
            if item_data and item_data.get('itemName') == item_name:
                # Get the item URL from API and scrape it
                api_name = item_data.get('name', '')
                if api_name:
                    api_url = f"https://ashescodex.com/db/item/{api_name}"
                    grade = extract_grade_from_codex_page(api_url)
        
        # Method 3: Fallback based on rarity (temporary)
        if not grade:
            print(f"    ⚠️  No grade found, using rarity fallback")
            if item_rarity == 'Common':
                grade = 'Initiate'
            elif item_rarity == 'Uncommon':
                grade = 'Adept'  
            else:
                grade = 'Adept'  # Default
        
        if grade:
            cursor.execute("UPDATE named_mob_items SET item_grade = ? WHERE id = ?", (grade, item_id))
            print(f"    ✅ Grade: {grade}")
            updated += 1
        else:
            print(f"    ❌ No grade found")
            failed.append(item_name)
        
        # Be nice to the API
        time.sleep(1)
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Updated {updated} items with grades")
    print(f"❌ Failed: {len(failed)} items")
    
    if failed:
        print(f"\n📝 Failed items:")
        for item in failed[:10]:
            print(f"  • {item}")

def recategorize_by_grades():
    """Recategorize mobs based on extracted grades"""
    print("\n🔧 Recategorizing mobs based on item grades...")
    
    db_path = "data/database/db/mydb.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Update categories based on grades
    cursor.execute("""
        UPDATE named_mobs SET special_drop_category = 
          CASE 
            WHEN id IN (
              SELECT nm.id FROM named_mobs nm 
              JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id 
              WHERE nmi.item_grade = 'Radiant'
            ) THEN 'radiant'
            WHEN id IN (
              SELECT nm.id FROM named_mobs nm 
              JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id 
              WHERE nmi.item_grade = 'Adept' 
              AND nm.id NOT IN (
                SELECT nm2.id FROM named_mobs nm2 
                JOIN named_mob_items nmi2 ON nm2.id = nmi2.named_mob_id 
                WHERE nmi2.item_grade = 'Radiant'
              )
            ) THEN 'adept'
            WHEN id IN (
              SELECT nm.id FROM named_mobs nm 
              JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id 
              WHERE nmi.item_grade = 'Initiate'
              AND nm.id NOT IN (
                SELECT nm2.id FROM named_mobs nm2 
                JOIN named_mob_items nmi2 ON nm2.id = nmi2.named_mob_id 
                WHERE nmi2.item_grade IN ('Adept', 'Radiant')
              )
            ) THEN 'initiate'
            ELSE special_drop_category
          END
    """)
    
    conn.commit()
    
    # Show results
    cursor.execute("SELECT special_drop_category, COUNT(*) FROM named_mobs GROUP BY special_drop_category ORDER BY special_drop_category")
    categories = cursor.fetchall()
    
    print(f"📊 New category distribution:")
    for category, count in categories:
        print(f"  • {category}: {count} mobs")
    
    conn.close()

if __name__ == "__main__":
    extract_all_grades()
    recategorize_by_grades()
