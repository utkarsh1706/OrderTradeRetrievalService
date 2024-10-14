import json
from schema import *

def getAllTrades(redisClient):
    data = [json.loads(item) for item in redisClient.lrange('tradeData', 0, -1)]
    
    if not data:
        print("No trades found in Redis, checking MongoDB!")
        trades = Trade.objects()  
        if not trades:
            print("No trades yet in MongoDB.")
            return []  
        data = [trade.to_mongo().to_dict() for trade in trades] 
    return data  