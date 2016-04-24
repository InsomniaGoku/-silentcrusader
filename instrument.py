
class stock:
    def __init__(self,ticker):
        self.ticker=ticker

class e_option:
    def __init__(self,CorP,K,r,TtoM,S):
        """
        :param CorP: Call or Put
        :param K: Strike Price
        :param r: Market Interest Rate
        :param TtoM: Time to Maturity
        :param S: Underlying
        """
        self.CorP = CorP
        self.K    = K
        self.r    = r
        self.TtoM = TtoM
        self.S    = S

class future:
    def __init__(self,S,TtoM,r,d):
        self.S    = S
        self.TtoM = TtoM
        self.r    = r
        self.d    = d
