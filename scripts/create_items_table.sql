-- Create named_mob_items table for better data normalization
-- This replaces the JSON special_drops column with a proper relational structure

CREATE TABLE IF NOT EXISTS named_mob_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    named_mob_id INTEGER NOT NULL,
    item_name TEXT NOT NULL,
    item_url TEXT,
    item_rarity TEXT CHECK(item_rarity IN ('Common', 'Uncommon', 'Rare', 'Epic', 'Legendary')),
    item_type TEXT,
    drop_order INTEGER DEFAULT 1, -- To maintain order of items (1=primary, 2=secondary, etc.)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (named_mob_id) REFERENCES named_mobs(id) ON DELETE CASCADE
);

-- Create index for performance
CREATE INDEX IF NOT EXISTS idx_named_mob_items_mob_id ON named_mob_items(named_mob_id);
CREATE INDEX IF NOT EXISTS idx_named_mob_items_order ON named_mob_items(named_mob_id, drop_order);

-- Migrate existing special_drops data to the new table
INSERT INTO named_mob_items (named_mob_id, item_name, item_url, item_rarity, item_type, drop_order)
SELECT 
    nm.id as named_mob_id,
    json_extract(drop_item.value, '$.name') as item_name,
    json_extract(drop_item.value, '$.url') as item_url,
    json_extract(drop_item.value, '$.rarity') as item_rarity,
    json_extract(drop_item.value, '$.type') as item_type,
    (drop_item.key + 1) as drop_order
FROM named_mobs nm,
     json_each(json_extract(nm.special_drops, '$.drops')) as drop_item
WHERE nm.special_drops IS NOT NULL 
  AND nm.special_drops != '';

-- Show migration results
SELECT 
    nm.name,
    nmi.item_name,
    nmi.item_rarity,
    nmi.drop_order
FROM named_mobs nm
JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id
ORDER BY nm.name, nmi.drop_order;
