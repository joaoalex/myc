from datetime import datetime
from binance.exceptions import BinanceAPIException
import numpy
import math
import bot5_bin_orders
from time import sleep

def trendadjust( curasset, change ):
   
#B1=1.400
#B2=1.100
#B3=1.010
#C1=1.005
#C2=1.010
#C3=1.060

   C1 = 1.005
   C2 = 1.020
   C3 = 1.070
   
   B1 = 1.200
   B2 = 1.030
   B3 = 1.005
   
   D1 = 0
   D2 = 400
   curasset.D2 = D2
   
   trendadjust=1
   #Shortterm negative
   #curasset.macd30mlast < 0 and
       
   xx=len(curasset.sma1m7A)
   #if  (float(curasset.sma1m7A[xx-1]) < float(curasset.sma1m7A[xx-2] ) * 0.94 ) or  (float(curasset.sma1m7A[xx-1]) < float(curasset.sma1m7A[xx-3] ) * 0.93 )  :
   if  curasset.sma1d200 * 0.85 > curasset.lastprice:
   
       curasset.path=curasset.path+'.M0'
       B1 = 1.50
       B2 = 1.15
       B1 = 1.05
   else:
       if  curasset.sma1d200 * 0.90 > curasset.lastprice:
   
            curasset.path=curasset.path+'.M1'
            B1 = 1.30
            B2 = 1.04
            B1 = 1.01

   if  curasset.macd1hlast < 0 and curasset.macd4hlast< 0 and curasset.regression < D2/3:
            trendadjust=B1
            #print('1h',curasset.macd1hlast, '4h',curasset.macd4hlast,  'reg',curasset.regression, 'D2',D2, D2/2)
            curasset.path=curasset.path+'.i1'
   else:   
         if curasset.macd4hlast < 0 and curasset.regression < D2/3:
               trendadjust=B2
               curasset.path=curasset.path+'.i2'
         else:
                  #mediumterm positive
                  if ( curasset.macd1hlast > 0 and curasset.macd1hlast > 0 ):
                        trendadjust=trendadjust * 0.98                  
                        curasset.path=curasset.path+'.i3'
                  else:
                        curasset.path=curasset.path+'.i4'
                        trendadjust=B3
   # ==============================================================
   if change >= 0.0:
            trendadjust=trendadjust * 0.990
            curasset.path=curasset.path+'.c0'
   if change > 0.50:
            trendadjust=trendadjust * 0.985
            curasset.path=curasset.path+'.c1'
   if change > 1.00:
            trendadjust=trendadjust * 0.980
            curasset.path=curasset.path+'.c2'
   if change > 2.00:
            trendadjust=trendadjust * 0.975
            curasset.path=curasset.path+'.c3'                                                  
   if change <= 0.0:
            trendadjust=trendadjust * 1
            curasset.path=curasset.path+'.c4'
   if change < -0.50:
            trendadjust=trendadjust * C1
            curasset.path=curasset.path+'.c5'
   if change < -1.0:
            trendadjust=trendadjust * C2
            curasset.path=curasset.path+'.c6'
   if change < -2.0:
            trendadjust=trendadjust * C3
            curasset.path=curasset.path+'.c7'
   if change < -5.0:
            trendadjust=trendadjust * C3 * C1
            curasset.path=curasset.path+'.c8' 
   if change < -7.0:
            trendadjust=trendadjust * C1 * C2 * C3
            curasset.path=curasset.path+'.c9'
   
   #if change < -10.0:
   #         trendadjust=trendadjust * C1 * C2 * C3 * 1.1
   #         curasset.path=curasset.path+'.c10'
   
   
   if curasset.macd1wlast < -D2 * 1.5 or (curasset.macd1wlast < -D2 and curasset.macd3dlast< -D2):
      trendadjust=trendadjust * 1.001
      curasset.path=curasset.path+'.t1'
      
   if curasset.regressionWeek < - D2:
      trendadjust=trendadjust * 1.008
      curasset.path=curasset.path+'.t1a'
   
      
   curasset.path=curasset.path+'='+str(round(trendadjust,2))
   #print(trendadjust, curasset.path)
   curasset.levdefault=round(curasset.levmin * 1.00 * trendadjust , 3)
   curasset.levmax=round(curasset.levmin * 1.005 * trendadjust , 3) 
   

   if curasset.symbol in('BTCUSDT','BTCBUSD','ETHBUSD') :
      #if curasset.ema1w7 >  curasset.ema1w14:
      #    curasset.path=curasset.path+'.e1'        
      #    if (curasset.macd4hlast <0 and change <0):
      #       if curasset.levdefault < 1.30:
       #         curasset.levdefault = 1.30
      #          curasset.levmax = 1.31
      #    else:
      #         curasset.levdefault = 1.13
       #        curasset.levmax = 1.14
      #else:
      #    if curasset.levdefault < 1.25:
      #          curasset.levdefault = 1.25
      #          curasset.levmax = 1.26
                
            
      if curasset.levdefault > 1.60 and curasset.regression > -D2 * 3:
         curasset.levdefault = 1.60
         curasset.levmax = 1.65
         
      if curasset.ema1w7 < curasset.ema1w14:
         curasset.levdefault = curasset.levdefault * 1.01
         curasset.levmax = curasset.levmax * 1.01
      if curasset.ema1w7 >  curasset.ema1w14:
         curasset.levdefault = curasset.levdefault * 0.99
         curasset.levmax = curasset.levmax * 0.99
         
   else:
      if curasset.levdefault < 1.27:
         curasset.levdefault = 1.27
         curasset.levmax = 1.29
      
      if curasset.levdefault > 1.60 and curasset.regression > -D2 * 3 and curasset.lastprice > curasset.sma1d200:
         curasset.levdefault = 1.60
         curasset.levmax = 1.70
         
         
   negative=0
   #if curasset.macd30mlast<0:
   #   negative=negative+1
   
   if curasset.macd1hlast<0:
      negative=negative+1

   if curasset.macd4hlast<0:
      negative=negative+1

   if curasset.macd12hlast<0:
      negative=negative+1

   if curasset.macd1dlast<0:
      negative=negative+1
   
   if curasset.macd3dlast<0:
      negative=negative+1
   
   if curasset.macd1wlast<0:
      negative=negative+1

   
   if curasset.levdefault < 1.12 :
         curasset.levdefault = 1.12
         curasset.levmax = 1.13
         
         
   curasset.negative=negative
   curasset.path=curasset.path+'tr=' + str(round(trendadjust,3))        
          
   return trendadjust

