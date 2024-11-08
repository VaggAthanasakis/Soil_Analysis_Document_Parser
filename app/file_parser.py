import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
import pdfplumber
import ocrmypdf
import json


class File_parser:

    def __init__(self) -> None:
        pass

    # Function to extract text from a scanned PDF using OCR
    # Converts the pdf pages to images and then performs OCR on each page
    # in order to extract the text

    # THIS IS NOT USED
    def extract_text_from_scanned_pdf(self,file_path):
        pages = convert_from_path(file_path, dpi=600)  # Convert PDF pages to images
        extracted_text = ""
        
        for page in pages:
            page_text = pytesseract.image_to_string(page)  # Perform OCR on each page
            extracted_text += f"{page_text}\n"             # Add the text to the output
        
        return extracted_text
    
    # Function to detect if the PDF is scanned or not
    def is_pdf_scanned(self,file_path):
        reader = PdfReader(file_path)
        num_pages = len(reader.pages)
        
        # Try to extract text from each page
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            if text and text.strip():  # If there's text, it's not scanned
                return False   
            
        return True  # No text found, likely a scanned PDF


   # Function to return the full text of the document
    def extract_text_from_file(self,input_file):

        # if we have a scanned document, perform OCR
        if self.is_pdf_scanned(input_file):
            print("\nPerforming OCR...")
            ocrmypdf.ocr(input_file, input_file, image_dpi=600)   

        # Read the text of the pdf file
        with pdfplumber.open(input_file) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text()  # Extracts text page-by-page
        
        return full_text
    
    # Function to create a json string from an LLM response
    def create_json(self,response):
        dict_string = json.loads(str(response))
        json_string = json.dumps(dict_string)

        return json_string