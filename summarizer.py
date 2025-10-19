# summarizer.py
# Phase 5: Summarization using Gemini LLM.

import google.generativeai as genai
import os
from dotenv import load_dotenv

class Summarizer:
    """
    Generates a summary of the extracted text using the Gemini API.
    """
    def __init__(self):
        """
        Initializes the summarizer and configures the Gemini API.
        """
        print("Initializing Summarizer...")
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Please set it in a .env file.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        print("Gemini model initialized.")

    def generate_summary(self, text_content, output_file):
        """
        Sends text to Gemini API and saves the summary.

        Args:
            text_content (str): The full text transcript from the slides.
            output_file (str): Path to save the final summary markdown file.
        """
        print("Generating summary...")
        
        prompt = f"""
        You are an expert academic assistant specializing in summarizing technical university lectures.
        Based on the following text extracted from lecture slides, provide a concise and structured summary.

        The summary should:
        1.  Identify the main topic of the lecture.
        2.  List the key concepts, definitions, and main points as bullet points.
        3.  Conclude with the overall takeaway or conclusion of the lecture.
        4.  The output should be in Markdown format.

        Here is the lecture text:
        ---
        {text_content}
        ---
        """

        try:
            response = self.model.generate_content(prompt)
            summary = response.text
            
            with open(output_file, "w") as f:
                f.write(summary)
            
            print(f"Summary successfully generated and saved to {output_file}")
            # print("\n--- Generated Summary ---")
            # print(summary)

        except Exception as e:
            print(f"An error occurred while generating the summary: {e}")
            # print("\n--- Response Details ---")
            # print(response.prompt_feedback)


if __name__ == '__main__':
    # Example Usage
    TEXT_FILE = "workspace/03_extracted_text.txt"
    OUTPUT_FILE = "lecture_summary.md"
    
    if not os.path.exists(TEXT_FILE):
        print(f"Error: Text file '{TEXT_FILE}' not found. Run text_extractor.py first.")
    else:
        with open(TEXT_FILE, "r") as f:
            text = f.read()
        
        # You need a .env file with your GEMINI_API_KEY
        
        summarizer = Summarizer()
        summarizer.generate_summary(text, OUTPUT_FILE)
