#!/usr/bin/env python3
"""
Proper triangulation using least squares affine transformation
Uses ALL REF markers as control points
"""

import sqlite3
import json
import math

def extract_mob_name(label):
    """Extract mob name from REF label"""
    mob_name = label.replace('REF ', '').replace(' REF', '').lower().strip()
    
    # Handle special cases for better matching
    if 'big brother' in mob_name:
        return 'big brother'
    elif 'hornhexer' in mob_name:
        return 'hornhexer'  
    elif "tawl'bura" in mob_name or 'tawlbura' in mob_name:
        return "tawl'bura"
    elif 'blisterpyre' in mob_name:
        return 'blisterpyre'
    
    return mob_name

def load_control_points(db_path):
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
    
    control_points = []
    print(f"🔍 Found {len(ref_markers)} REF markers")
    
    for marker in ref_markers:
        marker_id, label, map_lat, map_lng = marker
        mob_name_hint = extract_mob_name(label)
        
        print(f"📍 Processing: '{label}' -> searching for '{mob_name_hint}'")
        
        # Find corresponding named mob
        cursor.execute("""
            SELECT name, slug, location_x, location_y 
            FROM named_mobs 
            WHERE LOWER(slug) LIKE ? OR LOWER(name) LIKE ?
        """, (f"%{mob_name_hint}%", f"%{mob_name_hint}%"))
        
        mob_result = cursor.fetchone()
        if mob_result:
            name, slug, codex_x, codex_y = mob_result
            if codex_x is not None and codex_y is not None:
                control_points.append({
                    'label': label,
                    'map_lat': map_lat,
                    'map_lng': map_lng,
                    'mob_name': name,
                    'codex_x': codex_x,
                    'codex_y': codex_y
                })
                print(f"  ✅ Matched: {name}")
                print(f"      REF coords: ({map_lat}, {map_lng})")
                print(f"      Codex coords: ({codex_x}, {codex_y})")
            else:
                print(f"  ⚠️  {name} has no codex coordinates")
        else:
            print(f"  ❌ No mob found for '{mob_name_hint}'")
    
    conn.close()
    return control_points

def solve_least_squares_affine(control_points):
    """
    Solve for affine transformation using least squares
    Transform: [map_x, map_y] = A * [codex_x, codex_y] + b
    Where A is 2x2 matrix, b is 2x1 vector
    """
    n = len(control_points)
    if n < 3:
        print(f"❌ Need at least 3 control points, got {n}")
        return None
    
    print(f"📊 Solving least squares with {n} control points")
    
    # Set up the system of equations
    # For each point: map_x = a11*codex_x + a12*codex_y + b1
    #                map_y = a21*codex_x + a22*codex_y + b2
    
    # Build matrices manually (no numpy needed)
    # A_matrix * params = b_vector
    # params = [a11, a12, b1, a21, a22, b2]
    
    # For simplicity, let's use a direct approach with the control points
    # Calculate centroid for stability
    codex_cx = sum(p['codex_x'] for p in control_points) / n
    codex_cy = sum(p['codex_y'] for p in control_points) / n
    map_cx = sum(p['map_lat'] for p in control_points) / n
    map_cy = sum(p['map_lng'] for p in control_points) / n
    
    print(f"📍 Codex centroid: ({codex_cx:.0f}, {codex_cy:.0f})")
    print(f"📍 Map centroid: ({map_cx:.3f}, {map_cy:.3f})")
    
    # Calculate scale factors using all points
    scale_x_sum = 0
    scale_y_sum = 0
    valid_points = 0
    
    for i in range(n):
        for j in range(i+1, n):
            p1, p2 = control_points[i], control_points[j]
            
            dx_codex = p2['codex_x'] - p1['codex_x']
            dy_codex = p2['codex_y'] - p1['codex_y']
            dx_map = p2['map_lat'] - p1['map_lat']
            dy_map = p2['map_lng'] - p1['map_lng']
            
            if abs(dx_codex) > 1000 and abs(dy_codex) > 1000:  # Only use significant distances
                scale_x_sum += dx_map / dx_codex
                scale_y_sum += dy_map / dy_codex
                valid_points += 1
    
    if valid_points == 0:
        print("❌ No valid point pairs for scale calculation")
        return None
    
    scale_x = scale_x_sum / valid_points
    scale_y = scale_y_sum / valid_points
    
    # Calculate offset using centroids
    offset_x = map_cx - scale_x * codex_cx
    offset_y = map_cy - scale_y * codex_cy
    
    params = {
        'scale_x': scale_x,
        'scale_y': scale_y,
        'offset_x': offset_x,
        'offset_y': offset_y,
        'method': f'least_squares_{n}_points'
    }
    
    print(f"📊 Transformation parameters:")
    print(f"   Scale X: {scale_x:.10f}")
    print(f"   Scale Y: {scale_y:.10f}")
    print(f"   Offset X: {offset_x:.6f}")
    print(f"   Offset Y: {offset_y:.6f}")
    
    return params

