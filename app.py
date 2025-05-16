from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import os
import json
import sqlite3
from database import init_db, insert_order

app = Flask(__name__)
CORS(app)


@app.route("/submit-order", methods=["POST"])
def submit_order():
    data = request.json
    if not data or "products" not in data:
        return jsonify({"error": "Invalid request"}), 400

    order_id = str(uuid.uuid4())
    for index, product in enumerate(data["products"], start=1):
       
        insert_order(order_id, product["id"], index)

    return jsonify({"message": "Order received", "order_id": order_id}), 201


@app.route("/products")
def get_products():
    with open("industrial.json", "r") as f:
        products = json.load(f)
    return jsonify(products)

@app.route("/orders")
def get_orders():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT order_id, product_id, row_number FROM orders")
    rows = cursor.fetchall()
    conn.close()

    orders = [{"order_id": row[0], "product_id": row[1], "row_number": row[2]} for row in rows]
    return jsonify(orders)


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
