#!/usr/bin/env python3
"""
Search for missing items with proper quote handling
"""
import requests
import json
import os
import time
import sqlite3

def search_item_variants(item_name):
    """Search for an item using multiple query variants"""
    headers = {
        'content-type': 'application/json',
        'origin': 'https://ashescodex.com',
        'referer': 'https://ashescodex.com/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    }
    
    # Try different search variants
    variants = [
        item_name,  # Original name with quotes
        item_name.replace("'", ""),  # Remove apostrophes
        item_name.replace("'", " "),  # Replace apostrophes with spaces
        " ".join(item_name.split()[:2]),  # First two words only
        " ".join(item_name.split()[:3]),  # First three words only
    ]
    
    for variant in variants:
        try:
            data = {"query": variant, "resultType": None}
            response = requests.post('https://api.ashescodex.com/search', 
                                   headers=headers, 
                                   json=data, 
                                   timeout=10)
            
            if response.status_code == 200:
                results = response.json()
                
                # Look for exact match first, then partial matches
                for result in results:
                    if (result.get('item', {}).get('type') == 'item' and 
                        result.get('item', {}).get('itemName') == item_name):
                        
                        icon_path = result.get('item', {}).get('icon', '')
                        if icon_path and icon_path != "None":
                            return convert_to_cdn_url(icon_path), variant
                
                # If no exact match, look for close matches
                for result in results:
                    if (result.get('item', {}).get('type') == 'item'):
                        found_name = result.get('item', {}).get('itemName', '')
                        if (item_name.lower() in found_name.lower() or 
                            found_name.lower() in item_name.lower()):
                            
                            icon_path = result.get('item', {}).get('icon', '')
                            if icon_path and icon_path != "None":
                                print(f"    📝 Close match: '{found_name}' for '{item_name}'")
                                return convert_to_cdn_url(icon_path), variant
            
        except Exception as e:
            print(f"    ❌ Error searching '{variant}': {e}")
            continue
    
    return None, None

def convert_to_cdn_url(icon_path):
    """Convert game icon path to CDN URL"""
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
    """Download an icon from URL"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and len(response.content) > 100:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True
        return False
    except:
        return False

def get_missing_items():
    """Get list of items that don't have icons yet"""
    db_path = "data/database/db/mydb.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT item_name FROM named_mob_items ORDER BY item_name")
    all_items = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    icons_dir = "app/frontend-built/assets/icons/items/"
    missing_items = []
    
    for item_name in all_items:
        safe_name = item_name.lower().replace(' ', '_').replace("'", '').replace('-', '_')
        safe_name = ''.join(c for c in safe_name if c.isalnum() or c == '_').strip('_')
        
        icon_path = os.path.join(icons_dir, f"{safe_name}.webp")
        if not os.path.exists(icon_path):
            missing_items.append(item_name)
    
    return missing_items

def search_and_download_missing():
    """Search for and download all missing items"""
    print("🔍 Searching for missing items with proper quote handling...")
    
    missing_items = get_missing_items()
    print(f"Found {len(missing_items)} missing items")
    
    icons_dir = "app/frontend-built/assets/icons/items/"
    dev_icons_dir = "app/frontend-dev/src/assets/icons/items/"
    downloaded = 0
    
    for item_name in missing_items[:10]:  # Limit to first 10 for testing
        print(f"📥 {item_name}")
        
        safe_name = item_name.lower().replace(' ', '_').replace("'", '').replace('-', '_')
        safe_name = ''.join(c for c in safe_name if c.isalnum() or c == '_').strip('_')
        
        icon_path = os.path.join(icons_dir, f"{safe_name}.webp")
        dev_icon_path = os.path.join(dev_icons_dir, f"{safe_name}.webp")
        
        cdn_url, variant_used = search_item_variants(item_name)
        
        if cdn_url:
            print(f"    🔍 Found via '{variant_used}': {cdn_url}")
            
            if download_icon(cdn_url, icon_path):
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
            print(f"    ❌ Not found with any variant")
        
        time.sleep(1)
    
    print(f"\n✅ Downloaded {downloaded} new icons")
    print(f"📊 Total icons now: {len(os.listdir(icons_dir))}")

if __name__ == "__main__":
    search_and_download_missing()
