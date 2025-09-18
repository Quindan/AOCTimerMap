#!/usr/bin/env python3
"""
Improved icon download script using the correct Codex URL patterns
Based on user-provided working examples:
- Wand: /Gear/Weapon/Wand/1H/TUI_Icon_Gear_Weapons_Wand_1H_Copper_64.webp
- Book: /Gear/Weapon/Book/2H/TUI_Icon_Gear_Weapons_Book_2H_Common_64.webp
"""
import sqlite3
import requests
import os
import time

# Weapon type mappings based on discovered patterns
WEAPON_PATTERNS = {
    'Weapon': {
        'Sword': '/Gear/Weapon/Sword/1H/TUI_Icon_Gear_Weapons_Sword_1H_{type}_64.webp',
        'Wand': '/Gear/Weapon/Wand/1H/TUI_Icon_Gear_Weapons_Wand_1H_{type}_64.webp',
        'Book': '/Gear/Weapon/Book/2H/TUI_Icon_Gear_Weapons_Book_2H_{type}_64.webp',
        'Shield': '/Gear/Weapon/Shield/OH/TUI_Icon_Gear_Weapons_Shield_OH_{type}_64.webp',
        'Bow': '/Gear/Weapon/Bow/2H/TUI_Icon_Gear_Weapons_Bow_2H_{type}_64.webp',
        'Staff': '/Gear/Weapon/Staff/2H/TUI_Icon_Gear_Weapons_Staff_2H_{type}_64.webp',
        'Axe': '/Gear/Weapon/Axe/1H/TUI_Icon_Gear_Weapons_Axe_1H_{type}_64.webp',
        'Mace': '/Gear/Weapon/Mace/1H/TUI_Icon_Gear_Weapons_Mace_1H_{type}_64.webp',
        'Dagger': '/Gear/Weapon/Dagger/1H/TUI_Icon_Gear_Weapons_Dagger_1H_{type}_64.webp',
        'Greatsword': '/Gear/Weapon/Greatsword/2H/TUI_Icon_Gear_Weapons_Greatsword_2H_{type}_64.webp',
    },
    'Accessory': {
        'Ring': '/Gear/Jewelry/TUI_Icon_Gear_Accessory_Ring_{type}_64.webp',
        'Necklace': '/Gear/Jewelry/TUI_Icon_Gear_Accessory_Necklace_{type}_64.webp',
        'Earring': '/Gear/Jewelry/TUI_Icon_Gear_Accessory_Earring_{type}_64.webp',
    },
    'Armor': {
        'Helmet': '/Gear/Armor/Heavy/Helmet/TUI_Icon_Gear_Armor_Heavy_Helmet_{type}_64.webp',
        'Chestpiece': '/Gear/Armor/Heavy/Chestpiece/TUI_Icon_Gear_Armor_Heavy_Chestpiece_{type}_64.webp',
        'Leggings': '/Gear/Armor/Light/Leggings/TUI_Icon_Gear_Armor_Light_Leggings_{type}_64.webp',
        'Gloves': '/Gear/Armor/Light/Gloves/TUI_Icon_Gear_Armor_Light_Gloves_{type}_64.webp',
        'Boots': '/Gear/Armor/Light/Boots/TUI_Icon_Gear_Armor_Light_Boots_{type}_64.webp',
    },
    'Bag': {
        'Bag': '/Gear/Bags/TUI_Icon_Gear_Bags_{type}_64.webp',
    },
    'Artisan Tool': {
        'Pickaxe': '/Gear/Artisan/Mining/Tool/TUI_Icon_Gear_Artisan_Mining_Tool_Pickaxe_{type}_64.webp',
        'Axe': '/Gear/Artisan/Logging/Tool/TUI_Icon_Gear_Artisan_Logging_Tool_Axe_{type}_64.webp',
        'Sickle': '/Gear/Artisan/Herbalism/Tool/TUI_Icon_Gear_Artisan_Herbalism_Tool_Sickle_{type}_64.webp',
    }
}

