#!/usr/bin/env python3
"""
Test de la page map avec Selenium pour diagnostiquer les problèmes
"""

import time
import json
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

def setup_driver():
    """Configure le driver Chrome avec les options appropriées"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--ignore-certificate-errors-spki-list')
    
    # Configuration pour basic auth
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    
    return webdriver.Chrome(options=options)

def test_map_page():
    """Test la page map et diagnostique les problèmes"""
    print("🔍 Test Selenium de la page AOC Timer Map")
    print("=" * 50)
    
    driver = None
    try:
        driver = setup_driver()
        
        # URL avec basic auth
        auth_url = "http://invicta:invicta@localhost:9090/map/"
        
        print(f"📍 Accès à: {auth_url}")
        driver.get(auth_url)
        
        # Attendre que la page se charge
        print("⏳ Attente du chargement de la page...")
        time.sleep(5)
        
        # Vérifier le titre
        title = driver.title
        print(f"📄 Titre de la page: {title}")
        
        # Vérifier la structure HTML
        print("\n🏗️ Structure HTML:")
        body = driver.find_element(By.TAG_NAME, "body")
        print(f"  - Body classes: {body.get_attribute('class')}")
        
        # Chercher les éléments principaux
        try:
            app_root = driver.find_element(By.TAG_NAME, "app-root")
            print(f"  - app-root trouvé: {app_root.tag_name}")
        except:
            print("  - ❌ app-root non trouvé")
        
        try:
            map_component = driver.find_element(By.CSS_SELECTOR, "app-map, .map-container, #map")
            print(f"  - Composant map trouvé: {map_component.tag_name}")
        except:
            print("  - ❌ Composant map non trouvé")
        
        # Vérifier les scripts chargés
        print("\n📜 Scripts chargés:")
        scripts = driver.find_elements(By.TAG_NAME, "script")
        for i, script in enumerate(scripts[:5]):  # Limiter à 5 premiers
            src = script.get_attribute("src")
            if src:
                print(f"  - Script {i+1}: {src}")
        
        # Vérifier les erreurs JavaScript
        print("\n🐛 Erreurs JavaScript:")
        logs = driver.get_log('browser')
        js_errors = []
        
        for log in logs:
            if log['level'] in ['SEVERE', 'WARNING']:
                js_errors.append({
                    'level': log['level'],
                    'message': log['message'],
                    'source': log.get('source', 'unknown')
                })
                print(f"  - {log['level']}: {log['message']}")
        
        # Vérifier les requêtes réseau
        print("\n🌐 Requêtes réseau:")
        network_logs = driver.get_log('performance')
        for log in network_logs[-5:]:  # Dernières 5 requêtes
            message = json.loads(log['message'])
            if message['message']['method'] == 'Network.responseReceived':
                response = message['message']['params']['response']
                print(f"  - {response['status']} {response['url']}")
        
        # Prendre une capture d'écran
        print("\n📸 Capture d'écran:")
        screenshot = driver.get_screenshot_as_base64()
        with open('/tmp/map_screenshot.png', 'wb') as f:
            f.write(base64.b64decode(screenshot))
        print("  - Capture sauvée: /tmp/map_screenshot.png")
        
        # Vérifier le contenu de la page
        print("\n📝 Contenu de la page:")
        page_source = driver.page_source
        if "Angular" in page_source:
            print("  - ✅ Angular détecté dans la page")
        if "leaflet" in page_source.lower():
            print("  - ✅ Leaflet détecté dans la page")
        if "error" in page_source.lower():
            print("  - ⚠️ Erreurs détectées dans la page")
        
        # Vérifier si la page est vide/blanche
        body_text = body.text.strip()
        if len(body_text) < 100:
            print(f"  - ⚠️ Page semble vide (seulement {len(body_text)} caractères)")
        else:
            print(f"  - ✅ Page a du contenu ({len(body_text)} caractères)")
        
        return {
            'title': title,
            'js_errors': js_errors,
            'page_loaded': len(body_text) > 100,
            'angular_detected': "Angular" in page_source,
            'leaflet_detected': "leaflet" in page_source.lower()
        }
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return {'error': str(e)}
        
    finally:
        if driver:
            driver.quit()

def main():
    result = test_map_page()
    
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 50)
    
    if 'error' in result:
        print(f"❌ Test échoué: {result['error']}")
    else:
        print(f"📄 Titre: {result['title']}")
        print(f"🔄 Page chargée: {'✅' if result['page_loaded'] else '❌'}")
        print(f"🅰️ Angular détecté: {'✅' if result['angular_detected'] else '❌'}")
        print(f"🗺️ Leaflet détecté: {'✅' if result['leaflet_detected'] else '❌'}")
        print(f"🐛 Erreurs JS: {len(result['js_errors'])} erreurs")
        
        if result['js_errors']:
            print("\n🔍 Erreurs détaillées:")
            for error in result['js_errors'][:3]:  # Top 3 erreurs
                print(f"  - {error['level']}: {error['message'][:100]}...")

if __name__ == "__main__":
    main()
