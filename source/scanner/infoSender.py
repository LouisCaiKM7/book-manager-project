
from scanner import ISBNScanner
from validator import Validator
import ISBNinfo
import cv2
from bookdatabase import database
# Inside infosender.py
import requests

import requests  # Import requests if you need to use it elsewhere
from scanner import ISBNScanner  # Import ISBNScanner if it's in a separate module
from validator import Validator  # Import Validator if it's in a separate module
import ISBNinfo # Import your ISBNinfo module

class InfoSender:
    def __init__(self, cap):
        self.cap = cap

    def main(self):
        status = False
        isbn_scanner = ISBNScanner(self.cap)
        isbn = isbn_scanner.scan_isbn()
        db = database()
        db.create_database()

        if isbn:
            print(f"Scanned ISBN: {isbn}")

            # Validate the scanned ISBN
            validator = Validator(isbn_scanner, isbn)
            is_valid = validator.validate_isbn()
            
            if is_valid:
                print("The ISBN is valid.")

                # Fetch book info
                print(type(isbn))
                print(isbn)
                isbninfo = ISBNinfo.fetch_book_info(isbn)
                
                if isbninfo is None:
                    print("No information found for the ISBN.")
                else:
                    print(isbninfo)
                    
                    # You can handle the book information here instead of sending it to the Flask server
                    # For example, you could save it to a database or display it to the user
                    self.handle_book_info(isbn, isbninfo)
                     # Create an instance of your database class
                    status = True
                    return (isbn,
                            isbninfo.get("title", "Unknown Title"),
                            isbninfo.get("authors", ["Unknown Author"])[0],
                            status)
                
                    
            else:
                print("The ISBN is not valid.")
                return None
        else:
            print("No ISBN found.")
            return None

    def handle_book_info(self, isbn, isbninfo):
        # This method can handle the book information as you see fit
        print(f"Title: {isbninfo.get('title', 'Unknown Title')}")
        print(f"Author: {isbninfo.get('authors', ['Unknown Author'])[0]}")
        print(f"Publisher ID: null")  # Update as needed
        print(f"Location: null")       # Update as needed


# class InfoSender:
#     def __init__(self,cap):
#         self.cap = cap
#     def main(self):
#         isbn_scanner = ISBNScanner(self.cap)  # Instantiate the scanner
#         isbn = isbn_scanner.scan_isbn()  # Call the method to scan ISBN
#         bdb = database()
#         bdb.create_database()# Instantiate the database
#         if isbn:
#             print(f"Scanned ISBN: {isbn}")

#             # Validate the scanned ISBN
#             validator = Validator(isbn_scanner, isbn)
#             is_valid = validator.validate_isbn()  # Call the validate_isbn method
            
#             if is_valid:
#                 print("The ISBN is valid.")
#             else:
#                 print("The ISBN is not valid.")

#             # Fetch book info
#             ISBNinfoFinder = ISBNinfo.ISBNinfo
#             isbninfo = ISBNinfoFinder.fetch_book_info(isbn)
            
#             if isbninfo is None:
#                 print("No information found for the ISBN.")
#             else:
#                 print(isbninfo)
#                 bdb.insert_book(isbn = isbn, title = isbninfo["title"], author = "null",publisher_id="null",location="null")
                

#         else:
#             print("No ISBN found.")

