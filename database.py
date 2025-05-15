import sqlite3

def init_db():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT,
            row_number INTEGER,
            product_id TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_order(order_id, product_id, row_number):
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (order_id, row_number, product_id) VALUES (?, ?, ?)",
                   (order_id, row_number, product_id))
    conn.commit()
    conn.close()
