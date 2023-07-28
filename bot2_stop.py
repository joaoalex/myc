from datetime import datetime
from binance.exceptions import BinanceAPIException
import numpy
#import dic
import bot4_bin_orders

def create (client,  df, curasset):

    now = datetime.now()  
    
    #print("----------- Create Stop -----------")
    # ------------- create stop loss ---------------------
    # sideEffectType (str)  NO_SIDE_EFFECT, MARGIN_BUY, AUTO_REPAY; default NO_SIDE_EFFECT.
    # ----------------------------------------------------
    orderprice=round(curasset.liqprice * (1 + curasset.lossrisk),curasset.decplaces)
    #print('LOSS evaluate', numpy.format_float_positional(maxstop), numpy.format_float_positional(orderprice), numpy.format_float_positional(lossrisk))
    if (curasset.maxstop == 0 or curasset.maxstop < float(orderprice)):
       print('CREATE LOSS', float(curasset.stopOrder))
       if ( float(curasset.stopOrder)>0 ):
           print(now.strftime("%Y-%m-%d %H:%M:%S"),curasset.symbol,'cancel stop order')
           try:
          
              bot4_bin_orders.cancel(client, curasset, curasset.stopOrder,'cancel stop order')
           
              curasset.stopOrder=0
           except BinanceAPIException as e:
              print('error cancel stop loss')
              print(e)
       
       orderqtd=round(float(curasset.netasset) * curasset.lossreserve, curasset.decplacesqtd)
       
       if orderqtd * orderprice < curasset.minValue and orderprice>0:
          orderqtd=round(curasset.minValue/orderprice,curasset.decplacesqtd)
       
       if orderqtd  > float(curasset.freetosell):
          orderqtd=round(float(curasset.freetosell)*0.99, curasset.decplacesqtd)
       
       print('create order, qtd, price:', orderqtd, orderprice, orderqtd * orderprice, curasset.minValue, curasset.freetosell)
       
       if orderqtd * orderprice >= curasset.minValue * 0.999 :
        try:
          print(now.strftime("%Y-%m-%d %H:%M:%S"),curasset.symbol, 'STOP', 'free', curasset.freetosell, 'total', float(curasset.netasset), 'qtd:', orderqtd, 'price:',curasset.liqprice,'stop:',  orderprice)
          orderprice1=round(orderprice * 0.990, curasset.decplaces)
          order = client.create_margin_order( symbol=curasset.symbol, isIsolated='TRUE',  sideEffectType='AUTO_REPAY', side='SELL', type='STOP_LOSS_LIMIT', timeInForce='GTC', quantity=orderqtd, price=curasset.liqprice, stopPrice=orderprice)
          
        except BinanceAPIException as e:
          print('error create stop loss')
          print(e)
       else:
          try:
             bot4_bin_orders.cancel(client, curasset, curasset.sellOrder,'cancel - under the minimum')
          except BinanceAPIException as e:
             print('error cancel sell order')
             print(e)
          

def cancel (client,  df, curasset):
    now = datetime.now() 
    
    #print("----------- Cancel STOP -----------")
    # ------------- cancel to recreate low order ---------------------
    #print(numpy.format_float_positional(maxstop*1.001), numpy.format_float_positional(liqprice * (1 + lossrisk )))
    if ( float(curasset.stopOrder)>0 and ( (curasset.liqprice * (1 + curasset.lossrisk ) > curasset.maxstop*1.001 ) or ( curasset.maxstop*0.995 >  curasset.liqprice * (1 + curasset.lossrisk )  ) ) ):
          #print(now.strftime("%Y-%m-%d %H:%M:%S"),curasset.symbol, 'cancel stop order')
          try:

             bot4_bin_orders.cancel(client, curasset, curasset.stopOrder,'cancel stop order')

             curasset.maxstop=0
             curasset.stopOrder=0
          except BinanceAPIException as e:
             # nedd to cencel curasset.sellOrder
             print('error cancel stop loss', e)

