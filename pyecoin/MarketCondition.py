import requests
from CustomErrors import *
import ast
import logging
import time
import pdb
from shared_conf import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)20s - %(name)20s - %(levelname)20s - %(message)20s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class MarketCondition:

	def __init__(self, market = "btctrade", coin = "ltc", coin2 = None, logging = False):
		if logging:
			logger.info('initilize. market: %s, coin type: %s', market, coin)
		if market not in support_market:
			raise Exception("Unknown market. Report to xfanzone@gmail.com to add support.")
		self._market = market
		if self._market == "btctrade":
			self._base_url = "http://api.btctrade.com/api"
		if self._market == "jubi":
			self._base_url = "http://www.jubi.com/api/v1"
		if self._market == "btc-e":
			self._base_url = "https://btc-e.com/api/3"
		self._coin = coin
		if market != "btc-e" and coin2 is not None:
			if logging:
				logger.warning("does not support set pair")
			coins = None
		self._coin2 = coin2
		self._adjust_pair()
		self._logging = logging

	@property 
	def coin(self):
		return self._coin

	@coin.setter
	def coin(self, value):
		if self._logging:
			logger.info('coin type set to %s', value)
		self._coin = value
		self._adjust_pair()

	@property 
	def coin2(self):
		return self._coin2

	@coin2.setter
	def coin2(self, value):
		if self._logging:
			logger.info('coin2 type set to %s', value)
		self._coin2 = value
		self._adjust_pair()


	def get_ticker(self):
		#url construction
		url = self._get_request_url('ticker')
		#make the request
		if self._logging:
			logger.info('request for %s', url)
		r = requests.get(url, headers = headers)
		#check http status
		if r.status_code != 200:
			raise ServerError(r.status_code)	
		#parse and check content
		resp = r.json()
		self._check_resp(resp)

		#market specific operation
		#jubi does not come with server time.
		if self._market == "jubi":
			resp['time'] = time.time()

		return resp


	def get_depth(self):
		url = self._get_request_url('depth')
		if self._logging:
			logger.info('request for %s', url)
		r = requests.get(url, headers = headers)
		if r.status_code != 200:
			raise ServerError(r.status_code)	
		resp = r.json()
		self._check_resp(resp)

		#market specific operation
		#btctrade comes with an additional 'result' key 
		if 'result' in resp:
			del resp['result']
		if self._market in ('jubi', 'btctrade'):
			asks = resp["asks"]
			resp["asks"] = [[float(x[0]), float(x[1])] for x in asks]
			bids = resp["bids"]
			resp["bids"] = [[float(x[0]), float(x[1])] for x in bids]
		return resp


	def get_trades(self):
		url = self._get_request_url('trades')
		if self._logging:
			logger.info('request for %s', url)
		r = requests.get(url, headers = headers)
		if r.status_code != 200:
			raise ServerError(r.status_code)	
		resp = r.json()
		if 'result' in resp and resp['result'] == False:
			if 'message' in resp:
				raise Exception(resp['message'])
			else:
				raise Exception("unkonwn return content")
		return resp

	def _check_resp(self, resp):
		if 'result' in resp and resp['result'] == False:
			if 'message' in resp:
				raise Exception(resp['message'], self._market)
			elif 'code' in resp:
				raise Exception(resp['code'], self._market)
			else:
				raise Exception("unkonwn return content")

	def _get_request_url(self, request_type):
		if self._market == "btctrade":
			url = "{0}/{1}?coin={2}".format(self._base_url, btctrade_api[request_type], self._coin)
		elif self._market == "jubi":
			url = "{0}/{1}/?coin={2}".format(self._base_url, jubi_api[request_type], self._coin)
		elif self._market == "btc-e":
			if self._coin is None or self._coin2 is None:
				raise Exception("illegal pair")
			url = "{0}/{1}/{2}_{3}".format(self._base_url, btce_api[request_type], self._coin, self._coin2)
		return url

	def _adjust_pair(self):
		if self._market != "btc-e":
			return 
		if self._coin is None or self._coin2 is None:
			return
		pair = "{0}_{1}".format(self._coin, self._coin2)
		if pair not in btce_pairs:
			pair = "{0}_{1}".format(self._coin2, self._coin)
			if pair in btce_pairs:
				(self._coin, self._coin2) = (self._coin2, self._coin)
			else:
				raise Exception("illegal pair")
