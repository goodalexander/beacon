### The Summary application is for simple account balances and exposure
### API outputs are anonymized and don't contain order level data

from ibapi import wrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper #just for decorator
from ibapi.common import *
import pandas as pd
import datetime
arr=[]
class SummaryApp(wrapper.EWrapper, EClient):
    def __init__(self):
        wrapper.EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

    @iswrapper
    def nextValidId(self, orderId:int):
        '''
        print("setting nextValidOrderId: %d", orderId)
        '''
        self.nextValidOrderId = orderId
        self.reqAccountSummary(9003, "All", "$LEDGER")

    @iswrapper
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        '''
        print("Error. Id: " , reqId,
            " Code: " , errorCode ,
            " Msg: " , errorString)
        '''

    @iswrapper
    def accountSummary(self, reqId:int, account:str, tag:str, value:str, currency:str):

        print("Acct Summary. ReqId:" , reqId , "Acct:", account,
            "Tag: ", tag, "Value:", value, "Currency:", currency)
        arr.append([account, value, currency, tag])
    @iswrapper
    def accountSummaryEnd(self, reqId:int):
        #print("AccountSummaryEnd. Req Id: ", reqId)
        # now we can disconnect
        self.disconnect()

def output_summary_json(connection_ip="127.0.0.1",connection_port=7496, client_id=123):
    ''' connection_ip is what machine you are hitting interactive brokers from.
    defaults to local.note, client will need to permission other IPs than local.
    Connection port is set in the interface. client ID is a user inputted value
    '''
    app = SummaryApp()
    app.connect(connection_ip, connection_port, clientId=client_id)
    app.run()
    temp_df=pd.DataFrame(arr)
    temp_df.columns = ['Acct','Value','Currency','Field']
    json_blob=temp_df.groupby('Field').last().to_json()
    return json_blob
