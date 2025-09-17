#!/usr/bin/env python3
"""
Add some sample items to test the new named_mob_items functionality.
This will add items for a few well-known named mobs based on common knowledge.
"""

import sqlite3
import sys

def add_sample_items():
    """Add sample items for testing purposes."""
    conn = sqlite3.connect('data/database/db/mydb.sqlite')
    cursor = conn.cursor()
    
    # Sample items based on common Ashes of Creation knowledge
    sample_items = [
        # Format: (mob_name, item_name, item_url, rarity, type, drop_order)
        ('Chief Armorer Jannus', 'Buttressed Shield', 'https://ashescodex.com/db/item/Gear_Weapon_Shield_OH_Jannus', 'Uncommon', 'Shield', 1),
        ('Wormwig', 'Wormwig Trinket', 'https://ashescodex.com/db/item/wormwig-trinket', 'Rare', 'Accessory', 1),
        
        # Add some more examples for testing
        ('Administrator Crucia', 'Administrative Seal', 'https://ashescodex.com/db/item/administrative-seal', 'Rare', 'Accessory', 1),
        ('Administrator Crucia', 'Crucia\'s Ledger', 'https://ashescodex.com/db/item/crucias-ledger', 'Uncommon', 'Consumable', 2),
        
        ('Bellowsmasher', 'Forge Hammer', 'https://ashescodex.com/db/item/forge-hammer', 'Epic', 'Weapon', 1),
        ('Bellowsmasher', 'Bellows Components', 'https://ashescodex.com/db/item/bellows-components', 'Common', 'Material', 2),
        
        ('Captain Bulwark', 'Captain\'s Bulwark', 'https://ashescodex.com/db/item/captains-bulwark', 'Epic', 'Shield', 1),
        ('Captain Bulwark', 'Naval Insignia', 'https://ashescodex.com/db/item/naval-insignia', 'Rare', 'Accessory', 2),
        
        ('Forgelord Zammer', 'Zammer\'s Anvil Fragment', 'https://ashescodex.com/db/item/zammers-anvil-fragment', 'Legendary', 'Material', 1),
        ('Forgelord Zammer', 'Masterwork Tongs', 'https://ashescodex.com/db/item/masterwork-tongs', 'Epic', 'Tool', 2),
    ]
    
    added_count = 0
    
    for mob_name, item_name, item_url, rarity, item_type, drop_order in sample_items:
        # Get the mob ID
        cursor.execute("SELECT id FROM named_mobs WHERE name = ?", (mob_name,))
        mob_result = cursor.fetchone()
        
        if not mob_result:
            print(f"Warning: Mob '{mob_name}' not found in database")
            continue
            
        mob_id = mob_result[0]
        
        # Check if item already exists
        cursor.execute("""
            SELECT id FROM named_mob_items 
            WHERE named_mob_id = ? AND item_name = ?
        """, (mob_id, item_name))
        
        if cursor.fetchone():
            print(f"Item '{item_name}' already exists for '{mob_name}', skipping")
            continue
        
        # Add the item
        cursor.execute("""
            INSERT INTO named_mob_items 
            (named_mob_id, item_name, item_url, item_rarity, item_type, drop_order)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (mob_id, item_name, item_url, rarity, item_type, drop_order))
        
        added_count += 1
        print(f"Added '{item_name}' ({rarity} {item_type}) to '{mob_name}'")
    
    conn.commit()
    conn.close()
    
    print(f"\nAdded {added_count} sample items successfully!")
    
    # Show summary
    conn = sqlite3.connect('data/database/db/mydb.sqlite')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            nm.name,
            COUNT(nmi.id) as item_count
        FROM named_mobs nm
        LEFT JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id
        GROUP BY nm.id, nm.name
        HAVING item_count > 0
        ORDER BY item_count DESC, nm.name
        LIMIT 10
    """)
    
    print("\nNamed mobs with special items:")
    print("=" * 40)
    for mob_name, item_count in cursor.fetchall():
        print(f"{mob_name:30s} | {item_count} items")
    
    conn.close()

if __name__ == "__main__":
    add_sample_items()
