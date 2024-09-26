# Example using ZBar for Python
import cv2
from pyzbar.pyzbar import decode
import constants.constants
# import constants.constants

def scan_isbn(image):
    # Load image
    img = cv2.imread(image)

    # Check if the image was loaded successfully
    if img is None:
        print("Failed to load image.")
        return None

    # Decode the barcode
    barcodes = decode(img)
    
    for barcode in barcodes:
        isbn = barcode.data.decode('utf-8')  # Decode ISBN barcode
        return isbn

    return None

ImagetestConstant = r"E:\\01_programming\\book-manager-project\\tester\\OIP.jpg"
isbn = scan_isbn(ImagetestConstant)
print(isbn)
