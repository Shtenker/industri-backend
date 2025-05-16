from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import uuid
import os
import json
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
    return send_from_directory(os.path.abspath(os.path.dirname(__file__)), 'industrial.json')

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
