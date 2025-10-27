# AI Lecture Summarizer

This project is an end-to-end pipeline that automatically summarizes video lectures. It ingests a video file, uses computer vision to extract and read text from presentation slides, and then leverages a Large Language Model (LLM) to generate a concise, structured summary.

This pipeline was developed as a project for a "Computer Vision with Deep Learning" course, applying core concepts such as image processing, CNN-based feature extraction, and transfer learning.

## Features

* **Automated Keyframe Extraction:** Intelligently identifies unique presentation slides from a video, ignoring redundant frames and transitions.
* **Image Pre-processing:** Enhances extracted slides using contrast stretching to ensure optimal text clarity for OCR.
* **Deep Learning OCR:** Uses state-of-the-art CRAFT and CRNN models (via EasyOCR) to detect and recognize text from the enhanced images.
* **LLM-Powered Summarization:** Leverages the Google Gemini Pro API to transform the raw, extracted text into a clean, well-structured, and easy-to-read Markdown summary.

---

## Technical Approach: A 5-Phase Pipeline

The project operates as a sequential pipeline, where the output of one phase becomes the input for the next. The entire workflow is managed by `main.py`.

### 1. Keyframe (Slide) Extraction
* **Goal:** To identify and save only the unique slide frames from the video.
* **Process:**
    1.  The video is sampled at a regular interval (e.g., every 15 frames) to avoid redundant processing.
    2.  Each sampled frame is passed through a pre-trained **MobileNetV2** CNN, which generates a high-dimensional feature vector (embedding) representing the image's content.
    3.  **Cosine Similarity** is used to compare the current frame's vector to the vector of the *last saved keyframe*.
    4.  If the similarity score falls below a set threshold (e.g., 0.98), it signifies a significant visual change, and the current frame is saved as a new, unique slide.
* **Output:** A directory of unique slide images (`workspace/01_keyframes/`).

### 2. Image Enhancement
* **Goal:** To pre-process the keyframes to maximize OCR accuracy.
* **Process:**
    1.  Each keyframe image is converted from color to grayscale.
    2.  A **Contrast Stretching** algorithm is applied. This finds the minimum and maximum pixel values and "stretches" this range to the full 0-255, making dark text darker and light backgrounds lighter.
* **Output:** A directory of enhanced, high-contrast images (`workspace/02_enhanced/`).

### 3. Text Detection & Recognition (OCR)
* **Goal:** To locate and read all text from the enhanced slides.
* **Process:** This phase uses the **EasyOCR** library, which bundles two deep learning models:
    1.  **Detection (CRAFT):** A CNN-based model scans the image and draws tight bounding boxes around all regions containing text.
    2.  **Recognition (CRNN):** A Convolutional Recurrent Neural Network (CRNN) analyzes the pixels within each bounding box and translates them into a machine-readable text string.
* **Output:** A single text file containing the aggregated transcript from all slides (`workspace/03_extracted_text.txt`).

### 4. AI Summarization
* **Goal:** To transform the raw transcript into a structured summary.
* **Process:**
    1.  The full text transcript is loaded from the file.
    2.  A detailed prompt is programmatically constructed, instructing the LLM on its persona (an academic assistant) and the desired output format (Markdown).
    3.  The transcript and prompt are sent to the **Google Gemini Pro** API.
    4.  The model processes the information and generates the final summary.
* **Output:** The final summary saved as a Markdown file (`lecture_summary.md`).

---

## Technologies Used

* **Computer Vision & Deep Learning:**
    * **OpenCV:** For all video/image I/O and processing.
    * **TensorFlow & Keras:** To load and run the pre-trained MobileNetV2 model.
    * **EasyOCR:** For the high-accuracy, pre-trained text detection (CRAFT) and recognition (CRNN) models.
    * **Pillow (PIL):** For image file handling.
* **AI & Language Model:**
    * **Google Gemini Pro:** For content summarization and structuring.
    * **google-generativeai SDK:** The official Python client for the Gemini API.
* **Core Libraries:**
    * **NumPy:** For high-performance numerical operations on image arrays.

---

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/chinmay1p/AI-Lecture-Summarizer.git](https://github.com/chinmay1p/AI-Lecture-Summarizer.git)
    cd AI-Lecture-Summarizer
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```

3.  **Install the required packages:**
    (It is recommended to create a `requirements.txt` file with the libraries below)
    ```bash
    pip install opencv-python-headless tensorflow easyocr numpy pillow google-generativeai
    ```

4.  **Set up your API Key:**
    * Get a Google AI Studio API key.
    * Store it securely, for example, in a `.env` file or as an environment variable.

---

