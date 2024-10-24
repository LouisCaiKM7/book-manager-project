import sqlite3

class database:
    def __init__(self):
        self.conn = sqlite3.connect(r"E:\01_programming\book-manager-project\source\Database\bookexchange.db")
        self.cursor = self.conn.cursor()
    def create_database(self):
       # Creating Users table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email_hash TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ChatMessages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            user_id TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (book_id) REFERENCES Users(id)
        )
        ''')

        # Creating Books table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            isbn TEXT NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publisher_id INTEGER,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (publisher_id) REFERENCES Users(user_id)
        )
        ''')

        # Creating Chats table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Chats (
            chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            sender_id INTEGER,
            recipient_id INTEGER,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (book_id) REFERENCES Books(book_id),
            FOREIGN KEY (sender_id) REFERENCES Users(user_id),
            FOREIGN KEY (recipient_id) REFERENCES Users(user_id)
        )
        ''')

        # Creating Transactions table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            buyer_id INTEGER,
            seller_id INTEGER,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (book_id) REFERENCES Books(book_id),
            FOREIGN KEY (buyer_id) REFERENCES Users(user_id),
            FOREIGN KEY (seller_id) REFERENCES Users(user_id)
        )
        ''')

        
    def insert_user(self, username, email_hash, password_hash, location):
        self.cursor.execute("INSERT INTO Users (username, email_hash, password_hash, location) VALUES (?,?,?,?)", (username, email_hash, password_hash, location))
        self.conn.commit()
        self.conn.close()
    def insert_book(self, isbn, title, author, publisher_id, latitude, longitude, user_id):
        self.cursor.execute("INSERT INTO Books (user_id, isbn, title, author, publisher_id, latitude, longitude) VALUES (?,?,?,?,?,?,?)", (user_id, isbn, title, author, publisher_id, latitude, longitude))
        self.conn.commit()
        self.conn.close()
    def insert_chat(self, book_id, sender_id, recipient_id, message):
        self.cursor.execute("INSERT INTO Chats (book_id, sender_id, recipient_id, message) VALUES (?,?,?,?)", (book_id, sender_id, recipient_id, message))
        self.conn.commit()
        self.conn.close()
    def insert_transaction(self, book_id, buyer_id, seller_id, amount, payment_method):
        self.cursor.execute("INSERT INTO Transactions (book_id, buyer_id, seller_id, amount, payment_method) VALUES (?,?,?,?,?)", (book_id, buyer_id, seller_id, amount, payment_method))
        self.conn.commit()
        self.conn.close()
    def save_chat_message(self, book_id, user_id, content):
        """Save a chat message associated with a specific book."""
        try:
            self.cursor.execute(
                "INSERT INTO ChatMessages (book_id, user_id, content) VALUES (?, ?, ?)",
                (book_id, user_id, content)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error saving chat message: {e}")

    def get_user_by_username(self, username):
        try:
            
            self.cursor.execute("SELECT user_id, username, password_hash FROM Users WHERE username = ?", (username,))
            user = self.cursor.fetchone()
                
            if user:
                return {
                    'id': user[0],
                    'username': user[1],
                    'password_hash': user[2]
                }
            return None  # No user found
        except sqlite3.Error as e:
            print("Database error:", e)
            return None  # Handle the error appropriately
    def get_all_books(self):
        self.cursor.execute("SELECT book_id, title, latitude, longitude FROM Books")
        rows = self.cursor.fetchall()
        books = [{'book_id':row[0], 'title': row[1], 'latitude': row[2], 'longitude': row[3]} for row in rows]
        print(books)
        return books
    def get_chat_messages(self, book_id):
        self.cursor.execute("SELECT user_id, content FROM ChatMessages WHERE book_id = ?", (book_id,))
        rows = self.cursor.fetchall()
        
        # Convert tuples to dictionaries for better access
        messages = [{'user_id': row[0], 'content': row[1]} for row in rows]
        return messages





database().create_database()
database().insert_book(user_id = "1", isbn=9787535896797,title="世界名画",author="Null",publisher_id="Null",latitude="31.18",longitude="121.54")