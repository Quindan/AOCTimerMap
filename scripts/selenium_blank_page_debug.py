#!/usr/bin/env python3
"""
Script Selenium pour diagnostiquer et corriger la page blanche
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

def debug_blank_page():
    print('🧪 Selenium Debug - Blank Page Diagnostic')
    print('=' * 50)

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=options)

    try:
        print('🌐 Loading http://invicta:invicta@localhost:9090/map/')
        driver.get('http://invicta:invicta@localhost:9090/map/')
        
        time.sleep(5)  # Wait for page load
        
        print(f'📄 Title: {driver.title}')
        print(f'🌐 URL: {driver.current_url}')
        
        # Check console errors
        logs = driver.get_log('browser')
        print(f'📊 Console logs: {len(logs)} entries')
        error_count = 0
        for log in logs:
            if log['level'] in ['SEVERE', 'ERROR']:
                error_count += 1
                print(f'   ❌ {log["level"]}: {log["message"]}')
        
        if error_count == 0:
            print('✅ No console errors found')
        
        # Check app-root
        try:
            app_root = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'app-root'))
            )
            content = app_root.get_attribute('innerHTML')
            print(f'✅ app-root found: {len(content)} characters')
            
            if 'router-outlet' in content:
                print('✅ router-outlet detected')
            if 'loading' in content.lower():
                print('⏳ Loading state detected')
            if not content.strip():
                print('❌ app-root is EMPTY!')
            else:
                print(f'📝 app-root content preview: {content[:200]}...')
                
        except TimeoutException:
            print('❌ app-root not found in 10 seconds')
        
        # Check scripts loading
        scripts = driver.find_elements(By.TAG_NAME, 'script')
        print(f'📜 Scripts found: {len(scripts)}')
        main_script_found = False
        for script in scripts:
            src = script.get_attribute('src')
            if src:
                if 'main-' in src:
                    main_script_found = True
                    print(f'   📜 Main script: {src}')
                elif 'polyfills' in src:
                    print(f'   📜 Polyfills: {src}')
                elif 'chunk-' in src:
                    print(f'   📜 Chunk: {src}')
        
        if not main_script_found:
            print('❌ Main Angular script not found!')
        
        # Test JavaScript execution
        try:
            result = driver.execute_script('return typeof window.angular !== "undefined" ? "Angular found" : "No Angular"')
            print(f'🅰️  Angular detection: {result}')
            
            # Test if we can access basic DOM
            body_text = driver.execute_script('return document.body.innerText.length')
            print(f'📄 Body text length: {body_text}')
            
        except Exception as e:
            print(f'❌ JS execution error: {e}')
        
        # Test network requests
        try:
            # Test main script loading
            main_script_status = driver.execute_async_script("""
                var callback = arguments[0];
                fetch('/main-CRYVEFH6.js')
                    .then(response => callback(response.status))
                    .catch(error => callback('error: ' + error.message));
            """)
            print(f'📜 Main script fetch: {main_script_status}')
            
            # Test API
            api_status = driver.execute_async_script("""
                var callback = arguments[0];
                fetch('/api.php', {
                    headers: {Authorization: 'Basic ' + btoa('invicta:invicta')}
                })
                .then(response => callback(response.status))
                .catch(error => callback('error: ' + error.message));
            """)
            print(f'🔌 API fetch: {api_status}')
            
        except Exception as e:
            print(f'❌ Network test error: {e}')
        
        # Check for specific error patterns in page source
        page_source = driver.page_source
        print(f'📄 Page source length: {len(page_source)} characters')
        
        error_patterns = [
            'Failed to load module script',
            'MIME type',
            'Unexpected token',
            'SyntaxError',
            'Cannot resolve module'
        ]
        
        for pattern in error_patterns:
            if pattern in page_source:
                print(f'❌ Error pattern found: {pattern}')
        
        # Take screenshot for debugging
        try:
            driver.save_screenshot('/tmp/debug_blank_page.png')
            print('📸 Screenshot saved to /tmp/debug_blank_page.png')
        except Exception as e:
            print(f'⚠️  Screenshot failed: {e}')
        
        # Final diagnosis
        print('\n🔍 DIAGNOSIS:')
        if error_count > 0:
            print('❌ Console errors detected - check JavaScript loading')
        if not main_script_found:
            print('❌ Main Angular script missing - check file names/paths')
        
        return error_count == 0 and main_script_found
        
    except Exception as e:
        print(f'❌ Critical error: {e}')
        return False
        
    finally:
        driver.quit()

if __name__ == "__main__":
    success = debug_blank_page()
    print(f'\n📊 Result: {"✅ PASS" if success else "❌ FAIL"}')
