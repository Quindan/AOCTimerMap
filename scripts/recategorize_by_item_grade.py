#!/usr/bin/env python3
"""
Recategorize mobs based on the grade of their special items, not mob level
"""
import sqlite3

def recategorize_mobs_by_item_grade():
    print("🔧 Recategorizing mobs based on item grades...")
    
    # Connect to database
    db_path = "data/database/db/mydb.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all mobs with their highest item grade
    cursor.execute("""
        SELECT nm.id, nm.name, nm.level, nm.special_drop_category,
               GROUP_CONCAT(nmi.item_rarity) as item_rarities,
               MAX(CASE 
                   WHEN nmi.item_rarity = 'Common' THEN 1
                   WHEN nmi.item_rarity = 'Uncommon' THEN 2  
                   WHEN nmi.item_rarity = 'Rare' THEN 3
                   WHEN nmi.item_rarity = 'Epic' THEN 4
                   WHEN nmi.item_rarity = 'Legendary' THEN 5
                   ELSE 0 END) as max_grade
        FROM named_mobs nm 
        LEFT JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id 
        GROUP BY nm.id
        ORDER BY nm.name
    """)
    
    mobs = cursor.fetchall()
    
    updated = 0
    for mob_id, name, level, current_category, item_rarities, max_grade in mobs:
        
        # Determine new category based on item grade
        if max_grade is None or max_grade == 0:
            new_category = 'noSpecialDrop'
        elif max_grade == 1:  # Common
            new_category = 'initiate'
        elif max_grade == 2:  # Uncommon  
            new_category = 'adept'
        elif max_grade >= 3:  # Rare, Epic, Legendary
            new_category = 'radiant'
        else:
            new_category = 'noSpecialDrop'
        
        # Update if category changed
        if current_category != new_category:
            cursor.execute("UPDATE named_mobs SET special_drop_category = ? WHERE id = ?", 
                         (new_category, mob_id))
            
            grade_name = {0: 'No items', 1: 'Common', 2: 'Uncommon', 3: 'Rare', 4: 'Epic', 5: 'Legendary'}.get(max_grade or 0, 'Unknown')
            
            print(f"📝 {name} (Level {level})")
            print(f"   Items: {item_rarities or 'None'} (Grade: {grade_name})")
            print(f"   Category: {current_category} → {new_category}")
            updated += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Updated {updated} mob categories based on item grades")
    
    # Show summary by category
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT special_drop_category, COUNT(*) as count
        FROM named_mobs 
        GROUP BY special_drop_category
        ORDER BY special_drop_category
    """)
    
    print(f"\n📊 Category distribution:")
    for category, count in cursor.fetchall():
        print(f"  • {category}: {count} mobs")
    
    conn.close()

if __name__ == "__main__":
    recategorize_mobs_by_item_grade()
