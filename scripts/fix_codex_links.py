#!/usr/bin/env python3
"""
Correction des liens Ashes Codex dans la base de données
Conversion de /mobs/ vers /db/mob/ et ajout des drops spéciaux
"""

import sqlite3
import json

# Mapping des named mobs avec leurs drops spéciaux (exemples connus)
SPECIAL_DROPS = {
    'chief-armorer-jannus': {
        'drops': [
            {
                'name': 'Buttressed Shield',
                'url': 'https://ashescodex.com/db/item/Gear_Weapon_Shield_OH_Jannus',
                'rarity': 'Uncommon',
                'type': 'Shield'
            }
        ]
    },
    'wormwig': {
        'drops': [
            {
                'name': 'Wormwig Trinket',
                'url': 'https://ashescodex.com/db/item/wormwig-trinket',
                'rarity': 'Rare',
                'type': 'Accessory'
            }
        ]
    },
    # Ajouter d'autres named mobs avec leurs drops spéciaux
}

def fix_codex_links(db_path):
    """Corrige les liens codex dans la base de données"""
    print("🔧 Correction des liens Ashes Codex...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Ajouter la colonne special_drops si elle n'existe pas
    try:
        cursor.execute("ALTER TABLE named_mobs ADD COLUMN special_drops TEXT")
        print("✅ Colonne special_drops ajoutée")
    except sqlite3.OperationalError:
        print("ℹ️  Colonne special_drops existe déjà")
    
    # Corriger les URLs codex
    cursor.execute("SELECT id, slug, codex_url FROM named_mobs WHERE codex_url LIKE '%/mobs/%'")
    mobs_to_fix = cursor.fetchall()
    
    fixed_count = 0
    for mob_id, slug, old_url in mobs_to_fix:
        # Convertir /mobs/ vers /db/mob/
        new_url = old_url.replace('/mobs/', '/db/mob/')
        
        # Ajouter les drops spéciaux si disponibles
        special_drops_json = None
        if slug in SPECIAL_DROPS:
            special_drops_json = json.dumps(SPECIAL_DROPS[slug])
        
        # Mettre à jour la base de données
        if special_drops_json:
            cursor.execute("""
                UPDATE named_mobs 
                SET codex_url = ?, special_drops = ?
                WHERE id = ?
            """, (new_url, special_drops_json, mob_id))
        else:
            cursor.execute("""
                UPDATE named_mobs 
                SET codex_url = ?
                WHERE id = ?
            """, (new_url, mob_id))
        
        fixed_count += 1
        if fixed_count <= 5:  # Afficher les 5 premiers
            print(f"✅ {slug}: {old_url} → {new_url}")
    
    conn.commit()
    conn.close()
    
    print(f"\n🎯 Corrigé {fixed_count} liens codex")
    return fixed_count

def main():
    db_path = 'data/database/db/mydb.sqlite'
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    print("🔗 Correction des liens Ashes Codex")
    print("=" * 40)
    
    fixed_count = fix_codex_links(db_path)
    
    print(f"\n✅ Correction terminée : {fixed_count} liens mis à jour")
    print("💡 Redémarrez l'application pour voir les changements")

if __name__ == "__main__":
    import os
    main()
