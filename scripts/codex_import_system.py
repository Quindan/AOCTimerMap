#!/usr/bin/env python3
"""
Flexible Codex Import System for AOC Timer Map

This system handles regular imports from Ashes Codex while preserving local modifications:
- Triangulated coordinates (map_lat, map_lng, coordinate_source)
- Custom special items and drop chances
- Local respawn timer adjustments
- Custom notes and modifications

The system is designed to:
1. Import new named mobs from Codex
2. Update existing mobs while preserving local data
3. Detect changes in Codex data (respawn times, locations, etc.)
4. Generate import reports for review
5. Handle incremental updates without data loss
"""

import sqlite3
import json
import requests
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import argparse

class CodexImportSystem:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self.import_log = []
        
    def connect_db(self):
        """Connect to the database."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
    def disconnect_db(self):
        """Disconnect from the database."""
        if self.conn:
            self.conn.close()
            
    def log(self, message: str, level: str = "INFO"):
        """Log import actions."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.import_log.append(log_entry)
        print(log_entry)
        
    def get_local_preservations(self) -> Dict:
        """Get data that should be preserved during imports."""
        cursor = self.conn.cursor()
        
        # Get triangulated coordinates
        cursor.execute("""
            SELECT id, name, map_lat, map_lng, coordinate_source 
            FROM named_mobs 
            WHERE map_lat IS NOT NULL AND map_lng IS NOT NULL
        """)
        triangulated_coords = {row['name']: {
            'map_lat': row['map_lat'],
            'map_lng': row['map_lng'], 
            'coordinate_source': row['coordinate_source']
        } for row in cursor.fetchall()}
        
        # Get custom items
        cursor.execute("""
            SELECT nm.name, nmi.item_name, nmi.item_url, nmi.item_rarity, 
                   nmi.item_type, nmi.drop_order, nmi.drop_chance
            FROM named_mobs nm
            JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id
        """)
        custom_items = {}
        for row in cursor.fetchall():
            mob_name = row['name']
            if mob_name not in custom_items:
                custom_items[mob_name] = []
            custom_items[mob_name].append({
                'item_name': row['item_name'],
                'item_url': row['item_url'],
                'item_rarity': row['item_rarity'],
                'item_type': row['item_type'],
                'drop_order': row['drop_order'],
                'drop_chance': row['drop_chance']
            })
            
        return {
            'triangulated_coords': triangulated_coords,
            'custom_items': custom_items
        }
        
    def detect_changes(self, codex_data: List[Dict], local_data: Dict) -> Dict:
        """Detect changes between Codex and local data."""
        changes = {
            'new_mobs': [],
            'updated_respawn_times': [],
            'updated_locations': [],
            'removed_mobs': []
        }
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, respawn_time, location_x, location_y FROM named_mobs")
        local_mobs = {row['name']: dict(row) for row in cursor.fetchall()}
        
        codex_mob_names = {mob['name'] for mob in codex_data}
        local_mob_names = set(local_mobs.keys())
        
        # New mobs in Codex
        changes['new_mobs'] = [mob for mob in codex_data if mob['name'] not in local_mob_names]
        
        # Removed mobs (in local but not in Codex)
        changes['removed_mobs'] = list(local_mob_names - codex_mob_names)
        
        # Updated data
        for mob in codex_data:
            if mob['name'] in local_mobs:
                local_mob = local_mobs[mob['name']]
                
                # Check respawn time changes
                if mob.get('respawn_time') != local_mob['respawn_time']:
                    changes['updated_respawn_times'].append({
                        'name': mob['name'],
                        'old': local_mob['respawn_time'],
                        'new': mob.get('respawn_time')
                    })
                    
                # Check location changes
                if (mob.get('location_x') != local_mob['location_x'] or 
                    mob.get('location_y') != local_mob['location_y']):
                    changes['updated_locations'].append({
                        'name': mob['name'],
                        'old': [local_mob['location_x'], local_mob['location_y']],
                        'new': [mob.get('location_x'), mob.get('location_y')]
                    })
        
        return changes
        
    def import_mob_data(self, codex_data: List[Dict], preserve_local: bool = True):
        """Import mob data while preserving local modifications."""
        preserved = self.get_local_preservations() if preserve_local else {'triangulated_coords': {}, 'custom_items': {}}
        changes = self.detect_changes(codex_data, preserved)
        
        self.log(f"Starting import of {len(codex_data)} named mobs")
        self.log(f"Preserving {len(preserved['triangulated_coords'])} triangulated coordinates")
        self.log(f"Preserving {len(preserved['custom_items'])} custom item sets")
        
        # Report changes
        if changes['new_mobs']:
            self.log(f"Found {len(changes['new_mobs'])} new mobs")
        if changes['updated_respawn_times']:
            self.log(f"Found {len(changes['updated_respawn_times'])} respawn time changes")
        if changes['updated_locations']:
            self.log(f"Found {len(changes['updated_locations'])} location changes")
        if changes['removed_mobs']:
            self.log(f"Found {len(changes['removed_mobs'])} removed mobs", "WARNING")
            
        cursor = self.conn.cursor()
        
        for mob in codex_data:
            # Check if mob exists
            cursor.execute("SELECT id FROM named_mobs WHERE name = ?", (mob['name'],))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing mob, preserving local data
                mob_id = existing['id']
                
                # Prepare update data
                update_data = {
                    'level': mob.get('level'),
                    'level_range': mob.get('level_range'),
                    'respawn_time': mob.get('respawn_time'),
                    'respawn_minutes': mob.get('respawn_minutes'),
                    'codex_url': mob.get('codex_url'),
                    'location_x': mob.get('location_x'),
                    'location_y': mob.get('location_y'),
                    'location_z': mob.get('location_z'),
                    'updated_at': datetime.now().isoformat()
                }
                
                # Preserve triangulated coordinates
                if mob['name'] in preserved['triangulated_coords']:
                    coords = preserved['triangulated_coords'][mob['name']]
                    update_data.update(coords)
                    self.log(f"Preserving triangulated coords for {mob['name']}")
                
                # Build update query
                set_clause = ', '.join([f"{k} = ?" for k in update_data.keys()])
                values = list(update_data.values()) + [mob_id]
                
                cursor.execute(f"UPDATE named_mobs SET {set_clause} WHERE id = ?", values)
                
            else:
                # Insert new mob
                cursor.execute("""
                    INSERT INTO named_mobs 
                    (name, slug, level, level_range, respawn_time, respawn_minutes, 
                     codex_url, location_x, location_y, location_z, type)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    mob['name'],
                    mob.get('slug'),
                    mob.get('level'),
                    mob.get('level_range'),
                    mob.get('respawn_time'),
                    mob.get('respawn_minutes'),
                    mob.get('codex_url'),
                    mob.get('location_x'),
                    mob.get('location_y'),
                    mob.get('location_z'),
                    'named_mob'
                ))
                self.log(f"Added new mob: {mob['name']}")
        
        self.conn.commit()
        self.log("Import completed successfully")
        
        return changes
        
    def generate_import_report(self, changes: Dict) -> str:
        """Generate a human-readable import report."""
        report = []
        report.append("=" * 50)
        report.append("CODEX IMPORT REPORT")
        report.append("=" * 50)
        report.append(f"Import Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        if changes['new_mobs']:
            report.append(f"NEW MOBS ({len(changes['new_mobs'])}):")
            for mob in changes['new_mobs']:
                report.append(f"  + {mob['name']} (Level {mob.get('level', '?')})")
            report.append("")
            
        if changes['updated_respawn_times']:
            report.append(f"RESPAWN TIME CHANGES ({len(changes['updated_respawn_times'])}):")
            for change in changes['updated_respawn_times']:
                report.append(f"  ~ {change['name']}: {change['old']} → {change['new']}")
            report.append("")
            
        if changes['updated_locations']:
            report.append(f"LOCATION CHANGES ({len(changes['updated_locations'])}):")
            for change in changes['updated_locations']:
                report.append(f"  ~ {change['name']}: {change['old']} → {change['new']}")
            report.append("")
            
        if changes['removed_mobs']:
            report.append(f"REMOVED MOBS ({len(changes['removed_mobs'])}):")
            for mob_name in changes['removed_mobs']:
                report.append(f"  - {mob_name}")
            report.append("")
            
        report.append("PRESERVED LOCAL DATA:")
        report.append(f"  ✓ Triangulated coordinates preserved")
        report.append(f"  ✓ Custom special items preserved") 
        report.append(f"  ✓ Drop chances preserved")
        
        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description='Import Codex data flexibly')
    parser.add_argument('--source', choices=['file', 'api'], default='file',
                       help='Data source: file (JSON) or api (direct Codex)')
    parser.add_argument('--input', type=str, 
                       help='Input file path (for file source)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be imported without making changes')
    parser.add_argument('--report-only', action='store_true',
                       help='Generate report only, no imports')
    
    args = parser.parse_args()
    
    db_path = 'data/database/db/mydb.sqlite'
    importer = CodexImportSystem(db_path)
    
    try:
        importer.connect_db()
        
        if args.report_only:
            # Just show current state
            preserved = importer.get_local_preservations()
            print(f"Triangulated coordinates: {len(preserved['triangulated_coords'])}")
            print(f"Custom items: {len(preserved['custom_items'])}")
            return
            
        # Example usage with dummy data for now
        # In the future, this would fetch from Codex API or read from JSON export
        example_codex_data = [
            {
                'name': 'Forgelord Zammer',
                'level': 25,
                'respawn_time': '30-45 minutes',
                'respawn_minutes': 30,
                'codex_url': 'https://ashescodex.com/db/mob/forgelord-zammer',
                'location_x': -123456.789,
                'location_y': 654321.123,
                'location_z': 100.0
            }
        ]
        
        if not args.dry_run:
            changes = importer.import_mob_data(example_codex_data)
            report = importer.generate_import_report(changes)
            print(report)
            
            # Save report
            with open(f'data/import_reports/import_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt', 'w') as f:
                f.write(report)
        else:
            print("DRY RUN - No changes made")
            changes = importer.detect_changes(example_codex_data, importer.get_local_preservations())
            report = importer.generate_import_report(changes)
            print(report)
            
    except Exception as e:
        importer.log(f"Import failed: {e}", "ERROR")
        sys.exit(1)
    finally:
        importer.disconnect_db()

if __name__ == "__main__":
    main()
