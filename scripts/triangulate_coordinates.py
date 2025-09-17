#!/usr/bin/env python3
"""
Named Mob Coordinate Triangulation Script
Uses 3 reference points to recalculate all named mob positions on the interactive map.
"""

import sqlite3
import json
import sys
import os
from typing import List, Tuple, Dict, Any
import numpy as np
from scipy.optimize import minimize
import math

class CoordinateTriangulator:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.reference_points = []
        
    def load_reference_points(self) -> List[Dict[str, Any]]:
        """Load the 3 reference markers and their corresponding named mobs."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get reference markers
        cursor.execute("""
            SELECT id, label, lat, lng, type, rarity 
            FROM markers 
            WHERE label LIKE 'REF %' 
            ORDER BY id
        """)
        ref_markers = cursor.fetchall()
        
        # Get corresponding named mobs
        reference_points = []
        for marker in ref_markers:
            marker_id, label, map_lat, map_lng, marker_type, rarity = marker
            
            # Extract named mob name from label (e.g., "REF worwig" -> "wormwig")
            mob_name_hint = label.replace('REF ', '').lower().strip()
            
            # Find corresponding named mob
            cursor.execute("""
                SELECT name, slug, location_x, location_y, location_z 
                FROM named_mobs 
                WHERE LOWER(slug) LIKE ? OR LOWER(name) LIKE ?
            """, (f"%{mob_name_hint}%", f"%{mob_name_hint}%"))
            
            mob_result = cursor.fetchone()
            if mob_result:
                name, slug, codex_x, codex_y, codex_z = mob_result
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
                print(f"✅ Found reference: {label} -> {name}")
                print(f"   Map coords: ({map_lat}, {map_lng})")
                print(f"   Codex coords: ({codex_x}, {codex_y})")
            else:
                print(f"❌ Could not find named mob for: {label}")
        
        conn.close()
        self.reference_points = reference_points
        return reference_points
    
    def calculate_transformation_matrix(self) -> Dict[str, float]:
        """Calculate transformation parameters using least squares method with 3+ points."""
        if len(self.reference_points) < 2:
            raise ValueError("Need at least 2 reference points for transformation")
        
        # Prepare data for transformation calculation
        codex_points = np.array([[p['codex_x'], p['codex_y']] for p in self.reference_points])
        map_points = np.array([[p['map_lng'], p['map_lat']] for p in self.reference_points])  # Note: lng=x, lat=y
        
        if len(self.reference_points) == 2:
            # Linear transformation with 2 points
            return self._calculate_2point_transformation(codex_points, map_points)
        else:
            # Least squares transformation with 3+ points
            return self._calculate_least_squares_transformation(codex_points, map_points)
    
    def _calculate_2point_transformation(self, codex_points: np.ndarray, map_points: np.ndarray) -> Dict[str, float]:
        """Calculate transformation using 2 reference points (original method)."""
        # Reference point 1
        ref1_codex_x, ref1_codex_y = codex_points[0]
        ref1_map_lng, ref1_map_lat = map_points[0]
        
        # Reference point 2  
        ref2_codex_x, ref2_codex_y = codex_points[1]
        ref2_map_lng, ref2_map_lat = map_points[1]
        
        # Calculate scale factors
        delta_lng = ref2_map_lng - ref1_map_lng
        delta_codex_x = ref2_codex_x - ref1_codex_x
        scale_x = delta_lng / delta_codex_x if delta_codex_x != 0 else 0
        
        delta_lat = ref2_map_lat - ref1_map_lat
        delta_codex_y = ref2_codex_y - ref1_codex_y
        scale_y = delta_lat / delta_codex_y if delta_codex_y != 0 else 0
        
        # Calculate offset using reference point 1
        offset_lng = ref1_map_lng - (ref1_codex_x * scale_x)
        offset_lat = ref1_map_lat - (ref1_codex_y * scale_y)
        
        return {
            'scale_x': scale_x,
            'scale_y': scale_y,
            'offset_x': offset_lng,
            'offset_y': offset_lat,
            'method': '2-point linear',
            'rmse': 0.0  # Perfect fit with 2 points
        }
    
    def _calculate_least_squares_transformation(self, codex_points: np.ndarray, map_points: np.ndarray) -> Dict[str, float]:
        """Calculate affine transformation using least squares method."""
        n = len(codex_points)
        
        # Set up the system of equations for affine transformation
        # [lng]   [a b tx] [x]
        # [lat] = [c d ty] [y]
        # [1  ]   [0 0 1 ] [1]
        
        # Create coefficient matrix A and target vector b
        A = np.zeros((2 * n, 6))
        b = np.zeros(2 * n)
        
        for i in range(n):
            x, y = codex_points[i]
            lng, lat = map_points[i]
            
            # For longitude equation: lng = a*x + b*y + tx
            A[2*i] = [x, y, 1, 0, 0, 0]
            b[2*i] = lng
            
            # For latitude equation: lat = c*x + d*y + ty
            A[2*i + 1] = [0, 0, 0, x, y, 1]
            b[2*i + 1] = lat
        
        # Solve least squares
        params, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
        a, b_coeff, tx, c, d, ty = params
        
        # Calculate RMSE
        predicted = A @ params
        rmse = np.sqrt(np.mean((b - predicted) ** 2))
        
        return {
            'a': a,           # x coefficient for longitude
            'b': b_coeff,     # y coefficient for longitude  
            'c': c,           # x coefficient for latitude
            'd': d,           # y coefficient for latitude
            'tx': tx,         # x translation (longitude offset)
            'ty': ty,         # y translation (latitude offset)
            'method': 'least squares affine',
            'rmse': rmse
        }
    
    def transform_coordinates(self, codex_x: float, codex_y: float, transform_params: Dict[str, float]) -> Tuple[float, float]:
        """Transform codex coordinates to map coordinates."""
        if transform_params['method'] == '2-point linear':
            # Simple linear transformation
            map_lng = (codex_x * transform_params['scale_x']) + transform_params['offset_x']
            map_lat = (codex_y * transform_params['scale_y']) + transform_params['offset_y']
        else:
            # Affine transformation
            map_lng = transform_params['a'] * codex_x + transform_params['b'] * codex_y + transform_params['tx']
            map_lat = transform_params['c'] * codex_x + transform_params['d'] * codex_y + transform_params['ty']
        
        return map_lat, map_lng
    
    def add_map_coordinate_columns(self):
        """Add map coordinate columns to the named_mobs table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(named_mobs)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'map_lat' not in columns:
            cursor.execute("ALTER TABLE named_mobs ADD COLUMN map_lat REAL")
            print("✅ Added map_lat column")
        
        if 'map_lng' not in columns:
            cursor.execute("ALTER TABLE named_mobs ADD COLUMN map_lng REAL")
            print("✅ Added map_lng column")
        
        if 'coordinate_source' not in columns:
            cursor.execute("ALTER TABLE named_mobs ADD COLUMN coordinate_source TEXT DEFAULT 'triangulated'")
            print("✅ Added coordinate_source column")
        
        conn.commit()
        conn.close()
    
    def update_all_coordinates(self, transform_params: Dict[str, float]):
        """Update all named mob coordinates using the transformation."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all named mobs with codex coordinates
        cursor.execute("""
            SELECT id, name, slug, location_x, location_y 
            FROM named_mobs 
            WHERE location_x IS NOT NULL AND location_y IS NOT NULL
        """)
        
        mobs = cursor.fetchall()
        updated_count = 0
        
        for mob_id, name, slug, codex_x, codex_y in mobs:
            # Transform coordinates
            map_lat, map_lng = self.transform_coordinates(codex_x, codex_y, transform_params)
            
            # Update database
            cursor.execute("""
                UPDATE named_mobs 
                SET map_lat = ?, map_lng = ?, coordinate_source = ? 
                WHERE id = ?
            """, (map_lat, map_lng, transform_params['method'], mob_id))
            
            updated_count += 1
            
            if updated_count <= 5:  # Show first 5 examples
                print(f"✅ {name}: ({codex_x:.0f}, {codex_y:.0f}) -> ({map_lat:.6f}, {map_lng:.6f})")
        
        conn.commit()
        conn.close()
        
        print(f"\n🎯 Updated coordinates for {updated_count} named mobs")
        return updated_count
    
    def validate_transformation(self, transform_params: Dict[str, float]):
        """Validate the transformation using reference points."""
        print(f"\n🔍 Validation using {transform_params['method']}:")
        print(f"RMSE: {transform_params['rmse']:.6f}")
        
        total_error = 0
        for ref in self.reference_points:
            predicted_lat, predicted_lng = self.transform_coordinates(
                ref['codex_x'], ref['codex_y'], transform_params
            )
            
            error_lat = abs(predicted_lat - ref['map_lat'])
            error_lng = abs(predicted_lng - ref['map_lng'])
            total_error += math.sqrt(error_lat**2 + error_lng**2)
            
            print(f"  {ref['mob_name']}:")
            print(f"    Expected: ({ref['map_lat']:.6f}, {ref['map_lng']:.6f})")
            print(f"    Predicted: ({predicted_lat:.6f}, {predicted_lng:.6f})")
            print(f"    Error: {math.sqrt(error_lat**2 + error_lng**2):.6f}")
        
        avg_error = total_error / len(self.reference_points)
        print(f"  Average Error: {avg_error:.6f}")
        
        return avg_error
    
    def export_transformation_report(self, transform_params: Dict[str, float], output_file: str):
        """Export a detailed report of the transformation."""
        report = {
            'timestamp': '2025-01-17',
            'method': transform_params['method'],
            'reference_points': self.reference_points,
            'transformation_parameters': transform_params,
            'validation_results': []
        }
        
        # Add validation for each reference point
        for ref in self.reference_points:
            predicted_lat, predicted_lng = self.transform_coordinates(
                ref['codex_x'], ref['codex_y'], transform_params
            )
            
            error_lat = abs(predicted_lat - ref['map_lat'])
            error_lng = abs(predicted_lng - ref['map_lng'])
            
            report['validation_results'].append({
                'mob_name': ref['mob_name'],
                'expected_lat': ref['map_lat'],
                'expected_lng': ref['map_lng'],
                'predicted_lat': predicted_lat,
                'predicted_lng': predicted_lng,
                'error_lat': error_lat,
                'error_lng': error_lng,
                'total_error': math.sqrt(error_lat**2 + error_lng**2)
            })
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Transformation report saved to: {output_file}")

def main():
    db_path = 'db/mydb.sqlite'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        sys.exit(1)
    
    print("🎯 Named Mob Coordinate Triangulation")
    print("=" * 50)
    
    triangulator = CoordinateTriangulator(db_path)
    
    # Step 1: Load reference points
    print("\n1️⃣ Loading reference points...")
    ref_points = triangulator.load_reference_points()
    
    if len(ref_points) < 2:
        print("❌ Need at least 2 reference points. Please place reference markers first.")
        sys.exit(1)
    
    print(f"✅ Found {len(ref_points)} reference points")
    
    # Step 2: Calculate transformation
    print("\n2️⃣ Calculating coordinate transformation...")
    transform_params = triangulator.calculate_transformation_matrix()
    print(f"✅ Using {transform_params['method']} transformation")
    
    # Step 3: Validate transformation
    print("\n3️⃣ Validating transformation...")
    avg_error = triangulator.validate_transformation(transform_params)
    
    if avg_error > 5.0:  # If average error > 5 map units
        print(f"⚠️  High validation error ({avg_error:.2f}). Check reference point accuracy.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("❌ Aborted")
            sys.exit(1)
    
    # Step 4: Add database columns
    print("\n4️⃣ Preparing database...")
    triangulator.add_map_coordinate_columns()
    
    # Step 5: Update all coordinates
    print("\n5️⃣ Updating all named mob coordinates...")
    updated_count = triangulator.update_all_coordinates(transform_params)
    
    # Step 6: Export report
    print("\n6️⃣ Generating report...")
    report_file = 'data/triangulation_report.json'
    triangulator.export_transformation_report(transform_params, report_file)
    
    print("\n" + "=" * 50)
    print("🎉 Triangulation Complete!")
    print(f"📍 Updated {updated_count} named mob coordinates")
    print(f"📊 Average validation error: {avg_error:.6f}")
    print(f"📄 Report saved to: {report_file}")
    print("\n💡 Next steps:")
    print("   - Update the frontend to use map_lat/map_lng instead of transformed coordinates")
    print("   - Test a few named mobs on the map to verify accuracy")

if __name__ == "__main__":
    main()
