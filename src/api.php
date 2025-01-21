<?php
// Code in English, textual prompts minimal.
// Using SQLite for partial create/update/delete + getAll.

header('Content-Type: application/json; charset=utf-8');
// For cross-origin if needed:
// header('Access-Control-Allow-Origin: *');
// header('Access-Control-Allow-Methods: GET, POST');
// header('Access-Control-Allow-Headers: Content-Type');

$dbFile = __DIR__ . '/db/mydb.sqlite';

$db = new PDO('sqlite:' . $dbFile);
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

// Create table if not exists
$db->exec("
CREATE TABLE IF NOT EXISTS markers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  label TEXT,
  lat REAL,
  lng REAL,
  startTime INTEGER,
  alarmAfter INTEGER,
  inGameCoord TEXT,
  type TEXT,
  state TEXT
)
");


$action = isset($_GET['action']) ? $_GET['action'] : null;

// GET => list all markers (if no specific action)
if ($_SERVER['REQUEST_METHOD'] === 'GET' && !$action) {
    $stmt = $db->prepare("SELECT id, label, lat, lng, startTime, alarmAfter, inGameCoord, type, state FROM markers");
    $stmt->execute();
    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
    echo json_encode($rows);
    exit;
}

// POST => partial ops
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $raw = file_get_contents('php://input');
    $data = json_decode($raw, true);

    if ($action === 'create') {
        // Insert a new marker
        $stmt = $db->prepare("
            INSERT INTO markers (label, lat, lng, startTime, alarmAfter, inGameCoord, type)
            VALUES (:label, :lat, :lng, :startTime, :alarmAfter, :inGameCoord, :type)
        ");
        $stmt->execute([
            ':label'      => $data['label'] ?? '',
            ':lat'        => $data['lat'] ?? 0,
            ':lng'        => $data['lng'] ?? 0,
            ':startTime'  => $data['startTime'] ?? (time()*1000),
            ':alarmAfter' => $data['alarmAfter'] ?? 60,
            ':inGameCoord'=> $data['inGameCoord'] ?? '',
            ':type'       => $data['type'] ?? ''
        ]);
        $newId = $db->lastInsertId();

        // Return the newly inserted marker
        $stmt2 = $db->prepare("SELECT * FROM markers WHERE id = :id");
        $stmt2->execute([':id' => $newId]);
        $marker = $stmt2->fetch(PDO::FETCH_ASSOC);

        echo json_encode([
            'success' => true,
            'marker' => $marker
        ]);
        exit;
    }
    elseif ($action === 'update') {
        // Expect an existing marker with an id
        if (!isset($data['id'])) {
            http_response_code(400);
            echo json_encode(['error' => 'Missing id for update']);
            exit;
        }
        $stmt = $db->prepare("
            UPDATE markers
            SET label = :label,
                lat = :lat,
                lng = :lng,
                startTime = :startTime,
                alarmAfter = :alarmAfter,
                inGameCoord = :inGameCoord,
                type = :type,
                state = :state
            WHERE id = :id
        ");
        $stmt->execute([
            ':label'      => $data['label'] ?? '',
            ':lat'        => $data['lat'] ?? 0,
            ':lng'        => $data['lng'] ?? 0,
            ':startTime'  => $data['startTime'] ?? (time()*1000),
            ':alarmAfter' => $data['alarmAfter'] ?? 1800,
            ':inGameCoord'=> $data['inGameCoord'] ?? '',
            ':type'       => $data['type'] ?? '',
            ':id'         => $data['id'],
            ':state'      => $data['state']
        ]);
        echo json_encode(['success' => true]);
        exit;
    }
    elseif ($action === 'delete') {
        // Expect an id
        if (!isset($data['id'])) {
            http_response_code(400);
            echo json_encode(['error' => 'Missing id for delete']);
            exit;
        }
        $stmt = $db->prepare("DELETE FROM markers WHERE id = :id");
        $stmt->execute([':id' => $data['id']]);
        echo json_encode(['success' => true]);
        exit;
    }
    else {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid or missing action']);
        exit;
    }
}

http_response_code(405);
echo json_encode(['error' => 'Method not allowed or unknown action']);
