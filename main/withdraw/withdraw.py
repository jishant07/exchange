from flask import *
from main.helpers import schema_validator, success, failure
from ..in_memory_db import *

from cerberus import Validator

withdraw = Blueprint("withdraw", __name__)


@withdraw.route("/", methods = ["POST"])
def withdraw_endpoint():
    
    request_data = request.get_json()

    withdraw_schema = {
        "coin" : {"type" : "string", "required" : True , "empty" : False},
        "amount" : {"type" : "float", "required" : True, "empty" : False},
        "exchange" : {"type" : "string", "required" : True, "empty" : False},
        "wallet_address" : {"type" : "string", "required" : True, "empty" : False}
    }

    status, error = schema_validator(withdraw_schema, request_data)

    if(status):
        coin = request_data["coin"].upper()
        amount = request_data["amount"]
        exchange = request_data["exchange"]
        request_wallet_address = request_data["wallet_address"]
        if balances[exchange][coin] >= amount:
            if request_wallet_address in whitelisted_addresses:
                balances[exchange][coin] -= amount
                return success({"remaining_balance" : balances[exchange][coin]})
            else:
                return failure("Wallet address not whitelisted", 403)
        else:
            return failure("Not enough balance to withdraw requested amount", 403)
    else:
        return failure(error)
