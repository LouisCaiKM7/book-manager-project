import requests


def fetch_book_info(isbn):
    api_url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
    response = requests.get(api_url)
        
    if response.status_code == 200:
        book_data = response.json()
        if 'items' in book_data:
            return book_data['items'][0]['volumeInfo']  # Return the book details
    return None

# ISBNinfo(9787535896797)
# a = ISBNinfo.fetch_book_info(9787535896797)
# print(a)