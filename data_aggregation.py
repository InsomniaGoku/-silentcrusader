import pandas
file_dict = {'CALL':"C:\Users\Jianing Song\Documents\mkt_data\\50etf\option\\20160401\OP10000573.csv",\
              'PUT':"C:\Users\Jianing Song\Documents\mkt_data\\50etf\option\\20160401\OP10000574.csv",\
              'ETF':"C:\Users\Jianing Song\Documents\mkt_data\\50etf\etf\std_sh510050_20160401.csv"}
mapping_tags = ['CALL','PUT','ETF']
reader_list = []
Index = []
for each in file_dict.keys():
    tmp_df = pandas.read_csv(file_dict[each],index_col=0,skiprows=0)
    tmp_df.columns = [each+each_column for each_column in tmp_df.columns]
    reader_list.append(tmp_df)
    Index.append(tmp_df.index)
aggregated_data_feed = pandas.concat(reader_list, axis=0, join='outer')
#aggregated_data_feed = aggregated_data_feed.reindex(sorted(Index))
print aggregated_data_feed
print aggregated_data_feed.columns
print len(aggregated_data_feed.index)




# check all data frames.

for each in reader_list:
    #print each.columns
    print each.shape
    print each.index.name

aggregated_data_feed.to_csv("C:\Users\Jianing Song\Documents\mkt_data\\50etf\etf\\test.csv")
