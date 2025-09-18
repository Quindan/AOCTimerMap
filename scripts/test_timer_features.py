#!/usr/bin/env python3
"""
Test script to verify timer features are working
"""
import requests
import json
import time
from requests.auth import HTTPBasicAuth

def test_api_and_features():
    base_url = "http://localhost:9090"
    auth = HTTPBasicAuth('invicta', 'invicta')
    
    print("🧪 Testing Timer Features")
    print("=" * 50)
    
    # Test 1: API connectivity
    print("1. Testing API connectivity...")
    try:
        response = requests.get(f"{base_url}/named_mobs_api.php", auth=auth, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API working: {data['total']} mobs loaded")
        else:
            print(f"   ❌ API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ API error: {e}")
        return False
    
    # Test 2: Check for timer fields
    print("2. Checking timer fields in API...")
    first_mob = data['data'][0] if data['data'] else None
    if first_mob:
        timer_fields = ['last_killed_time', 'timer_active', 'notify_when_ready']
        missing_fields = [field for field in timer_fields if field not in first_mob]
        if missing_fields:
            print(f"   ❌ Missing timer fields: {missing_fields}")
        else:
            print("   ✅ All timer fields present")
    
    # Test 3: Test timer reset
    print("3. Testing timer reset...")
    test_mob_id = 26  # Bluequill
    try:
        reset_response = requests.put(
            f"{base_url}/named_mobs_api.php/named-mobs/reset-timer",
            auth=auth,
            json={"mob_id": test_mob_id},
            timeout=10
        )
        if reset_response.status_code == 200:
            result = reset_response.json()
            if result.get('success'):
                print(f"   ✅ Timer reset successful: {result['message']}")
            else:
                print(f"   ❌ Timer reset failed: {result.get('error')}")
        else:
            print(f"   ❌ Timer reset HTTP error: {reset_response.status_code}")
    except Exception as e:
        print(f"   ❌ Timer reset error: {e}")
    
    # Test 4: Check frontend files
    print("4. Checking frontend files...")
    try:
        index_response = requests.get(f"{base_url}/", auth=auth, timeout=10)
        if index_response.status_code == 200:
            content = index_response.text
            if 'background-color:#1a1a1a' in content:
                print("   ✅ Dark theme found in HTML")
            else:
                print("   ❌ Dark theme NOT found in HTML")
            
            if 'main-' in content and '.js' in content:
                print("   ✅ JavaScript bundle found")
            else:
                print("   ❌ JavaScript bundle NOT found")
        else:
            print(f"   ❌ Frontend HTTP error: {index_response.status_code}")
    except Exception as e:
        print(f"   ❌ Frontend error: {e}")
    
    print("\n🎯 Test Summary:")
    print("If all tests pass, the issue is likely browser caching.")
    print("Try: Ctrl+Shift+R (hard refresh) or open in incognito mode")
    
    return True

if __name__ == "__main__":
    test_api_and_features()
