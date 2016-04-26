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
        self.input_handlers = {"csv": self.read_from_csv, "wind": self.read_from_wind}
        self.output_handler = {"default": print}
        #self.output = self.output_handler["default"]
        self.std_format =["ticker","date","time","volume","bid1","ask1","bsize1","asize1"]
        self.data = pd.DataFrame()
        print ("Mkt Data Obj inited, please provide format before load data...")

    def format(self, the_format):
        self.std_format = the_format

    def load(self, data,format="csv"):
        self.data = self.input_handlers[format](data)

    def load_input_handler(self, target_format, new_handler):
        if target_format in self.input_handlers:
            print ("Overwriting current input handler ", target_format, " with new one.")
        else:
            print ("Adding new input handler for ", target_format)
        self.input_handlers[target_format] = new_handler

    def load_output_handler(self, target_format, new_handler):
        if target_format in self.output_handler:
            print ("Overwriting current output handler ", target_format, " with new one.")
        else:
            print ("Adding new output handler for ", target_format)
        self.output_handler[target_format] = new_handler

    # def bind_output_method(self,output_format):
    #     self.output = self.output_handler[output_format]

    def play(self,output_format="default"):
        """behave like a market data generator, call target receiver function in loop. """
        self.output = self.output_handler[output_format]
        for i,row in self.data.iterrows():
            self.output(row)

    def read_from_csv(self, filepath):
        """ convert data from csv file into pandas.dataframe"""
        data = pd.read_csv(filepath,index_col=2,skiprows=1) # based on current file format.use time column as index
        return data[self.std_format]

    def read_from_wind(self, data):
        """ convert data from wind into pandas.dataframe"""
        return pd.DataFrame

