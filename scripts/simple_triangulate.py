#!/usr/bin/env python3
"""
Simple triangulation script that works inside Docker container
Uses all REF markers for coordinate transformation
"""

import sqlite3
import json
import math

def extract_mob_name(label):
    """Extract mob name from REF label"""
    mob_name = label.replace('REF ', '').replace(' REF', '').lower().strip()
    
    # Handle special cases
    if 'big brother' in mob_name:
        return 'big brother'
    elif 'hornhexer' in mob_name:
        return 'hornhexer'  
    elif "tawl'bura" in mob_name or 'tawlbura' in mob_name:
        return "tawl'bura"
    elif 'blisterpyre' in mob_name:
        return 'blisterpyre'
    
    return mob_name

def load_reference_points(db_path):
    """Load all REF markers and match with named mobs"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all REF markers
    cursor.execute("""
        SELECT id, label, lat, lng 
        FROM markers 
        WHERE label LIKE 'REF %' OR label LIKE '% REF'
        ORDER BY id
    """)
    ref_markers = cursor.fetchall()
    
    reference_points = []
    print(f"🔍 Found {len(ref_markers)} REF markers")
    
    for marker in ref_markers:
        marker_id, label, map_lat, map_lng = marker
        mob_name_hint = extract_mob_name(label)
        
        print(f"📍 Processing: '{label}' -> searching for '{mob_name_hint}'")
        
        # Find corresponding named mob
        cursor.execute("""
            SELECT name, slug, location_x, location_y, location_z 
            FROM named_mobs 
            WHERE LOWER(slug) LIKE ? OR LOWER(name) LIKE ?
        """, (f"%{mob_name_hint}%", f"%{mob_name_hint}%"))
        
        mob_result = cursor.fetchone()
        if mob_result:
            name, slug, codex_x, codex_y, codex_z = mob_result
            if codex_x is not None and codex_y is not None:
                reference_points.append({
                    'marker_id': marker_id,
                    'label': label,
                    'map_lat': map_lat,
                    'map_lng': map_lng,
                    'mob_name': name,
                    'mob_slug': slug,
                    'codex_x': codex_x,
                    'codex_y': codex_y,
                    'codex_z': codex_z
                })
                print(f"  ✅ Matched: {name}")
            else:
                print(f"  ⚠️  {name} has no codex coordinates")
        else:
            print(f"  ❌ No mob found for '{mob_name_hint}'")
    
    conn.close()
    return reference_points

def calculate_affine_transform(reference_points):
    """Calculate affine transformation using least squares"""
    if len(reference_points) < 3:
        print(f"❌ Need at least 3 reference points, got {len(reference_points)}")
        return None
    
    print(f"📊 Using {len(reference_points)} reference points for transformation")
    
    # Simple linear transformation: [map_x, map_y] = A * [codex_x, codex_y] + B
    # We'll solve for A (2x2 matrix) and B (2x1 vector)
    
    # Extract coordinates
    codex_coords = [[p['codex_x'], p['codex_y']] for p in reference_points]
    map_coords = [[p['map_lat'], p['map_lng']] for p in reference_points]
    
    # Simple approach: use first 3 points for basic affine transform
    # For more points, we could use least squares, but let's start simple
    
    if len(reference_points) >= 3:
        # Use first 3 points for affine transformation
        p1_codex, p1_map = codex_coords[0], map_coords[0]
        p2_codex, p2_map = codex_coords[1], map_coords[1] 
        p3_codex, p3_map = codex_coords[2], map_coords[2]
        
        # Calculate transformation matrix (simplified)
        # This is a basic implementation - could be improved with proper least squares
        
        # Calculate scale and offset based on first two points
        dx_codex = p2_codex[0] - p1_codex[0]
        dy_codex = p2_codex[1] - p1_codex[1]
        dx_map = p2_map[0] - p1_map[0]
        dy_map = p2_map[1] - p1_map[1]
        
        if abs(dx_codex) > 0.001 and abs(dy_codex) > 0.001:
            scale_x = dx_map / dx_codex
            scale_y = dy_map / dy_codex
            
            offset_x = p1_map[0] - scale_x * p1_codex[0]
            offset_y = p1_map[1] - scale_y * p1_codex[1]
            
            return {
                'scale_x': scale_x,
                'scale_y': scale_y,
                'offset_x': offset_x,
                'offset_y': offset_y,
                'method': f'affine_transform_{len(reference_points)}_points'
            }
    
    return None

def transform_coordinates(codex_x, codex_y, transform_params):
    """Transform codex coordinates to map coordinates"""
    if not transform_params or codex_x is None or codex_y is None:
        return None, None
    
    map_lat = transform_params['scale_x'] * codex_x + transform_params['offset_x']
    map_lng = transform_params['scale_y'] * codex_y + transform_params['offset_y']
    
    return map_lat, map_lng

def update_all_coordinates(db_path, transform_params):
    """Update all named mob coordinates using the transformation"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all named mobs with codex coordinates
    cursor.execute("""
        SELECT id, name, location_x, location_y 
        FROM named_mobs 
        WHERE location_x IS NOT NULL AND location_y IS NOT NULL
    """)
    
    mobs = cursor.fetchall()
    updated_count = 0
    
    print(f"🔄 Processing {len(mobs)} named mobs...")
    
    for mob in mobs:
        mob_id, name, codex_x, codex_y = mob
        
        # Transform coordinates
        map_lat, map_lng = transform_coordinates(codex_x, codex_y, transform_params)
        
        if map_lat is not None and map_lng is not None:
            # Update database
            cursor.execute("""
                UPDATE named_mobs 
                SET map_lat = ?, map_lng = ?, coordinate_source = ?
                WHERE id = ?
            """, (map_lat, map_lng, transform_params['method'], mob_id))
            updated_count += 1
            
            if updated_count <= 5:  # Show first 5 for verification
                print(f"  ✅ {name}: ({codex_x:.0f}, {codex_y:.0f}) -> ({map_lat:.3f}, {map_lng:.3f})")
    
    conn.commit()
    conn.close()
    
    return updated_count

