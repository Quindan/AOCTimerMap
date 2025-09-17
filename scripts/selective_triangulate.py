#!/usr/bin/env python3
"""
Selective triangulation - use only the best reference points
Focus on accuracy over quantity
"""

import sqlite3
import math

def main():
    db_path = '/app/database/db/mydb.sqlite'
    
    print("🎯 Selective Triangulation - Best Reference Points Only")
    print("=" * 55)
    
    # Use only the 3 most reliable reference points
    # Based on your feedback: Ysshokk and Wormwig are correctly placed
    reliable_refs = [
        {'name': 'Wormwig', 'map_lat': -235.619140625, 'map_lng': 137.396484375},
        {'name': 'Ysshokk', 'map_lat': -239.0, 'map_lng': 144.375},
        {'name': 'Olive Bootshredder', 'map_lat': -246.837890625, 'map_lng': 110.33203125}
    ]
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get codex coordinates for these mobs
    control_points = []
    for ref in reliable_refs:
        cursor.execute("SELECT location_x, location_y FROM named_mobs WHERE name = ?", (ref['name'],))
        result = cursor.fetchone()
        if result and result[0] is not None:
            control_points.append({
                'name': ref['name'],
                'map_lat': ref['map_lat'],
                'map_lng': ref['map_lng'],
                'codex_x': result[0],
                'codex_y': result[1]
            })
            print(f"✅ {ref['name']}: Map({ref['map_lat']:.3f}, {ref['map_lng']:.3f}) Codex({result[0]:.0f}, {result[1]:.0f})")
    
    if len(control_points) != 3:
        print(f"❌ Expected 3 control points, got {len(control_points)}")
        return
    
    # Calculate transformation using 3-point method
    print("\n📊 Calculating 3-point transformation...")
    
    # Use the first two points to calculate scale and rotation
    p1, p2, p3 = control_points[0], control_points[1], control_points[2]
    
    # Vector from p1 to p2 in both coordinate systems
    codex_vec = (p2['codex_x'] - p1['codex_x'], p2['codex_y'] - p1['codex_y'])
    map_vec = (p2['map_lat'] - p1['map_lat'], p2['map_lng'] - p1['map_lng'])
    
    # Calculate scale
    codex_dist = math.sqrt(codex_vec[0]**2 + codex_vec[1]**2)
    map_dist = math.sqrt(map_vec[0]**2 + map_vec[1]**2)
    scale = map_dist / codex_dist if codex_dist > 0 else 0
    
    # Calculate rotation angle
    codex_angle = math.atan2(codex_vec[1], codex_vec[0])
    map_angle = math.atan2(map_vec[1], map_vec[0])
    rotation = map_angle - codex_angle
    
    print(f"📊 Scale factor: {scale:.10f}")
    print(f"📊 Rotation: {math.degrees(rotation):.3f}°")
    
    # Calculate transformation matrix
    cos_r = math.cos(rotation)
    sin_r = math.sin(rotation)
    
    # Transform matrix: [map_x, map_y] = scale * R * [codex_x, codex_y] + offset
    # Where R is rotation matrix
    a11 = scale * cos_r
    a12 = -scale * sin_r  
    a21 = scale * sin_r
    a22 = scale * cos_r
    
    # Calculate offset using first point
    offset_x = p1['map_lat'] - (a11 * p1['codex_x'] + a12 * p1['codex_y'])
    offset_y = p1['map_lng'] - (a21 * p1['codex_x'] + a22 * p1['codex_y'])
    
    params = {
        'a11': a11, 'a12': a12, 'offset_x': offset_x,
        'a21': a21, 'a22': a22, 'offset_y': offset_y,
        'method': 'affine_3_point_selective'
    }
    
    print(f"📊 Transformation matrix:")
    print(f"   [{a11:.10f}  {a12:.10f}] [codex_x]   [{offset_x:.6f}]")
    print(f"   [{a21:.10f}  {a22:.10f}] [codex_y] + [{offset_y:.6f}]")
    
    # Validate with all 3 points
    print("\n🔍 Validation:")
    total_error = 0
    for point in control_points:
        pred_lat = params['a11'] * point['codex_x'] + params['a12'] * point['codex_y'] + params['offset_x']
        pred_lng = params['a21'] * point['codex_x'] + params['a22'] * point['codex_y'] + params['offset_y']
        
        error = math.sqrt((pred_lat - point['map_lat'])**2 + (pred_lng - point['map_lng'])**2)
        total_error += error
        
        print(f"  {point['name']}: Error = {error:.6f}")
    
    avg_error = total_error / 3
    print(f"📊 Average error: {avg_error:.6f}")
    
    if avg_error > 1.0:
        print("⚠️  High error - check reference points")
        return
    
    # Update all coordinates
    print("\n4️⃣ Updating all named mob coordinates...")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, location_x, location_y FROM named_mobs WHERE location_x IS NOT NULL AND location_y IS NOT NULL")
    mobs = cursor.fetchall()
    
    updated_count = 0
    for mob in mobs:
        mob_id, name, codex_x, codex_y = mob
        
        map_lat = params['a11'] * codex_x + params['a12'] * codex_y + params['offset_x']
        map_lng = params['a21'] * codex_x + params['a22'] * codex_y + params['offset_y']
        
        cursor.execute("""
            UPDATE named_mobs 
            SET map_lat = ?, map_lng = ?, coordinate_source = ?
            WHERE id = ?
        """, (map_lat, map_lng, params['method'], mob_id))
        updated_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ Updated {updated_count} named mobs")

if __name__ == "__main__":
    main()
