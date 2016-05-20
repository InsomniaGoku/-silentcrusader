import pandas
import datetime
option_file_dict = {'CALL':"C:\Users\Jianing Song\Documents\mkt_data\\50etf\option\\20160401\OP10000564.csv",\
              'PUT':"C:\Users\Jianing Song\Documents\mkt_data\\50etf\option\\20160401\OP10000563.csv"}
etf_file = "C:\Users\Jianing Song\Documents\mkt_data\\50etf\etf\sh510050_20160401.csv"

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
print aggregated_data_feed

# check all data frames.

for each in reader_list:
    #print each.columns
    print each.shape
    print each.index.name

aggregated_data_feed.to_csv("C:\Users\Jianing Song\Documents\mkt_data\\50etf\etf\\test.csv")
