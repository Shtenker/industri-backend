from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import os
import json
import sqlite3
from database import init_db, insert_order

app = Flask(__name__)
CORS(app)

# Submit order
@app.route("/submit-order", methods=["POST"])
def submit_order():
    data = request.json
    if not data or "products" not in data:
        return jsonify({"error": "Invalid request"}), 400

    order_id = str(uuid.uuid4())
    for index, product in enumerate(data["products"], start=1):
        # Use articleNumber as the product ID
        insert_order(order_id, product["id"], index)

    return jsonify({"message": "Order received", "order_id": order_id}), 201

# Serve products from JSON file
@app.route("/products")
def get_products():
    with open("industrial.json", "r") as f:
        products = json.load(f)
    return jsonify(products)

# View saved orders
@app.route("/orders")
def get_orders():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT order_id, product_id, line_number FROM orders")
    rows = cursor.fetchall()
    conn.close()

    orders = [{"order_id": row[0], "product_id": row[1], "line_number": row[2]} for row in rows]
    return jsonify(orders)

# Run the app
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
