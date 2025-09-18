#!/usr/bin/env python3
"""
Batch search and download missing items
"""
import requests
import json
import os
import time

# List of missing items from the check
MISSING_ITEMS = [
    "Archmage's Insight",
    "Bandit Captain's Shield", 
    "Bearmaster's Girdle",
    "Beastwarden's Prod",
    "Berenserker's Visage",
    "Bloodletter's Cloak",
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
    "Jackal's Knives",
    "Khalidur's Heavy Breastplate",
    "Khalidur's Pauldrons",
    "Librarian's Circlet",
    "Malevolent Mound's Ring",
    "Malgorach's Heart",
    "Martyr's Mantle",
    "Morellius's Mad Cap",
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
    "Varek's Silk Slippers",
    "Warden's Spite Shackles",
    "Warlord's Glowy Bauble"
]

def search_with_variants(item_name):
    """Search for item with multiple variants"""
    headers = {
        'content-type': 'application/json',
        'origin': 'https://ashescodex.com',
        'referer': 'https://ashescodex.com/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    }
    
    # Create search variants
    variants = [
        item_name,  # Full name
        item_name.replace("'", ""),  # No apostrophes
        item_name.replace("'", " "),  # Apostrophes as spaces
        " ".join(item_name.split()[:2]),  # First 2 words
        " ".join(item_name.split()[:3]),  # First 3 words
        item_name.split("'s")[0] if "'s" in item_name else item_name,  # Remove possessive
    ]
    
    for variant in variants:
        try:
            data = {"query": variant, "resultType": None}
            response = requests.post('https://api.ashescodex.com/search', 
                                   headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                results = response.json()
                
                # Look for exact match
                for result in results:
                    if (result.get('item', {}).get('type') == 'item'):
                        found_name = result.get('item', {}).get('itemName', '')
                        if found_name == item_name:
                            icon_path = result.get('item', {}).get('icon', '')
                            if icon_path and icon_path != "None":
                                return convert_to_cdn_url(icon_path), variant, found_name
                
                # Look for close matches
                for result in results:
                    if (result.get('item', {}).get('type') == 'item'):
                        found_name = result.get('item', {}).get('itemName', '')
                        if (item_name.lower().replace("'", "") in found_name.lower().replace("'", "") or
                            found_name.lower().replace("'", "") in item_name.lower().replace("'", "")):
                            icon_path = result.get('item', {}).get('icon', '')
                            if icon_path and icon_path != "None":
                                return convert_to_cdn_url(icon_path), variant, found_name
                            
        except Exception as e:
            continue
    
    return None, None, None

def convert_to_cdn_url(icon_path):
    """Convert game path to CDN URL"""
    if "/Game/UI/Icons/Items/" in icon_path:
        path_part = icon_path.split("/Game/UI/Icons/Items/")[1]
        icon_name = path_part.split("/")[-1]
        if "." in icon_name:
            icon_name = icon_name.split(".")[0]
        
        path_parts = path_part.split("/")[:-1]
        cdn_path = "/".join(path_parts)
        
        return f"https://cdn.ashescodex.com/UI/Icons/Items/{cdn_path}/{icon_name}_64.webp"
    return None

def download_icon(url, filepath):
    """Download icon"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and len(response.content) > 100:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True
        return False
    except:
        return False

def batch_search_and_download():
    """Search and download missing items in batches"""
    print("🔍 Batch searching for missing items...")
    
    icons_dir = "app/frontend-built/assets/icons/items/"
    dev_icons_dir = "app/frontend-dev/src/assets/icons/items/"
    downloaded = 0
    not_found = []
    
    for i, item_name in enumerate(MISSING_ITEMS):
        print(f"📥 [{i+1}/{len(MISSING_ITEMS)}] {item_name}")
        
        # Check if already exists
        safe_name = item_name.lower().replace(' ', '_').replace("'", '').replace('-', '_')
        safe_name = ''.join(c for c in safe_name if c.isalnum() or c == '_').strip('_')
        
        icon_path = os.path.join(icons_dir, f"{safe_name}.webp")
        dev_icon_path = os.path.join(dev_icons_dir, f"{safe_name}.webp")
        
        if os.path.exists(icon_path):
            print(f"    ✅ Already exists")
            continue
        
        # Search for the item
        cdn_url, variant_used, found_name = search_with_variants(item_name)
        
        if cdn_url:
            if found_name != item_name:
                print(f"    📝 Found close match: '{found_name}' via '{variant_used}'")
            else:
                print(f"    🎯 Found exact match via '{variant_used}'")
            
            print(f"    🔗 {cdn_url}")
            
            if download_icon(cdn_url, icon_path):
                try:
                    with open(icon_path, 'rb') as src:
                        with open(dev_icon_path, 'wb') as dst:
                            dst.write(src.read())
                    print(f"    ✅ Downloaded and copied")
                    downloaded += 1
                except Exception as e:
                    print(f"    ⚠️  Downloaded but copy failed: {e}")
                    downloaded += 1
            else:
                print(f"    ❌ Download failed")
                not_found.append(item_name)
        else:
            print(f"    ❌ Not found with any variant")
            not_found.append(item_name)
        
        time.sleep(1)  # Be nice to the API
    
    print(f"\n📊 BATCH RESULTS:")
    print(f"✅ Downloaded: {downloaded}")
    print(f"❌ Not found: {len(not_found)}")
    
    if not_found:
        print(f"\n📝 Items still missing:")
        for item in not_found:
            print(f"  • {item}")

if __name__ == "__main__":
    batch_search_and_download()
