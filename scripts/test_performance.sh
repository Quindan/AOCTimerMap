#!/bin/bash
# Tests de performance et temps de réponse

BASE_URL="http://localhost:9090"
AUTH="invicta:invicta"

echo "⚡ Tests de performance AOC Timer Map"
echo "===================================="

# Fonction de test avec timing
test_performance() {
    local name="$1"
    local url="$2"
    local auth_flag="$3"
    
    if [ "$auth_flag" = "true" ]; then
        time_total=$(curl -s -o /dev/null -w '%{time_total}' -u "$AUTH" "$url")
        time_connect=$(curl -s -o /dev/null -w '%{time_connect}' -u "$AUTH" "$url")
        time_download=$(curl -s -o /dev/null -w '%{time_starttransfer}' -u "$AUTH" "$url")
    else
        time_total=$(curl -s -o /dev/null -w '%{time_total}' "$url")
        time_connect=$(curl -s -o /dev/null -w '%{time_connect}' "$url")
        time_download=$(curl -s -o /dev/null -w '%{time_starttransfer}' "$url")
    fi
    
    # Convertir en millisecondes
    time_total_ms=$(echo "$time_total * 1000" | bc -l 2>/dev/null || echo "${time_total}000")
    time_connect_ms=$(echo "$time_connect * 1000" | bc -l 2>/dev/null || echo "${time_connect}000")
    
    printf "%-25s Total: %6.0fms  Connect: %6.0fms\n" "$name:" "$time_total_ms" "$time_connect_ms"
}

echo -e "\n📊 Temps de réponse:"

# Test des APIs
test_performance "API Markers" "$BASE_URL/api.php" "true"
test_performance "API Named Mobs" "$BASE_URL/named_mobs_api.php" "true"

# Test des pages
test_performance "Page Map" "$BASE_URL/map/" "true"

# Test des fichiers statiques
test_performance "JavaScript" "$BASE_URL/map/main-PFWT2COM.js" "false"
test_performance "CSS" "$BASE_URL/map/styles-XXTNYWA7.css" "false"

echo -e "\n🎯 Test de charge (5 requêtes simultanées):"
start_time=$(date +%s.%N)

for i in {1..5}; do
    curl -s -o /dev/null -u "$AUTH" "$BASE_URL/api.php" &
done
wait

end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc -l 2>/dev/null || echo "N/A")
echo "⚡ 5 requêtes API en: ${duration}s"

echo -e "\n✅ Tests de performance terminés!"
