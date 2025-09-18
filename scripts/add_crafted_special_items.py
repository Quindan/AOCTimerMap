#!/usr/bin/env python3
"""
Add crafted special items that are associated with named mobs
These items don't drop directly but are crafted using materials from the mob
"""

import sqlite3

def add_crafted_special_items():
    """Add known crafted special items associated with named mobs"""
    db_path = '/app/database/db/mydb.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Known crafted special items associated with named mobs
    crafted_items = {
        'Sir Jenry The Strong': [
            {
                'name': 'Breaching Pickaxe',
                'url': 'https://ashescodex.com/db/item/Gear_Artisan_Mining_Tool_Pickaxe_T3_Jenry',
                'rarity': 'Common',
                'type': 'Artisan Tool',
                'drop_chance': '0% (Crafted)'
            }
        ]
        # Add more crafted items here as we discover them
    }
    
    # Get mob IDs
    mob_names = list(crafted_items.keys())
    placeholders = ','.join(['?'] * len(mob_names))
    cursor.execute(f"SELECT id, name FROM named_mobs WHERE name IN ({placeholders})", mob_names)
    mobs = {row[1]: row[0] for row in cursor.fetchall()}
    
    print("🔨 Adding crafted special items...")
    
    for mob_name, items in crafted_items.items():
        if mob_name in mobs:
            mob_id = mobs[mob_name]
            print(f"\n📍 {mob_name} (ID: {mob_id})")
            
            # Don't clear existing items - add to them
            existing_count = cursor.execute("SELECT COUNT(*) FROM named_mob_items WHERE named_mob_id = ?", (mob_id,)).fetchone()[0]
            
            # Add crafted items
            for i, item in enumerate(items, existing_count + 1):
                cursor.execute("""
                    INSERT INTO named_mob_items 
                    (named_mob_id, item_name, item_url, item_rarity, item_type, drop_order, drop_chance)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (mob_id, item['name'], item['url'], item['rarity'], item['type'], i, item['drop_chance']))
                
                print(f"    ✅ Added: {item['name']} ({item['drop_chance']}) - {item['type']}")
            
            # Hide this mob since it now has items
            cursor.execute("UPDATE named_mobs SET is_hidden = 1 WHERE id = ?", (mob_id,))
            print(f"    🙈 Hid {mob_name} (now has special items)")
    
    conn.commit()
    conn.close()
    
    print(f"\n💾 Crafted special items added successfully!")

def verify_crafted_items():
    """Verify the crafted items were added correctly"""
    db_path = '/app/database/db/mydb.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"\n🔍 Verifying crafted items...")
    cursor.execute("""
        SELECT nm.name, nmi.item_name, nmi.drop_chance, nmi.item_type 
        FROM named_mobs nm 
        JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id 
        WHERE nm.name = 'Sir Jenry The Strong'
        ORDER BY nmi.drop_order
    """)
    
    for row in cursor.fetchall():
        mob_name, item_name, drop_chance, item_type = row
        print(f"  - {item_name} ({drop_chance}) - {item_type}")
    
    conn.close()

def check_other_artisan_tools():
    """Check if there are other artisan tools we should look for"""
    print(f"\n🔍 Other potential artisan tool mobs to investigate:")
    
    # List of mobs that might have associated artisan tools or crafted items
    potential_artisan_mobs = [
        "Beta Hauler C3-82",  # Might have mining/hauling tools
        "Bonebinder Outhouser",  # Might have crafting tools
        "Hoarder",  # Might have storage items
        "Ravenous Lockbox"  # Might have lockpicking tools
    ]
    
    for mob in potential_artisan_mobs:
        print(f"  - {mob}: Check for associated crafted items")

def main():
    print("🎯 Adding Crafted Special Items")
    print("=" * 35)
    
    add_crafted_special_items()
    verify_crafted_items()
    check_other_artisan_tools()
    
    print(f"\n🌐 Test at: http://localhost:9090")
    print(f"Sir Jenry The Strong should now show the Breaching Pickaxe with 0% drop rate!")

if __name__ == "__main__":
    main()
