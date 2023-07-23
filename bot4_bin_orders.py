from asyncio import current_task
from datetime import datetime
from binance.exceptions import BinanceAPIException
import numpy
import time;
from time import sleep


def cancel (client,  curasset, orderid, msg):
    if curasset.runmode=="REAL":
        try:
            now = datetime.now()  
            print(now.strftime("%Y-%m-%d %H:%M:%S"),curasset.symbol, msg)
            result = client.cancel_margin_order( symbol=curasset.symbol, isIsolated='TRUE', orderId=orderid)
            print(result)

        except BinanceAPIException as e:
            print(msg,e )   
   
   
def cancelall(client, curasset):
                  try:
                     orders = client.get_open_margin_orders(symbol=curasset.symbol,  isIsolated='TRUE')
                     print(orders)
                     if len(orders)>0:
                        for order in orders: # find orders <15 and with 2 nines at end of quatntity
                              try:
                                    Orderid = order['orderId']
                                    cancel( client, curasset, Orderid,'cancel all !!!!')
                                 
                              except:
                                 print('erro cancel order')
                  except:
                     print('error getting orders')                     
     
     
def execute (client,  curasset, typeorder, orderqtd, orderprice):
    #print('orders----------')
    #print(curasset.orders)
    if curasset.runmode=="SIMUL" or curasset.runmode=="CHART":
        #print('added', curasset.netasset)
        #if curasset.lastprice < orderprice and typeorder=='BUY':
           #curasset.netasset=curasset.netasset + orderqtd
           #curasset.freeAsset=curasset.freeAsset - orderqtd*orderprice
        #   return 1

        if (curasset.lastprice > orderprice and typeorder=='SELL') or orderprice==0:
            if orderprice==0:
               orderprice=curasset.lastprice

            if curasset.printdebug:
               print(datetime.fromtimestamp(curasset.millseconds_next),';',  'O',';', 'Executed',';', typeorder,';', orderqtd, ';',orderprice, ';',curasset.lastprice)
            curasset.netasset=curasset.netasset - orderqtd
            #curasset.freeAsset=curasset.freeAsset + orderqtd*orderprice
            if orderqtd*orderprice > curasset.borrowed:
              
              curasset.freeAsset=curasset.freeAsset + orderqtd*orderprice - curasset.borrowed
              curasset.borrowed = 0
            else:
              curasset.borrowed = curasset.borrowed - orderqtd*orderprice

            return 1
    return 0


def toSpot(client,  curasset, orderqtd, orderprice):
    print('toSpot')
    try:
       cancelall(client, curasset)
       #Transfer isolated margin account to spot
       #print('asset', curasset.atualasset,'borr', curasset.borrowed, 'qtd',orderqtd, orderprice)
       valtopay=curasset.borrowed + orderqtd * orderprice
       orderqtd1 = round(valtopay/curasset.lastprice,curasset.decplacesqtd)

       if orderqtd1>0:
          create(client, curasset, 'SELL', orderqtd1, orderprice,'SELL to send to Spot')
          sleep(5)
          transaction = client.transfer_isolated_margin_to_spot(asset=curasset.currency,symbol=curasset.symbol, amount=str(round(orderqtd * orderprice, 0)))
          sleep(2)
          orderqtd1 = round((curasset.borrowed - valtopay)/curasset.lastprice,curasset.decplacesqtd)
          #print('qtd2', orderqtd1)
          create(client, curasset, 'BUY', orderqtd1, round(curasset.lastprice * 1.005, curasset.decplaces),'re-buy after SELL to send to Spot')
    except BinanceAPIException as e:
          print(e )   
    

def fromSpot(client,  curasset, amount):
    try:
       #print('fromSpot')
       if amount>0:
          transaction = client.transfer_spot_to_isolated_margin(asset=curasset.currency,symbol=curasset.symbol, amount=str(amount))
    except BinanceAPIException as e:
        print(e )   
       


def create (client,  curasset, typeorder, orderqtd, orderprice, msg):
    if curasset.runmode=="REAL":
        try:
            now = datetime.now()  
            #print(now.strftime("%Y-%m-%d %H:%M:%S"),curasset.symbol, msg, 'qtd:', orderqtd, 'price:', orderprice)
            if typeorder=='SELL':
               order = client.create_margin_order( symbol=curasset.symbol, isIsolated='TRUE', sideEffectType='AUTO_REPAY', side=typeorder, type='LIMIT', timeInForce='GTC', quantity=orderqtd, price = orderprice)
            else:
               order = client.create_margin_order( symbol=curasset.symbol, isIsolated='TRUE',  sideEffectType='MARGIN_BUY',side=typeorder, type='LIMIT', timeInForce='GTC', quantity=orderqtd, price = orderprice)

        except BinanceAPIException as e:
            print(msg,e )   
    else:
        now = datetime.now()  
        if curasset.printdebug:
           print(datetime.fromtimestamp(curasset.millseconds_next),';','O', ';', typeorder, ';', orderqtd, ';', orderprice, ';',msg)

        if typeorder=='SELL':
           a=[]
           a=curasset.orders
           if msg=='PAYNOPRICE':
              a.append([now, typeorder, orderqtd, 0])
              curasset.orders=a
           else:
              a.append([now, typeorder, orderqtd, orderprice])
              curasset.orders=a
           if curasset.runmode=='SIMUL'  or curasset.runmode=="CHART":
                    curasset.lastsell = curasset.millseconds_next
        else:
           curasset.netasset=curasset.netasset + orderqtd
           #curasset.freeAsset=curasset.freeAsset - orderqtd*orderprice
           if orderqtd*orderprice > curasset.freeAsset:
              curasset.borrowed = curasset.borrowed - curasset.freeAsset + round(orderqtd*orderprice,2)
              curasset.freeAsset = 0
           else:
              curasset.freeAsset = curasset.freeAsset - round(orderqtd*orderprice,2)
           if curasset.runmode=='SIMUL'  or curasset.runmode=="CHART":
                    curasset.lastbuy = curasset.millseconds_next


def loan (client,  curasset,  valLoan, msg):
    if True:  #curasset.runmode=="REAL":
        try:
            now = datetime.now()
            if curasset.printdebug:
               print(now.strftime("%Y-%m-%d %H:%M:%S"),curasset.symbol, msg, 'valLoan:', valLoan)
            
             
            if curasset.runmode=='REAL':
               order = client.create_margin_loan(asset=curasset.currency, symbol=curasset.symbol , isIsolated='TRUE', amount= valLoan)                  
               print('Loan', order)
            else:
               curasset.borrowed=curasset.borrowed + valLoan
               curasset.freeAsset = curasset.freeAsset + valLoan

        except BinanceAPIException as e:
            print(msg,e )   


def pay (client,  curasset, typeorder, valtopay, msg):
    if True: #curasset.runmode=="REAL":
        try:
            now = datetime.now()  
            if curasset.printdebug:
                print(datetime.fromtimestamp(curasset.millseconds_next),';',curasset.symbol, msg,  'pay:', valtopay)
        
            if curasset.runmode=='REAL':
               order = client.repay_margin_loan(asset=curasset.currency, symbol=curasset.symbol , isIsolated='TRUE', amount=valtopay)
               if curasset.printdebug:
                   print('Payed', order)
            else:
               
               if curasset.borrowed > valtopay: 
                  curasset.borrowed=curasset.borrowed - valtopay
                  curasset.freeAsset=curasset.freeAsset - valtopay
                

        except BinanceAPIException as e:
            print(msg,e )   
            
