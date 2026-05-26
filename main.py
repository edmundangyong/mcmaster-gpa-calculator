import fitz
import easyocr

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
    return(full_document_text)

if __name__ == "__main__":
    pdf_file = "test.pdf" 
    extracted_text = "\n\n".join(extract_pdf(pdf_file))
    
    with open("output.txt", "w", encoding="utf-8") as text_file:
        text_file.write(extracted_text)
    
    print("DONE")