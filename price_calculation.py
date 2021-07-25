from typing import Tuple


def get_current_price_from(data) -> Tuple[bool, float]:
    """
    Get the current price of a crypto trading pair from the data the Kraken API returned
    :param data: Data returned by the Kraken API
    :return: Current price of crypto trading pair
    """
    if not data:
        return False, 0
    amount_index = -1
    closing_price_index = -3

    for entry in data:
        amount = entry[amount_index]
        if amount == 0:
            continue
        return True, float(entry[closing_price_index])

    return False, 0


def current_price(pair: str, kraken) -> float:
    """
    Get the current price of a crypto trading pair from the Kraken API
    :param kraken: Handle to the Kraken API
    :param pair: Trading pair
    :return: Current price of the trading pair
    """
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


def round_to_amount_of_decimals_kraken_accepts(number: float) -> float:
    """
    Round to the number of decimals the Kraken API accepts
    :param number: Number to round
    :return: Rounded number
    """
    # The Kraken API only accepts up to five decimals.
    number_of_accepted_decimals = 1
    return round(number, number_of_accepted_decimals)


