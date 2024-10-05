# scanner.py

import cv2
from pyzbar.pyzbar import decode

class ISBNScanner:
    def __init__(self, image):
        self.image = image

    def scan_isbn(self):
        # Decode the barcodes in the image
        barcodes = decode(self.image)

        # Process the decoded barcodes
        isbn = None
        for barcode in barcodes:
            # Get the data from the barcode
            isbn = barcode.data.decode('utf-8')
            # Optionally, do any other processing here (e.g., verify if it's a valid ISBN)
            break  # Exit after finding the first valid ISBN

        return isbn


# # Test the scanner
# ImagetestConstant = r"E:\\01_programming\\book-manager-project\\tester\\OIP.jpg"
# isbn_scanner = ISBNScanner(ImagetestConstant)  # Instantiate the class
# isbn = isbn_scanner.scan_isbn()  # Call the method to scan ISBN
# print(isbn)
