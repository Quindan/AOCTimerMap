#!/bin/bash
# Tests rapides des endpoints avec curl

BASE_URL="http://localhost:9090"
AUTH="invicta:invicta"

echo "🧪 Tests rapides des endpoints AOC Timer Map"
echo "============================================="

# Fonction de test
test_endpoint() {
    local name="$1"
    local url="$2" 
    local expected="$3"
    local auth_flag="$4"
    
    if [ "$auth_flag" = "true" ]; then
        status=$(curl -s -o /dev/null -w '%{http_code}' -u "$AUTH" "$url")
    else
        status=$(curl -s -o /dev/null -w '%{http_code}' "$url")
    fi
    
    if [ "$status" = "$expected" ]; then
        echo "✅ $name: $status"
        return 0
    else
        echo "❌ $name: $status (attendu: $expected)"
        return 1
    fi
}

# Tests des fichiers statiques (sans auth)
echo -e "\n📁 Fichiers statiques:"
test_endpoint "JavaScript principal" "$BASE_URL/map/main-PFWT2COM.js" "200" "false"
test_endpoint "CSS principal" "$BASE_URL/map/styles-XXTNYWA7.css" "200" "false" 
test_endpoint "Polyfills" "$BASE_URL/map/polyfills-Q763KACN.js" "200" "false"

# Tests des APIs (avec auth)
echo -e "\n🔌 APIs:"
test_endpoint "API Markers" "$BASE_URL/api.php" "200" "true"
test_endpoint "API Named Mobs" "$BASE_URL/named_mobs_api.php" "200" "true"

# Tests des pages (avec auth)
echo -e "\n📄 Pages:"
test_endpoint "Page principale" "$BASE_URL/" "200" "true"
test_endpoint "Page map" "$BASE_URL/map/" "200" "true"

# Tests d'authentification
echo -e "\n🔐 Authentification:"
test_endpoint "Sans auth (doit échouer)" "$BASE_URL/api.php" "401" "false"

# Test de contenu spécifique
echo -e "\n📊 Contenu:"
echo -n "🎯 Points de référence: "
ref_count=$(curl -s -u "$AUTH" "$BASE_URL/api.php" | grep -c "REF ")
if [ "$ref_count" -ge "3" ]; then
    echo "✅ $ref_count points trouvés"
else
    echo "❌ Seulement $ref_count points trouvés (attendu: 3+)"
fi

echo -n "🏆 Named mobs triangulés: "
triangulated_count=$(curl -s -u "$AUTH" "$BASE_URL/named_mobs_api.php" | grep -c '"map_lat":')
if [ "$triangulated_count" -ge "200" ]; then
    echo "✅ $triangulated_count mobs triangulés"
else
    echo "❌ Seulement $triangulated_count mobs triangulés"
fi

echo -e "\n✅ Tests rapides terminés!"
