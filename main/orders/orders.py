from flask import *
from constants import ORDER_STATUS
from main.helpers import success, failure, schema_validator
from ..in_memory_db import *
import time
import threading

order_endpoint = Blueprint("order_endpoint", __name__)


def execute_order_after_delay(order_id):
    time.sleep(10)
    if orders[order_id]["status"] == ORDER_STATUS["PENDING"]:
        orders[order_id]["status"] = ORDER_STATUS["SUCCESS"]
        order_details = orders[order_id]
        coin = order_details["coin"]
        exchange = order_details["exchange"]
        if exchange in balances.keys():
            exchange_data = balances[exchange]

            if coin in exchange_data.keys():
                balances[exchange][coin] += order_details["amount"]
            else:
                balances[exchange][coin] = order_details["amount"]
        else:
            balances[exchange][coin] = order_details["amount"]


def check_exchange(exchange):
    return exchange in available_exchanges.keys()

def check_coin_present(exchange, coin):
    if check_exchange(exchange):
        if coin.upper() in available_exchanges[exchange].keys():
            return True
    else:
        return False
    
def can_buy(quantity, exchange, coin, balance_amount):
    is_present = check_coin_present(exchange, coin)

    if is_present:

        amount_needed = quantity * available_exchanges[exchange][coin.upper()]

        if amount_needed <= balance_amount:

            balance_amount -= quantity

            return True, amount_needed
        else:
            return False, None
    else:
        return False, None

@order_endpoint.route("/", methods = ["GET"])
def order_list():
    return success(orders)


@order_endpoint.route("/place_order", methods = ["POST"])
def place_order():
    
    request_data = request.get_json()

    order_schema = { 
        "coin" : {"type" : "string", "required" : True , "empty" : False},
        "quantity" : {"type" : "integer", "required" : True, "empty" : False},
        "exchange" : {"type" : "string", "required" : True, "empty" : False}
    }

    status, error = schema_validator(order_schema, request_data)

    if status:
        coin = request_data["coin"]
        exchange = request_data["exchange"]
        quantity = request_data["quantity"]
        is_buy_possible, amount = can_buy(quantity, exchange, coin, balance_amount)
        if is_buy_possible:
            order_id = str(time.time())
            orders[order_id] = {
                'status': ORDER_STATUS["PENDING"],
                'coin' : coin,
                'amount': amount,
                'exchange': exchange
            }

            threading.Thread(target=execute_order_after_delay, args=(order_id,)).start()

            return success({"order_id": order_id, "status": "Order placed, will be executed after 60 seconds"})
        
        else:
            return failure("Something wrong occured.", 500)
            
    else:
        return failure(error)


