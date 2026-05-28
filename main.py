import fitz
import easyocr
import re

def extract_pdf(pdf_path, lang='en'):
    print("EXTRACTING PDF")

    doc = fitz.open(pdf_path)
    reader = easyocr.Reader([lang], gpu=False) 
    full_document_text = []

    for page_num in range(len(doc)):

        print("PROCESSING")

        page = doc.load_page(page_num)
        zoom_matrix = fitz.Matrix(4.0, 4.0)
        pix = page.get_pixmap(matrix=zoom_matrix)
        img_bytes = pix.tobytes("png")
        text_results = reader.readtext(img_bytes, detail=0)
        
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

if __name__ == "__main__":
    pdf_file = "test.pdf" 
    extracted_text = extract_pdf(pdf_file)
    
    with open("output.txt", "w", encoding="utf-8") as text_file:
        text_file.write(extracted_text)
    
    extract_dict(extracted_text)
    print("DONE")