
# coding: utf-8

# In[22]:

from ib.opt import ibConnection,message
from ib.ext.Contract import Contract
from ib.ext.TickType import TickType
from ib.ext.Order    import Order
from ib.ext.Execution import Execution
from ib.ext.ExecutionFilter import ExecutionFilter
from time import sleep
Debug = True

class snapshot:
    def __init__(self):
        self.data_seq =[{},{}]
        self.generic_data = {'lastPrice':0,'lastSize':0,
                             'bidPrice':0,'bidSize':0,
                             'askPrice':0,'askSize':0,
                            'high':0,'low':0,
                             'open':0,'close':0,
                             'volume':0}
    def cur_snapshot(self,levels):
        print(self.data_seq)
        print(self.generic_data)
        #for each in range(levels):
        #   print()
            
class tws():
    def __init__(self,contract,Id=1,mkt_depth=5,ClientId=512):
        self.mkt_data = snapshot()
        self.con  = ibConnection(clientId=ClientId)
        self.contract = contract
        self.mkt_depth = mkt_depth
        self.Id = Id #orderId, autoincrement.
        self.order_book = {}
        self.ticker_id = 1
        
    def connect(self):
        self.con.registerAll(self.debugHandler) #why
        self.con.register(self.nextvalididHandler,'NextValidId')
        self.con.register(self.orderstatusHandler,'OrderStatus')
        self.con.register(self.execdetailsHandler,'ExecDetail')
        self.con.register(self.positionHandler,'Position')
        self.con.register(self.tickPriceHandler,message.tickPrice)
        self.con.register(self.tickSizeHandler,message.tickSize)
        self.con.register(self.tickGenericHandler,message.tickGeneric)
        self.con.register(self.tickStringHandler,message.tickString)
        self.con.register(self.mktdepthHandler,message.updateMktDepth)
        self.con.register(self.errorHandler,message.error)
        self.con.connect()
        
    def tickPriceHandler(self,msg):
        if Debug:
            print(msg)
            print('['+TickType.getField(msg.field)+']: ',msg.price)
        self.mkt_data.generic_data.update({TickType.getField(msg.field):msg.price})
        

    def tickSizeHandler(self,msg):
        if Debug:
            print(msg)
            print('['+TickType.getField(msg.field)+']: ',msg.size)
        self.mkt_data.generic_data.update({TickType.getField(msg.field):msg.size})
        
    def tickGenericHandler(self,msg):
        if Debug:
            print(msg)
            print('['+TickType.getField(msg.TickType)+']: ',msg.value)

    def tickStringHandler(self,msg):
        if Debug:
            print(msg)
            print('['+TickType.getField(msg.TickType)+']: ',msg.value)

    def mktdepthHandler(self,msg):
        #msg.position
        #msg.side: 0 offer/1 bid
        self.mkt_data.data_seq[msg.side][msg.position] = {'price':msg.price,'size':msg.size}
        if Debug:
            print(msg)
            self.mkt_data.cur_snapshot(5)
        

    def debugHandler(self,msg):
        
        print('[Debug]: ',msg)
        if Debug:
            print(dir(msg))
            print('['+msg.typeName+']: ',msg.keys(),msg.values())

    def errorHandler(self,msg):
        print('[Error]: ',msg.errorCode,' | ',msg.errorMsg)
    
    def reqMktData(self,generic_format="",snapshot=0):
        self.con.reqMktData(self.ticker_id,self.contract,generic_format,snapshot)
        
    def reqMktDepth(self):
        self.con.reqMktDepth(self.ticker_id,self.contract,self.mkt_depth)
    
    def wait_n_disconnect(self,timeout=0):
        sleep(timeout)
        print('wait and see.....')
        self.con.disconnect()
                
    def valuation(self):
        print('check pricing and generate orders...')
        
    def generate_order_id(self):
        cur_id = self.Id
        return cur_id
    
    def nextvalididHandler(self,msg):
        self.Id = msg.orderId
        print("Current OrderId reset to ",self.Id)
    
    def sync_order_id(self):
        self.con.reqIds(self.Id)
        
    def place_order(self,order):
        self.con.placeOrder(self.generate_order_id(),self.contract,order)
    
    def orderstatusHandler(self,msg):
        '''
        'orderId', 'status', 'filled', 'remaining', 'avgFillPrice', 'permId', 
        'parentId', 'lastFillPrice', 'clientId', 'whyHeld'
        '''
        
        self.order_book.update({msg.orderId:{"status":msg.status,
                                  "filled":msg.filled,
                                  "remaining":msg.remaining,
                                  "avgFillPrice":msg.avgFillPrice,
                                  "permId":msg.permId,
                                  "parentId":msg.parentId,
                                  "lastFillPrice":msg.lastFillPrice,
                                  "whyHeld":msg.whyHeld}}) #pandas.dataframe is better..
    
    def openorderHandler(self,msg):
        pass
    
    def openorderendHandler(self,msg):
        pass
    
    def positionHandler(self,msg):
        pass
    
    def positionendHandler(self,msg):
        pass
    
    def commissionreportHandler(self,msg):
        pass
    
    def execdetailsHandler(self,msg):
        pass
    
    def create_order(self,order_type,price,qty,action):
        order = Order()
        ''' 
        main fields:
        m_orderId = 0
        m_clientId = 0
        m_permId = 0
        m_action = ""
        m_totalQuantity = 0
        m_orderType = ""
        m_lmtPrice = float()
        m_auxPrice = float()
        '''
        order.m_lmtPrice = price
        order.m_orderType = order_type
        order.m_totalQuantity = qty
        order.m_action = action
        # more functionalities....
        return order


# In[23]:

ng = Contract()
ng.m_symbol = "CN"
ng.m_secType = "FUT"
ng.m_exchange = "SGX"
ng.m_expiry = "20161129"
ng.m_currency = "USD"
ng.m_multiplier = 1
ng.m_tradingClass = "CN"


# In[24]:

TWS = tws(ng) 


# In[25]:

TWS.connect()
#TWS.con.connect()


# In[26]:

TWS.sync_order_id()


# In[ ]:

def req_position(msg):
    print(dir(msg))

TWS.con.reqAllOpenOrders()
TWS.con.reqOpenOrders()
subscribe = False
acctCode = 'U9015509'
TWS.con.reqAccountUpdates(subscribe, acctCode)
E_filter = ExecutionFilter()
reqId = 0
TWS.con.reqExecutions(reqId,E_filter)


# In[ ]:

a_order = TWS.create_order('LMT',9985,1,"BUY")


# In[ ]:

TWS.place_order(a_order)
#TWS.con.reqPositions()


# In[ ]:

TWS.con.cancelOrder(TWS.Id)


# In[ ]:

TWS.reqMktData()
TWS.reqMktDepth()
TWS.wait_n_disconnect(10)


# In[30]:

TWS.wait_n_disconnect(0)


# In[27]:

TWS.order_book


# In[28]:

TWS.con.reqOpenOrders()


# In[29]:

TWS.con.reqAllOpenOrders()


# In[8]:

TWS.con.reqPositions()


# In[10]:

TWS.con.reqPositions()


# In[11]:

TWS.con.cancelPositions()


# In[ ]:



