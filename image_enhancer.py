# image_enhancer.py
# Phase 2: Image Enhancement using Contrast Stretching.

import cv2
import numpy as np
import os
from PIL import Image

class ImageEnhancer:
    """
    Enhances images to improve text clarity for OCR.
    """
    def __init__(self):
        print("Initializing ImageEnhancer...")

    def _contrast_stretching(self, image):
        """
        Applies contrast stretching to a single channel (grayscale) image.
        """
        # Use PIL for robust image handling
        pil_img = Image.fromarray(image)
        # Find the min and max pixel values
        min_val, max_val = pil_img.getextrema()

        if max_val == min_val:
            return image # Avoid division by zero on solid color images

        # Apply the contrast stretching formula
        stretched_img = pil_img.point(lambda p: 255 * (p - min_val) / (max_val - min_val))
        return np.array(stretched_img)

    def enhance_images(self, input_dir, output_dir):
        """
        Loads images from a directory, enhances them, and saves to another.

        Args:
            input_dir (str): Directory containing the source images (keyframes).
            output_dir (str): Directory to save the enhanced images.

        Returns:
            list: A list of file paths to the saved enhanced images.
        """
        print(f"Starting image enhancement for images in {input_dir}...")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        enhanced_paths = []
        image_files = sorted([f for f in os.listdir(input_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])

        for filename in image_files:
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            # Read image in grayscale
            image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                print(f"  - Warning: Could not read {input_path}. Skipping.")
                continue

            # Apply enhancement
            enhanced_image = self._contrast_stretching(image)

            cv2.imwrite(output_path, enhanced_image)
            enhanced_paths.append(output_path)
            print(f"  - Enhanced {filename} and saved to {output_path}")

        print("Image enhancement complete.")
        return enhanced_paths

if __name__ == '__main__':
    # Example Usage
    INPUT_FOLDER = 'keyframes'
    OUTPUT_FOLDER = 'enhanced_keyframes'
    if not os.path.exists(INPUT_FOLDER) or not os.listdir(INPUT_FOLDER):
         print(f"Error: Input folder '{INPUT_FOLDER}' is empty or does not exist. Run keyframe_extractor.py first.")
    else:
        enhancer = ImageEnhancer()
        enhancer.enhance_images(INPUT_FOLDER, OUTPUT_FOLDER)
