import cv2
from pyzbar.pyzbar import decode

class ISBNScanner:
    def __init__(self, image_path):
        self.image_path = image_path  # Store the image path

    def scan_isbn(self):
        # Load image
        img = cv2.imread(self.image_path)

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

# # Test the scanner
# ImagetestConstant = r"E:\\01_programming\\book-manager-project\\tester\\OIP.jpg"
# isbn_scanner = ISBNScanner(ImagetestConstant)  # Instantiate the class
# isbn = isbn_scanner.scan_isbn()  # Call the method to scan ISBN
# print(isbn)
