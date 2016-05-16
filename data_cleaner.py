# convert csv data source to standard format.convert chinese into english, and delete useless columns.
import pandas
date_str = "20160429"
filepath = "C:\Users\Jianing Song\Documents\mkt_data\\50etf\etf\\sh510050_%s.csv" % date_str
raw_data = pandas.read_csv(filepath,index_col=0,skiprows=0,usecols=range(2,28))
columns = ['Price','Trades','TotalAmount','TotalVol','Side'\
    ,'BP1','BP2','BP3','BP4','BP5','SP1','SP2','SP3','SP4','SP5',\
           'BV1','BV2','BV3','BV4','BV5','SV1','SV2','SV3','SV4','SV5']
raw_data.columns = columns

raw_data.index.name = 'Time'

#print raw_data
raw_data.to_csv("C:\Users\Jianing Song\Documents\mkt_data\\50etf\etf\\std_sh510050_%s.csv" % date_str)
print date_str+ " done..."