# Kraken API Dollar cost averaging script

Hi! If you're looking for a way to automate your regular crypto purchases via [Kraken](https://www.kraken.com/), you
have come to the right place. The `kraken_api_dca.py` script allows you to specify orders in all trading pairs on
Kraken. Just let your computer run the script at regular intervals and you have your
automated [Dollar cost averaging](https://en.wikipedia.org/wiki/Dollar_cost_averaging) bot.

[![Python package](https://github.com/bewagner/kraken_api_dca/actions/workflows/workflow.yml/badge.svg?branch=main)](https://github.com/bewagner/kraken_api_dca/actions/workflows/workflow.yml)
# Support
If this code is useful to you, consider supporting me! This way I can continue maintaining and improving your DCA script.

![Ko-fi logo](/images/kofiLogo.png)
![Patreon logo](/images/patreonLogo.png)

# Dependencies

This script needs the `krakenex` pip package. To install it run

```commandline
pip install -r requirements.txt
```

# Usage

To use the script, you need to:

- Create a Kraken API key and save it to the file `kraken.key`.
  [See here for an explanation.](#kraken-api-key)
- Create a file `orders.json` and specify your orders.
  . [See this description of how to place your orders.](#specifying-your-orders)
- Run the script via `python3 kraken_api_dca.py`

## Kraken API key

To use this script, you need a Kraken API key that allows creating orders.

Below we explain how to create an API key if you don't have one already.

### How to create an API key

To create your API key, click on your profile icon. Then go to `Security->API`. You will see the following screen.

![API key screen](/images/API-key-screen.png)

Click on 'Add key' to add a new API key.

![API key screen with 'add key' button highlighted](/images/API-key-screen-with-button-highlight.png)
This will take you to the next screen.

![API creation screen which allows choosing the API key rights](/images/add-API-key.png)

Make sure you check **Create & Modify Orders**.

You should not check any other fields. Especially **not** 'Withdraw Funds', as this would allow people with access to
your API key to withdraw your funds.

Then click on 'Generate key'.

![API creation screen which allows choosing the API key rights, with highlight on 'generate key' button.](/images/add-API-key-button-highlight.png)

This creates your key and takes you to the next screen. Here you see your public and private key. This is the
information you have to store in the `kraken.key` file.


![API creation screen](/images/final-screen.png)
Copy the information from the 'API key' line and write it into the first line in `kraken.key`.
![API creation screen with highlight on API key](/images/final-screen-api-key-highlight.png)

Then copy the private key and save it in the second line of `kraken.key`.

![API creation screen with highlight on private key](/images/final-screen-private-key-highlight.png)

Finally, click 'Save.'

Your `kraken.key` file should look like this.

```text
<API key>
<Private key>
```

## Specifying your orders

To specify your orders, create a file called `orders.json`. The file should contain a list of orders in JSON format.
Each order object can contain the following fields:

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
    "pair": "XETHZUSD",
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

### Linux

On Linux you can use `anacron` to schedule execution of the script. To run the script monthly, you can add the following
line to `/etc/anacrontab`:

```text
@monthly 7 kraken-api-dca-script cd ~/kraken_api_dca && python3 ~/kraken_api_dca/kraken_api_dca.py
```

`anacron` has the advantage over `cron` that if your computer is turned off, the script will be executed the next time
the computer is turned on.
[See here](https://kifarunix.com/scheduling-tasks-using-anacron-in-linux-unix/) for more information on `anacron`.

### Windows

On Windows you could try the following library to schedule script execution:
[Advanced Python Scheduler](https://apscheduler.readthedocs.io/en/stable/)
(Note: I couldn't test this, since I don't have a Windows machine)

## Logging

The script will write logs to a file called `logs.txt`. Check this file for the results of your API calls.

# Use at your own risk

This code is correct to the best of my knowledge and belief. If you decide to use it, you do so at your own risk. I will
not be liable for any losses or damages in connection with using my code.