def st1(client, df, curasset, hhist1h, hhist12h, change):

       now = datetime.now()  
       ############################### 
       ############ BUY  ############# 
       ############################### 
       #print( 'XXX',curasset.margin, curasset.levmin, curasset.levmax ) 
       
       pos=len(df.close)
       
       posema1h7=len(curasset.ema1h7A)
       posema1h14=len(curasset.ema1h14A)
       
       
       posemaw7=len(curasset.ema1w7A)
       posemaw14=len(curasset.ema1w14A)
       
       posema7=len(curasset.ema1w7A)
       posema14=len(curasset.ema1w14A)
       orderprice=round(curasset.lastprice * 1.001, curasset.decplaces)
       
       
       if curasset.macd3dlast > -curasset.D2 / 1.5:
       
           orderqtd=round(round(float(curasset.freeLoan))*0.20/orderprice, curasset.decplacesqtd)
           if (curasset.ema1w7A[posemaw7-1] > curasset.ema1w14A[posemaw14-1] and curasset.ema1w7A[posemaw7-2] < curasset.ema1w14A[posemaw14-2] and curasset.buyseconds > 259200 and curasset.sellseconds > 3600):
                     curasset.path=curasset.path+'.st11'
                     orderqtd=round(round(float(curasset.freeLoan))*0.50/orderprice, curasset.decplacesqtd)
                     if orderprice * orderqtd < curasset.minValue :
                               orderqtd=round(float(curasset.minValue)/orderprice, curasset.decplacesqtd)
                               
                     if orderprice > 0 and orderprice * orderqtd > curasset.minValue and round(curasset.netasset, curasset.decplacesqtd) > orderqtd:
                               try:
                                  bot5_bin_orders.create(client, curasset,  'SELL', orderqtd, orderprice, 'SELL EMA')
                               except BinanceAPIException as e:
                                  print('SELL 1', orderqtd, orderprice, e) 
            
           posema7=len(curasset.ema12h7A)
           posema14=len(curasset.ema12h14A)
        
           if (curasset.ema12h7A[posema7-1] > curasset.ema12h14A[posema14-1] and curasset.ema12h7A[posema7-2] < curasset.ema12h14A[posema14-2]) and curasset.buyseconds > 125000 and curasset.sellseconds > 3600:
                     
                     
                     curasset.path=curasset.path+'.st12'
                     orderqtd=round(round(float(curasset.freeLoan))*0.40/orderprice, curasset.decplacesqtd)
                     if orderprice * orderqtd < curasset.minValue :
                               orderqtd=round(float(curasset.minValue)/orderprice, curasset.decplacesqtd)
                               
                     if orderprice > 0 and orderprice * orderqtd > curasset.minValue and round(curasset.netasset, curasset.decplacesqtd) > orderqtd:
                               try:
                                  bot5_bin_orders.create(client, curasset,  'SELL', orderqtd, orderprice, 'SELL EMA')
                               except BinanceAPIException as e:
                                  print('SELL 2', orderqtd, orderprice, e)                       
           
           
           if curasset.ema1w7A[posemaw7-1] > curasset.ema1w14A[posemaw14-1]  and curasset.rsi7h < 35 and curasset.buyseconds > 36000 and curasset.sellseconds > 3600:
                     
                     curasset.path=curasset.path+'.st13'
                     orderqtd=round(round(float(curasset.freeLoan))*0.30/orderprice, curasset.decplacesqtd)
                     if orderprice * orderqtd < curasset.minValue :
                               orderqtd=round(float(curasset.minValue)/orderprice, curasset.decplacesqtd)
                               
                     if orderprice > 0 and orderprice * orderqtd > curasset.minValue and curasset.netasset > orderqtd:
                               try:
                                  bot5_bin_orders.create(client, curasset,  'SELL', orderqtd, orderprice, 'SELL RSI')
                               except BinanceAPIException as e:
                                  print('SELL 3', orderqtd, orderprice, e)                            
           
           else:
              if  curasset.rsi7h < 25 and curasset.buyseconds > 36000:
                     
                     curasset.path=curasset.path+'.st13'
                     orderqtd=round(round(float(curasset.freeLoan))*0.30/orderprice, curasset.decplacesqtd)
                     if orderprice * orderqtd < curasset.minValue :
                               orderqtd=round(float(curasset.minValue)/orderprice, curasset.decplacesqtd)
                               
                     if orderprice > 0 and orderprice * orderqtd > curasset.minValue and round(curasset.netasset, curasset.decplacesqtd) > orderqtd :
                               try:
                                  bot5_bin_orders.create(client, curasset,  'SELL', orderqtd, orderprice, 'SELL DEEP RSI')
                               except BinanceAPIException as e:
                                  print('SELL 3', orderqtd, orderprice, e)                            
      
           if curasset.ema1h7A[posema1h7-1] > curasset.ema1h14A[posema1h14-1] and curasset.ema1h7A[posema1h7-2] < curasset.ema1h14A[posema1h14-2] and curasset.buyseconds > 2400 and curasset.sellseconds > 14400:
                 #print('--------------------------------------------------------------------------------------')         
                 orderqtd=round(round(float(curasset.freeLoan)) * 0.30/orderprice, curasset.decplacesqtd)
                 if orderprice * orderqtd < curasset.minValue :
                           orderqtd=round(float(curasset.minValue)/orderprice, curasset.decplacesqtd)
                           
                 if orderprice > 0 and orderprice * orderqtd > curasset.minValue and round(curasset.netasset, curasset.decplacesqtd) > orderqtd:
                           try:
                              bot5_bin_orders.create(client, curasset,  'SELL', orderqtd, orderprice, 'SELL 4 ' + str(curasset.netasset))
                           except BinanceAPIException as e:
                              print('SELL 4', orderqtd, orderprice, e)                 
       ################################# 
       ############ SELL for Gain ######
       ################################# 
       
       # alterem 1500 para 3600 rever e adicionei ultimo passo da st3
       posema7=len(curasset.ema1w7A)
       posema14=len(curasset.ema1w14A)
       orderprice=round(curasset.lastprice * 0.999, curasset.decplaces)
       if  (curasset.ema1w7A[posemaw7-1] < curasset.ema1w14A[posemaw14-1] and curasset.ema1w7A[posemaw7-2] > curasset.ema1w14A[posemaw14-2] ) :
          
                orderqtd=round(round(float(curasset.netasset))*0.35/orderprice, curasset.decplacesqtd)

                #print('RSI',curasset.rsi1h,'qtd', orderqtd, orderprice )
                
                if orderprice * orderqtd < curasset.minValue :
                        orderqtd=round(float(curasset.minValue+5)/orderprice, curasset.decplacesqtd)
                if orderqtd<float(curasset.netasset) and orderprice > 0 and orderprice * orderqtd > curasset.minValue and (float(curasset.netasset)-orderqtd)*orderprice > float(curasset.atualasset) * 0.4 and curasset.sellseconds > 259200:
                        try:
                           if curasset.sellcount<6:
                              bot5_bin_orders.create(client, curasset, 'BUY', orderqtd, orderprice, 'BUY EMA')
                        except BinanceAPIException as e:
                           print('BUY EMA', orderqtd, orderprice, e) 
       
       else:
         if curasset.rsi7h > 85 and change > 1.0 and curasset.sellseconds > 7200:
                 
                 orderqtd=round(round(float(curasset.netasset))*0.30/orderprice, curasset.decplacesqtd)
                 if orderprice * orderqtd < curasset.minValue :
                           orderqtd=round(float(curasset.minValue)/orderprice, curasset.decplacesqtd)
                           
                 if orderprice > 0 and orderprice * orderqtd > curasset.minValue :
                           try:
                              bot5_bin_orders.create(client, curasset,  'BUY', orderqtd, orderprice, 'BUY RSI')
                           except BinanceAPIException as e:
                              print('BUY 3', orderqtd, orderprice, e)                                   
       
         else:
             if curasset.rsi7h > 75 and change > 1.0 and curasset.sellseconds > 7200:
                 
                 orderqtd=round(round(float(curasset.netasset))*0.20/orderprice, curasset.decplacesqtd)
                 if orderprice * orderqtd < curasset.minValue :
                           orderqtd=round(float(curasset.minValue)/orderprice, curasset.decplacesqtd)
                           
                 if orderprice > 0 and orderprice * orderqtd > curasset.minValue :
                           try:
                              bot5_bin_orders.create(client, curasset,  'BUY', orderqtd, orderprice, 'BUY RSI')
                           except BinanceAPIException as e:
                              print('BUY 3', orderqtd, orderprice, e)        

       
          
             else:
                  if curasset.ema1h7A[posema1h7-1] < curasset.ema1h14A[posema1h14-1] and curasset.ema1h7A[posema1h7-2] > curasset.ema1h14A[posema1h14-2] and curasset.sellseconds > 2400:
                     #print('--------------------------------------------------------------------------------------')         
                     orderqtd=round(round(float(curasset.netasset)) * 0.30/orderprice, curasset.decplacesqtd)
                     if orderprice * orderqtd < curasset.minValue :
                               orderqtd=round(float(curasset.minValue)/orderprice, curasset.decplacesqtd)
                               
                     if orderprice > 0 and orderprice * orderqtd > curasset.minValue :
                               try:
                                  bot5_bin_orders.create(client, curasset,  'BUY', orderqtd, orderprice, 'BUY 4')
                               except BinanceAPIException as e:
                                  print('BUY 4', orderqtd, orderprice, e)                            

