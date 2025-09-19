#!/usr/bin/env python3
"""
Extract item GRADES from Codex pages (not rarities)
Grade determines the color scheme: Initiate, Adept, Radiant
"""
import sqlite3
import requests
import re
import time

def extract_grade_from_codex(item_url):
    """Extract the Grade from a Codex item page"""
    try:
        print(f"    🔍 Scraping: {item_url}")
        response = requests.get(item_url, timeout=15)
        if response.status_code != 200:
            return None
        
        # Look for Grade information in the HTML
        # Pattern: <span class="text-white/80">Radiant</span> after "Grade:"
        grade_match = re.search(r'Grade:</span>\s*<span[^>]*>([^<]+)</span>', response.text)
        
        if grade_match:
            grade = grade_match.group(1).strip()
            print(f"    ✅ Found grade: {grade}")
            return grade
        else:
            print(f"    ❌ No grade found")
            return None
            
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return None

def update_item_grades():
    """Update database with item grades from Codex"""
    print("🔍 Extracting item grades from Codex pages...")
    
    # Connect to database  
    db_path = "data/database/db/mydb.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Add grade column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE named_mob_items ADD COLUMN item_grade TEXT")
        print("✅ Added item_grade column")
    except:
        print("✅ item_grade column already exists")
    
    # Get items without grades
    cursor.execute("""
        SELECT id, item_name, item_url, item_rarity 
        FROM named_mob_items 
        WHERE item_url IS NOT NULL AND item_url != ''
        AND (item_grade IS NULL OR item_grade = '')
        ORDER BY item_name
        LIMIT 20
    """)
    
    items = cursor.fetchall()
    print(f"Processing {len(items)} items...")
    
    updated = 0
    for item_id, item_name, item_url, item_rarity in items:
        print(f"📥 {item_name} (Rarity: {item_rarity})")
        
        grade = extract_grade_from_codex(item_url)
        
        if grade:
            # Update database with grade
            cursor.execute("UPDATE named_mob_items SET item_grade = ? WHERE id = ?", (grade, item_id))
            updated += 1
        
        # Be nice to the server
        time.sleep(1)
    
    conn.commit()
    
    # Show grade distribution
    cursor.execute("SELECT item_grade, COUNT(*) FROM named_mob_items WHERE item_grade IS NOT NULL GROUP BY item_grade")
    grade_dist = cursor.fetchall()
    
    print(f"\n✅ Updated {updated} items with grades")
    print(f"📊 Grade distribution:")
    for grade, count in grade_dist:
        print(f"  • {grade}: {count} items")
    
    conn.close()

if __name__ == "__main__":
    update_item_grades()
