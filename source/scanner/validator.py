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




