import os
import shutil
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from keyframe_extractor import extract_keyframes
from image_enhancer import enhance_images
from text_extractor import extract_text
from summarizer import gen_summary

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'workspace'
app.secret_key = 'supersecretkey'

WORKSPACE_DIR = 'workspace' 

KEYFRAMES_DIR = os.path.join(WORKSPACE_DIR, '01_keyframes')
ENHANCED_DIR = os.path.join(WORKSPACE_DIR, '02_enhanced')
EXTRACTED_TEXT_FILE = os.path.join(WORKSPACE_DIR, '03_extracted_text.txt')
SUMMARY_FILE = 'lecture_summary.md' 

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
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(video_path)        
        return redirect(url_for('processing', video_path=video_path))

@app.route('/processing')
def processing():
    video_path = request.args.get('video_path')
    if not video_path or not os.path.exists(video_path):
        flash('Video file not found')
        return redirect(url_for('index'))    
    return render_template('processing.html')

@app.route('/process_video')
def process_video_route():
    video_path = request.args.get('video_path')
    if not video_path or not os.path.exists(video_path):
        flash('Video file not found')
        return redirect(url_for('index'))
    
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
    print("===================================================")
    print("      AI Lecture Summarizer Pipeline Started       ")
    print("===================================================")

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


    print("\n Extracting Keyframes from Video")
    keyframe_paths = extract_keyframes(video_path, KEYFRAMES_DIR, sim_th=0.98)
    if not keyframe_paths:
        print("No keyframes were extracted. Exiting pipeline.")
        return



    print("\n Enhancing Keyframes for OCR")
    enhance_images(KEYFRAMES_DIR, ENHANCED_DIR)



    print("\n Extracting Text from Enhanced Images")
    full_text = extract_text(ENHANCED_DIR, langs=['en'])
    with open(EXTRACTED_TEXT_FILE, 'w') as f:
        f.write(full_text)
    print(f"Full transcript saved to {EXTRACTED_TEXT_FILE}")



    print("\n Final Summary")
    try:
        gen_summary(full_text, SUMMARY_FILE)
    except ValueError as e:
        print(f"FATAL ERROR during summarization: {e}")
        print("Please ensure you have a .env file with your GEMINI_API_KEY.")
        return None
        
    print("Pipeline Completed Successfully")
    print(f"Final summary is in: {SUMMARY_FILE}")
    return SUMMARY_FILE


if __name__ == '__main__':
    app.run(debug=True)
