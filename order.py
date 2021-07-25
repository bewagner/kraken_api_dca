import json
from enum import Enum
from pathlib import Path
from typing import List

from logger import Logger
from price_calculation import current_price, round_to_amount_of_decimals_kraken_accepts, calculate_volume_from_price


class OrderStyle(Enum):
    buy = 1
    sell = 2


class OrderType(Enum):
    market = 1
    limit = 2


class Order:
    def __init__(self, pair: str,
                 amount_in_fiat: int,
                 debug: bool,
                 order_style: OrderStyle = OrderStyle.buy,
                 order_type: OrderType = OrderType.limit,
                 ):
        self.pair = pair
        self.amount_in_fiat = amount_in_fiat
        self.order_style = order_style
        self.order_type = order_type
        self.debug = debug

    def __repr__(self):
        return f"[pair: {self.pair}, amount_in_fiat: {self.amount_in_fiat}, debug: {self.debug}]"

    def place(self, kraken, logger: Logger):
        """
        Place an order via the Kraken API
        :param logger: Logger to write logging strings to
        :param kraken: Handle to the Kraken API
        """
        logger.log(f"Start placing order {self}")
        order_string = f"ORDER: pair: {self.pair}, " \
                       f"amount in fiat: {self.amount_in_fiat}, " \
                       f"style: {self.order_style.name}, " \
                       f"type: {self.order_type.name}"

        try:
            current_crypto_price = current_price(self.pair, kraken)
        except ValueError as exception:
            if "Unknown asset pair" in exception.args[0]:
                logger.exit(order_string
                            + "\n"
                              f"ERROR: You specified an unknown trading pair: {self.pair}"
                              f"\nSee here for a full list of all trading pairs "
                              f"https://support.kraken.com/hc/en-us/articles/360000920306-Ticker-pairs#:~:text="
                              f"A%20Ticker%20is%20a%20report,example%20the%20trading%20pair%20BTCEUR.&text="
                              f"This%20Ticker%20example%20will%20pull,re%20deployed%20to%20our%20platform.")

            if "Data extraction error" in exception.args[0]:
                logger.exit(order_string + "\nERROR: There was an error while extracting data from the Kraken API.")

            logger.exit(order_string + f"ERROR: {exception.args}")

        current_crypto_price = round(current_crypto_price, 3)

        # In debug mode, we set a limit order at 1% of the current price.
        # This way the user can check if everything works and cancel their order later.
        debug_multiplier = 1
        if self.debug:
            self.order_type = OrderType.limit
            debug_multiplier = 0.01

        order_price = round_to_amount_of_decimals_kraken_accepts(current_crypto_price * debug_multiplier)
        response = kraken.query_private('AddOrder',
                                        {'pair': self.pair,
                                         'type': self.order_style.name,
                                         'ordertype': self.order_type.name,
                                         'price': order_price,
                                         'volume': calculate_volume_from_price(self.amount_in_fiat,
                                                                               current_crypto_price),
                                         'trading_agreement': 'agree'
                                         })
        if response['error']:
            errors = response['error']

            if any("Invalid arguments:volume" in e for e in errors):
                logger.exit(order_string
                            + "\nERROR: The volume you specified for your order was invalid.\n"
                              "This probably means the specified fiat amount was too low.\n"
                              "See https://support.kraken.com/hc/en-us/articles/"
                              "205893708-Minimum-order-size-volume-for-trading "
                              "for the minimum required order sizes.")
            if any("Insufficient funds" in e for e in errors):
                logger.exit(order_string
                            + "\nERROR: Insufficient funds. "
                              "Your Kraken account does not contain enough funds for this order.")

            logger.exit(order_string + f"ERROR: {errors}")

        logger.log(f"Placed order: {self}\n")


def read_orders_from_file(logger: Logger) -> List[Order]:
    """
    Read orders from the orders.json file.
    Also, make sure they are formatted correctly and check the value types.
    :param logger: Logger to write logging strings to
    :return: Orders read from file
    """
    orders_file = Path("orders.json")
    if not orders_file.exists():
        logger.exit("ERROR: Couldn't find an order file orders.json. "
                    "Make sure this file exists in the same directory as kraken_api_dca.py")
    try:
        orders_file_content = orders_file.open("r").read()
    except Exception as e:
        logger.exit(f"ERROR: There was an error while reading the orders file.\n{e}")
    try:
        orders_json = json.loads(orders_file_content)
    except json.JSONDecodeError as e:
        logger.exit(f"ERROR: There was an error while decoding your orders file. "
                    f"Please make sure you wrote valid JSON.\n{e}")

    orders = []
    for order in orders_json:
        def check_parameter(parameter: str, desired_type):
            if parameter not in order or not isinstance(order[parameter], desired_type):
                logger.exit(f"ERROR: Your order\n{order}\ndid not contain a valid value for '{parameter}'."
                            "\nMake sure your JSON input in orders.json is correct.")

        check_parameter("pair", str)
        check_parameter("amount_in_fiat", (float, int))
        check_parameter("debug", bool)

        orders.append(Order(pair=order["pair"], amount_in_fiat=order["amount_in_fiat"], debug=order["debug"]))

    if orders:
        logger.log("Read the following orders from the orders.json file:")
        for order in orders:
            logger.log(f"\t- {order}")

    return orders
