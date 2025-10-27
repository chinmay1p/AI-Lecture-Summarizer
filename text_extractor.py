import easyocr
import os

_reader = None

def _get_reader(langs=['en']):
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(langs, gpu=True if 'CUDA_VISIBLE_DEVICES' in os.environ else False)
        print("EasyOCR reader initialized.")
    return _reader

def extract_text(inp_dir, langs=['en']):
    r = _get_reader(langs)
    chunks = []
    files = sorted([f for f in os.listdir(inp_dir) if f.endswith(('.png'))])
    for i, name in enumerate(files):
        path = os.path.join(inp_dir, name)
        print(f"  - Processing slide {i+1}/{len(files)}: {name}")
        res = r.readtext(path, paragraph=True)
        txt = "\n".join([x[1] for x in res])
        chunks.append(f"--- Slide {i+1} ---\n{txt}\n")
    print("Text extraction complete.")
    return "\n".join(chunks)


