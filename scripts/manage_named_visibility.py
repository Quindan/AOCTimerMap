#!/usr/bin/env python3
"""
Manage Named Mob Visibility

This script allows you to hide/show specific named mobs from the map display.
Useful for filtering out mobs without special drops or test mobs.
"""

import sqlite3
import sys
import argparse

def connect_db():
    conn = sqlite3.connect('data/database/db/mydb.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

def list_mobs(show_hidden=False):
    """List all named mobs with their visibility status."""
    conn = connect_db()
    cursor = conn.cursor()
    
    where_clause = "" if show_hidden else "WHERE is_hidden = 0"
    cursor.execute(f"""
        SELECT nm.id, nm.name, nm.level, nm.is_hidden,
               COUNT(nmi.id) as item_count
        FROM named_mobs nm
        LEFT JOIN named_mob_items nmi ON nm.id = nmi.named_mob_id
        {where_clause}
        GROUP BY nm.id, nm.name, nm.level, nm.is_hidden
        ORDER BY nm.is_hidden, nm.name
    """)
    
    visible_count = 0
    hidden_count = 0
    
    print("Named Mobs Status:")
    print("=" * 70)
    print(f"{'ID':>3} | {'Name':30} | {'Lvl':3} | {'Items':5} | {'Status':6}")
    print("-" * 70)
    
    for row in cursor.fetchall():
        status = "HIDDEN" if row['is_hidden'] else "SHOWN"
        status_icon = "❌" if row['is_hidden'] else "✅"
        
        print(f"{row['id']:3d} | {row['name']:30} | {row['level'] or '?':3} | {row['item_count']:5d} | {status_icon} {status}")
        
        if row['is_hidden']:
            hidden_count += 1
        else:
            visible_count += 1
    
    print("-" * 70)
    print(f"Total: {visible_count} shown, {hidden_count} hidden")
    
    conn.close()

def hide_mob(mob_identifier):
    """Hide a named mob by ID or name."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Try by ID first, then by name
    if mob_identifier.isdigit():
        cursor.execute("SELECT name FROM named_mobs WHERE id = ?", (int(mob_identifier),))
    else:
        cursor.execute("SELECT name FROM named_mobs WHERE name LIKE ?", (f"%{mob_identifier}%",))
    
    result = cursor.fetchone()
    if not result:
        print(f"❌ Mob '{mob_identifier}' not found")
        conn.close()
        return False
        
    mob_name = result['name']
    
    # Update visibility
    if mob_identifier.isdigit():
        cursor.execute("UPDATE named_mobs SET is_hidden = 1 WHERE id = ?", (int(mob_identifier),))
    else:
        cursor.execute("UPDATE named_mobs SET is_hidden = 1 WHERE name = ?", (mob_name,))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Hidden: {mob_name}")
    return True

def show_mob(mob_identifier):
    """Show a named mob by ID or name."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Try by ID first, then by name
    if mob_identifier.isdigit():
        cursor.execute("SELECT name FROM named_mobs WHERE id = ?", (int(mob_identifier),))
    else:
        cursor.execute("SELECT name FROM named_mobs WHERE name LIKE ?", (f"%{mob_identifier}%",))
    
    result = cursor.fetchone()
    if not result:
        print(f"❌ Mob '{mob_identifier}' not found")
        conn.close()
        return False
        
    mob_name = result['name']
    
    # Update visibility
    if mob_identifier.isdigit():
        cursor.execute("UPDATE named_mobs SET is_hidden = 0 WHERE id = ?", (int(mob_identifier),))
    else:
        cursor.execute("UPDATE named_mobs SET is_hidden = 0 WHERE name = ?", (mob_name,))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Shown: {mob_name}")
    return True

def hide_mobs_without_items():
    """Hide all mobs that don't have special items."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE named_mobs 
        SET is_hidden = 1 
        WHERE id NOT IN (
            SELECT DISTINCT named_mob_id 
            FROM named_mob_items
        )
        AND is_hidden = 0
    """)
    
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    print(f"✅ Hidden {affected} mobs without special items")
    return affected

def show_mobs_with_items():
    """Show all mobs that have special items."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE named_mobs 
        SET is_hidden = 0 
        WHERE id IN (
            SELECT DISTINCT named_mob_id 
            FROM named_mob_items
        )
        AND is_hidden = 1
    """)
    
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    print(f"✅ Shown {affected} mobs with special items")
    return affected

def main():
    parser = argparse.ArgumentParser(description='Manage Named Mob Visibility')
    parser.add_argument('action', choices=['list', 'hide', 'show', 'hide-no-items', 'show-with-items'],
                       help='Action to perform')
    parser.add_argument('target', nargs='?', help='Mob ID or name (for hide/show actions)')
    parser.add_argument('--include-hidden', action='store_true',
                       help='Include hidden mobs in list')
    
    args = parser.parse_args()
    
    if args.action == 'list':
        list_mobs(show_hidden=args.include_hidden)
    elif args.action == 'hide':
        if not args.target:
            print("❌ Please specify mob ID or name to hide")
            sys.exit(1)
        hide_mob(args.target)
    elif args.action == 'show':
        if not args.target:
            print("❌ Please specify mob ID or name to show")
            sys.exit(1)
        show_mob(args.target)
    elif args.action == 'hide-no-items':
        hide_mobs_without_items()
    elif args.action == 'show-with-items':
        show_mobs_with_items()

if __name__ == "__main__":
    main()
