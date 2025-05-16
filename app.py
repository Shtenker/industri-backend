from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from database import init_db, insert_order
import json

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

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

from flask import send_from_directory
import os

@app.route('/products')
def get_products():
    return send_from_directory(os.path.abspath(os.path.dirname(__file__)), 'industrial.json')
