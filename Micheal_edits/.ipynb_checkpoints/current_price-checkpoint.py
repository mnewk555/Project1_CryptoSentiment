import cryptocompare
def current_price(ticker):
    tick = ticker
    ticker = dict(cryptocompare.get_price(ticker,curr='USD',full=False))
    return ['USD']
