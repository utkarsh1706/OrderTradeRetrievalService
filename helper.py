import json
from schema import *

def getAllTrades(redisClient):
    try:
        data = [json.loads(item) for item in redisClient.lrange('tradeData', 0, -1)]
        
        if not data:
            print("No trades found in Redis, checking MongoDB!")
            trades = Trade.objects()  
            if not trades:
                print("No trades yet in MongoDB.")
                return []  
            data = [trade.to_mongo().to_dict() for trade in trades]
        
        return data
    
    except Exception as e:
        print(f"Error retrieving trades: {e}")
        return []

def getOrderInfoMongo(orderId):
    try:
        print("Checking MongoDB for orderID:", orderId)
        order = Orders.objects.get(oid=orderId)
        orderInfo = {
            "order_price": order.price,
            "order_quantity": order.quantity,
            "average_traded_price": order.averagePrice,
            "traded_quantity": order.filledQuantity,
            "order_alive": 1 if order.status in [OrderStatus.OPEN, OrderStatus.PARTIALLY_FILLED] else 0
        }
        return orderInfo
    except Exception as e:
        print(f"Error retrieving order {orderId} from MongoDB: {e}")
        return None

def getOrderInfo(redisClient, oid):
    try:
        orderKey = f"order:{oid}"
        orderData = redisClient.hgetall(orderKey)
        if not orderData:
            print(f"No order found with ID: {oid} in Redis")
            return getOrderInfoMongo(oid)
        
        orderData = {k.decode('utf-8'): v.decode('utf-8') for k, v in orderData.items()}
        orderInfo = {
            "order_price": float(orderData.get("price", 0)),
            "order_quantity": float(orderData.get("quantity", 0)),
            "average_traded_price": float(orderData.get("averagePrice", 0)),
            "traded_quantity": float(orderData.get("filledQuantity", 0)),
            "order_alive": 1 if orderData.get("status") in ["OPEN", "PARTIALLY FILLED"] else 0
        }
        return orderInfo
    
    except Exception as e:
        print(f"Error retrieving order {oid}: {e}")
        return None

def getAllOrders(redisClient):
    try:
        keys = redisClient.keys("order:*")
        
        orders = []
        
        if keys:
            for key in keys:
                orderData = redisClient.hgetall(key)
                if orderData:
                    orderData = {k.decode('utf-8'): v.decode('utf-8') for k, v in orderData.items()}
                    orderInfo = {
                        "order_price": float(orderData.get("price", 0)),
                        "order_quantity": float(orderData.get("quantity", 0)),
                        "average_traded_price": float(orderData.get("averagePrice", 0)),
                        "traded_quantity": float(orderData.get("filledQuantity", 0)),
                        "order_alive": 1 if orderData.get("status") in ["OPEN", "PARTIALLY_FILLED"] else 0
                    }
                    orders.append(orderInfo)
        else:
            print("Checking orders in MongoDB")
            mongo_orders = Orders.objects.all()
            if mongo_orders:
                for order in mongo_orders:
                    orderInfo = {
                        "order_price": order.price,
                        "order_quantity": order.quantity,
                        "average_traded_price": order.averagePrice,
                        "traded_quantity": order.filledQuantity,
                        "order_alive": 1 if order.status in [OrderStatus.OPEN, OrderStatus.PARTIALLY_FILLED] else 0
                    }
                    orders.append(orderInfo)

        return orders if orders else None
        
    except Exception as e:
        print(f"Error retrieving orders: {e}")
        return None