#!/usr/bin/env python3
"""
Script to research and populate special items for named mobs.
This script will help identify which named mobs need item data and 
provide a template for manually adding the items.
"""

import sqlite3
import json
import requests
from urllib.parse import urljoin
import time

def get_named_mobs_without_items():
    """Get all named mobs that don't have special items yet."""
    conn = sqlite3.connect('data/database/db/mydb.sqlite')
    cursor = conn.cursor()
    
    query = """
    SELECT nm.id, nm.name, nm.codex_url 
    FROM named_mobs nm 
    LEFT JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id 
    WHERE nmi.id IS NULL 
    ORDER BY nm.name
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    return results

def add_named_mob_item(named_mob_id, item_name, item_url, item_rarity, item_type, drop_order=1):
    """Add a special item for a named mob."""
    conn = sqlite3.connect('data/database/db/mydb.sqlite')
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO named_mob_items 
        (named_mob_id, item_name, item_url, item_rarity, item_type, drop_order)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (named_mob_id, item_name, item_url, item_rarity, item_type, drop_order))
    
    conn.commit()
    conn.close()
    print(f"Added item '{item_name}' for named mob ID {named_mob_id}")

def main():
    print("Named Mobs without special items:")
    print("=" * 50)
    
    mobs_without_items = get_named_mobs_without_items()
    
    for mob_id, mob_name, codex_url in mobs_without_items:
        print(f"ID: {mob_id:3d} | {mob_name:30s} | {codex_url}")
    
    print(f"\nTotal: {len(mobs_without_items)} named mobs need item data")
    
    # Example of how to add items manually:
    print("\n" + "=" * 50)
    print("Example usage to add items:")
    print("add_named_mob_item(mob_id, 'Item Name', 'https://ashescodex.com/db/item/item-slug', 'Rare', 'Weapon')")
    
    # Some known examples we can add based on common Ashes patterns:
    # These would need to be researched from the actual Ashes Codex
    known_items = [
        # Format: (mob_name, item_name, item_url, rarity, type, order)
        # Add more as we research them
    ]
    
    for mob_id, mob_name, codex_url in mobs_without_items[:5]:  # Just show first 5
        print(f"\n# Research needed for: {mob_name}")
        print(f"# Codex URL: {codex_url}")
        print(f"# add_named_mob_item({mob_id}, 'Item Name', 'https://ashescodex.com/db/item/item-slug', 'Rarity', 'Type')")

if __name__ == "__main__":
    main()
