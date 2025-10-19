# keyframe_extractor.py
# Phase 1: Video Processing & Keyframe (Slide) Extraction using a CNN.

import cv2
import numpy as np
import tensorflow as tf
import os
import gc

class KeyframeExtractor:
    """
    Extracts unique slides (keyframes) from a lecture video.

    This class uses a pre-trained CNN (MobileNetV2) to generate feature embeddings
    for each frame. It then compares the similarity of consecutive frames based
    on these embeddings to detect when a slide has changed.
    """
    def __init__(self, similarity_threshold=0.98):
        """
        Initializes the extractor.

        Args:
            similarity_threshold (float): Cosine similarity threshold to determine
                                          if two frames are from the same slide.
                                          Higher means more similar.
        """
        print("Initializing KeyframeExtractor...")
        self.similarity_threshold = similarity_threshold
        # Load a pre-trained CNN model (MobileNetV2) without the top classification layer
        self.model = tf.keras.applications.MobileNetV2(
            include_top=False,
            weights='imagenet',
            input_shape=(224, 224, 3),
            pooling='avg'
        )
        print("Pre-trained model loaded.")

    def _preprocess_frame(self, frame):
        """Preprocesses a single frame for the CNN."""
        img = cv2.resize(frame, (224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
        return img_array

    def _get_frame_embedding(self, frame):
        """Generates a feature embedding for a frame using the CNN."""
        processed_frame = self._preprocess_frame(frame)
        embedding = self.model.predict(processed_frame)
        return embedding.flatten()

    def _cosine_similarity(self, vec1, vec2):
        """Calculates the cosine similarity between two vectors."""
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        return dot_product / (norm_vec1 * norm_vec2)

    def extract_keyframes(self, video_path, output_dir):
        """
        Processes a video to extract and save keyframes.

        Args:
            video_path (str): The path to the input video file.
            output_dir (str): The directory to save the extracted frames.

        Returns:
            list: A list of file paths to the saved keyframes.
        """
        print(f"Starting keyframe extraction for {video_path}...")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file {video_path}")
            return []

        keyframes_paths = []
        last_frame_embedding = None
        frame_count = 0
        saved_frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Process every Nth frame to speed up the process (e.g., every 15 frames)
            if frame_count % 15 == 0:
                current_embedding = self._get_frame_embedding(frame)

                if last_frame_embedding is None:
                    # Always save the first frame
                    is_new_slide = True
                else:
                    # Compare with the last saved keyframe's embedding
                    similarity = self._cosine_similarity(current_embedding, last_frame_embedding)
                    if similarity < self.similarity_threshold:
                        is_new_slide = True
                    else:
                        is_new_slide = False

                if is_new_slide:
                    saved_frame_count += 1
                    filename = f"keyframe_{saved_frame_count:04d}.png"
                    filepath = os.path.join(output_dir, filename)
                    cv2.imwrite(filepath, frame)
                    keyframes_paths.append(filepath)
                    print(f"  - New slide detected. Saved {filename} (Similarity: {similarity if last_frame_embedding is not None else 'N/A'})")
                    last_frame_embedding = current_embedding
                    # Clean up memory
                    gc.collect()

            frame_count += 1

        cap.release()
        print(f"Keyframe extraction complete. Found {saved_frame_count} unique slides.")
        return keyframes_paths

if __name__ == '__main__':
    # Example Usage
    VIDEO_FILE = 'lecture.mp4' # Make sure you have a video file named 'lecture.mp4'
    OUTPUT_FOLDER = 'keyframes'
    if not os.path.exists(VIDEO_FILE):
        print(f"Error: Video file '{VIDEO_FILE}' not found. Please provide a sample video.")
    else:
        extractor = KeyframeExtractor()
        extractor.extract_keyframes(VIDEO_FILE, OUTPUT_FOLDER)
