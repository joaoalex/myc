from datetime import datetime
from binance.exceptions import BinanceAPIException
import numpy
import math
import bot4_bin_orders
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
   
   B1 = 1.180
   B2 = 1.010
   B3 = 1.005
   
   D1 = 0
   D2 = 400
   curasset.D2 = D2
   
   trendadjust=1
   #Shortterm negative
   #curasset.macd30mlast < 0 and
   
   
   if  curasset.macd1hlast < 0 and curasset.macd4hlast< 0 and curasset.regression < D2/4:
            trendadjust=B1
            #print('1h',curasset.macd1hlast, '4h',curasset.macd4hlast,  'reg',curasset.regression, 'D2',D2, D2/2)
            curasset.path=curasset.path+'.i1'
   else:   
         if curasset.macd4hlast < 0 and curasset.regression < D2/4:
               trendadjust=B2
               curasset.path=curasset.path+'.i2'
         else:
                  #mediumterm positive
                  if ( curasset.macd1hlast > 0 and curasset.macd1hlast > 0 ):
                        trendadjust=1                  
                        curasset.path=curasset.path+'.i3'
                  else:
                        curasset.path=curasset.path+'.i4'
                        trendadjust=B3

   #if curasset.ema1d14 < curasset.ema1d30:
   #                     curasset.path=curasset.path+'.e0'
   #                     trendadjust=B2

   #if curasset.ema1d14 < curasset.ema1d100:
   #                     curasset.path=curasset.path+'.e1'
   #                     trendadjust=B3
   
   #if curasset.lastprice < curasset.ema1d30:
   #                     curasset.path=curasset.path+'.e2'
   #                     trendadjust=trendadjust * 1.005
   
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
   if change < -4.0:
            trendadjust=trendadjust * C3 * C1 * 1.0
            curasset.path=curasset.path+'.c8' 
   if change < -6.0:
            trendadjust=trendadjust * C1 * C2 * C3 * 1.0
   if change < -8.0:
            trendadjust=trendadjust * C1 * C2 * C3 * 1.150
            curasset.path=curasset.path+'.c90'
   
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
                
            
      if curasset.levdefault > 1.90 and curasset.regression > -D2 * 2:
         curasset.levdefault = 1.90
         curasset.levmax = 2.00
      else:
         if curasset.levdefault > 4.0:
            curasset.levdefault = 4.00
            curasset.levmax = 4.10
             
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
      
      if curasset.levdefault > 1.60 and curasset.regression > -D2 * 3:
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

   
   if curasset.levdefault < 1.125:
         curasset.levdefault = 1.125
         curasset.levmax = 1.140       
         
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
       
       if float(curasset.netasset) <= 0 :
                 curasset.path=curasset.path+'.st10'
                 orderqtd=round(round(float(curasset.freeLoan)) * 0.20/orderprice, curasset.decplacesqtd)
                 if orderprice * orderqtd < curasset.minValue :
                           orderqtd=round(float(curasset.minValue)/orderprice, curasset.decplacesqtd)
                           
                 if orderprice > 0 and orderprice * orderqtd > curasset.minValue :
                           try:
                              bot4_bin_orders.create(client, curasset,  'BUY', orderqtd, orderprice, 'BUY INITIAL')
                           except BinanceAPIException as e:
                              print('BUY 0', orderqtd, orderprice, e) 
       
       
       if curasset.macd3dlast > -curasset.D2 / 2 and curasset.macd12hlast > 0:
       
           orderqtd=round(round(float(curasset.freeLoan))*0.20/orderprice, curasset.decplacesqtd)
           if (curasset.ema1w7A[posemaw7-1] > curasset.ema1w14A[posemaw14-1] and curasset.ema1w7A[posemaw7-2] < curasset.ema1w14A[posemaw14-2] and curasset.buyseconds > 259200 and curasset.sellseconds > 3600):
                     curasset.path=curasset.path+'.st11'
                     orderqtd=round(round(float(curasset.freeLoan))*0.50/orderprice, curasset.decplacesqtd)
                     if orderprice * orderqtd < curasset.minValue :
                               orderqtd=round(float(curasset.minValue)/orderprice, curasset.decplacesqtd)
                               
                     if orderprice > 0 and orderprice * orderqtd > curasset.minValue :
                               try:
                                  bot4_bin_orders.create(client, curasset,  'BUY', orderqtd, orderprice, 'BUY EMA')
                               except BinanceAPIException as e:
                                  print('BUY 1', orderqtd, orderprice, e) 
            
           posema7=len(curasset.ema12h7A)
           posema14=len(curasset.ema12h14A)
        
           if (curasset.ema12h7A[posema7-1] > curasset.ema12h14A[posema14-1] and curasset.ema12h7A[posema7-2] < curasset.ema12h14A[posema14-2]) and curasset.buyseconds > 125000 and curasset.sellseconds > 3600:
                     
                     
                     curasset.path=curasset.path+'.st12'
                     orderqtd=round(round(float(curasset.freeLoan))*0.40/orderprice, curasset.decplacesqtd)
                     if orderprice * orderqtd < curasset.minValue :
                               orderqtd=round(float(curasset.minValue)/orderprice, curasset.decplacesqtd)
                               
                     if orderprice > 0 and orderprice * orderqtd > curasset.minValue :
                               try:
                                  bot4_bin_orders.create(client, curasset,  'BUY', orderqtd, orderprice, 'BUY EMA')
                               except BinanceAPIException as e:
                                  print('BUY 2', orderqtd, orderprice, e)                       
           
           
           if curasset.ema1w7A[posemaw7-1] > curasset.ema1w14A[posemaw14-1]  and curasset.rsi7h < 35 and curasset.buyseconds > 36000 and curasset.sellseconds > 3600:
                     
                     curasset.path=curasset.path+'.st13'
                     orderqtd=round(round(float(curasset.freeLoan))*0.30/orderprice, curasset.decplacesqtd)
                     if orderprice * orderqtd < curasset.minValue :
                               orderqtd=round(float(curasset.minValue)/orderprice, curasset.decplacesqtd)
                               
                     if orderprice > 0 and orderprice * orderqtd > curasset.minValue :
                               try:
                                  bot4_bin_orders.create(client, curasset,  'BUY', orderqtd, orderprice, 'BUY RSI')
                               except BinanceAPIException as e:
                                  print('BUY 3', orderqtd, orderprice, e)                            
           
           else:
              if  curasset.rsi7h < 25 and curasset.buyseconds > 36000:
                     
                     curasset.path=curasset.path+'.st13'
                     orderqtd=round(round(float(curasset.freeLoan))*0.30/orderprice, curasset.decplacesqtd)
                     if orderprice * orderqtd < curasset.minValue :
                               orderqtd=round(float(curasset.minValue)/orderprice, curasset.decplacesqtd)
                               
                     if orderprice > 0 and orderprice * orderqtd > curasset.minValue :
                               try:
                                  bot4_bin_orders.create(client, curasset,  'BUY', orderqtd, orderprice, 'BUY DEEP RSI')
                               except BinanceAPIException as e:
                                  print('BUY 3', orderqtd, orderprice, e)                            
                
      
           if curasset.ema1h7A[posema1h7-1] > curasset.ema1h14A[posema1h14-1] and curasset.ema1h7A[posema1h7-2] < curasset.ema1h14A[posema1h14-2] and curasset.buyseconds > 2400 and curasset.sellseconds > 14400:
                 #print('--------------------------------------------------------------------------------------')         
                 orderqtd=round(round(float(curasset.freeLoan)) * 0.30/orderprice, curasset.decplacesqtd)
                 if orderprice * orderqtd < curasset.minValue :
                           orderqtd=round(float(curasset.minValue)/orderprice, curasset.decplacesqtd)
                           
                 if orderprice > 0 and orderprice * orderqtd > curasset.minValue :
                           try:
                              bot4_bin_orders.create(client, curasset,  'BUY', orderqtd, orderprice, 'BUY 4')
                           except BinanceAPIException as e:
                              print('BUY 4', orderqtd, orderprice, e)                 
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
                              bot4_bin_orders.create(client, curasset, 'SELL', orderqtd, orderprice, 'SELL EMA')
                        except BinanceAPIException as e:
                           print('SELL EMA', orderqtd, orderprice, e) 
       
       else:
         if ((curasset.rsi7h > 85 and change > 1.0 and curasset.sellseconds > 7200) or ( (curasset.rsi7h > 91 or curasset.rsi1h > 71) and curasset.sellseconds > 900) ) and curasset.buyseconds > 2400 and curasset.getbuy == False:
                 
                 orderqtd=round(round(float(curasset.netasset))*0.30/orderprice, curasset.decplacesqtd)
                 if orderprice * orderqtd < curasset.minValue :
                           orderqtd=round(float(curasset.minValue)/orderprice, curasset.decplacesqtd)
                           
                 if orderprice > 0 and orderprice * orderqtd > curasset.minValue :
                           try:
                              bot4_bin_orders.create(client, curasset,  'SELL', orderqtd, orderprice, 'SELL RSI')
                           except BinanceAPIException as e:
                              print('SELL 3', orderqtd, orderprice, e)                                   
       
         else:
             if curasset.rsi7h > 75 and change > 1.0 and curasset.sellseconds > 7200:
                 
                 orderqtd=round(round(float(curasset.netasset))*0.20/orderprice, curasset.decplacesqtd)
                 if orderprice * orderqtd < curasset.minValue :
                           orderqtd=round(float(curasset.minValue)/orderprice, curasset.decplacesqtd)
                           
                 if orderprice > 0 and orderprice * orderqtd > curasset.minValue :
                           try:
                              bot4_bin_orders.create(client, curasset,  'SELL', orderqtd, orderprice, 'SELL RSI')
                           except BinanceAPIException as e:
                              print('SELL 3', orderqtd, orderprice, e)        

       
          
             else:
                  if (curasset.ema1h7A[posema1h7-1] < curasset.ema1h14A[posema1h14-1] and curasset.ema1h7A[posema1h7-2] > curasset.ema1h14A[posema1h14-2] and curasset.sellseconds > 2400) and curasset.buyseconds > 2400 and curasset.getbuy == False:
                     #print('--------------------------------------------------------------------------------------')         
                     orderqtd=round(round(float(curasset.netasset)) * 0.30/orderprice, curasset.decplacesqtd)
                     if orderprice * orderqtd < curasset.minValue :
                               orderqtd=round(float(curasset.minValue)/orderprice, curasset.decplacesqtd)
                               
                     if orderprice > 0 and orderprice * orderqtd > curasset.minValue :
                               try:
                                  bot4_bin_orders.create(client, curasset,  'SELL', orderqtd, orderprice, 'SELL 4')
                               except BinanceAPIException as e:
                                  print('SELL 4', orderqtd, orderprice, e)                            

