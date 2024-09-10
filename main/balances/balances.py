from flask import Blueprint
from ..helpers import success, failure
from ..in_memory_db import *

balance_endpoints = Blueprint("balance_endpoints", __name__)


@balance_endpoints.route("/", methods = ["GET"])
def balances_endpoint():
    return success(balances)

@balance_endpoints.route("/<exchange_id>", methods = ["GET"])
def get_holdings(exchange_id):
    if exchange_id in balances:

        return success(balances[exchange_id])
    
    else:
        return failure("Exchange not found in portfolio", 404)