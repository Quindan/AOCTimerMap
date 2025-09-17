#!/usr/bin/env python3
"""
Smart Codex Import System

This script imports named mob data from Ashes Codex while:
1. Preserving triangulated coordinates (map_lat, map_lng, coordinate_source)
2. Preserving custom special items and drop chances
3. Detecting and reporting changes (respawn times, locations, etc.)
4. Adding new named mobs
5. Updating existing data intelligently
6. Filtering to only show named mobs with special drops
"""

import sqlite3
import json
import requests
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import argparse

class SmartCodexImporter:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self.changes = {
            'new_mobs': [],
            'updated_respawn_times': [],
            'updated_locations': [],
            'updated_levels': [],
            'removed_mobs': [],
            'preserved_triangulation': [],
            'preserved_items': []
        }
        
    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
    def disconnect(self):
        if self.conn:
            self.conn.close()
            
    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def get_current_mobs(self) -> Dict[str, Dict]:
        """Get current named mobs from database."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name, slug, level, level_range, respawn_time, respawn_minutes,
                   codex_url, location_x, location_y, location_z, type,
                   map_lat, map_lng, coordinate_source, is_hidden,
                   created_at, updated_at
            FROM named_mobs
        """)
        
        mobs = {}
        for row in cursor.fetchall():
            mobs[row['name']] = dict(row)
            
        return mobs
        
    def get_special_items(self) -> Dict[str, List[Dict]]:
        """Get current special items for each mob."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT nm.name, nmi.item_name, nmi.item_url, nmi.item_rarity,
                   nmi.item_type, nmi.drop_order, nmi.drop_chance
            FROM named_mobs nm
            JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id
            ORDER BY nm.name, nmi.drop_order
        """)
        
        items = {}
        for row in cursor.fetchall():
            mob_name = row['name']
            if mob_name not in items:
                items[mob_name] = []
            items[mob_name].append(dict(row))
            
        return items
        
    def simulate_codex_import(self) -> List[Dict]:
        """
        Simulate a Codex import with some example data.
        In the future, this would fetch from the actual Codex API.
        """
        return [
            {
                'name': 'Forgelord Zammer',
                'slug': 'forgelord-zammer',
                'level': 25,
                'level_range': '25',
                'respawn_time': '30-45 minutes',
                'respawn_minutes': 30,
                'codex_url': 'https://ashescodex.com/db/mob/forgelord-zammer',
                'location_x': -123456.789,
                'location_y': 654321.123,
                'location_z': 100.0,
                'special_drops': [
                    {
                        'name': 'Ancient Dunzen Longsword',
                        'url': 'https://ashescodex.com/db/item/Gear_Weapon_Sword_1H_Zammer',
                        'rarity': 'Uncommon',
                        'type': 'Weapon',
                        'drop_chance': '12%'  # Updated from Codex
                    },
                    {
                        'name': 'Forgelord Signet',
                        'url': 'https://ashescodex.com/db/item/Gear_Accessory_Ring_Zammer',
                        'rarity': 'Uncommon', 
                        'type': 'Ring',
                        'drop_chance': '8%'
                    }
                ]
            },
            {
                'name': 'Chief Armorer Jannus',
                'slug': 'chief-armorer-jannus',
                'level': 20,
                'level_range': '20',
                'respawn_time': '25-35 minutes',  # Changed from original
                'respawn_minutes': 25,  # Changed from original
                'codex_url': 'https://ashescodex.com/db/mob/chief-armorer-jannus',
                'location_x': -987654.321,
                'location_y': 123456.789,
                'location_z': 50.0,
                'special_drops': [
                    {
                        'name': 'Buttressed Shield',
                        'url': 'https://ashescodex.com/db/item/Gear_Weapon_Shield_OH_Jannus',
                        'rarity': 'Uncommon',
                        'type': 'Shield',
                        'drop_chance': '18%'  # New drop chance data
                    }
                ]
            },
            # New mob example
            {
                'name': 'Magnus the Cinderbound Colossus',
                'slug': 'magnus-the-cinderbound-colossus',
                'level': 50,
                'level_range': '50',
                'respawn_time': '60-90 minutes',
                'respawn_minutes': 60,
                'codex_url': 'https://ashescodex.com/db/mob/magnus-the-cinderbound-colossus',
                'location_x': -555555.555,
                'location_y': 777777.777,
                'location_z': 200.0,
                'special_drops': [
                    {
                        'name': 'Cinderbound Greatsword',
                        'url': 'https://ashescodex.com/db/item/cinderbound-greatsword',
                        'rarity': 'Epic',
                        'type': 'Weapon',
                        'drop_chance': '5%'
                    },
                    {
                        'name': 'Molten Core Fragment',
                        'url': 'https://ashescodex.com/db/item/molten-core-fragment',
                        'rarity': 'Rare',
                        'type': 'Material',
                        'drop_chance': '25%'
                    }
                ]
            }
        ]
        
    def detect_changes(self, codex_data: List[Dict]) -> Dict:
        """Detect what has changed between Codex and our database."""
        current_mobs = self.get_current_mobs()
        current_items = self.get_special_items()
        
        codex_mob_names = {mob['name'] for mob in codex_data}
        local_mob_names = set(current_mobs.keys())
        
        # New mobs
        new_mobs = [mob for mob in codex_data if mob['name'] not in local_mob_names]
        self.changes['new_mobs'] = new_mobs
        
        # Removed mobs (in our DB but not in Codex)
        removed_mobs = local_mob_names - codex_mob_names
        self.changes['removed_mobs'] = list(removed_mobs)
        
        # Check for changes in existing mobs
        for mob in codex_data:
            if mob['name'] in current_mobs:
                local_mob = current_mobs[mob['name']]
                
                # Check respawn time changes
                if mob.get('respawn_time') != local_mob['respawn_time']:
                    self.changes['updated_respawn_times'].append({
                        'name': mob['name'],
                        'old': local_mob['respawn_time'],
                        'new': mob.get('respawn_time')
                    })
                    
                # Check level changes
                if mob.get('level') != local_mob['level']:
                    self.changes['updated_levels'].append({
                        'name': mob['name'],
                        'old': local_mob['level'],
                        'new': mob.get('level')
                    })
                    
                # Check location changes (only if no triangulation)
                if (local_mob['map_lat'] is None and local_mob['map_lng'] is None and
                    (mob.get('location_x') != local_mob['location_x'] or 
                     mob.get('location_y') != local_mob['location_y'])):
                    self.changes['updated_locations'].append({
                        'name': mob['name'],
                        'old': [local_mob['location_x'], local_mob['location_y']],
                        'new': [mob.get('location_x'), mob.get('location_y')]
                    })
                    
        return self.changes
        
    def import_mob_data(self, codex_data: List[Dict], dry_run: bool = False):
        """Import mob data with intelligent preservation."""
        current_mobs = self.get_current_mobs()
        current_items = self.get_special_items()
        
        self.log(f"Starting {'DRY RUN' if dry_run else 'IMPORT'} of {len(codex_data)} mobs")
        
        if not dry_run:
            cursor = self.conn.cursor()
        
        for mob in codex_data:
            if mob['name'] in current_mobs:
                # Update existing mob
                local_mob = current_mobs[mob['name']]
                
                # Preserve triangulated coordinates
                if local_mob['map_lat'] is not None and local_mob['map_lng'] is not None:
                    self.changes['preserved_triangulation'].append(mob['name'])
                    self.log(f"Preserving triangulated coords for {mob['name']}")
                    
                # Prepare update
                update_fields = []
                update_values = []
                
                if mob.get('level') != local_mob['level']:
                    update_fields.append('level = ?')
                    update_values.append(mob.get('level'))
                    
                if mob.get('respawn_time') != local_mob['respawn_time']:
                    update_fields.append('respawn_time = ?')
                    update_fields.append('respawn_minutes = ?')
                    update_values.extend([mob.get('respawn_time'), mob.get('respawn_minutes')])
                    
                # Only update location if no triangulation exists
                if local_mob['map_lat'] is None and local_mob['map_lng'] is None:
                    if (mob.get('location_x') != local_mob['location_x'] or 
                        mob.get('location_y') != local_mob['location_y']):
                        update_fields.extend(['location_x = ?', 'location_y = ?', 'location_z = ?'])
                        update_values.extend([mob.get('location_x'), mob.get('location_y'), mob.get('location_z')])
                        
                if mob.get('codex_url') != local_mob['codex_url']:
                    update_fields.append('codex_url = ?')
                    update_values.append(mob.get('codex_url'))
                    
                if update_fields:
                    update_fields.append('updated_at = ?')
                    update_values.append(datetime.now().isoformat())
                    update_values.append(local_mob['id'])
                    
                    if not dry_run:
                        cursor.execute(f"UPDATE named_mobs SET {', '.join(update_fields)} WHERE id = ?", update_values)
                    self.log(f"Updated {mob['name']}: {', '.join([f.split(' = ')[0] for f in update_fields[:-1]])}")
                    
            else:
                # New mob
                if not dry_run:
                    cursor.execute("""
                        INSERT INTO named_mobs 
                        (name, slug, level, level_range, respawn_time, respawn_minutes,
                         codex_url, location_x, location_y, location_z, type, is_hidden)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                    """, (
                        mob['name'], mob.get('slug'), mob.get('level'), mob.get('level_range'),
                        mob.get('respawn_time'), mob.get('respawn_minutes'), mob.get('codex_url'),
                        mob.get('location_x'), mob.get('location_y'), mob.get('location_z'),
                        'named_mob'
                    ))
                    mob_id = cursor.lastrowid
                else:
                    mob_id = 999  # Dummy for dry run
                    
                self.log(f"Added new mob: {mob['name']} (Level {mob.get('level')})")
                
            # Handle special items
            if 'special_drops' in mob and mob['special_drops']:
                mob_name = mob['name']
                
                # Check if we have custom items for this mob
                if mob_name in current_items:
                    self.changes['preserved_items'].append(mob_name)
                    self.log(f"Preserving custom items for {mob_name}")
                else:
                    # Import new items
                    if not dry_run:
                        # Get mob ID
                        if mob['name'] in current_mobs:
                            mob_id = current_mobs[mob['name']]['id']
                        
                        # Clear existing items and add new ones
                        cursor.execute("DELETE FROM named_mob_items WHERE named_mob_id = ?", (mob_id,))
                        
                        for order, item in enumerate(mob['special_drops'], 1):
                            cursor.execute("""
                                INSERT INTO named_mob_items 
                                (named_mob_id, item_name, item_url, item_rarity, item_type, drop_order, drop_chance)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, (
                                mob_id, item['name'], item['url'], item['rarity'],
                                item['type'], order, item.get('drop_chance')
                            ))
                    
                    self.log(f"Updated items for {mob_name}: {len(mob['special_drops'])} items")
        
        if not dry_run:
            self.conn.commit()
            
    def generate_report(self) -> str:
        """Generate import report."""
        lines = []
        lines.append("=" * 60)
        lines.append("SMART CODEX IMPORT REPORT")
        lines.append("=" * 60)
        lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        if self.changes['new_mobs']:
            lines.append(f"🆕 NEW MOBS ({len(self.changes['new_mobs'])}):")
            for mob in self.changes['new_mobs']:
                drops_count = len(mob.get('special_drops', []))
                lines.append(f"   + {mob['name']} (Level {mob.get('level')}) - {drops_count} drops")
            lines.append("")
            
        if self.changes['updated_respawn_times']:
            lines.append(f"⏱️  RESPAWN TIME CHANGES ({len(self.changes['updated_respawn_times'])}):")
            for change in self.changes['updated_respawn_times']:
                lines.append(f"   ~ {change['name']}: {change['old']} → {change['new']}")
            lines.append("")
            
        if self.changes['updated_levels']:
            lines.append(f"📊 LEVEL CHANGES ({len(self.changes['updated_levels'])}):")
            for change in self.changes['updated_levels']:
                lines.append(f"   ~ {change['name']}: Level {change['old']} → {change['new']}")
            lines.append("")
            
        if self.changes['updated_locations']:
            lines.append(f"📍 LOCATION CHANGES ({len(self.changes['updated_locations'])}):")
            for change in self.changes['updated_locations']:
                lines.append(f"   ~ {change['name']}: {change['old']} → {change['new']}")
            lines.append("")
            
        if self.changes['preserved_triangulation']:
            lines.append(f"🎯 PRESERVED TRIANGULATION ({len(self.changes['preserved_triangulation'])}):")
            for mob_name in self.changes['preserved_triangulation']:
                lines.append(f"   ✓ {mob_name}")
            lines.append("")
            
        if self.changes['preserved_items']:
            lines.append(f"🎁 PRESERVED CUSTOM ITEMS ({len(self.changes['preserved_items'])}):")
            for mob_name in self.changes['preserved_items']:
                lines.append(f"   ✓ {mob_name}")
            lines.append("")
            
        if self.changes['removed_mobs']:
            lines.append(f"❌ REMOVED FROM CODEX ({len(self.changes['removed_mobs'])}):")
            for mob_name in self.changes['removed_mobs']:
                lines.append(f"   - {mob_name} (consider hiding instead of deleting)")
            lines.append("")
            
        lines.append("💡 RECOMMENDATIONS:")
        lines.append("   • Review respawn time changes for accuracy")
        lines.append("   • Verify new mob locations with triangulation if needed")
        lines.append("   • Check removed mobs - hide instead of delete if temporary")
        lines.append("   • Update drop chances based on community feedback")
        
        return "\n".join(lines)
        
    def save_report(self, report: str):
        """Save import report to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/import_reports/codex_import_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write(report)
            
        self.log(f"Report saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description='Smart Codex Import System')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be imported without making changes')
    parser.add_argument('--report-only', action='store_true',
                       help='Generate report of current state only')
    
    args = parser.parse_args()
    
    importer = SmartCodexImporter('data/database/db/mydb.sqlite')
    
    try:
        importer.connect()
        
        if args.report_only:
            current_mobs = importer.get_current_mobs()
            current_items = importer.get_special_items()
            
            print(f"Current state:")
            print(f"  Named mobs: {len(current_mobs)}")
            print(f"  With special items: {len(current_items)}")
            print(f"  With triangulation: {len([m for m in current_mobs.values() if m['map_lat'] is not None])}")
            return
            
        # Simulate Codex data (in future, fetch from real API)
        codex_data = importer.simulate_codex_import()
        
        # Detect changes
        changes = importer.detect_changes(codex_data)
        
        # Import data
        importer.import_mob_data(codex_data, dry_run=args.dry_run)
        
        # Generate and save report
        report = importer.generate_report()
        print(report)
        
        if not args.dry_run:
            importer.save_report(report)
            
    except Exception as e:
        importer.log(f"Import failed: {e}", "ERROR")
        sys.exit(1)
    finally:
        importer.disconnect()

if __name__ == "__main__":
    main()
