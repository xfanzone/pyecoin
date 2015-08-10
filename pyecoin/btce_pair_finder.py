import itertools
import requests

coin_types = ['btc', 'ltc', 'nmc', 'trc', 'ppc', 'ftc', 'xpm', 'usd', 'rur', 'eur', 'chn', 'gbp']
for ele in itertools.product(coin_types, coin_types):
	pair = "{0}_{1}".format(*ele)
	url = "https://btc-e.com/api/3/ticker/{0}".format(pair)
	r = requests.get(url).json()
	if 'success' in r and r['success'] == 0:
		pass
	else:
		print '"{0}",'.format(pair),