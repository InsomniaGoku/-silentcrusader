from WindEngine import WindEngine as WE
import pandas as pd

''' check ma: check current market price against MA with different periods'''
def check_ma((mkt_data,updated_keys)):
    print "check ma"
    epsilon = 0.001
    for each in updated_keys:
        #print mkt_data
        mid_price = (mkt_data[each]["RT_BID1"] + mkt_data[each]["RT_ASK1"])/2.0
        threshold = epsilon * mid_price
        ma_20_diff = mid_price - mkt_data[each]["ma_20"]
        ma_60_diff = mid_price - mkt_data[each]['ma_60']
        ma_120_diff = mid_price - mkt_data[each]['ma_60']
        print each, mkt_data[each]["ma_20"],threshold,ma_20_diff,ma_60_diff,ma_120_diff
        if 0 < ma_20_diff < threshold:
            print "Alert!!!!: ", each, "almost reaches support level ma 20..."
        if 0 < ma_60_diff < threshold:
            print "Alert!!!!: ", each, "almost reaches support level ma 60..."
        if 0 < ma_120_diff < threshold:
            print "Alert!!!!: ", each, "almost reaches support level ma 120..."
        if 0 < -ma_20_diff < threshold:
            print "Alert!!!!: ", each, "almost reaches pressure level ma 20..."
        if 0 < -ma_60_diff < threshold:
            print "Alert!!!!: ", each, "almost reaches pressure level ma 60..."
        if 0 < -ma_120_diff < threshold:
            print "Alert!!!!: ", each, "almost reaches pressure level ma 120..."
    return

stock_pool_file = "C:\Users\Jianing Song\Desktop\stockpool.csv"
stock_pool = pd.read_csv(stock_pool_file,skiprows=0,usecols=[0])
stock_pool.columns = ['ticker']
tickers = (stock_pool['ticker'].apply(lambda x:".".join([x[2:],x[:2]]))).tolist()
print tickers
tickers = tickers[:3]
fields   = ["rt_time","rt_last","rt_bid1","rt_bsize1","rt_ask1","rt_asize1"]
fields   = [each.upper() for each in fields]
data_source = WE(tickers,fields,update_func=check_ma)
data_source.run()
