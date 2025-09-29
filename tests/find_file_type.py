import os
import pandas as pd
import docx
import fitz

def load_document(file_name):
    # All of these lines must be indented to be inside the function
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
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

# --- Example of how to call the function ---
file_name = "AI.docx"
document_type = load_document(file_name)
#print(f"The file {file_name} is of type: {document_type}")
