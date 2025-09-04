<?php
/**
 * Script to fetch all named mobs from Ashes Codex API
 * Extracts: name, timer (respawn time), and codex link
 */

class NamedMobsFetcher {
    private const BASE_URL = 'https://api.ashescodex.com';
    private const MOBS_ENDPOINT = '/mobs';
    private const MOB_DETAIL_ENDPOINT = '/mob';
    
    private $namedMobs = [];
    
    public function fetchAllNamedMobs() {
        echo "🔄 Fetching named mobs from Ashes Codex API...\n";
        
        $page = 1;
        $totalFetched = 0;
        
        do {
            $url = self::BASE_URL . self::MOBS_ENDPOINT . "?page={$page}&per_page=30&sortColumn=name&sortDir=asc&namedMobs=true";
            echo "📡 Fetching page {$page}: {$url}\n";
            
            $response = $this->makeRequest($url);
            
            if (!$response || !isset($response['data'])) {
                echo "❌ Failed to fetch page {$page}\n";
                break;
            }
            
            $mobs = $response['data'];
            $totalOnPage = count($mobs);
            
            echo "✅ Found {$totalOnPage} mobs on page {$page}\n";
            
            foreach ($mobs as $mob) {
                $this->processMob($mob);
                $totalFetched++;
            }
            
            // Check if we have more pages (based on meta info or if page returned full results)
            $hasMorePages = isset($response['meta']) && 
                           $response['meta']['total'] > ($page * $response['meta']['per_page']);
            
            if (!$hasMorePages && $totalOnPage < 30) {
                break; // Last page if we got less than full page
            }
            
            $page++;
            usleep(100000); // 100ms delay to be respectful to API
            
        } while ($totalOnPage > 0 && $page <= 20); // Safety limit
        
        echo "🎉 Total named mobs fetched: {$totalFetched}\n";
        return $this->namedMobs;
    }
    
    private function processMob($mob) {
        if (!isset($mob['_displayName']) || !isset($mob['populationInstances'])) {
            return;
        }
        
        $name = $mob['_displayName'];
        $slug = $mob['_slug'] ?? '';
        $levelRange = $mob['_levelRange'] ?? 'Unknown';
        
        // Extract respawn time from population instances
        $respawnTime = null;
        $location = null;
        $level = null;
        
        foreach ($mob['populationInstances'] as $instance) {
            if (isset($instance['respawnTime'])) {
                $respawnTime = $instance['respawnTime'];
            }
            if (isset($instance['_location'])) {
                $location = $instance['_location'];
            }
            if (isset($instance['nPCLevelMin'])) {
                $level = $instance['nPCLevelMin'];
            }
        }
        
        // Convert respawn time to minutes
        $respawnMinutes = $this->parseRespawnTime($respawnTime);
        
        // Generate codex URL
        $codexUrl = "https://ashescodex.com/mobs/{$slug}";
        
        $this->namedMobs[] = [
            'name' => $name,
            'slug' => $slug,
            'level' => $level,
            'levelRange' => $levelRange,
            'respawnTime' => $respawnTime,
            'respawnMinutes' => $respawnMinutes,
            'codexUrl' => $codexUrl,
            'location' => $location,
            'type' => 'named_mob'
        ];
        
        echo "  📝 {$name} (Level {$level}) - {$respawnMinutes}min - {$codexUrl}\n";
    }
    
    private function parseRespawnTime($respawnTime) {
        if (!$respawnTime) return 0;
        
        // Parse "1200 seconds" format
        if (preg_match('/(\d+)\s*seconds?/i', $respawnTime, $matches)) {
            return intval($matches[1]) / 60; // Convert to minutes
        }
        
        // Parse "20 minutes" format
        if (preg_match('/(\d+)\s*minutes?/i', $respawnTime, $matches)) {
            return intval($matches[1]);
        }
        
        return 0;
    }
    
