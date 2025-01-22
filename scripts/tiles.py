#!/usr/bin/env python3

import os
import requests
from PIL import Image

# Config
BASE_URL = "https://cdn.ashescodex.com/map/20241219"
ZOOM = 8
MAX_COL = 90   # e.g. 0..90
MAX_ROW = 130  # e.g. 0..130
TILE_SIZE = 256  # common for many tile servers, might be 512 or other

# Local folder for downloaded tiles
os.makedirs("tiles", exist_ok=True)

def download_tiles():
    """
    Attempt to download all tiles for the given ZOOM level.
    Skip (continue) if 404 or any error occurs.
    """
    for col in range(MAX_COL+1):
        for row in range(MAX_ROW+1):
            url = f"{BASE_URL}/{ZOOM}/{col}/{row}.webp"
            out_path = f"tiles/{ZOOM}_{col}_{row}.webp"

            if os.path.exists(out_path):
                # already downloaded
                continue

            print(f"Downloading {url} -> {out_path}")
            try:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    with open(out_path, "wb") as f:
                        f.write(r.content)
                else:
                    print(f"  Not found or error: {r.status_code}")
            except Exception as e:
                print(f"  Error {e}, skipping {col},{row}")

def assemble_mosaic():
    """
    Create a large PNG from all the tiles that exist, placing them at
    correct offsets. Missing tiles => transparent area.
    """
    width_px = (MAX_COL+1) * TILE_SIZE
    height_px = (MAX_ROW+1) * TILE_SIZE

    # RGBA => can do transparent fill
    mosaic = Image.new("RGBA", (width_px, height_px), (0, 0, 0, 0))

    for col in range(MAX_COL+1):
        for row in range(MAX_ROW+1):
            tile_path = f"tiles/{ZOOM}_{col}_{row}.webp"
            if os.path.exists(tile_path):
                try:
                    tile_img = Image.open(tile_path).convert("RGBA")
                    x_offset = col * TILE_SIZE
                    y_offset = row * TILE_SIZE
                    mosaic.paste(tile_img, (x_offset, y_offset), tile_img)
                except Exception as e:
                    print(f"  Could not open {tile_path}: {e}")

    out_name = f"mosaic_zoom{ZOOM}.png"
    mosaic.save(out_name)
    print(f"Saved combined mosaic to {out_name}")

def main():
    download_tiles()
    assemble_mosaic()

if __name__ == "__main__":
    main()
