#!/usr/bin/env python3
"""
Selenium test to verify what's actually being rendered in the browser
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import base64

def test_browser_rendering():
    print("🤖 Selenium Test - Browser Rendering")
    print("=" * 50)
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = None
    try:
        print("1. Starting Chrome browser...")
        driver = webdriver.Chrome(options=chrome_options)
        
        print("2. Navigating to http://localhost:9090...")
        driver.get("http://localhost:9090")
        
        # Add basic auth
        auth_string = base64.b64encode(b"invicta:invicta").decode()
        driver.execute_script(f"""
            fetch(window.location.href, {{
                headers: {{
                    'Authorization': 'Basic {auth_string}'
                }}
            }}).then(() => window.location.reload());
        """)
        
        time.sleep(3)
        
        print("3. Checking page title...")
        title = driver.title
        print(f"   Title: '{title}'")
        if "TIMER MAP FIXED" in title:
            print("   ✅ Title change detected!")
        else:
            print("   ❌ Title change NOT detected")
        
        print("4. Checking background color...")
        body = driver.find_element(By.TAG_NAME, "body")
        bg_color = driver.execute_script("return window.getComputedStyle(document.body).backgroundColor")
        print(f"   Background color: {bg_color}")
        if "rgb(255, 0, 0)" in bg_color or "#ff0000" in bg_color:
            print("   ✅ Red background detected!")
        else:
            print("   ❌ Red background NOT detected (still cached)")
        
        print("5. Checking for return button...")
        try:
            return_button = driver.find_element(By.XPATH, "//button[contains(text(), 'RETURN TO LANDING')]")
            print("   ✅ Return button found!")
        except:
            print("   ❌ Return button NOT found")
        
        print("6. Checking for named mob markers...")
        try:
            markers = driver.find_elements(By.CLASS_NAME, "named-mob-icon")
            print(f"   Found {len(markers)} named mob markers")
            if len(markers) > 0:
                print("   ✅ Map is loading")
            else:
                print("   ❌ No markers found")
        except:
            print("   ❌ Error finding markers")
        
        print("7. Taking screenshot for debugging...")
        driver.save_screenshot("/tmp/test_screenshot.png")
        print("   Screenshot saved to /tmp/test_screenshot.png")
        
        print("8. Checking console logs...")
        logs = driver.get_log('browser')
        error_logs = [log for log in logs if log['level'] == 'SEVERE']
        if error_logs:
            print(f"   ❌ {len(error_logs)} console errors found:")
            for log in error_logs[:3]:  # Show first 3 errors
                print(f"      {log['message']}")
        else:
            print("   ✅ No console errors")
        
    except Exception as e:
        print(f"❌ Selenium test failed: {e}")
    finally:
        if driver:
            driver.quit()
    
    print("\n🎯 Test Summary:")
    print("If title changed but background/button didn't, it's a CSS/JS build issue")
    print("If nothing changed, it's a complete cache problem")

if __name__ == "__main__":
    test_browser_rendering()
