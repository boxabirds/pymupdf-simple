import fitz
import io
import os
from PIL import Image
import argparse

import re

import re

def extract_text(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        text = doc[i].get_text()

        # Remove extra spaces between single characters that are part of a word
        text = re.sub(r'(?<=\b\w) (?=\w\b)', '', text)

        # Add space before numbers
        text = re.sub(r'(\D)(\d)', r'\1 \2', text)

        with open(f'{output_path}/page_{i+1}.txt', 'w') as f:
            f.write(text)

def extract_images(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        for img in doc.get_page_images(i):
            xref = img[0]
            base = img[1]
            img_data = doc.extract_image(xref)
            img_bytes = img_data["image"]

            image = Image.open(io.BytesIO(img_bytes))
            image.save(open(f"{output_path}/{base}.png", "wb"), format="PNG")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=str, required=True, help="The path to the PDF file.")
    parser.add_argument("--output", type=str, required=False, default=None, help="The output directory.")
    args = parser.parse_args()

    pdf_path = args.pdf
    output_path = args.output if args.output else os.path.splitext(pdf_path)[0] + "-output"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    extract_text(pdf_path, output_path)
    extract_images(pdf_path, output_path)

if __name__ == "__main__":
    main()