def pay(client,df, curasset, change, millseconds_next):

    now = datetime.now()  
    
    #valtopay = round(float(curasset.borrowed) - (curasset.atualasset / (curasset.levmin-1)),2)
    
    #print("----------- Pay LOAN -----------", valtopay, curasset.margin, curasset.atualasset, curasset.borrowed, curasset.freeAsset )
    # --------------------------------------------------------------------------
    # ------ pay loan if margin below min value
    # --------------------------------------------------------------------------
    if ( curasset.margin < curasset.levcritical)  :
       valtopay = round(float(curasset.borrowed) - (curasset.atualasset / (curasset.levcritical * 1.07 - 1)), 2)
       if float(curasset.freeAsset) - valtopay < 0  and curasset.sellseconds > 1800: 
          if curasset.printdebug:
             print(datetime.fromtimestamp(curasset.millseconds_next),';', 'Repay 1 margin:', curasset.symbol, curasset.baseAsset , 'free amount:', curasset.freeAsset, 'pay',valtopay, 'margin', curasset.margin, 'min',curasset.levcritical,'lastprice', curasset.lastprice)
          if float(curasset.freeAsset) >0 and valtopay>0:
             
             bot4_bin_orders.pay(client, curasset, 'PAY', curasset.freeAsset,'pay from free')
             valtopay=valtopay-float(curasset.freeAsset)
          
          orderprice=round(float(curasset.lastprice) * 0.995, curasset.decplaces)   #ao melhor
          orderqtd=round(valtopay/orderprice, curasset.decplacesqtd)
          
          if orderqtd > float(curasset.netasset) * 0.25:
             orderqtd=float(curasset.netasset) * 0.25 
             orderqtd=round(orderqtd, curasset.decplacesqtd)
             
          if orderqtd * orderprice >  curasset.minValue:  
             # if < 
             # orderqtd=round((curasset.minValue)/orderprice, curasset.decplacesqtd)
             
             try:
                #print(now.strftime("%Y-%m-%d %H:%M:%S"), curasset.symbol, 'SELL to pay loan :',  curasset.freeLoan , 'pay', valtopay)
                #order = client.create_margin_order( symbol=curasset.symbol, isIsolated='TRUE', side='SELL', type='LIMIT', timeInForce='GTC', quantity=orderqtd, price = orderprice)
                
                #print(now.strftime("%Y-%m-%d %H:%M:%S"), 'SELL',orderqtd, orderprice)    
                bot4_bin_orders.create(client, curasset, 'SELL', orderqtd, orderprice,'PAYNOPRICE')

             except BinanceAPIException as e:
                print('erro buy limit' ) 
                print(e)

       valtopay = round(float(curasset.borrowed) - (curasset.atualasset / (curasset.levcritical * 1.03 - 1)),2)
       
       if float(curasset.freeAsset) > 0:
         # myasset / x = newracio => x = myasset / newracio
         if float(curasset.freeAsset) < valtopay and float(curasset.freeAsset)>0:
               valtopay=float(curasset.freeAsset)

         #print('Repay loan :', curasset.symbol, curasset.baseAsset , 'free amount:', curasset.freeAsset, 'pay',valtopay)
         if  valtopay>0:
            if valtopay>curasset.borrowed:
               valtopay=curasset.borrowed
            try:
               #print(now.strftime("%Y-%m-%d %H:%M:%S"),curasset.symbol, 'pay loan :', curasset.freeLoan, curasset.symbol , 'pay', valtopay) 
               #print ('USDTTTTTTTTTTTTTTTTTTTTTTTTTT')
               #transaction = client.repay_margin_loan(asset='USDT', symbol=curasset.symbol , isIsolated='TRUE', amount=valtopay)
               bot4_bin_orders.pay(client, curasset,'REPAY', valtopay, 'REPAY: margin too low')
               
            except BinanceAPIException as e:
               print('erro repay ...')
               print(e)

    else: 
      stoplimit = curasset.levdefault * 0.92
         
      if curasset.ema1w7 >  curasset.ema1w14 and curasset.ema12h7 >  curasset.ema12h14 and curasset.macd4hlast>0 and curasset.macd3dlast>0 :
         #good news 
         stoplimit=float(curasset.levmin) * 1
      #else:
      #    stoplimit=float(curasset.levdefault * 0.70 )
      if ( curasset.regression > curasset.D2 and curasset.regressionDay > curasset.D2/4 and change >0 and curasset.macd3dlast >  curasset.D2 and  curasset.macd1dlast >  curasset.D2 ):   
             stoplimit=float(curasset.levmin) * 1
      else:
           curasset.path=curasset.path+'.rg1'
           #+str(curasset.ema12h7)+' '+str(curasset.ema12h14)+' '+str(curasset.ema1d14)+' '+str(curasset.ema1d30)+' '+str(curasset.ema1d100)

           if curasset.ema12h7 <  curasset.ema12h14 and curasset.macd1hlast<0:
               curasset.path=curasset.path+'.rg2'
               stoplimit = curasset.levdefault * 0.95
               #if curasset.ema3d7 <  curasset.ema3d14:

           if curasset.ema1d14 < curasset.ema1d30 * 0.95:
                  curasset.path=curasset.path+'.rg3'
                  stoplimit = curasset.levdefault * 1.01

           if curasset.ema1d14 < curasset.ema1d100 * 0.95:
                  curasset.path=curasset.path+'.rg4'
                  stoplimit = curasset.levdefault * 1.02
      
      if stoplimit < curasset.levmin :
         stoplimit = curasset.levmin
        
      
      
      #else:
      #if stoplimit > 1.20 :
      #   stoplimit = 1.20
      
      #if curasset.levdefault > stoplimit:
      #   
      valtopay = round(float(curasset.borrowed) - (curasset.atualasset / (stoplimit - 1)),2)
      
      #else:
      #   valtopay = round(float(curasset.borrowed) - (curasset.atualasset / (curasset.levdefault -1)),2)
      
      curasset.path=curasset.path+'.sl='+str(round(stoplimit,3))

      #if ( curasset.margin  < curasset.levdefault ):   
      if ( curasset.margin  < stoplimit ):   
      #if ( curasset.margin  < curasset.levmin ):   
        #if  millseconds_next - curasset.lastsafeuse > 7200 and curasset.safe > curasset.minValue * 4:
        #     FromSafe(client,df, curasset, change, millseconds_next)
             
        #else:   
          if curasset.printdebug:
             print(datetime.fromtimestamp(curasset.millseconds_next),';','Repay 2 Reduce RISK / levdefault', curasset.symbol, curasset.baseAsset , 'free amount:', curasset.freeAsset, 'pay',valtopay, 'margin', curasset.margin, 'def', curasset.levdefault,'stoplimit',str(round(stoplimit,2)),'lastprice', curasset.lastprice)
          
          if float(curasset.freeAsset) >0  and valtopay>0:
             bot4_bin_orders.pay(client, curasset, 'SELL', curasset.freeAsset,'SELL to pay 2 ')
             valtopay=valtopay-float(curasset.freeAsset)
          
          if False and float(curasset.safe) - valtopay > curasset.atualasset * 1.5: # and curasset.ema1d14 > curasset.ema1d100:
             print(datetime.fromtimestamp(curasset.millseconds_next),';', 'Repay 2: from  safe', valtopay)
             if curasset.runmode=="SIMUL":
                curasset.safe = curasset.safe - valtopay
                curasset.freeAsset = curasset.freeAsset +  valtopay
             else:
                bot4_bin_orders.fromSpot(client, curasset, valtopay )
                curasset.safe = curasset.safe + valtopay
                                         
             curasset.lastposition = round(float(curasset.atualasset),0) +  curasset.freeAsset       #+ round(takefromsafe * curasset.lastprice,0)
             curasset.lastsafeuse=millseconds_next
          else:
               print(datetime.fromtimestamp(curasset.millseconds_next),';','Repay 2: from position', valtopay)
               orderprice=round(float(curasset.lastprice) * 0.995, curasset.decplaces)   #ao melhor
               #orderqtd=round(float(curasset.netasset) * 0.10,  curasset.decplacesqtd)
               orderqtd=round(valtopay/orderprice,  curasset.decplacesqtd)
                  
               if curasset.negative>3:
                  orderqtd=float(curasset.netasset) * 0.25
                  orderqtd=round(orderqtd, curasset.decplacesqtd)
               else:
                  #orderqtd=round(valtopay/orderprice, curasset.decplacesqtd)
                  if curasset.negative>2:
                     orderqtd=float(curasset.netasset) * 0.20
                     orderqtd=round(orderqtd, curasset.decplacesqtd)
                  else:
                     if curasset.negative==2:
                        orderqtd=float(curasset.netasset) * 0.15
                        orderqtd=round(orderqtd, curasset.decplacesqtd)
                     else:
                        if curasset.negative==1:
                           orderqtd=float(curasset.netasset) * 0.10
                           orderqtd=round(orderqtd, curasset.decplacesqtd)
                        else:
                           if curasset.negative>0:
                              orderqtd=float(curasset.netasset) * 0.07
                              orderqtd=round(orderqtd, curasset.decplacesqtd)
         
               if orderqtd * orderprice >  curasset.minValue:  
                    
                    try:
        
                        bot4_bin_orders.create(client, curasset, 'SELL', orderqtd, orderprice,'PAYNOPRICE')

                    except BinanceAPIException as e:
                        print('erro buy limit' ) 
                        print(e)

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
                  valLoan = round(curasset.freeLoan * 0.30, 2)  
                  if curasset.ema3d7 < curasset.ema3d14:
                      valLoan = round(curasset.freeLoan * 0.20, 2)  # 80%
              
          else:
          
                   valLoan = round(curasset.freeLoan * 0.75, 2)  # 80%
                   if curasset.ema3d7 < curasset.ema3d14 or curasset.rsi7h > 65:
                      valLoan = round(curasset.freeLoan * 0.50, 2)  # 80%
                   

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
                     
                     bot4_bin_orders.create(client, curasset, 'BUY', orderqtd, orderprice, 'LOAN BUY')
                     curasset.getbuy = True
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
                  
