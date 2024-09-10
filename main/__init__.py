from .helpers import *
from flask import *

app = Flask(__name__)

from .balances.balances import balance_endpoints
from .withdraw.withdraw import withdraw
from .orders.orders import order_endpoint

app.register_blueprint(balance_endpoints, url_prefix = "/balances")
app.register_blueprint(withdraw, url_prefix = "/withdraw")
app.register_blueprint(order_endpoint, url_prefix = "/orders")

@app.route("/", methods= ["GET"])
def health_check():
    return success("Server is up and running")