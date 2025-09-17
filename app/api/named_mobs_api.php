<?php
/**
 * Named Mobs API Extension for AOC Timer Map
 * Handles named mob timers integration with existing marker system
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit(0);
}

// Use the same database as the main application
$dbFile = '/app/database/db/mydb.sqlite';

try {
    $db = new PDO('sqlite:' . $dbFile);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Create named_mobs table if it doesn't exist
    $createTableSQL = "
    CREATE TABLE IF NOT EXISTS named_mobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        slug TEXT UNIQUE,
        level INTEGER,
        level_range TEXT,
        respawn_time TEXT,
        respawn_minutes INTEGER,
        codex_url TEXT,
        location_x REAL,
        location_y REAL,
        location_z REAL,
        type TEXT DEFAULT 'named_mob',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )";
    
    $db->exec($createTableSQL);

    // Create named_mob_timers table for active timer tracking
    $createTimersTableSQL = "
    CREATE TABLE IF NOT EXISTS named_mob_timers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        named_mob_id INTEGER NOT NULL,
        marker_id INTEGER,
        last_killed_at DATETIME,
        respawn_at DATETIME,
        server_name TEXT DEFAULT 'default',
        notes TEXT,
        player_name TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (named_mob_id) REFERENCES named_mobs(id),
        FOREIGN KEY (marker_id) REFERENCES markers(id)
    )";
    
    $db->exec($createTimersTableSQL);

    $method = $_SERVER['REQUEST_METHOD'];
    $path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
    
    switch ($method) {
        case 'GET':
            if (strpos($path, '/named-mobs/search') !== false) {
                handleSearchNamedMobs($db);
            } elseif (strpos($path, '/named-mobs/timers') !== false) {
                handleGetActiveTimers($db);
            } elseif (strpos($path, '/named-mobs/') !== false) {
                $parts = explode('/', trim($path, '/'));
                $mobId = end($parts);
                handleGetNamedMob($db, $mobId);
            } else {
                handleGetAllNamedMobs($db);
            }
            break;
            
        case 'POST':
            if (strpos($path, '/named-mobs/timer') !== false) {
                handleStartTimer($db);
            } elseif (strpos($path, '/named-mobs/import') !== false) {
                handleImportNamedMobs($db);
            } else {
                handleCreateNamedMob($db);
            }
            break;
            
        case 'PUT':
            if (strpos($path, '/named-mobs/timer') !== false) {
                handleUpdateTimer($db);
            } else {
                handleUpdateNamedMob($db);
            }
            break;
            
        case 'DELETE':
            if (strpos($path, '/named-mobs/timer') !== false) {
                handleDeleteTimer($db);
            } else {
                handleDeleteNamedMob($db);
            }
            break;
            
        default:
            http_response_code(405);
            echo json_encode(['error' => 'Method not allowed']);
            break;
    }

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['error' => $e->getMessage()]);
}

// Handler functions

function handleGetAllNamedMobs($db) {
    $level = $_GET['level'] ?? null;
    $search = $_GET['search'] ?? null;
    
    $sql = "SELECT nm.id, nm.name, nm.slug, nm.level, nm.level_range, nm.respawn_time, nm.respawn_minutes, nm.codex_url, 
                   nm.location_x, nm.location_y, nm.location_z, nm.type, 
                   nm.map_lat, nm.map_lng, nm.coordinate_source,
                   nm.created_at, nm.updated_at 
            FROM named_mobs nm WHERE 1=1";
    $params = [];
    
    if ($level) {
        $sql .= " AND nm.level = ?";
        $params[] = $level;
    }
    
    if ($search) {
        $sql .= " AND (nm.name LIKE ? OR nm.slug LIKE ?)";
        $params[] = "%$search%";
        $params[] = "%$search%";
    }
    
    $sql .= " ORDER BY nm.level, nm.name";
    
    $stmt = $db->prepare($sql);
    $stmt->execute($params);
    $mobs = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // Add special items for each mob
    $itemStmt = $db->prepare("
        SELECT item_name, item_url, item_rarity, item_type, drop_order, drop_chance 
        FROM named_mob_items 
        WHERE named_mob_id = ? 
        ORDER BY drop_order
    ");
    
    foreach ($mobs as &$mob) {
        $itemStmt->execute([$mob['id']]);
        $items = $itemStmt->fetchAll(PDO::FETCH_ASSOC);
        $mob['special_items'] = $items;
    }
    
    echo json_encode([
        'success' => true,
        'data' => $mobs,
        'total' => count($mobs)
    ]);
}

function handleSearchNamedMobs($db) {
    $query = $_GET['q'] ?? '';
    $level = $_GET['level'] ?? null;
    
    if (empty($query)) {
        echo json_encode(['success' => true, 'data' => []]);
        return;
    }
    
    $sql = "SELECT nm.id, nm.name, nm.slug, nm.level, nm.level_range, nm.respawn_time, nm.respawn_minutes, nm.codex_url, 
                   nm.location_x, nm.location_y, nm.location_z, nm.type, 
                   nm.map_lat, nm.map_lng, nm.coordinate_source,
                   nm.created_at, nm.updated_at 
            FROM named_mobs nm WHERE nm.name LIKE ? OR nm.slug LIKE ?";
    $params = ["%$query%", "%$query%"];
    
    if ($level) {
        $sql .= " AND nm.level = ?";
        $params[] = $level;
    }
    
    $sql .= " ORDER BY nm.level, nm.name LIMIT 20";
    
    $stmt = $db->prepare($sql);
    $stmt->execute($params);
    $mobs = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // Add special items for each mob
    $itemStmt = $db->prepare("
        SELECT item_name, item_url, item_rarity, item_type, drop_order, drop_chance 
        FROM named_mob_items 
        WHERE named_mob_id = ? 
        ORDER BY drop_order
    ");
    
    foreach ($mobs as &$mob) {
        $itemStmt->execute([$mob['id']]);
        $items = $itemStmt->fetchAll(PDO::FETCH_ASSOC);
        $mob['special_items'] = $items;
    }
    
    echo json_encode([
        'success' => true,
        'data' => $mobs
    ]);
}

function handleGetActiveTimers($db) {
    $server = $_GET['server'] ?? 'default';
    
    $sql = "
    SELECT 
        t.*,
        m.name as mob_name,
        m.level,
        m.respawn_minutes,
        m.codex_url,
        m.location_x,
        m.location_y,
        CASE 
            WHEN t.respawn_at > datetime('now') THEN 
                ROUND((julianday(t.respawn_at) - julianday('now')) * 1440)
            ELSE 0 
        END as minutes_remaining
    FROM named_mob_timers t
    JOIN named_mobs m ON t.named_mob_id = m.id
    WHERE t.server_name = ?
    ORDER BY t.respawn_at
    ";
    
    $stmt = $db->prepare($sql);
    $stmt->execute([$server]);
    $timers = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    echo json_encode([
        'success' => true,
        'data' => $timers,
        'server' => $server
    ]);
}

function handleStartTimer($db) {
    $input = json_decode(file_get_contents('php://input'), true);
    
    $namedMobId = $input['named_mob_id'] ?? null;
    $killedAt = $input['killed_at'] ?? date('Y-m-d H:i:s');
    $server = $input['server'] ?? 'default';
    $playerName = $input['player_name'] ?? null;
    $notes = $input['notes'] ?? null;
    
    if (!$namedMobId) {
        http_response_code(400);
        echo json_encode(['error' => 'Named mob ID is required']);
        return;
    }
    
    // Get respawn time from named_mobs table
    $stmt = $db->prepare("SELECT respawn_minutes FROM named_mobs WHERE id = ?");
    $stmt->execute([$namedMobId]);
    $mob = $stmt->fetch(PDO::FETCH_ASSOC);
    
    if (!$mob) {
        http_response_code(404);
        echo json_encode(['error' => 'Named mob not found']);
        return;
    }
    
    $respawnMinutes = $mob['respawn_minutes'];
    $respawnAt = date('Y-m-d H:i:s', strtotime($killedAt . " + $respawnMinutes minutes"));
    
    // Delete existing timer for this mob on this server
    $stmt = $db->prepare("DELETE FROM named_mob_timers WHERE named_mob_id = ? AND server_name = ?");
    $stmt->execute([$namedMobId, $server]);
    
    // Insert new timer
    $stmt = $db->prepare("
        INSERT INTO named_mob_timers (named_mob_id, last_killed_at, respawn_at, server_name, player_name, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ");
    $stmt->execute([$namedMobId, $killedAt, $respawnAt, $server, $playerName, $notes]);
    
    $timerId = $db->lastInsertId();
    
    echo json_encode([
        'success' => true,
        'timer_id' => $timerId,
        'respawn_at' => $respawnAt,
        'minutes_until_respawn' => $respawnMinutes
    ]);
}

function handleImportNamedMobs($db) {
    $jsonFile = __DIR__ . '/../data/named_mobs.json';
    
    if (!file_exists($jsonFile)) {
        http_response_code(404);
        echo json_encode(['error' => 'Named mobs data file not found']);
        return;
    }
    
    $data = json_decode(file_get_contents($jsonFile), true);
    $mobs = $data['mobs'] ?? [];
    
    $imported = 0;
    $updated = 0;
    
    $stmt = $db->prepare("
        INSERT OR REPLACE INTO named_mobs 
        (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z, type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ");
    
    foreach ($mobs as $mob) {
        $result = $stmt->execute([
            $mob['name'],
            $mob['slug'],
            $mob['level'],
            $mob['levelRange'],
            $mob['respawnTime'],
            $mob['respawnMinutes'],
            $mob['codexUrl'],
            $mob['location']['x'] ?? null,
            $mob['location']['y'] ?? null,
            $mob['location']['z'] ?? null,
            $mob['type']
        ]);
        
        if ($result) {
            $imported++;
        }
    }
    
    echo json_encode([
        'success' => true,
        'imported' => $imported,
        'total_mobs' => count($mobs),
        'message' => "Imported $imported named mobs successfully"
    ]);
}

function handleGetNamedMob($db, $mobId) {
    $stmt = $db->prepare("
        SELECT id, name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, 
               location_x, location_y, location_z, type, 
               map_lat, map_lng, coordinate_source,
               created_at, updated_at 
        FROM named_mobs WHERE id = ? OR slug = ?
    ");
    $stmt->execute([$mobId, $mobId]);
    $mob = $stmt->fetch(PDO::FETCH_ASSOC);
    
    if (!$mob) {
        http_response_code(404);
        echo json_encode(['error' => 'Named mob not found']);
        return;
    }
    
    // Add special items for this mob
    $itemStmt = $db->prepare("
        SELECT item_name, item_url, item_rarity, item_type, drop_order, drop_chance 
        FROM named_mob_items 
        WHERE named_mob_id = ? 
        ORDER BY drop_order
    ");
    $itemStmt->execute([$mob['id']]);
    $items = $itemStmt->fetchAll(PDO::FETCH_ASSOC);
    $mob['special_items'] = $items;
    
    echo json_encode([
        'success' => true,
        'data' => $mob
    ]);
}

function handleUpdateTimer($db) {
    $input = json_decode(file_get_contents('php://input'), true);
    $timerId = $input['timer_id'] ?? null;
    
    if (!$timerId) {
        http_response_code(400);
        echo json_encode(['error' => 'Timer ID is required']);
        return;
    }
    
    $updates = [];
    $params = [];
    
    if (isset($input['notes'])) {
        $updates[] = "notes = ?";
        $params[] = $input['notes'];
    }
    
    if (isset($input['player_name'])) {
        $updates[] = "player_name = ?";
        $params[] = $input['player_name'];
    }
    
    if (empty($updates)) {
        http_response_code(400);
        echo json_encode(['error' => 'No updates provided']);
        return;
    }
    
    $updates[] = "updated_at = ?";
    $params[] = date('Y-m-d H:i:s');
    $params[] = $timerId;
    
    $sql = "UPDATE named_mob_timers SET " . implode(', ', $updates) . " WHERE id = ?";
    $stmt = $db->prepare($sql);
    $result = $stmt->execute($params);
    
    echo json_encode([
        'success' => $result,
        'message' => $result ? 'Timer updated successfully' : 'Failed to update timer'
    ]);
}

function handleDeleteTimer($db) {
    $timerId = $_GET['timer_id'] ?? null;
    
    if (!$timerId) {
        http_response_code(400);
        echo json_encode(['error' => 'Timer ID is required']);
        return;
    }
    
    $stmt = $db->prepare("DELETE FROM named_mob_timers WHERE id = ?");
    $result = $stmt->execute([$timerId]);
    
    echo json_encode([
        'success' => $result,
        'message' => $result ? 'Timer deleted successfully' : 'Failed to delete timer'
    ]);
}
?>
