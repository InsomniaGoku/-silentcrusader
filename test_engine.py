from data_handler import *
from option_model import implied_volatility,BS
from Strategy import *

print "current version is ",
s = three_legs_strats.PutCallParity("a","b")
s.desc()

import pandas
import datetime
month_code_dict = ['20160401','20160405','20160406','20160407','20160408','20160411','20160412','20160413',\
                   '20160414','20160415','20160418','20160419','20160420','20160421','20160422','20160425',\
                   '20160426','20160427']
days = len(month_code_dict)
for each in range(days):
    _date_ = month_code_dict[each]
    _day_to_m_ = days - each
    option_file_dict = {'CALL':"C:\Users\Jianing Song\Documents\mkt_data\\50etf\option\\"+_date_+"\OP10000579.csv",\
                  'PUT':"C:\Users\Jianing Song\Documents\mkt_data\\50etf\option\\"+_date_+"\OP10000584.csv"}
    etf_file = "C:\Users\Jianing Song\Documents\mkt_data\\50etf\etf\sh510050_"+_date_+".csv"

    mapping_tags = ['CALL','PUT','ETF']
    reader_list = []
    Index = []
    #etf = pandas.read_csv(etf_file,index_col=0,skiprows=0,usecols=range(2,28))

    #use datetime type as index.
    def datetime_index(str):
        str = str.replace("/","-")
        try:
            return datetime.datetime.strptime(str,"%Y-%m-%d %H:%M:%S")
        except:
            return datetime.datetime.strptime(str,"%Y-%m-%d %H:%M")

    def datetime_index_opt(str):
        return datetime.datetime.strptime(str,"%Y/%m/%d %H:%M:%S")

    etf = pandas.read_csv(etf_file,skiprows=0,usecols=range(2,28))
    columns = ['Time','Price','Trades','TotalAmount','TotalVol','Side'\
        ,'BP1','BP2','BP3','BP4','BP5','SP1','SP2','SP3','SP4','SP5',\
               'BV1','BV2','BV3','BV4','BV5','SV1','SV2','SV3','SV4','SV5']
    etf.columns = columns
    etf.Time = etf.Time.apply(datetime_index)
    etf = etf.set_index(['Time'],drop=True)
    print etf

    for each in option_file_dict.keys():
        tmp_df = pandas.read_csv(option_file_dict[each],skiprows=0)
        tmp_df.Time = tmp_df.Time.apply(datetime_index)
        tmp_df = tmp_df.set_index(['Time'],drop=True)
        tmp_df.columns = [each+each_column for each_column in tmp_df.columns]
        reader_list.append(tmp_df)
        print tmp_df.index
    aggregated_data_feed = etf.join(reader_list,how='outer')
    aggregated_data_feed = aggregated_data_feed.fillna(method='ffill')

    aggregated_data_feed = aggregated_data_feed[aggregated_data_feed.Price>0]
    print aggregated_data_feed

    # check all data frames.

    for each in reader_list:
        #print each.columns
        print each.shape
        print each.index.name

    aggregated_data_feed.to_csv("C:\Users\Jianing Song\Documents\mkt_data\\50etf\etf\\test.csv")

    # init option model:
    call = BS((2.150,2.150,0.0135,_day_to_m_),32.5)
    print(call._price())
    filepath = "C:\Users\Jianing Song\Documents\mkt_data\\50etf\etf\\test.csv"

    mktdata = Tick()

    mktdata.format(["BP1","SP1","BV1","SV1","PUTBP1","PUTSP1","CALLBP1","CALLSP1"])

    mktdata.load(filepath)

    mktdata.load_output_handler('strategy_update',call.update)

    mktdata.play('strategy_update')

    arb = pandas.DataFrame(call.arbitrage_series,columns=['Time','Rate','Position','Return','CumR'])
    #print arb
    arb.to_csv("C:\Users\Jianing Song\Documents\mkt_data\\50etf\etf\\returns.csv",mode='a',header=False )
    #returns = arb[['Time','Return']]
    #returns.plot()
    #from matplotlib.pyplot import *
    #show()
    #arb.Rate.hist()
    #show()

