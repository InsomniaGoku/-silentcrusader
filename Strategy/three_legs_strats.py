from base_strategy import *

class PutCallParity(Strat):

    def __init(self,call,put,stock):
        Strat.__init__(call,put)
        self.contracts['leg3'] = stock
        print "this strategy is a PutCallParity strategy..\n"

    def valuation(self):
        print "Calculate PutCallParity opportunity....."
