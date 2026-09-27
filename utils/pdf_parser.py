import fitz  # PyMuPDF
from typing import Tuple

def extract_text_from_pdf(pdf_bytes: bytes) -> Tuple[str, bool, str]:
    """
    Extracts plain text from raw PDF bytes.
    
    Returns:
        tuple: (extracted_text, is_success, error_message)
    """
    try:
        # Open PDF document directly from memory buffer
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        if doc.page_count == 0:
            return "", False, "Uploaded PDF file contains no pages."
        
        extracted_pages = []
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            if text:
                extracted_pages.append(text)
                
        full_text = "\n".join(extracted_pages).strip()
        
        # Validation: Check if PDF was scanned (image-only)
        if not full_text or len(full_text) < 30:
            return "", False, "Extracted text is too short or empty. The PDF might be scanned/image-only."
            
        return full_text, True, ""
        
    except Exception as e:
        return "", False, f"Failed to parse PDF: {str(e)}"