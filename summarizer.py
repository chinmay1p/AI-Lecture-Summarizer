import google.generativeai as genai
import os
from dotenv import load_dotenv

_model = None

def _get_model():
    global _model
    if _model is None:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Please set it in a .env file.")
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel('gemini-2.5-flash')
        print("Gemini model initialized.")
    return _model

def gen_summary(txt, out_file):
    print("Generating summary...")
    prompt = f"""
    You are an expert academic assistant specializing in summarizing technical university lectures.
    Based on the following text extracted from lecture slides, provide a concise and structured summary.

    The summary should:
    1. Identify the main topic of the lecture.
    2. List the key concepts, definitions, and main points as bullet points.
    3. Conclude with the overall takeaway or conclusion of the lecture.
    4. The output should be in Markdown format.

    Here is the lecture text:
    ---
    {txt}
    ---
    """
    try:
        m = _get_model()
        r = m.generate_content(prompt)
        s = r.text
        with open(out_file, "w") as f:
            f.write(s)
        print(f"Summary successfully generated and saved to {out_file}")
    except Exception as e:
        print(f"An error occurred while generating the summary: {e}")