def safe1(client,df, curasset, change, millseconds_next):
    now = datetime.now()  
    if float(curasset.maxsafe) == 0 or float(curasset.maxsafe) < float(curasset.safe):
       curasset.maxsafe = curasset.safe
    
    if curasset.regression < -curasset.D2 * 1.5:
       curasset.lastposition = curasset.atualasset
       
    # teste transfer
    #bot4_bin_orders.fromSpot(client, curasset, 1 )
    #print(curasset.margin , millseconds_next,  curasset.lastsafeuse )
    if curasset.margin > 2 and millseconds_next - curasset.lastsafeuse < 3600:
        
          orderqtd1 = round(curasset.freeLoan * 0.30 / curasset.lastprice,curasset.decplacesqtd)
          #sprint('------------------ qtd2', orderqtd1)
          bot4_bin_orders.create(client, curasset, 'BUY', orderqtd1, round(curasset.lastprice * 1.005, curasset.decplaces),'SAFE: re-buy after SELL to send to Spot')

    else: #if True:
                    #if curasset.negative>=4:
                    diff  = 120000
                    diff1 = 2592000
                    diff2 = 25200   #7 horas
                    
                    if curasset.macd1wlast > -curasset.D2:
                           racio = 0.20
                           diif=120000
                    else:
                        if curasset.macd1wlast > -curasset.D2 * 1.5:
                           racio = 0.25    
                           diff=250000                            
                        else:
                           racio = 0.35
                           diff=350000 

                    #print('racio', racio, 'safe', curasset.safe, 'max', curasset.maxsafe, 'neg', curasset.negative)
             
                    factor=1.25
                    if curasset.macd3dlast < 0:
                       factor=1.15
                    
                    minpos=float(curasset.atualasset) > float(curasset.safe) * 0.4
                    if minpos>float(curasset.minposition):
                       minpos=float(curasset.minposition)
                                                 
                    if  (float(curasset.atualasset) > minpos)  and ( ( float(curasset.atualasset) > float(curasset.lastposition) * factor ) or ( curasset.regression < -curasset.D2 * 2 and curasset.millseconds_next - curasset.lastsafeuse > diff2 ) or ( curasset.regression > curasset.D2  and curasset.regressionDay > curasset.D2 ) ) and  float(curasset.lastposition) > 0:   # antes 1.25
                    #if float(curasset.atualasset) > float(curasset.atualasset) * 0.05 and float(curasset.atualasset) > curasset.lastposition * 1.35:
                    
                        profit=0.15
                        
                        
                        if curasset.macd3dlast < 0 :
                           profit=0.10
                        
                        takeprofit=round(float(curasset.atualasset) * profit,0)
                                     
                        if  float(curasset.atualasset) > float(curasset.safe) * 3:
                                     takeprofit=takeprofit * 1.10
                        else:
                           if  float(curasset.atualasset) > float(curasset.safe) * 4:
                                     takeprofit=takeprofit * 1.20
                           else:
                               if  float(curasset.atualasset) > float(curasset.safe) * 5:
                                     takeprofit=takeprofit * 1.30                                  
                                     
                                     
                        if  change > 2 :
                                     takeprofit=takeprofit * 1.10
                                     if curasset.rsi1h > 75:
                                         takeprofit=takeprofit * 1.20
                        else:
                             if  change > 5 :
                                 takeprofit=takeprofit * 1.20
                                 if curasset.rsi1h > 80:
                                         takeprofit=takeprofit * 1.30
                                         
                             else:
                                if  change > 7:
                                      takeprofit=takeprofit * 1.30
                                      
                                      if curasset.rsi1h > 80:
                                         takeprofit=takeprofit * 1.40                               
                                else:  
                                     
                                   if  change > 10:
                                       takeprofit=takeprofit * 1.40                                    
                                  
                                       if curasset.rsi1h > 80:
                                          takeprofit=takeprofit * 1.60
                                     
                         
                        #orderprice=round(curasset.lastprice, curasset.decplaces)
                        orderprice=round(float(curasset.lastprice) * 0.995, curasset.decplaces)   #ao melhor
                        orderqtd=round(float(takeprofit)/orderprice, curasset.decplacesqtd)
                         
                        if float(curasset.netasset) < orderqtd:
                           orderqtd=curasset.netasset

                        print(datetime.fromtimestamp(curasset.millseconds_next),';', 'to safe',curasset.safe, float(curasset.atualasset), 'last', curasset.lastposition, curasset.netasset, takeprofit,'qtd', orderqtd, 'price', orderprice)
                        if curasset.runmode=="SIMUL":
                           curasset.netasset = curasset.netasset - orderqtd
                           curasset.safe = float(curasset.safe) + ( orderqtd * orderprice )
                        else:
                           bot4_bin_orders.toSpot(client, curasset, orderqtd , orderprice)
                           curasset.safe = float(curasset.safe) + orderqtd
                        
                        curasset.lastposition = round(float(curasset.atualasset) * (1-profit),0)
                        
                        curasset.lastsafeuse = millseconds_next

                    else:
                      if float(curasset.safe) > 0 and (float(curasset.safe) > float(curasset.maxsafe) * racio or curasset.millseconds_next - curasset.lastsafeuse > diff1)  and change > -4 and curasset.macd3dlast > -curasset.D2 /2:
                        #   and (curasset.ema1d100 > curasset.ema1d200 * 0.85 or curasset.ema1d14 > curasset.ema1d30):    
                        # * curasset.lastprice 
                        #factor=0.01 + math.pow(round(curasset.safe/curasset.maxsafe,2),2)
                        factor=1                      
                        if millseconds_next - curasset.lastsafeuse> diff/2 and ( curasset.macd1dlast > curasset.D2/2 and curasset.macd3dlast > curasset.D2 and curasset.macd1wlast > curasset.D2) and curasset.regressionDay > 0:
                                     
                                 factor=0.99
                                 safex=0.25
                        
                                 takefromsafe=round(float(curasset.safe) * safex * (0.01 + factor), 0) #curasset.decplacesqtd)  
                                                                 
                                 print(datetime.fromtimestamp(curasset.millseconds_next),';','from safe X','factor:',factor, 'safe', curasset.safe, 'max', curasset.maxsafe, 'val', curasset.atualasset, 'last', curasset.lastposition, 'net', curasset.netasset, 'take', takefromsafe, 'D2', curasset.D2,curasset.maxsafe)
                                 if curasset.runmode=="SIMUL":
                                    curasset.safe = curasset.safe - takefromsafe 
                                    curasset.freeAsset = curasset.freeAsset +  takefromsafe
                                 else:
                                    
                                    bot4_bin_orders.fromSpot(client, curasset, takefromsafe )
                                    curasset.safe = curasset.safe + takefromsafe
                        
                                 curasset.lastposition = round(float(curasset.atualasset),0) +  curasset.freeAsset       #+ round(takefromsafe * curasset.lastprice,0)
                                 curasset.lastsafeuse=millseconds_next
                        
                        else:
                           if millseconds_next - curasset.lastsafeuse> diff1 and (curasset.ema1w7 > curasset.ema1w14 or curasset.macd3dlast >0 ) and curasset.macd1dlast > 0: # and curasset.regression > - curasset.D2/10:
                                
                                 #takefromsafe=round(float(curasset.safe) * 0.25 * factor, 0)                                 
                                 #factor=math.pow(round(curasset.safe/curasset.maxsafe,2),2) 
                                 factor=0.60
                                 if float(curasset.safe) < float(curasset.maxsafe) * racio or curasset.ema1d200 > curasset.ema1d100 or curasset.regressionDay < 0:
                                    factor=0.08
                                 safex=0.10
                                 #if curasset.regression > curasset.D2/2 and curasset.lastprice > curasset.ema1d14 * 0.90:
                                 #   safex=0.20
                                 takefromsafe=round(float(curasset.safe) * safex * (0.01 + factor), 0) #curasset.decplacesqtd)  
                                                                 
                                 print(datetime.fromtimestamp(curasset.millseconds_next),';','from safe 0','factor:',factor, 'safe', curasset.safe, 'max', curasset.maxsafe, 'val', curasset.atualasset, 'last', curasset.lastposition, 'net', curasset.netasset, 'take', takefromsafe, 'D2', curasset.D2,curasset.maxsafe)
                                 if curasset.runmode=="SIMUL":
                                    curasset.safe = curasset.safe - takefromsafe 
                                    curasset.freeAsset = curasset.freeAsset +  takefromsafe
                                 else:
                                    
                                    bot4_bin_orders.fromSpot(client, curasset, takefromsafe )
                                    curasset.safe = curasset.safe + takefromsafe
                        
                                    
                                 curasset.lastposition = round(float(curasset.atualasset),0) +  curasset.freeAsset       #+ round(takefromsafe * curasset.lastprice,0)
                                 curasset.lastsafeuse=millseconds_next
                           else:
                             if millseconds_next - curasset.lastsafeuse> diff and (curasset.macd1wlast > -curasset.D2 and curasset.safe > curasset.atualasset * racio and curasset.macd3dlast > -curasset.D2  and curasset.regression > -curasset.D2/4 and curasset.regressionDay >  -curasset.D2/8):

                              # and (curasset.ema1d100 > curasset.ema1d200 * 0.85 or curasset.ema1d14 > curasset.ema1d30):
                        
                                 #takefromsafe=round(float(curasset.safe) * 0.25 * factor, 0)                                 
                                 #factor=math.pow(round(curasset.safe/curasset.maxsafe,2),2) 
                                 factor=0.75
                                                  
                                 if float(curasset.safe) < float(curasset.maxsafe) * racio or curasset.ema1d200 > curasset.ema1d100 or curasset.regressionDay < 0:
                                    factor=0.05

                                 safex=0.15
                                 #if curasset.regression > curasset.D2/2 and curasset.lastprice > curasset.ema1d14 * 0.90:
                                 #   safex=0.25
                                 takefromsafe=round(float(curasset.safe) * safex * (0.01 + factor), 0) #curasset.decplacesqtd)  
                                                                 
                                 print(datetime.fromtimestamp(curasset.millseconds_next),';','from safe 1', 'factor:',factor,'safe', curasset.safe, 'max', curasset.maxsafe, 'val', curasset.atualasset, 'last', curasset.lastposition, 'net', curasset.netasset, 'take', takefromsafe, 'D2', curasset.D2, curasset.maxsafe)
                                 if curasset.runmode=="SIMUL":
                                    curasset.safe = curasset.safe - takefromsafe
                                    curasset.freeAsset = curasset.freeAsset +  takefromsafe
                                 else:
                                    bot4_bin_orders.fromSpot(client, curasset, takefromsafe )
                                    curasset.safe = curasset.safe + takefromsafe
                        
                                 
                                 curasset.lastposition = round(float(curasset.atualasset),0) +  curasset.freeAsset       #+ round(takefromsafe * curasset.lastprice,0)
                                 curasset.lastsafeuse=millseconds_next
                            