    private function makeRequest($url) {
        $context = stream_context_create([
            'http' => [
                'method' => 'GET',
                'header' => [
                    'User-Agent: AOCTimerMap/1.0 (Named Mobs Fetcher)',
                    'Accept: application/json',
                ],
                'timeout' => 30
            ]
        ]);
        
        $response = file_get_contents($url, false, $context);
        
        if ($response === false) {
            return null;
        }
        
        return json_decode($response, true);
    }
    
    public function saveToJson($filename = 'named_mobs.json') {
        $jsonData = json_encode([
            'timestamp' => date('Y-m-d H:i:s'),
            'total_count' => count($this->namedMobs),
            'mobs' => $this->namedMobs
        ], JSON_PRETTY_PRINT);
        
        file_put_contents($filename, $jsonData);
        echo "💾 Saved " . count($this->namedMobs) . " named mobs to {$filename}\n";
    }
    
    public function generateSqlInserts($filename = 'named_mobs.sql') {
        $sql = "-- Named Mobs Data from Ashes Codex\n";
        $sql .= "-- Generated on: " . date('Y-m-d H:i:s') . "\n\n";
        
        $sql .= "CREATE TABLE IF NOT EXISTS named_mobs (\n";
        $sql .= "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n";
        $sql .= "    name TEXT NOT NULL,\n";
        $sql .= "    slug TEXT,\n";
        $sql .= "    level INTEGER,\n";
        $sql .= "    level_range TEXT,\n";
        $sql .= "    respawn_time TEXT,\n";
        $sql .= "    respawn_minutes INTEGER,\n";
        $sql .= "    codex_url TEXT,\n";
        $sql .= "    location_x REAL,\n";
        $sql .= "    location_y REAL,\n";
        $sql .= "    location_z REAL,\n";
        $sql .= "    type TEXT DEFAULT 'named_mob',\n";
        $sql .= "    created_at DATETIME DEFAULT CURRENT_TIMESTAMP\n";
        $sql .= ");\n\n";
        
        foreach ($this->namedMobs as $mob) {
            $name = sqlite_escape_string($mob['name']);
            $slug = sqlite_escape_string($mob['slug']);
            $levelRange = sqlite_escape_string($mob['levelRange']);
            $respawnTime = sqlite_escape_string($mob['respawnTime']);
            $codexUrl = sqlite_escape_string($mob['codexUrl']);
            
            $locationX = $mob['location']['x'] ?? 'NULL';
            $locationY = $mob['location']['y'] ?? 'NULL';
            $locationZ = $mob['location']['z'] ?? 'NULL';
            
            $sql .= "INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (\n";
            $sql .= "    '{$name}',\n";
            $sql .= "    '{$slug}',\n";
            $sql .= "    {$mob['level']},\n";
            $sql .= "    '{$levelRange}',\n";
            $sql .= "    '{$respawnTime}',\n";
            $sql .= "    {$mob['respawnMinutes']},\n";
            $sql .= "    '{$codexUrl}',\n";
            $sql .= "    {$locationX},\n";
            $sql .= "    {$locationY},\n";
            $sql .= "    {$locationZ}\n";
            $sql .= ");\n\n";
        }
        
        file_put_contents($filename, $sql);
        echo "💾 Generated SQL inserts in {$filename}\n";
    }
}

// Helper function for SQLite escaping
function sqlite_escape_string($str) {
    return str_replace("'", "''", $str);
}

// Run the script
if (php_sapi_name() === 'cli') {
    $fetcher = new NamedMobsFetcher();
    $mobs = $fetcher->fetchAllNamedMobs();
    
    // Save data in multiple formats
    $fetcher->saveToJson('data/named_mobs.json');
    $fetcher->generateSqlInserts('data/named_mobs.sql');
    
    echo "\n🎯 Summary:\n";
    echo "- Total named mobs: " . count($mobs) . "\n";
    echo "- JSON file: data/named_mobs.json\n";
    echo "- SQL file: data/named_mobs.sql\n";
    echo "- Use these files to populate your timer database\n";
}
?>
