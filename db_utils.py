import sqlite3

def get_sales_data():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sales')
    rows = cursor.fetchall()
    conn.close()

    sales_data = [
        {'id': row[0], 'product_name': row[1], 'sale_amount': row[2], 'sale_date': row[3]}
        for row in rows
    ]
    return sales_data

def get_chat_history():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM chat_history ORDER BY timestamp')
    rows = cursor.fetchall()
    conn.close()

    chat_history = [
        {'timestamp': row[0], 'message': row[1], 'sender': row[2]}
        for row in rows
    ]
    return chat_history

def insert_chat_message(message, sender):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            message TEXT,
            sender TEXT
        )
    ''')
    cursor.execute('INSERT INTO chat_history (message, sender) VALUES (?, ?)', (message, sender))
    conn.commit()
    conn.close()
