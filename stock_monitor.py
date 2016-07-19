from WindEngine import WindEngine as WE
import pandas as pd
stock_pool_file = "C:\Users\Jianing Song\Desktop\stockpool.csv"
stock_pool = pd.read_csv(stock_pool_file,skiprows=0,usecols=[0])
stock_pool.columns = ['ticker']
tickers = (stock_pool['ticker'].apply(lambda x:".".join([x[2:],x[:2]]))).tolist()
print tickers
fields   = ["rt_time","rt_last","rt_bid1","rt_bsize1","rt_ask1","rt_asize1"]
fields   = [each.upper() for each in fields]
data_source = WE(tickers,fields)
data_source.run()
