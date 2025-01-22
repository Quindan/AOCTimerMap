#!/usr/bin/env python3

import os
import re
from PIL import Image

TILE_SIZE = 512
ZOOM_LEVEL = 8   # if tile filenames start with "8_"
TILES_FOLDER = "tiles"  # folder containing your .webp tiles
OUTPUT_NAME = f"mosaic_zoom{ZOOM_LEVEL}.png"

def main():
    # 1) Collect all tile files that match the pattern "8_col_row.webp"
    pattern = re.compile(rf"^{ZOOM_LEVEL}_(\d+)_(\d+)\.webp$")

    all_tiles = []
    for fname in os.listdir(TILES_FOLDER):
        m = pattern.match(fname)
        if m:
            col_str, row_str = m.groups()
            col = int(col_str)
            row = int(row_str)
            filepath = os.path.join(TILES_FOLDER, fname)
            all_tiles.append((col, row, filepath))

    if not all_tiles:
        print("No tiles found matching the pattern in", TILES_FOLDER)
        return

    # 2) Find colMin, colMax, rowMin, rowMax
    cols = [t[0] for t in all_tiles]
    rows = [t[1] for t in all_tiles]
    col_min = min(cols)
    col_max = max(cols)
    row_min = min(rows)
    row_max = max(rows)

    print(f"Found tile columns from {col_min}..{col_max}")
    print(f"Found tile rows from {row_min}..{row_max}")

    # 3) Create the mosaic image (width x height)
    width_px = (col_max - col_min + 1) * TILE_SIZE
    height_px = (row_max - row_min + 1) * TILE_SIZE
    print(f"Mosaic size = {width_px} x {height_px}")

    # RGBA so we can have transparency for missing areas
    mosaic = Image.new("RGBA", (width_px, height_px), (0,0,0,0))

    # 4) Paste each tile at its offset
    for col, row, path in all_tiles:
        try:
            tile_img = Image.open(path).convert("RGBA")
            x_offset = (col - col_min) * TILE_SIZE
            y_offset = (row - row_min) * TILE_SIZE
            mosaic.paste(tile_img, (x_offset, y_offset), tile_img)
        except Exception as e:
            print(f"Error opening {path}: {e}")

    # 5) Save the result
    mosaic.save(OUTPUT_NAME)
    print(f"Saved mosaic to {OUTPUT_NAME}")

if __name__ == "__main__":
    main()
