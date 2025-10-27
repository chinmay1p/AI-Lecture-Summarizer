import cv2
import numpy as np
import os
from PIL import Image

def _stretch(img):
    pil = Image.fromarray(img)
    mn, mx = pil.getextrema()
    if mx == mn:
        return img
    out = pil.point(lambda p: 255 * (p - mn) / (mx - mn))
    return np.array(out)

def enhance_images(inp_dir, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    paths = []
    files = sorted([f for f in os.listdir(inp_dir) if f.endswith(('.png'))])

    for name in files:
        inp = os.path.join(inp_dir, name)
        out = os.path.join(out_dir, name)

        img = cv2.imread(inp, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"  - Warning: Could not read {inp}. Skipping.")
            continue

        enh = _stretch(img)
        cv2.imwrite(out, enh)
        paths.append(out)
        print(f"  - Enhanced {name} and saved to {out}")

    print("Image enhancement complete.")
    return paths
