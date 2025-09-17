#!/usr/bin/env python3
"""
Script Selenium pour diagnostiquer la page blanche
"""
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

def setup_driver():
    """Configure le driver Chrome"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"❌ Erreur Chrome driver: {e}")
        return None

def test_page_load():
    """Test le chargement de la page avec diagnostic détaillé"""
    driver = setup_driver()
    if not driver:
        return
    
    try:
        print("🌐 Accès à http://localhost:9090/map/")
        
        # Authentification
        driver.get("http://invicta:invicta@localhost:9090/map/")
        
        # Attendre le chargement initial
        time.sleep(3)
        
        print(f"📄 Title: {driver.title}")
        print(f"🌐 URL: {driver.current_url}")
        
        # Vérifier les erreurs console
        logs = driver.get_log('browser')
        if logs:
            print("🚨 Erreurs console:")
            for log in logs:
                if log['level'] in ['SEVERE', 'ERROR']:
                    print(f"   ❌ {log['level']}: {log['message']}")
        
        # Vérifier les éléments Angular
        try:
            app_root = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "app-root"))
            )
            print("✅ app-root trouvé")
            
            # Vérifier le contenu de app-root
            content = app_root.get_attribute('innerHTML')
            if content.strip():
                print(f"📝 Contenu app-root: {len(content)} caractères")
                if "router-outlet" in content:
                    print("✅ router-outlet détecté")
                if "loading" in content.lower():
                    print("⏳ État de chargement détecté")
            else:
                print("❌ app-root vide")
                
        except TimeoutException:
            print("❌ app-root non trouvé")
        
        # Vérifier les scripts chargés
        scripts = driver.find_elements(By.TAG_NAME, "script")
        print(f"📜 Scripts trouvés: {len(scripts)}")
        for script in scripts:
            src = script.get_attribute('src')
            if src:
                print(f"   📜 {src}")
        
        # Vérifier les styles
        links = driver.find_elements(By.TAG_NAME, "link")
        css_count = 0
        for link in links:
            rel = link.get_attribute('rel')
            if rel == 'stylesheet':
                css_count += 1
                href = link.get_attribute('href')
                print(f"   🎨 CSS: {href}")
        print(f"🎨 Feuilles de style: {css_count}")
        
        # Test des APIs
        print("\n🔌 Test des APIs via JavaScript:")
        api_test = """
        return new Promise((resolve) => {
            Promise.all([
                fetch('/api.php', {headers: {Authorization: 'Basic ' + btoa('invicta:invicta')}}).then(r => ({api: r.status})).catch(e => ({api: 'error'})),
                fetch('/named_mobs_api.php', {headers: {Authorization: 'Basic ' + btoa('invicta:invicta')}}).then(r => ({named: r.status})).catch(e => ({named: 'error'}))
            ]).then(results => {
                resolve(Object.assign({}, ...results));
            });
        });
        """
        
        api_results = driver.execute_async_script(api_test)
        print(f"   📊 API status: {api_results}")
        
        # Screenshot pour debug
        driver.save_screenshot("/tmp/debug_screenshot.png")
        print("📸 Screenshot sauvé: /tmp/debug_screenshot.png")
        
        # Source de la page
        page_source = driver.page_source[:1000]
        print(f"📄 Source (1000 premiers chars): {page_source}")
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    print("🧪 Diagnostic Selenium - Page blanche")
    print("=" * 50)
    test_page_load()