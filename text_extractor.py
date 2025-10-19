# text_extractor.py
# Phases 3 & 4: Text Detection and Recognition (OCR).

import easyocr
import os

class TextExtractor:
    """
    Detects and recognizes text from a directory of enhanced images.
    
    This class uses EasyOCR, which combines a text detection model (CRAFT)
    and a text recognition model (CRNN), effectively handling both
    Phase 3 (detection) and Phase 4 (recognition). It's a robust,
    pre-trained solution that simplifies the pipeline.
    """
    def __init__(self, languages=['en']):
        """
        Initializes the OCR reader.

        Args:
            languages (list): List of language codes to be recognized (e.g., ['en']).
        """
        print("Initializing TextExtractor with EasyOCR...")
        # This will download the models the first time it is run
        self.reader = easyocr.Reader(languages, gpu=True if 'CUDA_VISIBLE_DEVICES' in os.environ else False)
        print("EasyOCR reader initialized.")

    def extract_text_from_images(self, input_dir):
        """
        Extracts all text from images in a directory.

        Args:
            input_dir (str): The directory containing enhanced images.

        Returns:
            str: A single string containing all concatenated text from all images.
        """
        print(f"Starting text extraction from images in {input_dir}...")
        full_text = []
        
        image_files = sorted([f for f in os.listdir(input_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])

        for i, filename in enumerate(image_files):
            image_path = os.path.join(input_dir, filename)
            print(f"  - Processing slide {i+1}/{len(image_files)}: {filename}")
            
            # EasyOCR reads an image and returns a list of (bounding_box, text, confidence)
            results = self.reader.readtext(image_path, paragraph=True)
            
            # We only need the text part
            slide_text = "\n".join([res[1] for res in results])
            
            full_text.append(f"--- Slide {i+1} ---\n{slide_text}\n")

        print("Text extraction complete.")
        return "\n".join(full_text)

if __name__ == '__main__':
    # Example Usage
    INPUT_FOLDER = 'enhanced_keyframes'
    if not os.path.exists(INPUT_FOLDER) or not os.listdir(INPUT_FOLDER):
        print(f"Error: Input folder '{INPUT_FOLDER}' is empty or does not exist. Run image_enhancer.py first.")
    else:
        extractor = TextExtractor()
        extracted_text = extractor.extract_text_from_images(INPUT_FOLDER)
        
        # Save the extracted text to a file
        with open("extracted_text.txt", "w") as f:
            f.write(extracted_text)
            
        print("\nExtracted Text saved to extracted_text.txt")
        # print("\n--- Full Extracted Text ---")
        # print(extracted_text)
