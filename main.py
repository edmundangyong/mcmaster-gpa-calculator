import fitz
import easyocr
import re

import cv2
import numpy as np

def extract_pdf(pdf_path, lang='en'):
    print("EXTRACTING PDF")

    doc = fitz.open(pdf_path)
    reader = easyocr.Reader([lang], gpu=False) 
    full_document_text = []

    for page_num in range(len(doc)):

        print("PROCESSING")

        page = doc.load_page(page_num)
        zoom_matrix = fitz.Matrix(3.0, 3.0)
        pix = page.get_pixmap(matrix=zoom_matrix)
        img_bytes = pix.tobytes("png")

        np_arr = np.frombuffer(img_bytes, np.uint8)
        img_cv = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        _, processed_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        text_results = reader.readtext(
            processed_img, 
            detail=0,
            paragraph=False
        )
        
        page_text = "\n".join(text_results)
        full_document_text.append(page_text)

    doc.close()
    print("PDF EXTRACTION COMPLETE")
    return("\n\n".join(full_document_text))

def extract_dict(transcript):
    print("EXTRACTING DICTIONARY")

    transcript = transcript.split("\n")

    grades = {}
    pattern1 = r"^\d\.\d{2}\/\d\.\d{2}$"

    for line in range(len(transcript)):

        clean_line = transcript[line].strip()

        if re.match(pattern1, clean_line):

            course_code = transcript[line-2]
            course_name = transcript[line-1]
            weight = clean_line
            grade = transcript[line+1]

            grades[course_code] = {
                "name": course_name,
                "weight": weight,
                "grade": grade
            }

            print(course_code, course_name, weight, grade)
    
    print("DICTIONARY EXTRACTION COMPLETE")
    return grades


def debug_pdf_to_images(pdf_path):
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):

        page = doc.load_page(page_num)
        zoom_matrix = fitz.Matrix(3.0, 3.0) 
        pix = page.get_pixmap(matrix=zoom_matrix)
        img_bytes = pix.tobytes("png")
        
        np_arr = np.frombuffer(img_bytes, np.uint8)
        img_cv = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        _, processed_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        output_filename = f"debug_processed_page_{page_num + 1}.png"
        cv2.imwrite(output_filename, processed_img)
        print(f"Saved: {output_filename}")

    doc.close()
    print("--- DEBUG IMAGES GENERATED ---")

if __name__ == "__main__":

    pdf_file = "test.pdf"

    debug_pdf_to_images(pdf_file)

    extracted_text = extract_pdf(pdf_file)
    
    with open("output.txt", "w", encoding="utf-8") as text_file:
        text_file.write(extracted_text)
    
    extract_dict(extracted_text)
    print("DONE")