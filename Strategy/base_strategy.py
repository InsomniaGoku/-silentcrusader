import pandas as pd
import threading


class Strat:
    """ strategy object, contains everything to do with backtesting strategy, position and net capital requirement. """
    def __init__(self,base_contract,trade_contract):
        self.position          = 0
        self.net_capital_usage = 0
        self.contracts         = {'leg1':base_contract, 'leg2':trade_contract}
        self.mkt_snapshot      = pd.Series()
        self.lock              = threading.Lock()

    def desc(self):
        print "This strategy is a ",len(self.contracts),"-leg strategy..\n"
        print "We need to get market updates of: ", ",".join(self.contracts.keys()),'\n'

    def data_format(self,new_format):
        self.mkt_data = pd.Series(columns=[new_format['columns']],index=new_format['index'])

    def valuation(self):
        print 'Doing Valuation now....\n'
        return

    def mkt_update(self,data):
        self.lock.acquire()
        self.mkt_data = data
        #print "Got Update from mkt_feed: ",type(data)
        self.valuation()
        self.lock.release()
        return

    def run(self):
        return