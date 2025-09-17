#!/usr/bin/env python3
"""
Suite de tests automatisés pour AOC Timer Map
Tests API, endpoints, et interface avec Selenium
"""

import subprocess
import json
import time
import sys
import os
from urllib.parse import urlparse

class TestSuite:
    def __init__(self, base_url="http://localhost:9090", username="invicta", password="invicta"):
        self.base_url = base_url
        self.auth = f"{username}:{password}"
        self.results = []
        
    def run_curl_test(self, name, url, expected_status=200, auth=True, check_content=None):
        """Exécute un test curl et vérifie le résultat"""
        auth_flag = f"-u {self.auth}" if auth else ""
        cmd = f"curl -s -o /dev/null -w '%{{http_code}}' {auth_flag} '{url}'"
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            status_code = int(result.stdout.strip())
            
            success = status_code == expected_status
            self.results.append({
                'test': name,
                'type': 'curl',
                'status': status_code,
                'expected': expected_status,
                'success': success,
                'url': url
            })
            
            status_icon = "✅" if success else "❌"
            print(f"{status_icon} {name}: {status_code} (attendu: {expected_status})")
            
            return success
            
        except Exception as e:
            self.results.append({
                'test': name,
                'type': 'curl',
                'error': str(e),
                'success': False,
                'url': url
            })
            print(f"❌ {name}: Erreur - {e}")
            return False
    
    def run_content_test(self, name, url, expected_content, auth=True):
        """Test le contenu d'une réponse"""
        auth_flag = f"-u {self.auth}" if auth else ""
        cmd = f"curl -s {auth_flag} '{url}'"
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            content = result.stdout
            
            if expected_content in content:
                print(f"✅ {name}: Contenu trouvé")
                self.results.append({'test': name, 'type': 'content', 'success': True})
                return True
            else:
                print(f"❌ {name}: Contenu manquant")
                print(f"   Recherché: {expected_content}")
                print(f"   Reçu: {content[:100]}...")
                self.results.append({'test': name, 'type': 'content', 'success': False})
                return False
                
        except Exception as e:
            print(f"❌ {name}: Erreur - {e}")
            self.results.append({'test': name, 'type': 'content', 'error': str(e), 'success': False})
            return False
    
    def test_static_files(self):
        """Test les fichiers statiques (JS, CSS)"""
        print("\n📁 Tests des fichiers statiques:")
        
        # Test des fichiers JS et CSS via /map/
        js_files = ["main-T3EQFCJX.js", "polyfills-Q763KACN.js", "chunk-ZHYZGWJY.js"]
        css_files = ["styles-GUDYXLDC.css"]
        
        for js_file in js_files:
            self.run_curl_test(f"JS via /map/: {js_file}", f"{self.base_url}/map/{js_file}", 200, False)
        
        for css_file in css_files:
            self.run_curl_test(f"CSS via /map/: {css_file}", f"{self.base_url}/map/{css_file}", 200, False)
    
    def test_api_endpoints(self):
        """Test les endpoints API"""
        print("\n🔌 Tests des APIs:")
        
        # Test API markers
        self.run_curl_test("API Markers", f"{self.base_url}/api.php", 200, True)
        
        # Test API named mobs
        self.run_curl_test("API Named Mobs", f"{self.base_url}/named_mobs_api.php", 200, True)
        
        # Test contenu API
        self.run_content_test("API Markers Data", f"{self.base_url}/api.php", '"id":', True)
        self.run_content_test("Named Mobs Triangulation", f"{self.base_url}/named_mobs_api.php", '"map_lat":', True)
    
    def test_pages(self):
        """Test les pages principales"""
        print("\n📄 Tests des pages:")
        
        # Test page principale
        self.run_curl_test("Page principale", f"{self.base_url}/", 200, True)
        
        # Test page map
        self.run_curl_test("Page map", f"{self.base_url}/map/", 200, True)
        
        # Test contenu Angular
        self.run_content_test("Angular app-root", f"{self.base_url}/map/", "<app-root>", True)
        self.run_content_test("Scripts JS chargés", f"{self.base_url}/map/", "main-T3EQFCJX.js", True)
    
    def test_authentication(self):
        """Test l'authentification"""
        print("\n🔐 Tests d'authentification:")
        
        # Test sans auth (doit échouer)
        self.run_curl_test("Sans auth (doit échouer)", f"{self.base_url}/api.php", 401, False)
        
        # Test avec mauvais credentials
        cmd = f"curl -s -o /dev/null -w '%{{http_code}}' -u wrong:credentials '{self.base_url}/api.php'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        status = int(result.stdout.strip())
        if status == 401:
            print("✅ Mauvais credentials rejetés: 401")
        else:
            print(f"❌ Mauvais credentials acceptés: {status}")
    
    def test_reference_points(self):
        """Test les points de référence pour la triangulation"""
        print("\n🎯 Tests des points de référence:")
        
        ref_points = ["wormwig", "ysshokk", "olive"]
        
        for ref in ref_points:
            cmd = f"curl -s -u {self.auth} '{self.base_url}/named_mobs_api.php' | grep -i '{ref}' | head -1"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.stdout.strip():
                print(f"✅ Point de référence {ref}: Trouvé")
                # Vérifier les coordonnées triangulées
                if '"map_lat":' in result.stdout and '"map_lng":' in result.stdout:
                    print(f"   ✅ Coordonnées triangulées présentes")
                else:
                    print(f"   ❌ Coordonnées triangulées manquantes")
            else:
                print(f"❌ Point de référence {ref}: Non trouvé")
    
    def run_selenium_test(self):
        """Test avec Selenium si disponible"""
        print("\n🌐 Test Selenium (optionnel):")
        
        try:
            # Vérifier si Selenium est disponible
            subprocess.run(["python3", "-c", "import selenium"], check=True, capture_output=True)
            
            # Lancer le test Selenium
            selenium_script = """
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

try:
    driver = webdriver.Chrome(options=options)
    driver.get('http://invicta:invicta@localhost:9090/map/')
    time.sleep(3)
    
    title = driver.title
    print(f'✅ Selenium - Titre: {title}')
    
    # Vérifier app-root
    app_root = driver.find_element(By.TAG_NAME, 'app-root')
    print('✅ Selenium - app-root trouvé')
    
    # Vérifier les erreurs JS
    logs = driver.get_log('browser')
    errors = [log for log in logs if log['level'] == 'SEVERE']
    
    if errors:
        print(f'⚠️  Selenium - {len(errors)} erreurs JS détectées')
        for error in errors[:2]:
            print(f'   - {error["message"][:60]}...')
    else:
        print('✅ Selenium - Aucune erreur JS critique')
        
except Exception as e:
    print(f'❌ Selenium - Erreur: {e}')
finally:
    try:
        driver.quit()
    except:
        pass
"""
            
            result = subprocess.run(["python3", "-c", selenium_script], 
                                  capture_output=True, text=True, timeout=30)
            print(result.stdout)
            if result.stderr:
                print(f"Selenium warnings: {result.stderr}")
                
        except subprocess.CalledProcessError:
            print("⚠️  Selenium non disponible (optionnel)")
        except Exception as e:
            print(f"⚠️  Selenium test échoué: {e}")
    
    def generate_report(self):
        """Génère un rapport des tests"""
        print("\n" + "=" * 50)
        print("📊 RAPPORT DES TESTS")
        print("=" * 50)
        
        total_tests = len(self.results)
        successful_tests = len([r for r in self.results if r.get('success', False)])
        
        print(f"🎯 Total: {total_tests} tests")
        print(f"✅ Réussis: {successful_tests}")
        print(f"❌ Échecs: {total_tests - successful_tests}")
        print(f"📊 Taux de réussite: {(successful_tests/total_tests*100):.1f}%")
        
        # Détails des échecs
        failures = [r for r in self.results if not r.get('success', False)]
        if failures:
            print(f"\n❌ Échecs détaillés:")
            for failure in failures:
                print(f"   - {failure['test']}: {failure.get('error', 'Échec')}")
        
        # Sauvegarde du rapport
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'success_rate': successful_tests/total_tests*100,
            'results': self.results
        }
        
        with open('/tmp/aoc_test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Rapport sauvé: /tmp/aoc_test_report.json")
        
        return successful_tests == total_tests

def main():
    print("🧪 AOC Timer Map - Suite de tests automatisés")
    print("=" * 50)
    
    # Vérifier que le service est démarré
    try:
        result = subprocess.run("curl -s -o /dev/null -w '%{http_code}' http://localhost:9090/", 
                              shell=True, capture_output=True, text=True, timeout=5)
        if result.stdout.strip() not in ["200", "401"]:  # 401 OK car page nécessite auth
            print("❌ Service non disponible sur localhost:9090")
            print("   Lancez d'abord: make local")
            sys.exit(1)
    except:
        print("❌ Impossible de contacter le service")
        sys.exit(1)
    
    suite = TestSuite()
    
    # Exécuter tous les tests
    suite.test_static_files()
    suite.test_api_endpoints() 
    suite.test_pages()
    suite.test_authentication()
    suite.test_reference_points()
    suite.run_selenium_test()
    
    # Générer le rapport
    all_passed = suite.generate_report()
    
    if all_passed:
        print("\n🎉 Tous les tests sont passés !")
        sys.exit(0)
    else:
        print("\n⚠️  Certains tests ont échoué")
        sys.exit(1)

if __name__ == "__main__":
    main()
