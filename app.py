from flask import Flask, jsonify, request
from constants import *
import redis
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from helper import *
import os
from schema import *
from dotenv import load_dotenv
from mongoengine import connect

app = Flask(__name__)
load_dotenv()

mongoURI = os.getenv("mongoURI")
connect(db="StockBrokerSystem", host = mongoURI)

try:
    redisClient = redis.Redis(host=redisHost, port=redisPort, password=redisPassword)
    redisClient.ping()
    print("Connected to Redis")
except redis.ConnectionError as e:
    print("Redis not connected due to ", e)

# Initialize the Limiter with default rate limiting settings and redis as the storage backend
limiter = Limiter(get_remote_address, app=app, default_limits=["1000 per minute"], storage_uri=storageRateLimit)

@app.route('/api/fetch_trades', methods=['GET'])
@limiter.limit("100 per minute")
def fetchTradesAPI():
    
    print("Received request for fetching all trades")
    trades = getAllTrades(redisClient)

    if not trades:
        return jsonify({"success": True, "message": "No trades available", "data": []}), 200
    
    return jsonify({"success": True, "data": trades}), 200

@app.route('/api/fetch_order', methods=['GET'])
@limiter.limit("100 per minute")
def fetchOrderAPI():
    
    print("Received request for fetching an order")
    data = request.json
    print("Data received:", data)

    if not data or 'order_id' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    order = getOrderInfo(redisClient, data['order_id'])
    if not order:
        return jsonify({"error": "Invalid Order_ID"}), 400

    return jsonify({"success": True, "data": order}), 200

@app.route('/api/fetch_allOrders', methods=['GET'])
@limiter.limit("100 per minute")
def fetchAllOrdersAPI():
    
    print("Received request for fetching all orders")
    
    orders = getAllOrders(redisClient)
    if not orders:
        return jsonify({"error": "No orders yet!"}), 400

    return jsonify({"success": True, "data": orders}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0') 