def pay(client,df, curasset, change, millseconds_next):
    now = datetime.now()  
    
    
    if True: 
      stoplimit = curasset.levdefault * 1.05
         
      if curasset.ema1w7 >  curasset.ema1w14 and curasset.ema12h7 >  curasset.ema12h14 and curasset.macd4hlast>0 and curasset.lastprice > curasset.sma1d200 :
         #good news 
         stoplimit=float(curasset.levmin) * 1
      #else:
      #    stoplimit=float(curasset.levdefault * 0.70 )
          
      if curasset.ema12h7 <  curasset.ema12h14 and curasset.macd1hlast<0:
        stoplimit = curasset.levdefault * 1.05
        if curasset.ema3d7 <  curasset.ema3d14:
           stoplimit = curasset.levdefault * 1
       
      else:
         if stoplimit < curasset.levmin :
            stoplimit = curasset.levmin
      
      valtopay = round(float(curasset.borrowed) - (curasset.atualasset / (stoplimit - 1)),2)
      
      curasset.path=curasset.path+'.sl='+str(round(stoplimit,3))

      if ( curasset.margin  < stoplimit ):   
          if curasset.printdebug:
             print('Repay Reduce RISK / levdefault', curasset.symbol, curasset.baseAsset , 'free amount:', curasset.freeAsset, 'pay',valtopay, 'margin', curasset.margin, 'def', curasset.levdefault,'stoplimit',str(round(stoplimit,2)),'lastprice', curasset.lastprice)
          
          if float(curasset.freeAsset) >0  and valtopay>0:
             bot5_bin_orders.pay(client, curasset, 'BUY', valtopay, 'pay from free ')
             


