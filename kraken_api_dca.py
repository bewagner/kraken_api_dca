import krakenex

from order import read_orders_from_file
from logger import Logger
if __name__ == "__main__":

    kraken = krakenex.API()
    kraken.load_key('kraken.key')
    logger = Logger("logs.txt")

    orders = read_orders_from_file(logger)
    for order in orders:
        order.place(kraken, logger)
