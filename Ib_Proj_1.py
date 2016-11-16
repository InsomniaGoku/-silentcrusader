
# coding: utf-8

# In[9]:

from ib.opt import ibConnection,message
from ib.ext.Contract import Contract
from ib.ext.TickType import TickType
from time import sleep
Debug = True

class snapshot:
    def __init__(self):
        self.bid_seq =[]
        self.bidSize_seq = []
        self.ask_seq =[]
        self.askSize_seq = []
        self.LastTradePrice = 0
        self.LastTradeSize  = 0
        self.bid = 0
        self.ask = 0

class tws():
    def __init__(self,contract,ClientId=512):
        self.mkt_data = snapshot()
        self.con  = ibConnection(clientId=ClientId)
        self.contract = contract
        self.ticker_id = 1

    def connect(self):
        self.con.registerAll(self.debugHandler) #why
        self.con.register(self.tickPriceHandler,message.tickPrice)
        self.con.register(self.tickSizeHandler,message.tickSize)
        self.con.register(self.tickGenericHandler,message.tickGeneric)
        self.con.register(self.tickStringHandler,message.tickString)
        self.con.register(self.mktdepthHandler,message.updateMktDepth)
        self.con.register(self.errorHandler,message.error)
        self.con.connect()

    def tickPriceHandler(self,msg):
        if Debug:print(msg)
        print('['+TickType.getField(msg.field)+']: ',msg.price)

    def tickSizeHandler(self,msg):
        if Debug:print(msg)
        print('['+TickType.getField(msg.field)+']: ',msg.size)
    def tickGenericHandler(self,msg):
        if Debug:print(msg)
        print('['+TickType.getField(msg.TickType)+']: ',msg.value)

    def tickStringHandler(self,msg):
        if Debug:print(msg)
        print('['+TickType.getField(msg.TickType)+']: ',msg.value)

    def mktdepthHandler(self,msg):
        #msg.position
        #msg.side: 0 offer/1 bid
        msg.price
        msg.size
        if Debug:print(msg)
        print('['+TickType.getField(msg.TickType)+']: ',msg.value)

    def debugHandler(self,msg):
        if Debug:
            print('[Debug]: ',msg)

    def errorHandler(self,msg):
        print('[Error]: ',msg.errorCode,' | ',msg.errorMsg)

    def reqMktData(self,generic_format="",snapshot=0):
        self.con.reqMktData(self.ticker_id,self.contract,generic_format,snapshot)

    def reqMktDepth(self,depth=5):
        self.con.reqMktDepth(self.ticker_id,self.contract,depth)

    def wait_n_disconnect(self,timeout=0):
        sleep(timeout)
        print('wait and see.....')
        self.con.disconnect()



# In[10]:

ng = Contract()
ng.m_symbol = "CN"
ng.m_secType = "FUT"
ng.m_exchange = "SGX"
ng.m_expiry = "20161129"
ng.m_currency = "USD"
ng.m_multiplier = 1
ng.m_tradingClass = "CN"


# In[11]:

TWS = tws(ng)


# In[12]:

TWS.contract


# In[13]:

TWS.connect()
#TWS.con.connect()


# In[14]:

TWS.reqMktData()
TWS.reqMktDepth()
TWS.wait_n_disconnect(30)


# In[8]:

#TWS.wait_n_disconnect(0)


# In[ ]:
