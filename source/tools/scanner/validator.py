from scanner import ISBNScanner  # Import the ISBNScanner class

class Validator:
    def __init__(self, scanner, isbn):
        self.isbn = isbn
        self.scanner = scanner
    
    def validate_isbn(self):
        # Check if the ISBN is 13 digits long and starts with '978' or is 10 digits long
        if len(self.isbn) == 13 and self.isbn.startswith('978'):
            return True  # Valid ISBN-13
        elif len(self.isbn) == 10:
            return True  # Valid ISBN-10
        return False

# Instantiate the scanner and scan the ISBN
ImagetestConstant = r"E:\\01_programming\\book-manager-project\\tester\\OIP.jpg"
isbn_scanner = ISBNScanner(ImagetestConstant)  # Instantiate the ISBNScanner class
isbn = isbn_scanner.scan_isbn()  # Call the method to scan ISBN
print(f"Scanned ISBN: {isbn}")

# Validate the scanned ISBN
validator = Validator(isbn_scanner, isbn)
is_valid = validator.validate_isbn()  # Call the validate_isbn method
if is_valid:
    print("The ISBN is valid.")
else:
    print("The ISBN is not valid.")



