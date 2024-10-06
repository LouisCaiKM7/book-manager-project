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

        # Creating Books table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publisher_id INTEGER,
            location TEXT,
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
    def insert_book(self, isbn, title, author, publisher_id, location):
        self.cursor.execute("INSERT INTO Books (isbn, title, author, publisher_id, location) VALUES (?,?,?,?,?)", (isbn, title, author, publisher_id, location))
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

database().create_database()
