import pandas as pd
import pandas_datareader as pd_datareader
# current data source:
# 1. Wind terminal with python api. (Chinese)
# 2. Pandas DataReader.( Yahoo & Google )
try:
    from WindPy import *
except ImportError:
    print "Program needs to run with Wind Terminal or Wind Python API."
    pass
