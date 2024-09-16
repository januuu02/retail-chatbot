import sqlite3

def create_database():
    conn = sqlite3.connect('chatbot_database.db')
    cursor = conn.cursor()

    # Create sales_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            product_id INTEGER,
            quantity INTEGER,
            total_price REAL,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')

    # Create customer_queries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            response TEXT
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print("Database and tables created successfully.")
