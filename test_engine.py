from data_handler import *

from Strategy import *

print "current version is ",
s = three_legs_strats.PutCallParity("a","b")
s.desc()
filepath = "C:\Users\Jianing Song\Documents\mkt_data\optiontick20150209-0420\FutureAB\SH\MultDate\\10000003.csv"

mktdata = Tick()

mktdata.format(["wind_code","date","time","volume","bid1","ask1","bsize1","asize1"])

mktdata.load(filepath)

mktdata.load_output_handler('strategy_update',s.mkt_update)

mktdata.play('strategy_update')