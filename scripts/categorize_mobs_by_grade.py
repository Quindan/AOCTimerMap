#!/usr/bin/env python3
"""
Categorize named mobs by their grade tier based on special drops
- initiate: 0-9 level mobs or drop initiate grade gear only
- adept: 10-19 level mobs or drop at most adept grade gear  
- radiant: 20+ level mobs or drop at least radiant grade gear
- noSpecialDrop: already marked, will show as grey
"""

import sqlite3
import subprocess
import json
import re
import time

def get_item_grade_from_codex(item_url):
    """Get item grade from Codex item page"""
    try:
        # Extract item code from URL
        if '/db/item/' in item_url:
            item_code = item_url.split('/db/item/')[-1]
            
            # Fetch item page
            result = subprocess.run(['curl', '-s', f"https://ashescodex.com/db/item/{item_code}"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                return "Unknown"
                
            content = result.stdout
            
            # Look for grade information
            grade_patterns = [
                r'Grade:\s*([A-Z]+)',
                r'"grade":"([A-Z]+)"',
                r'grade.*?([A-Z]{1,2})'
            ]
            
            for pattern in grade_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    grade = match.group(1).upper()
                    if grade in ['NG', 'D', 'C', 'B', 'A', 'S']:
                        return grade
            
            return "Unknown"
            
    except Exception as e:
        return "Unknown"

def categorize_all_mobs():
    """Categorize all mobs based on their level and special drop grades"""
    db_path = '/app/database/db/mydb.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all mobs with their items
    cursor.execute("""
        SELECT nm.id, nm.name, nm.level, 
               GROUP_CONCAT(nmi.item_url) as item_urls,
               COUNT(nmi.id) as item_count
        FROM named_mobs nm 
        LEFT JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id 
        WHERE nm.special_drop_category IS NULL
        GROUP BY nm.id, nm.name, nm.level
        ORDER BY nm.level, nm.name
    """)
    
    mobs = cursor.fetchall()
    
    print(f"🏷️ Categorizing {len(mobs)} mobs by grade tier...")
    
    categories = {
        'initiate': 0,
        'adept': 0, 
        'radiant': 0
    }
    
    for mob in mobs:
        mob_id, name, level, item_urls, item_count = mob
        
        print(f"\n📍 {name} (Level: {level}, Items: {item_count})")
        
        # Default categorization based on level
        if level is None:
            level = 0
            
        if level <= 9:
            category = 'initiate'
        elif level <= 19:
            category = 'adept'
        else:
            category = 'radiant'
        
        # If mob has special items, check their grades to potentially upgrade category
        if item_count > 0 and item_urls:
            highest_grade = 'NG'  # No Grade
            urls = item_urls.split(',') if item_urls else []
            
            for url in urls[:3]:  # Check first 3 items to avoid too many requests
                if url and url.strip():
                    grade = get_item_grade_from_codex(url.strip())
                    print(f"    🔍 Item grade: {grade}")
                    
                    # Grade hierarchy: NG < D < C < B < A < S
                    grade_order = {'NG': 0, 'D': 1, 'C': 2, 'B': 3, 'A': 4, 'S': 5, 'Unknown': 0}
                    if grade_order.get(grade, 0) > grade_order.get(highest_grade, 0):
                        highest_grade = grade
                
                # Rate limiting
                time.sleep(0.5)
            
            # Upgrade category based on highest item grade found
            if highest_grade in ['B', 'A', 'S']:  # High grades = radiant tier
                category = 'radiant'
            elif highest_grade in ['C']:  # Medium grade = adept tier
                if category == 'initiate':  # Only upgrade from initiate
                    category = 'adept'
            # D and NG grades don't change the level-based category
            
            print(f"    📊 Highest item grade: {highest_grade}")
        
        # Update database
        cursor.execute("UPDATE named_mobs SET special_drop_category = ? WHERE id = ?", (category, mob_id))
        categories[category] += 1
        
        print(f"    🏷️ Categorized as: {category}")
    
    conn.commit()
    conn.close()
    
    print(f"\n📊 Categorization complete:")
    print(f"  - Initiate (0-9): {categories['initiate']} mobs")
    print(f"  - Adept (10-19): {categories['adept']} mobs") 
    print(f"  - Radiant (20+): {categories['radiant']} mobs")

def show_category_summary():
    """Show summary of all categories"""
    db_path = '/app/database/db/mydb.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"\n📊 COMPLETE Category Summary:")
    
    cursor.execute("""
        SELECT special_drop_category, COUNT(*) as count
        FROM named_mobs 
        GROUP BY special_drop_category
        ORDER BY 
            CASE special_drop_category
                WHEN 'initiate' THEN 1
                WHEN 'adept' THEN 2  
                WHEN 'radiant' THEN 3
                WHEN 'noSpecialDrop' THEN 4
                ELSE 5
            END
    """)
    
    for row in cursor.fetchall():
        category, count = row
        if category:
            print(f"  - {category}: {count} mobs")
    
    # Show some examples from each category
    print(f"\n🎨 Suggested Marker Colors (avoiding quality colors):")
    print(f"  - 🔵 initiate (0-9): Light Blue / Cyan")
    print(f"  - 🟠 adept (10-19): Orange / Amber") 
    print(f"  - 🔴 radiant (20+): Red / Crimson")
    print(f"  - ⚫ noSpecialDrop: Grey / Dark Grey")
    
    conn.close()

def main():
    print("🎯 Categorizing Mobs by Grade Tier")
    print("=" * 35)
    
    categorize_all_mobs()
    show_category_summary()
    
    print(f"\n🌐 Ready for marker color implementation!")
    print(f"Each category can now have different colored markers on the map.")

if __name__ == "__main__":
    main()
