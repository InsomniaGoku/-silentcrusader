from base_strategy import *

class CoveredCall(Strat):

    def __init(self,call,stock):
        Strat.__init__(call,stock)
        print "this strategy is a Covered-Call strategy..\n"

    def valuation(self):
        print "Calculate Covered Call opportunity....."