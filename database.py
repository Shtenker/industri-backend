import sqlite3

def init_db():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT,
            line_number INTEGER,
            product_id TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_order(order_id, product_id, line_number):
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (order_id, line_number, product_id)
        VALUES (?, ?, ?)
    """, (order_id, line_number, product_id))
    conn.commit()
    conn.close() 