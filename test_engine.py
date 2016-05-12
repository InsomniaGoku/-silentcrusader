from data_handler import *
from option_model import implied_volatility,BS
from Strategy import *

print "current version is ",
s = three_legs_strats.PutCallParity("a","b")
s.desc()


# init option model:
call = BS((0.0971,0.1,0,30),16)
print(call._price())
filepath = "C:\Users\Jianing Song\Documents\mkt_data\\50etf\Opt_Tick_201604\\20160401\OP10000449.csv"

mktdata = Tick()

mktdata.format(["Price","Volume","BP1","SP1","BV1","SV1"])

mktdata.load(filepath)

mktdata.load_output_handler('strategy_update',call.update)

mktdata.play('strategy_update')