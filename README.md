# What does it do?

# Dependencies

To install the required Python dependencies run:

```commandline
pip install -r requirements.txt
```

# Usage

To use the script, you need to:

- Create a Kraken API key and save it to the file `kraken.key`.
  [See here for an explanation.](#kraken-api-key)
- Specifiy your orders in the file `orders.json`
  . [See this description of how to place your orders.](#specifying-your-orders)
- Run the script via `python3 kraken_api_dca.py`

## Kraken API key

To use this script, you need a Kraken API key. To create your API key, click on your profile icon. Then go
to `Security->API`.

TODO ... TODO image

## Specifying your orders

You can specify with orders you want to place in the file `orders.json`. The file contains a list of orders in JSON
format. Each order object contains the following fields:

- `pair (string)`: The trading pair you want to buy (for example `ALGOUSD` for trading Algorand for US$). Have a look
  at `trading_pairs.txt` for an overview of all trading pairs. Note that Bitcoin is called `XBT`.
- `amount_in_fiat (number)`: The amount you want to buy (in fiat currency). E.g. if you want to buy 400$ of Bitcoin,
  enter `400` and choose the `XXBTZUSD` trading pair.
- `debug (boolean)`: This gives you the possibility to test the script before you let it place orders for you. If you
  set `debug:true` the order will be placed as a limit order for 1% of the current price. This is, so you can verify
  that the order is created and delete the order before it is executed. After you checked that everything worked,
  set `debug:false` for all your orders.

An example `orders.json` could look like this:

```json5
[
  {
    "pair": "XETHZEUR",
    "amount_in_fiat": 100,
    "debug": true
  },
  {
    "pair": "XXBTZUSD",
    "amount_in_fiat": 200,
    "debug": true
  }
]
```

This would create two orders. The first order buys 100$ of Ether, the second order buys 200$ of Bitcoin. Both orders
have debug mode activated, which means they will be placed as limit orders on 1% of the current price. This way you can
check that everything works out, delete the created orders and set `debug:false` once you want to start using the
script.

## How can you automate calling the script

TODO

# Use at your own risk

This code is correct to the best of my knowledge and belief. If you decide to use it, you do so at your own risk. I will
not be liable for any loses or damages in connection with using my code.

TODO Mention logging