-- Add timer tracking columns to named_mobs table
ALTER TABLE named_mobs ADD COLUMN last_killed_time INTEGER DEFAULT NULL;
ALTER TABLE named_mobs ADD COLUMN timer_active INTEGER DEFAULT 0;
ALTER TABLE named_mobs ADD COLUMN notify_when_ready INTEGER DEFAULT 0;

-- Update existing named_mob_timers table if needed
CREATE TABLE IF NOT EXISTS named_mob_timers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    named_mob_id INTEGER NOT NULL,
    last_killed_time INTEGER NOT NULL,
    timer_active INTEGER DEFAULT 1,
    notify_when_ready INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (named_mob_id) REFERENCES named_mobs(id) ON DELETE CASCADE
);