# Common type suffixes found in URLs
COMMON_TYPES = ['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary', 'Copper', 'Bronze', 'Iron', 'Steel', 'Mithril']

def guess_icon_url(item_name, item_type):
    """Try to guess the icon URL based on item name and type"""
    base_url = "https://cdn.ashescodex.com/UI/Icons/Items"
    
    # Clean item name for URL (remove special chars, spaces)
    clean_name = item_name.replace(" ", "_").replace("'", "").replace("-", "_")
    clean_name = ''.join(c for c in clean_name if c.isalnum() or c == '_')
    
    # Try to determine weapon subtype from name
    name_lower = item_name.lower()
    
    if item_type == 'Weapon':
        for weapon_type, pattern in WEAPON_PATTERNS['Weapon'].items():
            if weapon_type.lower() in name_lower:
                for type_suffix in COMMON_TYPES:
                    url = base_url + pattern.format(type=type_suffix)
                    yield url
                # Also try with the clean item name
                url = base_url + pattern.format(type=clean_name)
                yield url
    
    elif item_type in ['Accessory', 'Ring', 'Necklace', 'Earring']:
        for acc_type, pattern in WEAPON_PATTERNS['Accessory'].items():
            if acc_type.lower() in name_lower or item_type == acc_type:
                for type_suffix in COMMON_TYPES:
                    url = base_url + pattern.format(type=type_suffix)
                    yield url
                # Try with clean item name
                url = base_url + pattern.format(type=clean_name)
                yield url
    
    elif item_type == 'Bag':
        pattern = WEAPON_PATTERNS['Bag']['Bag']
        for type_suffix in COMMON_TYPES:
            url = base_url + pattern.format(type=type_suffix)
            yield url
        url = base_url + pattern.format(type=clean_name)
        yield url
    
    elif item_type == 'Artisan Tool':
        for tool_type, pattern in WEAPON_PATTERNS['Artisan Tool'].items():
            if tool_type.lower() in name_lower:
                for type_suffix in COMMON_TYPES:
                    url = base_url + pattern.format(type=type_suffix)
                    yield url
                url = base_url + pattern.format(type=clean_name)
                yield url

def download_missing_icons():
    """Download icons for items that don't have them yet"""
    print("🔍 Downloading missing item icons with improved patterns...")
    
    # Connect to database
    db_path = "data/database/db/mydb.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get items without icons
    cursor.execute("""
        SELECT DISTINCT item_name, item_type 
        FROM named_mob_items 
        WHERE item_name IS NOT NULL AND item_name != ''
        ORDER BY item_name
    """)
    
    items = cursor.fetchall()
    conn.close()
    
    icons_dir = "app/frontend-built/assets/icons/items/"
    downloaded = 0
    
    for item_name, item_type in items:
        # Create safe filename
        safe_name = item_name.lower().replace(' ', '_').replace("'", '').replace('-', '_')
        safe_name = ''.join(c for c in safe_name if c.isalnum() or c == '_')
        icon_path = os.path.join(icons_dir, f"{safe_name}.webp")
        
        # Skip if already exists
        if os.path.exists(icon_path):
            continue
        
        print(f"📥 {item_name} ({item_type})")
        
        # Try different URL patterns
        success = False
        for url in guess_icon_url(item_name, item_type):
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200 and len(response.content) > 100:
                    with open(icon_path, 'wb') as f:
                        f.write(response.content)
                    print(f"    ✅ Downloaded from: {url}")
                    downloaded += 1
                    success = True
                    break
                else:
                    print(f"    ❌ Failed: {url}")
            except Exception as e:
                print(f"    ❌ Error: {e}")
        
        if not success:
            print(f"    ⚠️ No icon found for {item_name}")
        
        # Be nice to the server
        time.sleep(0.5)
    
    print(f"\n✅ Downloaded {downloaded} new icons")
    print(f"📊 Total icons now: {len(os.listdir(icons_dir))}")

if __name__ == "__main__":
    download_missing_icons()
