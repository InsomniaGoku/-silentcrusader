from __future__ import print_function
import pandas as pd
import pandas_datareader as pd_datareader

# current data source:
# 1. Wind terminal with python api. (Chinese)
# 2. Pandas DataReader.( Yahoo & Google )

try:
    from WindPy import *
except ImportError:
    print ("Program needs to run with Wind Terminal or Wind Python API.")
    pass


class Tick:
    """
    standard market data format, pandas dataframe.

    """
    def __init__(self):
        self.handlers["csv"] = self.read_from_csv
        self.handlers["wind"]= self.read_from_wind
        self.output_handler   = print # default output, just print these shit
        self.std_format       = ["ticker","date","time","volume","bid1","ask1","bsize1","asize1"]
        self.data             = pd.DataFrame()


    def format(self,the_format):
        self.std_format = the_format

    def load(self,data,format="csv"):
        self.data = self.handlers[format](data)

    def bind(self,output_handler=print):
        """ bind itself to a target receiver function."""
        self.output_handler = output_handler

    def play(self):
        """behave like a market data generator, call target receiver function in loop. """
        for i,row in self.data:
            self.output_handler(row)

    def read_from_csv(self,filepath):
        """ convert data from csv file into pandas.dataframe"""
        data = pd.read_csv(filepath,index_col=2) # based on current file format.use time column as index
        return data[self.std_format]

    def read_from_wind(self,data):
        """ convert data from wind into pandas.dataframe"""
        return pd.DataFrame
