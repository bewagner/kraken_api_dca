import sys

import krakenex
from typing import Tuple
from enum import Enum

kraken = krakenex.API()
kraken.load_key('kraken.key')


# response = kraken.query_private('AddOrder',
#                                 {'pair': 'ALGOEUR',
#                                  'type': 'sell',
#                                  'ordertype': 'limit',
#                                  'price': 5,
#                                  'volume': 4,
#                                  'trading_agreement': 'agree'
#                                  })


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
        print("There was an error when accessing the Kraken API:")
        sys.exit(price_data["error"])
        # TODO Handle error
    if pair not in price_data:
        pass
    # TODO Handle error
    data = price_data['result'][pair]
    ok, price = get_current_price_from(data)
    if not ok:
        pass
    # TODO Handle error

    return price


class Crypto(Enum):
    ETH = 'XETHZEUR',
    BITCOIN = 'XXBTZEUR'


price = current_price("ALGOEUR")


print(price)