def get(client,df, curasset):
    now = datetime.now()  
    
    # --------------------------------------------------------------------------
    # ------ get loan if margin over  max value
    # --------------------------------------------------------------------------
    #print(float(curasset.levdefault) * 1.005, curasset.macd1dlast, curasset.macd3dlast, curasset.buyseconds, curasset.D2 , curasset.regression )    

    if (curasset.margin > float(curasset.levdefault) )  and  curasset.macd1hlast > 0 and curasset.macd4hlast > 0 and curasset.macd3dlast  > -curasset.D2 /2 and curasset.buyseconds > 28800 and  curasset.ema1d14 > curasset.ema1d30:
          curasset.path=curasset.path+'.g1'
       #if curasset.freeLoan > 0:
          

          if curasset.ema1w7 < curasset.ema1w14 and  curasset.rsi7h < 65:
                  valLoan = round(curasset.freeLoan * 0.75, 2)  
                  if curasset.ema3d7 < curasset.ema3d14:
                      valLoan = round(curasset.freeLoan * 0.50, 2)  # 80%
          else:
                   valLoan = round(curasset.freeLoan * 0.30, 2)  # 80%
                   if curasset.ema3d7 < curasset.ema3d14 or curasset.rsi7h > 65:
                      valLoan = round(curasset.freeLoan * 0.20, 2)  # 80%
                   

          curasset.path=curasset.path+'.g2'  
          #if curasset.printdebug:
          #   print('L', curasset.moment, curasset.symbol, 'get loan :', curasset.freeLoan,  'amount:', curasset.minValue, 'new loan', valLoan) 
       
          try:
          
             if float(valLoan)  > curasset.minValue and curasset.freeLoan > curasset.minValue and float(valLoan)  <  curasset.freeLoan: # and curasset.rsi7h < 80:  # in review
                 #valLoan = round(curasset.freeLoan * 0.60, 2)  # 80%
                 #print('Loan', valLoan)
                 if "USDT" in curasset.symbol:
                    #transaction = client.create_margin_loan(asset='USDT', symbol=curasset.symbol , isIsolated='TRUE', amount= valLoan) 
                    curasset.currency='USDT'
     #              bot4_bin_orders.loan(client, curasset, valLoan, 'Loan '+ str(valLoan))
                     
                 else:
                    curasset.currency='USDT'
      #              bot4_bin_orders.loan(client, curasset, valLoan, 'Loan '+ str(valLoan))
                   #transaction = client.create_margin_loan(asset='BUSD', symbol=curasset.symbol , isIsolated='TRUE', amount= valLoan) 

                 orderprice=round(float(curasset.lastprice) * 1.001,  curasset.decplaces)              
                 orderqtd=round((valLoan * 0.98 )/orderprice, curasset.decplacesqtd)
                 if (orderqtd * orderprice < curasset.minValue and orderqtd>0 ):
                     orderqtd = round(float(curasset.minValue)/orderprice, curasset.decplacesqtd)

                 try:
                     
                     #bot5_bin_orders.create(client, curasset, 'BUY', orderqtd, orderprice, 'LOAN BUY')
                     curasset.borrowed = curasset.borrowed +  orderqtd * orderprice
                     curasset.netasset = curasset.netasset + orderqtd
                     #curasset.getbuy = True
                     #if curasset.sellcount<5:
                        #order = client.create_margin_order( symbol=curasset.symbol, isIsolated='TRUE', side='SELL', type='LIMIT', timeInForce='GTC', quantity=orderqtd, price=round(orderprice * curasset.gain, curasset.decplaces) ) 
                        #print(now.strftime("%Y-%m-%d %H:%M:%S"), 'LOAN SELL',orderqtd, orderprice)
                     #   bot4_bin_orders.create(client, curasset, 'SELL', orderqtd, orderprice, 'LOAN SELL')

                 except BinanceAPIException as e:
                     print('DIPS: erro buy limit' )   
                     print(e)

          except BinanceAPIException as e:
                  print('erro loan ...')
                  print(e)
   