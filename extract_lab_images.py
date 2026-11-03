"""
extract_lab_images.py
---------------------
Auxiliary script for ANAT 1009 Lab Bellringer Exam.
Extracts all anatomical diagrams, models, and cadaver prosection images
from Lab 3, Lab 4, and Lab 5 PDFs into the './extracted_lab_images/' directory.

Requirements:
    pip install pypdf pillow
"""

import os
import io
from pypdf import PdfReader
from PIL import Image

PDF_FILES = {
    "lab3": "ANAT 1009- Lab 3 - Muscular System_STUDENT_F2026 (1).pdf",
    "lab4": "ANAT 1009- Lab 4 - Nervous System_STUDENT_F2026 (1).pdf",
    "lab5": "ANAT 1009- Lab 5 - Respiratory System_STUDENT_F2026 (1).pdf"
}

OUTPUT_DIR = "extracted_lab_images"

def extract_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    total_extracted = 0

    print("Starting extraction of all ANAT 1009 Lab images (models & cadaver prosections)...")

    for lab_key, pdf_name in PDF_FILES.items():
        if not os.path.exists(pdf_name):
            alt_name = pdf_name.replace(".pdf", "_2.pdf")
            if os.path.exists(alt_name):
                pdf_name = alt_name
            else:
                print(f"[!] Warning: PDF file {pdf_name} not found in working directory. Skipping.")
                continue

        reader = PdfReader(pdf_name)

        for page_idx, page in enumerate(reader.pages):
            page_num = page_idx + 1
            images = page.images

            if not images:
                continue

            for img_idx, img_obj in enumerate(images):
                img_name = img_obj.name
                img_bytes = img_obj.data

                try:
                    img = Image.open(io.BytesIO(img_bytes))
                    # Filter out tiny icon images / video play icons (< 120px width/height or < 12KB)
                    if img.width < 120 or img.height < 120 or len(img_bytes) < 12000:
                        continue

                    out_filename = f"{lab_key}_p{page_num}_img{img_idx+1}.png"
                    out_path = os.path.join(OUTPUT_DIR, out_filename)

                    # Convert CMYK or indexed modes to RGB for safe PNG saving
                    if img.mode in ("CMYK", "P"):
                        img = img.convert("RGB")

                    img.save(out_path, "PNG")
                    total_extracted += 1
                    print(f"  [+] Saved: {out_filename} ({img.width}x{img.height})")
                except Exception as e:
                    print(f"  [-] Failed to extract image on page {page_num}: {e}")

    print(f"\nExtraction complete! Total images extracted: {total_extracted}")
    print(f"Saved into: ./{OUTPUT_DIR}/")

if __name__ == "__main__":
    extract_all()
