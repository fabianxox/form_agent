import cv2
import pytesseract

# --- Set Tesseract path ---
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --- Load image ---
img_path = r"D:\autonomize\data\patients.png"
img = cv2.imread(img_path)
if img is None:
    raise FileNotFoundError(f"Image not found: {img_path}")

# --- Preprocessing ---
def preprocess(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply slight blur to reduce noise
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    # Apply Otsu's thresholding for better binarization
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

# --- OCR function ---
def ocr_find(image):
    # psm 6 = assume a uniform block of text
    config = '--oem 3 --psm 6'
    return pytesseract.image_to_string(image, config=config)

# --- Run preprocessing and OCR ---
img_preprocessed = preprocess(img)
text = ocr_find(img_preprocessed)

print("Detected text:\n", text)

# --- Optional: save preprocessed image ---
#cv2.imwrite(r"D:\autonomize\data\img2_preprocessed.png", img_preprocessed)
