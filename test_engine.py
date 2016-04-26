from data_handler import *

filepath = "C:\Users\Jianing Song\Documents\mkt_data\optiontick20150209-0420\FutureAB\SH\MultDate\\10000002.csv"

mktdata = Tick()

mktdata.format(["wind_code","date","time","volume","bid1","ask1","bsize1","asize1"])

mktdata.load(filepath)

mktdata.play()