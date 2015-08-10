#pyecoin
A python wrapper for e-coin (btc, ltc, etc) trading site.
Currently it support market information from 
 
 + btctrade.com
 + jubi.com
 + btc-e.com
 
And trading at 

 + btctrade.com
 + jubi.com

trading API from btc-e is much different from those two above, and will be supported soon.



##installation
###install from source
download the source, and then

```
python setup install
```
###install with pip

```
pip install pyecoin
```

##usage
### get market depth
```
from pyecoin import pyecoin
market = pyecoin.market_condition(market = "btctrade", coin = "ltc")
print market.get_depth()
```

###buy some bitcoin
```
from pyecoin import pyecoin
btctrade_pubkey = "{your public key}"
btctrade_secretkey = "{your secret key}"
dealer = pyecoin.dealer(market = "btctrade", coin = "btc", logging = True, public_key = btctrade_pubkey, secret_key = btctrade_secretkey)
#back in the golden age, when 1 bitcoin costs 10 RMB
dealer.buy(price = 10.0, amount = 10000)
```

