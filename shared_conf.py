headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0', 'Content-Type':'application/x-www-form-urlencoded'}

btctrade_api = {'ticker': 'ticker', 'depth':'depth', 'trades': 'trades', \
'balance': 'balance', 'orders': 'orders', 'fetch_order': 'fetch_order', \
'cancel_order': 'cancel_order', 'buy': 'buy', 'sell': 'sell'}

jubi_api = {'ticker': 'ticker', 'depth': 'depth', 'trades':'orders', \
'balance': 'balance', 'orders': 'trade_list', 'fetch_order': 'trade_view', \
'cancel_order': 'trade_cancel', 'buy': 'trade_add', 'sell': 'trade_add'}

btce_api = {'ticker': 'ticker', 'depth': 'depth', 'trades':'trades'}

support_market = ('btc-e', 'jubi', 'btctrade')

btce_pairs = ("btc_usd", "btc_rur", "btc_eur", "ltc_btc", "ltc_usd", "ltc_rur", "ltc_eur", "nmc_btc", "nmc_usd", "ppc_btc", "usd_rur", "eur_usd", "eur_rur",)
