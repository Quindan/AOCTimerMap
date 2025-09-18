#!/usr/bin/env python3
"""
Download missing icons using the Codex search API
"""
import requests
import json
import os
import time

# Items that are confirmed missing
MISSING_ITEMS = [
    "Ancient Dunzen Longsword",
    "Archmage's Insight", 
    "Bandit Captain's Shield",
    "Bearmaster's Girdle",
    "Beastwarden's Prod",
    # "Bellsong Purification Helm Mk 2",  # Has "None" icon
    # "Berenserker's Visage",  # Already downloaded
    "Bizhbug's Robe",
    "Bloodletter's Cloak",
    "Bone Shard Greatsword",
    "Bough Warden's Recurve",
    "Breaker's Bulwark",
    "Cadet's Poignard",
    "Captain Threnody's Mariner Belt",
    "Commander's Breastplate",
    "Conservator's Gloves",
    "Counter's Cuff",
    "Deadman's Spaulders",
    "Djinnmagi's Folly",
    "Dun'mor Helm",
    "Everlasting Sower's Bone Necklace",
    "Flayer's Fleshripper",
    "Forgeguard's Deflector",
    "Gatekeeper's Earring",
    "Gatewarden's Will",
    "Groundskeeper's Maul",
    "Hammer of Kuu'Shuu",
    "Hornhexer's Headband",
    "Jackal's Knives",
    "Khalidur's Heavy Breastplate",
    "Khalidur's Pauldrons",
    "Librarian's Circlet",
    "Malevolent Mound's Ring",
    "Malgorach's Heart",
    "Martyr's Mantle",
    "Morellius's Mad Cap",
    "Muckmaw's Greatsword",
    "Mystic's Leather Pauldrons",
    "Necromancer's Guide to Puppetry",
    "Porceilion's Mad Cap",
    "Proctor's Focus",
    "Rebel's Reward",
    "Sorrow's Edge",
    "Steward's Breeches",
    "Sweeper's Dusty Shoes",
    "The Librarian's Hush",
    "Tidewarden's Compass",
    "Timeless Tiller's Bone Ring",
    "Trechery's Vessel",
    "Valor's Protector",
    "Varek's Silk Slippers",
    "Warden's Spite Shackles",
    "Warlord's Glowy Bauble",
    "Ysshokk's Webbed Gloves"
]

def search_item_via_api(item_name):
    """Search for item using Codex API"""
    headers = {
        'content-type': 'application/json',
        'origin': 'https://ashescodex.com',
        'referer': 'https://ashescodex.com/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    }
    
    data = {
        "query": item_name,
        "resultType": None
    }
    
    try:
        response = requests.post('https://api.ashescodex.com/search', 
                               headers=headers, 
                               json=data, 
                               timeout=10)
        
        if response.status_code == 200:
            results = response.json()
            
            # Find exact match for the item
            for result in results:
                if (result.get('item', {}).get('type') == 'item' and 
                    result.get('item', {}).get('itemName') == item_name):
                    
                    icon_path = result.get('item', {}).get('icon', '')
                    if icon_path and icon_path != "None":
                        # Convert game path to CDN URL
                        # /Game/UI/Icons/Items/Gear/Weapon/Sword/1H/TUI_Icon_Gear_Weapons_Sword_1H_Implacable.TUI_Icon_Gear_Weapons_Sword_1H_Implacable
                        # becomes: https://cdn.ashescodex.com/UI/Icons/Items/Gear/Weapon/Sword/1H/TUI_Icon_Gear_Weapons_Sword_1H_Implacable_64.webp
                        
                        # Extract the path after /Game/UI/Icons/Items/
                        if "/Game/UI/Icons/Items/" in icon_path:
                            path_part = icon_path.split("/Game/UI/Icons/Items/")[1]
                            # Get the icon name (last part)
                            icon_name = path_part.split("/")[-1]
                            # Remove the duplicate part after the dot
                            if "." in icon_name:
                                icon_name = icon_name.split(".")[0]
                            
                            # Reconstruct the path
                            path_parts = path_part.split("/")[:-1]  # Remove the filename
                            cdn_path = "/".join(path_parts)
                            
                            cdn_url = f"https://cdn.ashescodex.com/UI/Icons/Items/{cdn_path}/{icon_name}_64.webp"
                            return cdn_url
            
            print(f"    ❌ No exact match found for '{item_name}'")
            return None
        else:
            print(f"    ❌ API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return None

def download_icon(url, filepath):
    """Download an icon from URL"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and len(response.content) > 100:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True
        else:
            print(f"    ❌ Download failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"    ❌ Download error: {e}")
        return False

def download_missing_icons():
    """Download all missing icons using API search"""
    print("🔍 Downloading missing icons via Codex API...")
    
    icons_dir = "app/frontend-built/assets/icons/items/"
    dev_icons_dir = "app/frontend-dev/src/assets/icons/items/"
    downloaded = 0
    
    for item_name in MISSING_ITEMS:
        print(f"📥 {item_name}")
        
        # Create safe filename
        safe_name = item_name.lower().replace(' ', '_').replace("'", '').replace('-', '_')
        safe_name = ''.join(c for c in safe_name if c.isalnum() or c == '_')
        safe_name = safe_name.strip('_')
        
        icon_path = os.path.join(icons_dir, f"{safe_name}.webp")
        dev_icon_path = os.path.join(dev_icons_dir, f"{safe_name}.webp")
        
        # Skip if already exists
        if os.path.exists(icon_path):
            print(f"    ⏭️  Already exists")
            continue
        
        # Search via API
        cdn_url = search_item_via_api(item_name)
        
        if cdn_url:
            print(f"    🔍 Found: {cdn_url}")
            
            # Download to both directories
            if download_icon(cdn_url, icon_path):
                # Copy to dev directory
                try:
                    with open(icon_path, 'rb') as src:
                        with open(dev_icon_path, 'wb') as dst:
                            dst.write(src.read())
                    print(f"    ✅ Downloaded and copied")
                    downloaded += 1
                except Exception as e:
                    print(f"    ⚠️  Downloaded but failed to copy: {e}")
                    downloaded += 1
            else:
                print(f"    ❌ Download failed")
        else:
            print(f"    ❌ No icon URL found")
        
        # Be nice to the API
        time.sleep(1)
    
    print(f"\n✅ Downloaded {downloaded} new icons via API")
    print(f"📊 Total icons now: {len(os.listdir(icons_dir))}")

if __name__ == "__main__":
    download_missing_icons()
