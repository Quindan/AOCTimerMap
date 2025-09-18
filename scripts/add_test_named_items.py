#!/usr/bin/env python3
"""
Add test special items for the 4 test mobs to verify the system works
Based on the _Named categories pattern
"""

import sqlite3

def add_test_items():
    """Add sample special items for testing"""
    db_path = '/app/database/db/mydb.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Test items based on _Named pattern examples
    test_items = {
        'Bloodmage Triune': [
            {
                'name': 'Cultist Bloodmage Staff',
                'url': 'https://ashescodex.com/db/item/Gear_Weapon_Staff_2H_Cultist_Mage_Triune1',
                'rarity': 'Uncommon',
                'type': 'Weapon',
                'drop_chance': '12%'
            }
        ],
        'Waterlogged Liffy': [
            {
                'name': 'Waterlogged Shell',
                'url': 'https://ashescodex.com/db/item/Gear_Accessory_Ring_Waterlogged_Liffy',
                'rarity': 'Common',
                'type': 'Accessory',
                'drop_chance': '25%'
            }
        ],
        'Crunch Trunk': [
            {
                'name': 'Crunch Bark Shield',
                'url': 'https://ashescodex.com/db/item/Gear_Weapon_Shield_OH_Crunch_Trunk_1',
                'rarity': 'Uncommon',
                'type': 'Weapon',
                'drop_chance': '8%'
            },
            {
                'name': 'Twisted Branch Material',
                'url': 'https://ashescodex.com/db/item/Resource_Material_Crunch_Trunk_Branch',
                'rarity': 'Common',
                'type': 'Material',
                'drop_chance': '35%'
            }
        ]
    }
    
    # Get mob IDs
    cursor.execute("SELECT id, name FROM named_mobs WHERE name IN (?, ?, ?, ?)", 
                  ('Bloodmage Triune', 'Waterlogged Liffy', 'Forgelord Zammer', 'Crunch Trunk'))
    mobs = {row[1]: row[0] for row in cursor.fetchall()}
    
    print("🎁 Adding test special items...")
    
    for mob_name, items in test_items.items():
        if mob_name in mobs:
            mob_id = mobs[mob_name]
            print(f"\n📍 {mob_name} (ID: {mob_id})")
            
            # Clear existing test items (but preserve Forgelord Zammer's real items)
            if mob_name != 'Forgelord Zammer':
                cursor.execute("DELETE FROM named_mob_items WHERE named_mob_id = ?", (mob_id,))
            
            # Add new test items
            for i, item in enumerate(items, 1):
                cursor.execute("""
                    INSERT INTO named_mob_items 
                    (named_mob_id, item_name, item_url, item_rarity, item_type, drop_order, drop_chance)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (mob_id, item['name'], item['url'], item['rarity'], item['type'], i, item['drop_chance']))
                
                print(f"    ✅ Added: {item['name']} ({item['drop_chance']}) - {item['type']}")
    
    conn.commit()
    conn.close()
    
    print(f"\n💾 Test items added successfully!")
    print(f"\n🌐 You can now test the map at: http://localhost:9090")
    print(f"The special items should appear in the named mob popups with:")
    print(f"  - Item names with proper color (not white on white)")
    print(f"  - Drop chances instead of [uncommon] labels")
    print(f"  - Codex hover tooltips on item links")

def verify_items():
    """Verify the items were added correctly"""
    db_path = '/app/database/db/mydb.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"\n🔍 Verifying added items...")
    cursor.execute("""
        SELECT nm.name, nmi.item_name, nmi.drop_chance, nmi.item_type 
        FROM named_mobs nm 
        JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id 
        WHERE nm.name IN ('Bloodmage Triune', 'Waterlogged Liffy', 'Forgelord Zammer', 'Crunch Trunk') 
        ORDER BY nm.name, nmi.drop_order
    """)
    
    current_mob = None
    for row in cursor.fetchall():
        mob_name, item_name, drop_chance, item_type = row
        if mob_name != current_mob:
            print(f"\n📍 {mob_name}:")
            current_mob = mob_name
        print(f"    - {item_name} ({drop_chance}) - {item_type}")
    
    conn.close()

def main():
    print("🎯 Adding Test _Named Items")
    print("=" * 30)
    
    add_test_items()
    verify_items()

if __name__ == "__main__":
    main()
