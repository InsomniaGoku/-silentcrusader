from data_handler import *
from option_model import implied_volatility,BS
from Strategy import *
import pandas
import numpy as np
import datetime
from WindPy import *

def default_update(data):
    print data


class WindEngine():

    def __init__(self,products,fields,update_func=default_update):
        self.products = products
        self.fields   = fields
        self.update_func = update_func
        self.mkt_data = dict.fromkeys(products,dict.fromkeys(fields)) # it is actually a snapshot

    def run(self):
        w.start()
        products_str = ','.join(self.products)
        fields_str   = ','.join(self.fields)
        print "Downloading historical data from data source..."
        self.get_stats()
        print "Subscribe data fields ",fields_str," of ",products_str," from Wind api"
        w.wsq(products_str,fields_str,func=self.market_update)
        while w.isconnected():
            sys_message = "API is still running is other thread..."

    def get_stats(self,stats="ma"):
        w.start()
        if stats == "ma":
            lgth = 150
            for each in self.products:
                histo = (w.wsd(each,"close", datetime.today()-timedelta(lgth))).Data[0]
                self.mkt_data[each]["ma_120"] = np.mean(histo[lgth - 120: ])
                self.mkt_data[each]["ma_60"] = np.mean(histo[lgth - 60: ])
                self.mkt_data[each]["ma_20"] = np.mean(histo[lgth - 20: ])
                print "Getting MA for ", each, "....\n"
        w.stop()


    def market_update(self,wind_data):
        #print wind_data # for test use. Display all data
        global begintime
        if wind_data.ErrorCode!=0:
            print('error code:'+str(wind_data.ErrorCode)+'\n')
            return()
        else:
            tmp_products = wind_data.Codes
            for k in range(len(wind_data.Fields)):
                for j in range(len(tmp_products)):
                    #print tmp_products[j],wind_data.Fields[k],wind_data.Data[k][j]
                    self.mkt_data[tmp_products[j]][wind_data.Fields[k]] = wind_data.Data[k][j]
            # should generate a dict of mkt data and call update_func from whatever model you want to use
            self.update_func(self.mkt_data)

if __name__ == "__main__":
    products = ["10000641.SH","1000642.SH","510050.SH"]
    fields   = ["rt_time","rt_last","rt_last_vol","rt_bid1","rt_bsize1","rt_ask1","rt_asize1"]
    fields   = [each.upper() for each in fields]
    WE = WindEngine(products,fields)
    WE.run()