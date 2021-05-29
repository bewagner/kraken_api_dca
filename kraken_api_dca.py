import sys
from enum import Enum
from typing import Tuple

import krakenex

kraken = krakenex.API()
kraken.load_key('kraken.key')


def get_current_price_from(data) -> Tuple[bool, float]:
    """
    TODO
    :param data:
    :return:
    """
    if not data:
        return False, 0
    AMOUNT_INDEX = -1
    CLOSING_PRICE_INDEX = -3

    for entry in data:
        amount = entry[AMOUNT_INDEX]
        if amount == 0:
            continue
        return True, float(entry[CLOSING_PRICE_INDEX])

    return False, 0


def current_price(pair: str) -> float:
    price_data = kraken.query_public('OHLC', data={'pair': pair})
    if price_data['error']:
        raise ValueError(price_data['error'][0])
    if pair not in price_data['result']:
        raise ValueError("Data extraction error")

    data = price_data['result'][pair]
    ok, price = get_current_price_from(data)
    if not ok:
        raise ValueError("Data extraction error")

    return round_to_amount_of_decimals_kraken_accepts(price)


def calculate_volume_from_price(fiat_volume: float, crypto_price: float) -> float:
    """
    Calculate the order volume in crypto from a given fiat amount.
    Example: if crypto_price is 1000€ and your fiat_volume is 100€, the volume of your order can be 0.1 crypto.
    :param fiat_volume: Amount of fiat to spend.
    :param crypto_price: Current price of the crypto you want to buy
    :return: Calculated crypto volume
    """
    volume = fiat_volume / crypto_price
    return round_to_amount_of_decimals_kraken_accepts(volume)


class OrderStyle(Enum):
    buy = 1
    sell = 2


class OrderType(Enum):
    market = 1
    limit = 2


def round_to_amount_of_decimals_kraken_accepts(number: float) -> float:
    """
    Round to the number of decimals the Kraken API accepts
    :param number: Number to round
    :return: Rounded number
    """
    # The Kraken API only accepts up to five decimals.
    number_of_accepted_decimals = 5
    return round(number, number_of_accepted_decimals)


def place_order(pair: str, amount_in_fiat: float, order_style: OrderStyle, order_type: OrderType, debug=False):
    order_string = f"ORDER: pair: {pair}, amount in fiat: {amount_in_fiat}, style: {order_style.name}, type: {order_type.name}"

    try:
        current_crypto_price = current_price(pair)
    except ValueError as exception:
        if "Unknown asset pair" in exception.args[0]:
            sys.exit(order_string
                     + "\n"
                       f"ERROR: You specified an unknown trading pair: {pair}"
                       f"\nSee here for a full list of all trading pairs "
                       f"https://support.kraken.com/hc/en-us/articles/360000920306-Ticker-pairs#:~:text=A%20Ticker%20is%20a%20report,example%20the%20trading%20pair%20BTCEUR.&text=This%20Ticker%20example%20will%20pull,re%20deployed%20to%20our%20platform.")

        if "Data extraction error" in exception.args[0]:
            sys.exit(order_string + "\nERROR: There was an error while extracting data from the Kraken API.")

        sys.exit(order_string + f"ERROR: {exception.args}")

    current_crypto_price = round(current_crypto_price, 3)

    # In debug mode, we se a limit order at 1% of the current price.
    # This way the user can check if everything works and cancel their order later.
    debug_multiplier = 1
    if debug:
        order_type = OrderType.limit
        debug_multiplier = 0.01

    response = kraken.query_private('AddOrder',
                                    {'pair': pair,
                                     'type': order_style.name,
                                     'ordertype': order_type.name,
                                     'price': round_to_amount_of_decimals_kraken_accepts(
                                         current_crypto_price * debug_multiplier),
                                     'volume': calculate_volume_from_price(amount_in_fiat, current_crypto_price),
                                     'trading_agreement': 'agree'
                                     })
    if response['error']:
        errors = response['error']

        if any("Invalid arguments:volume" in e for e in errors):
            sys.exit(order_string
                     + "\nERROR: The volume you specified for your order was invalid.\n"
                       "This probably means the specified fiat amount was too low.\n"
                       "See https://support.kraken.com/hc/en-us/articles/205893708-Minimum-order-size-volume-for-trading"
                       "for the minimum required order sizes.")
        if any("Insufficient funds" in e for e in errors):
            sys.exit(order_string
                     + "\nERROR: Insufficient funds. Your Kraken account does not contain enough funds for this order.")

        sys.exit(order_string + f"ERROR: {errors}")

    print(response)


place_order("ALGOEUR", amount_in_fiat=500, order_style=OrderStyle.buy, order_type=OrderType.limit, debug=True)