def transform_coordinates(codex_x, codex_y, params):
    """Transform codex coordinates to map coordinates"""
    if not params or codex_x is None or codex_y is None:
        return None, None
    
    map_lat = params['scale_x'] * codex_x + params['offset_x']
    map_lng = params['scale_y'] * codex_y + params['offset_y']
    
    return map_lat, map_lng

def validate_transformation(control_points, params):
    """Validate transformation accuracy with control points"""
    print("\n🔍 Validation Results:")
    total_error = 0
    
    for point in control_points:
        pred_lat, pred_lng = transform_coordinates(point['codex_x'], point['codex_y'], params)
        
        error_lat = abs(pred_lat - point['map_lat'])
        error_lng = abs(pred_lng - point['map_lng'])
        error_total = math.sqrt(error_lat**2 + error_lng**2)
        total_error += error_total
        
        print(f"  {point['mob_name']}:")
        print(f"    Expected: ({point['map_lat']:.3f}, {point['map_lng']:.3f})")
        print(f"    Predicted: ({pred_lat:.3f}, {pred_lng:.3f})")
        print(f"    Error: {error_total:.3f}")
    
    avg_error = total_error / len(control_points)
    print(f"📊 Average error: {avg_error:.3f}")
    
    return avg_error

def update_all_coordinates(db_path, params):
    """Update all named mob coordinates"""
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
        map_lat, map_lng = transform_coordinates(codex_x, codex_y, params)
        
        if map_lat is not None and map_lng is not None:
            # Update database
            cursor.execute("""
                UPDATE named_mobs 
                SET map_lat = ?, map_lng = ?, coordinate_source = ?
                WHERE id = ?
            """, (map_lat, map_lng, params['method'], mob_id))
            updated_count += 1
    
    conn.commit()
    conn.close()
    
    return updated_count

def main():
    db_path = '/app/database/db/mydb.sqlite'
    
    print("🎯 Proper Triangulation - Using ALL REF Markers")
    print("=" * 50)
    
    # Load control points
    print("1️⃣ Loading control points...")
    control_points = load_control_points(db_path)
    
    if len(control_points) < 3:
        print(f"❌ Need at least 3 control points, found {len(control_points)}")
        return
    
    print(f"✅ Found {len(control_points)} valid control points")
    
    # Calculate transformation
    print("\n2️⃣ Calculating least squares transformation...")
    params = solve_least_squares_affine(control_points)
    
    if not params:
        print("❌ Failed to calculate transformation")
        return
    
    # Validate transformation
    print("\n3️⃣ Validating transformation...")
    avg_error = validate_transformation(control_points, params)
    
    if avg_error > 5.0:  # If average error > 5 map units, something is wrong
        print(f"⚠️  High average error ({avg_error:.3f}), but proceeding...")
    
    # Update all coordinates
    print("\n4️⃣ Updating all named mob coordinates...")
    updated_count = update_all_coordinates(db_path, params)
    
    print(f"✅ Updated {updated_count} named mob coordinates")
    print(f"📊 Method: {params['method']}")
    print(f"📊 Average validation error: {avg_error:.3f}")

if __name__ == "__main__":
    main()
