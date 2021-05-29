import krakenex

from order import read_orders_from_file

if __name__ == "__main__":

    kraken = krakenex.API()
    kraken.load_key('kraken.key')

    orders = read_orders_from_file()
    for order in orders:
        order.place(kraken)
