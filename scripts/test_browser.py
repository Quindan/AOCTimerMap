#!/usr/bin/env python3
"""
Test de l'interface utilisateur avec Selenium
Nécessite: pip install selenium
"""

import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_map_interface():
    """Test complet de l'interface map"""
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox') 
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    driver = None
    try:
        print("🌐 Démarrage du test Selenium...")
        driver = webdriver.Chrome(options=options)
        
        # Accès à la page map avec auth
        print("📍 Accès à la page map...")
        driver.get("http://invicta:invicta@localhost:9090/map/")
        
        # Attendre le chargement
        print("⏳ Attente du chargement...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "app-root"))
        )
        
        # Vérifications de base
        print(f"📄 Titre: {driver.title}")
        print(f"🔗 URL: {driver.current_url}")
        
        # Vérifier les composants Angular
        try:
            app_root = driver.find_element(By.TAG_NAME, "app-root")
            print("✅ app-root trouvé")
            
            # Chercher le composant map
            map_elements = driver.find_elements(By.CSS_SELECTOR, "app-map, .map-container, #map, .leaflet-container")
            if map_elements:
                print(f"✅ Composant map trouvé: {len(map_elements)} éléments")
            else:
                print("❌ Composant map non trouvé")
                
        except Exception as e:
            print(f"❌ Erreur composants: {e}")
        
        # Vérifier les erreurs JavaScript
        print("\n🐛 Erreurs JavaScript:")
        logs = driver.get_log('browser')
        severe_errors = [log for log in logs if log['level'] == 'SEVERE']
        warning_errors = [log for log in logs if log['level'] == 'WARNING']
        
        if severe_errors:
            print(f"❌ {len(severe_errors)} erreurs critiques:")
            for error in severe_errors[:3]:
                print(f"   - {error['message'][:80]}...")
        else:
            print("✅ Aucune erreur critique")
            
        if warning_errors:
            print(f"⚠️  {len(warning_errors)} avertissements")
        
        # Vérifier le contenu
        body_text = driver.find_element(By.TAG_NAME, "body").text
        if len(body_text.strip()) > 50:
            print(f"✅ Page a du contenu ({len(body_text)} caractères)")
        else:
            print(f"❌ Page semble vide ({len(body_text)} caractères)")
        
        # Prendre une capture d'écran
        try:
            driver.save_screenshot("/tmp/map_test_screenshot.png")
            print("📸 Capture d'écran sauvée: /tmp/map_test_screenshot.png")
        except:
            print("⚠️  Impossible de sauver la capture")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False
        
    finally:
        if driver:
            driver.quit()

def main():
    try:
        # Vérifier si Selenium est disponible
        from selenium import webdriver
        print("✅ Selenium disponible")
    except ImportError:
        print("❌ Selenium non installé")
        print("   Installation: pip install selenium")
        print("   Ou utilisez: make test-selenium (avec Docker)")
        sys.exit(1)
    
    success = test_map_interface()
    
    if success:
        print("\n🎉 Test Selenium réussi !")
        sys.exit(0)
    else:
        print("\n❌ Test Selenium échoué")
        sys.exit(1)

if __name__ == "__main__":
    main()
