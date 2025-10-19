# main.py
# Orchestrates the entire lecture summarization pipeline.

import os
import shutil
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from keyframe_extractor import KeyframeExtractor
from image_enhancer import ImageEnhancer
from text_extractor import TextExtractor
from summarizer import Summarizer

# --- Flask App Setup ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'workspace'
app.secret_key = 'supersecretkey'

# --- Configuration ---
WORKSPACE_DIR = 'workspace' 

# Define sub-directory paths
KEYFRAMES_DIR = os.path.join(WORKSPACE_DIR, '01_keyframes')
ENHANCED_DIR = os.path.join(WORKSPACE_DIR, '02_enhanced')
EXTRACTED_TEXT_FILE = os.path.join(WORKSPACE_DIR, '03_extracted_text.txt')
SUMMARY_FILE = 'lecture_summary.md' # Final output

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        flash('No video file selected')
        return redirect(request.url)
    file = request.files['video']
    if file.filename == '':
        flash('No video file selected')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        # Ensure the workspace directory exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(video_path)
        summary_path = process_video(video_path)
        if summary_path:
            return redirect(url_for('results', summary_file=summary_path))
        else:
            flash('Error processing video. Please check the console for details.')
            return redirect(url_for('index'))

@app.route('/results')
def results():
    summary_file = request.args.get('summary_file')
    with open(summary_file, 'r') as f:
        summary_content = f.read()
    return render_template('results.html', summary_content=summary_content)

def process_video(video_path):
    """
    Runs the full summarization pipeline.
    """
    print("===================================================")
    print("      AI Lecture Summarizer Pipeline Started       ")
    print("===================================================")

    # --- Setup ---
    # Ensure base workspace directory exists
    if not os.path.exists(WORKSPACE_DIR):
        os.makedirs(WORKSPACE_DIR)

    # Clean up previous pipeline run directories, but preserve the uploaded video
    if os.path.exists(KEYFRAMES_DIR):
        shutil.rmtree(KEYFRAMES_DIR)
    if os.path.exists(ENHANCED_DIR):
        shutil.rmtree(ENHANCED_DIR)
    if os.path.exists(EXTRACTED_TEXT_FILE):
        os.remove(EXTRACTED_TEXT_FILE)

    if not os.path.exists(video_path):
        print(f"FATAL ERROR: Input video '{video_path}' not found. Exiting.")
        return None

    # --- Phase 1: Keyframe Extraction ---
    print("\n--- Phase 1: Extracting Keyframes from Video ---")
    extractor = KeyframeExtractor(similarity_threshold=0.98)
    keyframe_paths = extractor.extract_keyframes(video_path, KEYFRAMES_DIR)
    if not keyframe_paths:
        print("No keyframes were extracted. Exiting pipeline.")
        return

    # --- Phase 2: Image Enhancement ---
    print("\n--- Phase 2: Enhancing Keyframes for OCR ---")
    enhancer = ImageEnhancer()
    enhancer.enhance_images(KEYFRAMES_DIR, ENHANCED_DIR)

    # --- Phase 3 & 4: Text Extraction ---
    print("\n--- Phase 3 & 4: Extracting Text from Enhanced Images ---")
    text_extractor = TextExtractor(languages=['en'])
    full_text = text_extractor.extract_text_from_images(ENHANCED_DIR)
    with open(EXTRACTED_TEXT_FILE, 'w') as f:
        f.write(full_text)
    print(f"Full transcript saved to {EXTRACTED_TEXT_FILE}")

    # --- Phase 5: Summarization ---
    print("\n--- Phase 5: Generating Final Summary ---")
    try:
        summarizer = Summarizer()
        summarizer.generate_summary(full_text, SUMMARY_FILE)
    except ValueError as e:
        print(f"FATAL ERROR during summarization: {e}")
        print("Please ensure you have a .env file with your GEMINI_API_KEY.")
        return None
        
    print("\n===================================================")
    print("           Pipeline Completed Successfully         ")
    print(f"          Final summary is in: {SUMMARY_FILE}      ")
    print("===================================================")
    return SUMMARY_FILE


if __name__ == '__main__':
    app.run(debug=True)
