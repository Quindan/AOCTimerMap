#!/usr/bin/env python3
"""
Simple Codex item fetching using curl (no external dependencies)
"""

import sqlite3
import subprocess
import re
import json
from urllib.parse import unquote

def fetch_mob_page(mob_slug):
    """Fetch mob page using curl"""
    try:
        url = f"https://ashescodex.com/db/mob/{mob_slug}?embed=true"
        result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return result.stdout
        return None
    except Exception as e:
        print(f"Error fetching {mob_slug}: {e}")
        return None

def parse_special_items(content):
    """Parse special items from Codex content"""
    if not content:
        return []
    
    items = []
    
    # Look for table rows with item links and drop rates
    # Pattern: [Item Name ](/db/item/item-url) | | | Drop Rate%
    pattern = r'\[([^]]+)\s+\]\(/db/item/([^)]+)\).*?(\d+(?:\.\d+)?%)'
    
    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
    
    for match in matches:
        item_name = match[0].strip()
        item_url_encoded = match[1]
        drop_rate = match[2]
        
        # Decode URL encoding
        item_url = unquote(item_url_encoded)
        full_item_url = f"https://ashescodex.com/db/item/{item_url}"
        
        # Filter for special items (uncommon gear, not recipes or common materials)
        is_special = False
        item_type = "Unknown"
        rarity = "Uncommon"
        
        # Skip recipes and common materials
        if "Recipe" in item_name or "Fragment" in item_name:
            continue
            
        # Look for gear items (weapons, armor, accessories)
        if "Gear_Weapon" in item_url:
            item_type = "Weapon"
            is_special = True
        elif "Gear_Accessory" in item_url:
            item_type = "Accessory"
            is_special = True
        elif "Gear_Armor" in item_url:
            item_type = "Armor"
            is_special = True
        elif "Earring" in item_name or "Ring" in item_name or "Necklace" in item_name:
            item_type = "Accessory"
            is_special = True
        elif any(weapon in item_name.lower() for weapon in ['sword', 'axe', 'bow', 'staff', 'shield', 'hammer']):
            item_type = "Weapon"
            is_special = True
        
        # Only include special items with reasonable drop rates (not common materials)
        if is_special and float(drop_rate.replace('%', '')) <= 20:  # Max 20% drop rate for special items
            items.append({
                'name': item_name,
                'url': full_item_url,
                'rarity': rarity,
                'type': item_type,
                'drop_chance': drop_rate
            })
    
    return items

def test_specific_mobs():
    """Test with specific mobs that should have special items"""
    test_mobs = [
        ('skeletal-reaper', 'Skeletal Reaper'),
        ('forgelord-zammer', 'Forgelord Zammer'),
        ('riverlord-otter', 'Riverlord Otter')
    ]
    
    for slug, name in test_mobs:
        print(f"\n📍 Testing: {name} ({slug})")
        content = fetch_mob_page(slug)
        
        if content:
            print(f"  📄 Page fetched ({len(content)} chars)")
            items = parse_special_items(content)
            
            if items:
                print(f"  🎁 Found {len(items)} special items:")
                for item in items:
                    print(f"    - {item['name']} ({item['drop_chance']}) - {item['type']}")
            else:
                print(f"  ⚠️  No special items found")
        else:
            print(f"  ❌ Failed to fetch page")

def main():
    print("🎯 Testing Codex Special Items Fetching")
    print("=" * 45)
    
    test_specific_mobs()

if __name__ == "__main__":
    main()