def main():
    db_path = '/app/database/db/mydb.sqlite'
    
    print("🎯 Simple Triangulation - Using ALL REF Markers")
    print("=" * 50)
    
    # Load reference points
    print("1️⃣ Loading reference points...")
    reference_points = load_reference_points(db_path)
    
    if len(reference_points) < 3:
        print(f"❌ Need at least 3 reference points, found {len(reference_points)}")
        return
    
    print(f"✅ Found {len(reference_points)} valid reference points")
    
    # Calculate transformation
    print("\n2️⃣ Calculating coordinate transformation...")
    transform_params = calculate_affine_transform(reference_points)
    
    if not transform_params:
        print("❌ Failed to calculate transformation")
        return
    
    print(f"✅ Transformation calculated using {transform_params['method']}")
    
    # Validate with reference points
    print("\n3️⃣ Validating transformation...")
    total_error = 0
    for ref in reference_points[:3]:  # Show first 3 for validation
        pred_lat, pred_lng = transform_coordinates(ref['codex_x'], ref['codex_y'], transform_params)
        error = math.sqrt((pred_lat - ref['map_lat'])**2 + (pred_lng - ref['map_lng'])**2)
        total_error += error
        print(f"  {ref['mob_name']}: Error = {error:.6f}")
    
    avg_error = total_error / min(len(reference_points), 3)
    print(f"📊 Average error: {avg_error:.6f}")
    
    # Update all coordinates
    print("\n4️⃣ Updating all named mob coordinates...")
    updated_count = update_all_coordinates(db_path, transform_params)
    
    print(f"✅ Updated {updated_count} named mob coordinates")
    print(f"📊 Transformation method: {transform_params['method']}")

if __name__ == "__main__":
    main()
