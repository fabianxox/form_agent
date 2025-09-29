import os
import pandas as pd
import docx
import fitz
import cv2
import pytesseract

def load_document(file_name):
    _, file_extension = os.path.splitext(file_name)
    file_extension = file_extension.lower()

    if file_extension == ".pdf":
        return "pdf"
    elif file_extension == ".docx":
        return "docx" 
    elif file_extension == ".csv":
        return "csv"
    elif file_extension in [".xls", ".xlsx"]:
        return "excel"
    elif file_extension in [".png", ".jpeg", ".jpg"]:
        return "image"
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")


def read_file_as_text(file_path):
    doc_type = load_document(file_path)
    
    if doc_type == "pdf":
        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text
    
    elif doc_type == "docx":
        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text
    
    elif doc_type == "csv":
        df = pd.read_csv(file_path)
        return "\n".join([", ".join(map(str, row)) for row in df.values])
    
    elif doc_type == "excel":
        df = pd.read_excel(file_path)
        return "\n".join([", ".join(map(str, row)) for row in df.values])
    
    elif doc_type == "image":
        img = cv2.imread(file_path)
        if img is None:
            raise FileNotFoundError(f"Image not found: {file_path}")

        def preprocess(image):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (3, 3), 0)
            _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            return thresh

        def ocr_find(image):
            config = '--oem 3 --psm 6'
            return pytesseract.image_to_string(image, config=config)

        img_preprocessed = preprocess(img)
        text = ocr_find(img_preprocessed)

        print("Detected text:\n", text)
        return text
