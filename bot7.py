import os
import talib
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np

import json
import sys
from binance.client import Client
from binance.exceptions import BinanceAPIException

from datetime import datetime
from time import sleep
import time
import numpy
import bot2_stop

import bot7_ra2 as rules
import bot4_bin_orders

#import dic
from decimal import Decimal, getcontext
import math

import mpmath
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression

def klinefile(klines,filename):
    print(filename+'.txt')
    with open(filename + '.txt', 'w') as f:
                     for line in klines:
                           strline=str(line[0]) +','+ line[1]+','+ line[2]+','+ line[3]+','+ line[4]+','+line[5]
                           print(strline,file=f)
                     f.close()

def getklinefile(filename):
            nlines=[]
            
            file1 = open(filename+'.txt', 'r')
            Lines = file1.readlines()
            file1.close()
            for line in Lines:    
                nline=line.strip('\n').split(",")
                res = [eval(i) for i in nline]
                nlines.append(res)

            return nlines

class myposition:
    qtd = 0
    free = 1000



class myAsset:
    # cfg
    symbol = ""
    currency = "BUSD"
    decplaces = 2
    decplacesqtd = 5
    lossrisk = 0
    buymargin = 0
    minvalue = 0
    levcritical = 0
    levmin = 0
    levdefault = 0
    levmax = 0
    orderinvestracio = 0
    autocontrol = False

    # variable
    margin = 0
    buyseconds=0
    sellseconds=0
    lastbuy=0
    lastsell=0
    buycount = 0
    sellcount = 0
    
    lastbuyprice=0
    lastsellprice=0
    sellPrice=0
    sellcount=0
    atualasset=0
    borrowed=0
    marginLevelStatus=""
    rsi1h=0
    smarsi1h=0
    rsi4h=0
    smarsi4h=0
    rsi1d=0
    sma30m50 = 0
    sma1h50  = 0
    sma4h30 = 0
    sma1d20 = 0
    sma3d14 = 0
    sma1w7 = 0
    lastprice=0
    stopOrder=0

    sellOrder=0
    buyOrder=0
    maxstop=0
    diff=0
    gain=0
    
    macd4hlast = 0
    racio =0
    lossreserve = 0
    netasset = 0
    maxasset = 0
    liqprice = 0
    freeAsset = 0
    asset = 0
    baseAsset = 0
    freeLoan = 0
    hhist30m = 0
    hhist3d = 0
    rsi14 = 0                           
    orders=[]
    printdebug= True
    run = False
    
    D2 = 0
    moment = ''
    safe=0
    regression=0
    negative=0
    lastsafeuse=0
    path=''

# init
api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

#sFrancisco
api_key='W1LSaNO1anluDLl4bw0Kw82dqMjoSjXxtKPur4fueHrM3MAxn07vrkvQhalqbJg1'
api_secret='6PgCrJpGJv6N24e0V4vgTTSJJnqaLcbKjBrR4Auj4xjbFqgg6NQM0LrUsyIRYMkd'

#CGD
#api_key='0woY87XwWa5MYaE6uIBywL5UJifO4JHzIAsnmHwYoLTzj74afgbZ4cP44FhYojFa'
#api_secret='jolrK230a5jp9OJ049Ws0TwnF48R9gU4zwPbI72nlZpECo8YHxwhfJkjirdkeEbf'

#VODAFONE
#api_key='nLNO2P3l9QFLhCwQD5xJLb2frcVWn4N2XM24gTmGDTQPbkU05tUH78vnOQnLIA0J'
#api_secret='39kCPjPO9mLL9528OCiWvyGPtDgFx3TVL3nkFSIVe2oDUfdeBGxZvnlkIf7CiWP6'

#API Key
#nLNO2P3l9QFLhCwQD5xJLb2frcVWn4N2XM24gTmGDTQPbkU05tUH78vnOQnLIA0J
#Secret Key
#39kCPjPO9mLL9528OCiWvyGPtDgFx3TVL3nkFSIVe2oDUfdeBGxZvnlkIf7CiWP6

runmode='SIMUL'
try:
     runmode=sys.argv[1]
except:
     runmode="SIMUL"

getRealData=True
try:
     if sys.argv[2]=="FILE" and runmode=="SIMUL" :
        getRealData=False
except:
     getRealData=True

if runmode=='REAL' or sys.argv[2]=="NET":
   client = Client(api_key, api_secret)
else:
   client=''
   
   

#a=["BTCBUSD","ETHBUSD","DOGEBUSD","SHIBBUSD","LUNCBUSD"]

#print(f"Arguments count: {len(sys.argv)}")
#for i, arg in enumerate(sys.argv):
#    print(f"Argument {i:>6}: {arg}")

#B1=1.400
#B2=1.100
#B3=1.010
#C1=1.005
#C2=1.010
#C3=1.060

#D1=0
D2=0

#try:
   #if len(sys.argv[3]) > 0 :
   #   B1=float(sys.argv[3])
#except:
#      print('no parameter for B1')

#try:
#   if len(sys.argv[4]) > 0 :
#      B2=float(sys.argv[4])
#except:
#      print('no parameter for B2')

#try:
#   if len(sys.argv[5]) > 0 :
#      B3=float(sys.argv[5])
#except:
#      print('no parameter for B3')

#try:
#   if len(sys.argv[6]) > 0 :
#      C1=float(sys.argv[6])
#except:
#      print('no parameter for C1')

#try:
#   if len(sys.argv[7]) > 0 :
#      C2=float(sys.argv[7])
#except:
#      print('no parameter for C2')

#try:
#   if len(sys.argv[8]) > 0 :
#      C3=float(sys.argv[8])
#except:
#      print('no parameter for C3')
#try:
#   if len(sys.argv[9]) > 0 :
#      D1=float(sys.argv[9])
#except:
#      print('no parameter for D1')

#try:
#   if len(sys.argv[10]) > 0 :
#      D2=float(sys.argv[10])
#except:
#      print('no parameter for D2')

datarunned=False
millseconds_last=0
first_millseconds_next=1677628800
try:
   if len(sys.argv[3]) > 0 :
      first_millseconds_next=float(sys.argv[3])
except:
      print('no parameter for net')
millseconds_next=first_millseconds_next

#millseconds_next=1672577186
balance=0
sellPrice=0
high=0
low=0
diff=0
minor=0 
major=0
         
mypos = myposition()
curasset = myAsset()
curasset.runmode=runmode
curasset.path=''
if runmode=='SIMUL':
   curasset.freeAsset=1000
   curasset.safe=0
   curasset.lastposition=curasset.freeAsset
   curasset.minposition=300
   curasset.borrowed=0
   curasset.minValue=50
   curasset.freeLoan=0
   
totalrec=-1
progress=-1
printdebug=True
curasset.printdebug=printdebug
#curasset.D1=D1
curasset.D2=D2
curasset.negative=0
useSafe=True
curasset.maxsafe=0
         
while True:
      getConfig=True
      runReport=True 
      toRun=True
      checkOrders=True
      openOrders=True
      
      loopCFG=True
      executeRules=True
      
      accountData=True
      cutData=True
      getPrices=True
      othervalues=True

               
      if runmode=='REAL':
         if getConfig:
            file1 = open('trade.cfg', 'r')
            Lines = file1.readlines()
            tot_lines=len(Lines) -1 # remove header 
            symbol_cfg = [['' for x in range(15)] for x in range(tot_lines)]
            cont=-1
            
            for line in Lines:
               if (cont==-1):
                  cont=0
                  continue
               else:
                  linecfg=line.strip('\n').split(";")
                  #print(linecfg)
                  c=0
                  for col in linecfg:
                     symbol_cfg[cont][c]=col
                     c=c+1
                  cont=cont+1
         balance=0
         buyseconds=0
         sellseconds=0
         sellPrice=0
         high=0
         low=0
         diff=0
         minor=0 
         major=0
         
      else:
         symbol_cfg = [['' for x in range(15)] for x in range(1)]
         symbol_cfg[0][0] = 'BTCUSDT'
         symbol_cfg[0][1] = 2
         symbol_cfg[0][2] = 4
         symbol_cfg[0][3] = 0.009
         symbol_cfg[0][4] = 0.15
         symbol_cfg[0][5] = 1.07000
         symbol_cfg[0][6] = 1.08500
         symbol_cfg[0][7] = 1.12
         symbol_cfg[0][8] = 1.14
         symbol_cfg[0][9] = 1.012
         symbol_cfg[0][10] = 50
         symbol_cfg[0][11] = 15000
         symbol_cfg[0][12] = 0.35
         symbol_cfg[0][13] = 0.15
         symbol_cfg[0][14] = 1
      

         #BTCBUSD;2;4;0.009;0.15;1.080;1.089;1.115;1.115;1.012;25;15000;0.35;0.15;1

      racio=1.5
      minValue=15
      run=False
      now = datetime.now()  
 
      if toRun:
    
         if runReport and runmode == "REAL":
            report="<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
            report=report+ "<table border=\"1\"><tr>"
            report=report+"<td><p>ativo</p></td>"
            report=report+"<td><p>margin</p></td>"
            report=report+"<td><p>qtd</p></td>"
            report=report+"<td><p>free</p></td>"
            report=report+"<td><p style=\"color:black;\">30m/1h</p></td>"     
            report=report+"<td><p style=\"color:black;\">4h/1d</p></td>"
            report=report+"<td><p style=\"color:black;\">3d/1w</p></td>"
         
         if loopCFG:
            #print('LOOP', datetime.now() )
            #sys.stdout.flush()
            for cfg in symbol_cfg:
               
               #symbol;decplaces;decplacesqtd;lossrisk;buymargin;levcritical;levmin;levdefault;levmax;
               if runmode=="REAL":
                  curasset = myAsset()

                  curasset.runmode=runmode
                  curasset.buyseconds=0
                  curasset.sellseconds=0
                  curasset.sellPrice=0
                  curasset.lastbuyprice=0
                  curasset.lastsellprice=0
                  curasset.maxstop=0
                  curasset.stopOrder=0
                  curasset.buyOrder=0
                  curasset.sellOrder=0
                  curasset.sellcount=0
                  curasset.sellamount=0
                  curasset.minsellammount=0
                  curasset.buycount=0
                  curasset.buyamount=0
                  curasset.maxbuyammount=0
                  curasset.negative=0
                  datarunned=False
                  try:
                     #print('cleaning')
                     data=[]
                     df=pd.DataFrame(data)
                     df30m=pd.DataFrame(data)
                     df1h=pd.DataFrame(data)
                     df4h=pd.DataFrame(data)
                     df1d=pd.DataFrame(data)
                     df3d=pd.DataFrame(data)
                     df1w=pd.DataFrame(data)
                     
                  except:
                      aa=1             
                  
                  
               if getConfig:
                  curasset.symbol=cfg[0]
                  curasset.decplaces=int(cfg[1])
                  curasset.decplacesqtd=int(cfg[2])
                  curasset.lossrisk=float(cfg[3])
                  curasset.lossrisk=float(cfg[3])
                  curasset.buymargin=float(cfg[4])
                  curasset.levcritical=float(cfg[5])
                  curasset.levmin=float(cfg[6])
                  curasset.levdefault = float(cfg[7])
                  curasset.levmax = float(cfg[8])
                  curasset.gain = float(cfg[9])
                  curasset.minValue = float(cfg[10])
                  curasset.pricereserve = float(cfg[11])
                  curasset.lossreserve = float(cfg[12])
                  curasset.orderinvestracio = float(cfg[13])
                  curasset.buyOrdersCancelled=False
                  curasset.autoControl=True
                  if float(cfg[14]) == 1:
                     curasset.run = True

                                 
               #print('-------------------- '+curasset.symbol+'-------------------')
  
               
               if getRealData and datarunned==False:
                     #print('REAL data')
                     millseconds_last=0
                     millseconds_next=int(time.time())
                     curasset.millseconds_next=millseconds_next
                     periodtxt="48 month ago UTC"
                     # ------------------ 15m --------------------------
                     if runmode=="REAL":
                        periodtxt="24 Hour ago UTC"

                     klines    = client.get_historical_klines(curasset.symbol, Client.KLINE_INTERVAL_15MINUTE, periodtxt)
                     if runmode=="SIMUL":
                        klinefile(klines,runmode+'klines')
                     # ------------------ 30m --------------------------
                     if runmode=="REAL":
                        periodtxt="1 week ago UTC"

                     klines30m = client.get_historical_klines(curasset.symbol, Client.KLINE_INTERVAL_30MINUTE, periodtxt)
                     if runmode=="SIMUL":
                        klinefile(klines30m,runmode+'klines30m')
                     # ------------------ 1h --------------------------        
                     if runmode=="REAL":
                        periodtxt="1 week ago UTC"           
                     klines1h  = client.get_historical_klines(curasset.symbol, Client.KLINE_INTERVAL_1HOUR, periodtxt)
                     
                     if runmode=="SIMUL":
                        klinefile(klines1h,runmode+'klines1h')
                     if runmode=="REAL":
                        periodtxt="2 week ago UTC"
                     klines4h  = client.get_historical_klines(curasset.symbol, Client.KLINE_INTERVAL_4HOUR, periodtxt)
                     if runmode=="SIMUL":
                        klinefile(klines4h,runmode+'klines4h')

                     if runmode=="REAL":
                        periodtxt="2 month ago UTC"
                     
                     klines12h  = client.get_historical_klines(curasset.symbol, Client.KLINE_INTERVAL_12HOUR, periodtxt)   
                     if runmode=="SIMUL":
                        klinefile(klines12h,runmode+'klines12h')

                     if runmode=="REAL":
                        periodtxt="12 month ago UTC"
                     klines1d  = client.get_historical_klines(curasset.symbol, Client.KLINE_INTERVAL_1DAY, periodtxt)   
                     if runmode=="SIMUL":
                        klinefile(klines1d,runmode+'klines1d')
                     if runmode=="REAL":
                        periodtxt="9 month ago UTC"
                     klines3d  = client.get_historical_klines(curasset.symbol, Client.KLINE_INTERVAL_3DAY, periodtxt)
                     if runmode=="SIMUL":
                        klinefile(klines3d,runmode+'klines3d')
                     if runmode=="REAL":
                        periodtxt="9 month ago UTC"   
                     klines1w  = client.get_historical_klines(curasset.symbol, Client.KLINE_INTERVAL_1WEEK, periodtxt)
                     if runmode=="SIMUL":
                        klinefile(klines1w,runmode+'klines1w')

                     klines1m  = client.get_historical_klines(curasset.symbol, Client.KLINE_INTERVAL_1MONTH, periodtxt)
                     if runmode=="SIMUL":
                        klinefile(klines1m,runmode+'klines1m')
                     #print( datetime.now() )
                     datarunned=True
               else:
                     if datarunned==False:

                        millseconds_next = first_millseconds_next #1677628800 # 1672577186


                        print('storing data', datetime.now() )
                        klines    = getklinefile(runmode+'klines')
                        klines30m = getklinefile(runmode+'klines30m')
                        klines1h  = getklinefile(runmode+'klines1h')
                        #print(klines1h)
                        klines4h  = getklinefile(runmode+'klines4h')
                        klines12h  = getklinefile(runmode+'klines12h')
                        klines1d  = getklinefile(runmode+'klines1d')
                        klines3d  = getklinefile(runmode+'klines3d')
                        
                        klines1w  = getklinefile(runmode+'klines1w')
                        klines1m  = getklinefile(runmode+'klines1m')
                        
                        #print( klines[-1:])

                        datarunned=True
                                    
               if getPrices: 
                     
                  
                     now = datetime.now()
                     #print('getprices  ', now)
                     #------------------------- get hist prices from klines ---------------------
                     # open time, open, high, low, close, volume
                     #---------------------------------------------------------------------------
                     for i in range(9):
                         
                         if i==0:
                            klines_aux=klines
                            #klines_aux=klines1h
                            #klines_aux=klines30m
                            #klines_pos=klines_pos
                            #print(klines)
                            if runmode=='SIMUL':
                               progress=len(klines_aux)
                         if i==1:
                            klines_aux=klines30m
                            #klines_pos=klines30m_pos
                         if i==2:
                            klines_aux=klines1h
                         if i==3:
                            klines_aux=klines4h
                         if i==4:
                            klines_aux=klines12h
                         if i==5:
                            klines_aux=klines1d
                         if i==6:
                            klines_aux=klines3d
                            #print(klines_aux)
                         if i==7:
                            klines_aux=klines1w
                         if i==8:
                            klines_aux=klines1m



                         if runmode=="REAL":
                            data=[]
                            #print (klines_aux[-1:]) 
                            for line in klines_aux:
                               if runmode=="REAL":
                                  data.append([datetime.fromtimestamp(float(line[0])/1000), line[1], line[2], line[3], line[4],line[5]]);
                         else:
                            #try:
                            data=[]
                            #   if len(data)==0:
                            #      data=[]
                            #except Exception as e:
                            #      data=[]
                            #print (klines_aux[-1:]) 


                            curasset.millseconds_next=millseconds_next
                            curasset.buyseconds=millseconds_next - curasset.lastbuy
                            curasset.sellseconds=millseconds_next - curasset.lastsell
                            
                            #print(millseconds_last, millseconds_next)
                            pos=0
                            posbefore=0
                           
                            for line in klines_aux: 
                               #if i==5:
                               #   print(i, millseconds_last, '<', round(float(line[0])/1000,0), '<', millseconds_next, datetime.fromtimestamp(float(line[0])/1000), line[1])
                               
                               posbefore = posbefore + 1
                               if runmode=="SIMUL" and round(float(line[0])/1000,0) >= millseconds_last and round(float(line[0])/1000,0) < millseconds_next:
                                  #if i==5:
                                  #   sys.stdout.flush()
                                  #   sleep(20)
                                  data.append([datetime.fromtimestamp(float(line[0])/1000), line[1], line[2], line[3], line[4],line[5]])
                                  if pos==0 and posbefore > 0:
                                     pos = posbefore
                                  else:
                                     pos = pos+1
                                    
                                  #if i==5:
                                  #   print(i, millseconds_last, millseconds_next, round(float(line[0])/1000,0), datetime.fromtimestamp(float(line[0])/1000), line[1])
                               if runmode=="SIMUL" and round(float(line[0])/1000,0) >= millseconds_next:
                                  break
                            df_aux=pd.DataFrame(data) 
                            
                            if len(data)>0:
                               df_aux.columns = ['date','open','high','low','close','volume']
                               df_aux.set_index(['date'], inplace=True)
                            #else:   
                            #   break
                            
                         try:
                            if i==0:
                               #print('pos', pos)
                               if runmode=='SIMUL':
                                  #print(klines_aux[:pos])
                                  klines = klines_aux[pos:]
                                  #print(pos, len(klines))
                               
                               try:
                                  if len(df.close)>0:    
                                     df = pd.concat([df, df_aux])
                    
                               except Exception as e:
                                  #print ('error creating df',e)
                                  #print(data)
                                  df = pd.DataFrame(data)  
                                  df.columns = ['date','open','high','low','close','volume']
                                  df.set_index(['date'], inplace=True)
                                  
                            if i==1:
                               if runmode=='SIMUL':
                                  klines30m = klines_aux[pos:]
                               try:
                                  if len(df30m.close)>0:
                                     #df30m = df30m.append(df_aux)
                                     df30m = pd.concat([df30m, df_aux])
                                  
                               except:
                                  df30m = pd.DataFrame(data)  
                                  df30m.columns = ['date','open','high','low','close','volume']
                                  df30m.set_index(['date'], inplace=True)
                               
                            if i==2:
                               if runmode=='SIMUL':
                                  klines1h = klines_aux[pos:]
                               try:
                                  
                                  if len(df1h.close)>0:
                                     
                                     #df1h = df1h.append(df_aux)
                                     df1h = pd.concat([df1h, df_aux])
                                                                    
                               except Exception as e:
                                  #print ('error creating df',e)

                                  df1h = pd.DataFrame(data)  
                                  df1h.columns = ['date','open','high','low','close','volume']
                                  df1h.set_index(['date'], inplace=True)
                               
                            if i==3:
                               #df4h = pd.DataFrame(data)  
                               if runmode=='SIMUL':
                                  klines4h = klines_aux[pos:]
                               try:
                                  if len(df4h.close)>0:
                                     #df4h = df4h.append(df_aux)
                                     df4h = pd.concat([df4h, df_aux])
                               
                               except:
                                  df4h = pd.DataFrame(data)  
                                  df4h.columns = ['date','open','high','low','close','volume']
                                  df4h.set_index(['date'], inplace=True)
                            if i==4:
                               if runmode=='SIMUL':
                                  klines12h = klines_aux[pos:]
                               try:
                                  if len(df12h.close)>0:
                                     #df1d = df1d.append(df_aux)
                                     df12h = pd.concat([df12h, df_aux])
                               except:
                                  df12h = pd.DataFrame(data)  
                                  df12h.columns = ['date','open','high','low','close','volume']
                                  df12h.set_index(['date'], inplace=True)
                            if i==5:
                               if runmode=='SIMUL':
                                  klines1d = klines_aux[pos:]
                               try:
                                  if len(df1d.close)>0:
                                     #df1d = df1d.append(df_aux)
                                     df1d = pd.concat([df1d, df_aux])
                               except:
                                  df1d = pd.DataFrame(data)  
                                  df1d.columns = ['date','open','high','low','close','volume']
                                  df1d.set_index(['date'], inplace=True)
                               
                            if i==6:
                               try:
                                  if len(df3d.close)>0:
                                     #df3d = df3d.append(df_aux)
                                     df3d = pd.concat([df3d, df_aux])
                  
                               except:
                                  df3d = pd.DataFrame(data)  
                                  df3d.columns = ['date','open','high','low','close','volume']
                                  df3d.set_index(['date'], inplace=True)
             
                            if i==7:
                               try:
                                  if len(df1w.close)>0:
                                     #df1w = df1w.append(df_aux)
                                     df1w = pd.concat([df1w, df_aux])
            
                               except:
                                  df1w = pd.DataFrame(data)  
                                  df1w.columns = ['date','open','high','low','close','volume']
                                  df1w.set_index(['date'], inplace=True)
                            
                            if i==8:
                               try:
                                  if len(df1m.close)>0:
                                     #df1w = df1w.append(df_aux)
                                     df1m = pd.concat([df1m, df_aux])
            
                               except:
                                  df1m = pd.DataFrame(data)  
                                  df1m.columns = ['date','open','high','low','close','volume']
                                  df1m.set_index(['date'], inplace=True)
                     
                         except Exception as e:
                            print ('error creating df',e)
                            break
                     # for
                     #print(i, millseconds_last, millseconds_next)

               if True:   #indicators 
                     
                     curasset.moment = df.index[len(df.close)-1]
                     #curasset.macd4hlast = -1
                     now = datetime.now()
                     #print('end', now)
                     macd1h, signal1h, hhist1h = talib.MACD(df1h.close, 12, 26, 9)
                     curasset.macd1hlast = round(hhist1h[len(hhist1h)-1], curasset.decplaces)
                                           
                     # ---------------------- indicators -----------------------------
                     macd30m, signal30m, hhist30m = talib.MACD(df30m.close, 12, 26, 9)
                     curasset.macd30mlast = round(hhist30m[len(hhist30m)-1], curasset.decplaces)
                     
                     macd4h , signal4h , hhist4h  = talib.MACD(df4h.close, 12, 26, 9)
                     curasset.macd4hlast = round(hhist4h[len(hhist4h)-1], curasset.decplaces)
                  
                     ema12h7A = talib.EMA(df12h.close, timeperiod=7)
                     curasset.ema12h7A = ema12h7A
                     curasset.ema12h7  = round(float(ema12h7A[len(ema12h7A)-1]),curasset.decplaces)

                     ema12h14A = talib.EMA(df12h.close, timeperiod=14)
                     curasset.ema12h14A = ema12h14A
                     curasset.ema12h14  = round(float(ema12h14A[len(ema12h14A)-1]),curasset.decplaces)
                     
 
                     macd12h , signal12h , hhist12h  = talib.MACD(df12h.close, 12, 26, 9)
                     curasset.macd12hlast = round(hhist12h[len(hhist12h)-1], curasset.decplaces)
                        
                     macd1d , signal1d , hhist1d  = talib.MACD(df1d.close, 12, 26, 9)
                     curasset.macd1dlast = round(hhist1d[len(hhist1d)-1], curasset.decplaces)
                     #print(df3d)
                     macd3d , signal3d , hhist3d  = talib.MACD(df3d.close, 12, 26, 9)
                     curasset.macd3dlast = round(hhist3d[len(hhist3d)-1], curasset.decplaces)
                     
                     ema3d7A = talib.EMA(df3d.close, timeperiod=7)
                     curasset.ema3d7A = ema3d7A
                     curasset.ema3d7  = round(float(ema3d7A[len(ema3d7A)-1]),curasset.decplaces)

                     ema3d14A = talib.EMA(df3d.close, timeperiod=14)
                     curasset.ema3d14A = ema3d14A
                     curasset.ema3d14  = round(float(ema3d14A[len(ema3d14A)-1]),curasset.decplaces)

                     #print(hhist3d)
                     rsi3dA = talib.RSI(df3d.close, timeperiod=14)
                     curasset.rsi3d  = round(float(rsi3dA[len(rsi3dA)-1]),2)                              
                     
                     rsi1hA = talib.RSI(df1h.close, timeperiod=14)
                     curasset.rsi1h  = round(float(rsi1hA[len(rsi1hA)-1]),2)
                     
                     smarsi1hA = talib.SMA(rsi1hA, timeperiod=7)
                     curasset.smarsi1h  = round(float(smarsi1hA[len(smarsi1hA)-1]),2)
                     
                     rsi4hA = talib.RSI(df4h.close, timeperiod=14)
                     curasset.rsi4h  = round(float(rsi4hA[len(rsi4hA)-1]),2)
                     
                     smarsi4hA = talib.SMA(rsi4hA, timeperiod=7)
                     curasset.smarsi4h  = round(float(smarsi4hA[len(smarsi4hA)-1]),2)
                     
                     rsi1dA = talib.RSI(df1d.close, timeperiod=14)
                     curasset.rsi1d  = round(float(rsi1dA[len(rsi1dA)-1]),2)
                     
                     smarsi1dA = talib.SMA(rsi1dA, timeperiod=7)
                     curasset.smarsi1d  = round(float(smarsi1dA[len(smarsi1dA)-1]),2)
                  
                     rsi14A = talib.RSI(df.close, timeperiod=14)
                     curasset.rsi14  = round(float(rsi14A[len(rsi14A)-1]),2)

                     rsi6A  = talib.RSI(df.close, timeperiod=6)    
                     curasset.rsi6  = round(float(rsi6A[len(rsi6A)-1]),2)

                     #short term
                     sma30m7A = talib.SMA(df30m.close, timeperiod=7)
                     curasset.sma30m7  = round(float(sma30m7A[len(sma30m7A)-1]),curasset.decplaces)

                     ema30m7A = talib.EMA(df30m.close, timeperiod=7)
                     curasset.ema30m7  = round(float(ema30m7A[len(ema30m7A)-1]),curasset.decplaces)

                     ema30m25A = talib.EMA(df30m.close, timeperiod=7)
                     curasset.ema30m25  = round(float(ema30m25A[len(ema30m25A)-1]),curasset.decplaces)

                     sma30m50A = talib.SMA(df30m.close, timeperiod=50)
                     curasset.sma30m50  = round(float(sma30m50A[len(sma30m50A)-1]),curasset.decplaces)
                     
                     #short term
                     sma1h50A = talib.SMA(df1h.close, timeperiod=50)
                     curasset.sma1h50  = round(float(sma1h50A[len(sma1h50A)-1]),curasset.decplaces)
                     
                     rsi7hA  = talib.RSI(df1h.close, timeperiod=6)    
                     curasset.rsi7h  = round(float(rsi7hA[len(rsi7hA)-1]),2)
               
                     rsi14hA  = talib.RSI(df1h.close, timeperiod=14)    
                     curasset.rsi14h  = round(float(rsi1hA[len(rsi14hA)-1]),2)
                     
                     ema1h7A = talib.EMA(df1h.close, timeperiod=7)
                     curasset.ema1h7A = ema1h7A
                     curasset.ema1h7  = round(float(ema1h7A[len(ema1h7A)-1]),curasset.decplaces)

                     ema1h14A = talib.EMA(df1h.close, timeperiod=14)
                     curasset.ema1h14A = ema1h14A
                     curasset.ema1h14  = round(float(ema1h14A[len(ema1h14A)-1]),curasset.decplaces)

                     #med term
                     sma4h30A = talib.SMA(df4h.close, timeperiod=30)
                     curasset.sma4h30  = round(float(sma4h30A[len(sma4h30A)-1]),curasset.decplaces)
                     
                     #short term
                     sma1d9A = talib.SMA(df1d.close, timeperiod=9)
                     curasset.sma1d9  = round(float(sma1d9A[len(sma1d9A)-1]),curasset.decplaces)

                     sma1d20A = talib.SMA(df1d.close, timeperiod=20)
                     curasset.sma1d20  = round(float(sma1d20A[len(sma1d20A)-1]),curasset.decplaces)
                     
                     sma1d100A = talib.SMA(df1d.close, timeperiod=100)
                     curasset.sma1d100  = round(float(sma1d100A[len(sma1d100A)-1]),curasset.decplaces)
                                      
                     sma1d200A = talib.SMA(df1d.close, timeperiod=200)
                     curasset.sma1d200  = round(float(sma1d200A[len(sma1d200A)-1]),curasset.decplaces)

                     ema1d100A = talib.EMA(df1d.close, timeperiod=100)
                     curasset.ema1d100  = round(float(ema1d100A[len(ema1d100A)-1]),curasset.decplaces)
                     
                     ema1d200A = talib.EMA(df1d.close, timeperiod=200)
                     curasset.ema1d200  = round(float(ema1d200A[len(ema1d200A)-1]),curasset.decplaces)
                     #print(ema1d200A)

                     ema1d14A = talib.EMA(df1d.close, timeperiod=14)  #14
                     curasset.ema1d14  = round(float(ema1d14A[len(ema1d14A)-1]),curasset.decplaces)
                     #print(ema1d14A)
                     ema1d30A = talib.EMA(df1d.close, timeperiod=30)  #30
                     curasset.ema1d30  = round(float(ema1d30A[len(ema1d30A)-1]),curasset.decplaces)
                     
                     #long term
                     sma3d14A = talib.SMA(df3d.close, timeperiod=14)
                     curasset.sma3d14  = round(float(sma3d14A[len(sma3d14A)-1]),curasset.decplaces)
                     
                     sma1w7A = talib.SMA(df1w.close, timeperiod=7)
                     curasset.sma1w7  = round(float(sma1w7A[len(sma1w7A)-1]),curasset.decplaces)
                     
                     macd1w , signal1w , hhist1w  = talib.MACD(df1w.close, 12, 26, 9)
                     curasset.macd1wlast = round(hhist1w[len(hhist1w)-1], curasset.decplaces)

                     ema1w7A = talib.EMA(df1w.close, timeperiod=7)
                     curasset.ema1w7A = ema1w7A
                     curasset.ema1w7  = round(float(ema1w7A[len(ema1w7A)-1]),curasset.decplaces)

                     ema1w14A = talib.EMA(df1w.close, timeperiod=14)
                     curasset.ema1w14A = ema1w14A
                     curasset.ema1w14  = round(float(ema1w14A[len(ema1w14A)-1]),curasset.decplaces)

                     sma14A = talib.SMA(df.close, timeperiod=14)
                     curasset.sma14  = round(float(sma14A[len(sma14A)-1]),curasset.decplaces)
            
                     sma6A  = talib.SMA(df.close, timeperiod=6)
                     curasset.sma6   = round(float(sma6A[len(sma6A)-1]),2)
                     
                     #df[["high", "low", "close","volume"]].to_numpy(),
                     upper, middle, lower = talib.BBANDS(df.close,timeperiod=14, nbdevup=2, nbdevdn=2)
                     upper4h, middle4h, lower4h = talib.BBANDS(df4h.close,timeperiod=14, nbdevup=2, nbdevdn=2)
                     upper1h, middle1h, lower1h = talib.BBANDS(df1h.close,timeperiod=14, nbdevup=2, nbdevdn=2)
                     
                     #short term
                     sma1h20A = talib.SMA(df1h.close, timeperiod=20)
                     curasset.sma1h20  = round(float(sma1h50A[len(sma1h20A)-1]),curasset.decplaces)
                     
                     #short term
                     sma1h7A = talib.SMA(df1h.close, timeperiod=7)
                     curasset.sma1h7  = round(float(sma1h7A[len(sma1h7A)-1]),curasset.decplaces)
                     
                     changeday=round((float(float(df1h.close[len(df1h)-1])) - float(df1h.close[len(df1h)-24]))/float(df1h.close[len(df1h)-24]),2)

                     sma1m7A = talib.SMA(df1m.close, timeperiod=7)
                     curasset.sma1m7A = sma1m7A
                     curasset.sma1m7  = round(float(sma1m7A[len(sma1m7A)-1]),curasset.decplaces)

                     #print('end', datetime.now() )
         
               if accountData and runmode=="REAL":
                     #print('-------------------- Account info -------------------')
                     #account_info = client.get_isolated_margin_account()
                     new_symbols = {'symbols': curasset.symbol}
                     new_symbol = {'symbol': curasset.symbol}
                     #account_info = client.get_isolated_margin_account(**new_symbols)
                     try:
                        account_info = client.get_isolated_margin_account(symbols=curasset.symbol)
                     except Exception as e:
                        print ('error getting account:',e)
                        break
                     asset=account_info['assets']

                     curasset.baseAsset  = asset[0]['baseAsset']['asset']
                     
                     curasset.netasset   = asset[0]['baseAsset']['netAsset']
                     #totalAsset = asset[0]['quoteAsset']['free']
                     curasset.freeAsset = asset[0]['quoteAsset']['free']
                     
                     curasset.freetosell = asset[0]['baseAsset']['free']
                     curasset.borrowed = round(float(asset[0]['quoteAsset']['borrowed']),2)
                     curasset.position = float(curasset.netasset) * round(float(asset[0]['indexPrice']),curasset.decplaces)
                     curasset.atualasset = curasset.position + float(asset[0]['quoteAsset']['locked']) + float(curasset.freeAsset) - curasset.borrowed
                     
                     balance = balance+round(curasset.atualasset,0)
                     curasset.maxasset = curasset.atualasset * round(float(asset[0]['marginRatio']),2)

                     curasset.freeLoan = curasset.maxasset  - curasset.borrowed - curasset.atualasset
                     
                     if "USDT" in curasset.symbol:
                        curasset.currency = 'USDT'
                 
                     else:
                        curasset.currency = 'BUSD'
                 
                     new_symbol = {'symbol': curasset.symbol}
                     #price = client.get_symbol_ticker(**new_symbol)
                     price = client.get_symbol_ticker(symbol=curasset.symbol)

                     totalInvest = float(asset[0]['baseAsset']['totalAsset']) * float(price['price'])
                     now = datetime.now()
                     #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                     margin=round(float(asset[0]['marginLevel']),4)
                     curasset.margin = margin 

                     curasset.marginLevelStatus=asset[0]['marginLevelStatus'][0:6]

                     curasset.liqprice=round(float(asset[0]['liquidatePrice']),curasset.decplaces)
                     #curasset.macd4hlast = -1
                     #------------------------- get hist prices from klines4h -------------------
                     # open time, open, high, low, close, volume

                     #---------------------------------------------------------------------------
                     
                     curasset.minposition=100
               
                     try:
                        file1 = open(curasset.symbol+'.safe', 'r')
                        Lines = file1.readlines()
                        file1.close()
                        linecfg=Lines[0].strip('\n').split(";")
                     
                        curasset.lastposition=float(linecfg[0])
              
                        if curasset.lastposition==0:
                           curasset.lastposition=round(curasset.atualasset,2)
                        curasset.safe=float(linecfg[1])
                        curasset.maxsafe=float(linecfg[2])
                        curasset.lastsafeuse=float(linecfg[3])
                        
                     except:
                         curasset.lastposition=round(curasset.atualasset,2)
                         curasset.safe=0
                         curasset.maxsafe=0              
                         curasset.lastsafeuse=0              
                     
                     
               if accountData and runmode=="SIMUL":
                     
                     #print('seconds',curasset.buyseconds)
                     new_symbols = {'symbols': curasset.symbol}
                     new_symbol = {'symbol': curasset.symbol}
                     asset="BTC"
                     curasset.baseAsset  = ""
                     #curasset.lossreserve = 0.3
                     curasset.freetosell = 0
                     #curasset.borrowed = 0
                     curasset.position = 0
                     
                     balance = balance + 0
                     curasset.maxasset = 0
                     #curasset.freeLoan = 0
                     new_symbol = {'symbol': curasset.symbol}

                     price = {'price' : round(float(df.close[len(df.close)-1]), curasset.decplaces) }
                     
                     #if millseconds_next == 1678148100:
                        #print(price)
                     #   print(df)
                     #   sleep(20)

                     totalInvest = 0
                     now = datetime.now()
                     #margin=1.10
                     #curasset.margin = margin 
                     curasset.marginLevelStatus="NORMAL"
                     curasset.liqprice=0

               if True: # get regression
                   # higher points are returned

                   #print(df1d['low'][-20:])
                   #print(np.arange(1, 21, 1, dtype=int))
                   #print(df1d['close'].tail(20))
                   #slope, intercept, r_value, p_value, std_err = linregress(x=np.arange(1, 21, 1, dtype=int), y=df1d['close'].tail(20))
                   xx=np.arange(1, 11, 1, dtype=int).reshape(-1, 1)
                   #print(xx)
                   yy=df12h['close'].tail(10)
                   #print(yy)
                   lm = LinearRegression()

                   lm.fit(xx, yy)

                   #print(lm.intercept_)
                   # print(lm.coef_)
                   curasset.regression=lm.coef_[0]
                   #sleep(0.2)
                   
                   # 3d
                   xx=np.arange(1, 11, 1, dtype=int).reshape(-1, 1)
                   yy=df3d['close'].tail(10)
                   lm = LinearRegression()
                   lm.fit(xx, yy)
                   curasset.regressionWeek=lm.coef_[0]
                   #print(curasset.regressionWeek)

                   # day
                   xx=np.arange(1, 21, 1, dtype=int).reshape(-1, 1)
                   yy=df1d['close'].tail(20)
                   lm = LinearRegression()
                   lm.fit(xx, yy)
                   curasset.regressionDay=lm.coef_[0]
                   

               if othervalues:      
                     if runmode=="REAL":
                        diff = round(float(upper1h[-1:])-float(price['price']),curasset.decplaces) * 1.25
                     else:
                        diff = round(float(upper1h[-1:])-float(price['price']),curasset.decplaces)
                     #print (upper1h)
                     
                     if (diff<0):
                        diff=float(price['price']) * 0.01
                     #print(numpy.format_float_positional(liqprice))
                     #print(curasset.sma1h7,curasset.sma1h20, changeday)
                     timeperiod = 24
                     
                     curasset.diff=diff
                     change=round((float(float(df1h.close[len(df1h)-1])) - float(df1h.close[len(df1h)-timeperiod]))/float(df1h.close[len(df1h)-timeperiod]) * 100,2)
                     #print(float(df1h.close[len(df1h)-24]),float(df1h.close[len(df1h)-1]), change)
                     aux_change=change 
                     curasset.path=''
                     trendadjust=1
                 
                     
                     #if change<-4.00:
                     #   trendadjust=trendadjust * 1.08
                     #if change<-5.00:
                     #   trendadjust=trendadjust * 1.09                      

                     #print('adjust', trendadjust) 
                     #curasset.levcritical=round(curasset.levcritical * trendadjust , 3)
                     #curasset.levmin=round(curasset.levmin * trendadjust   , 3)
                     #curasset.levdefault=round(curasset.levdefault * trendadjust , 3)
                     #curasset.levmax=round(curasset.levmax * trendadjust , 3) 
                     if True:
                        trendadjust = rules.trendadjust(curasset, change)
                        #if runmode=="SIMUL" and curasset.lastposition * 0.5 >  curasset.atualasset:
                        #   curasset.levdefault = curasset.levdefault * 1.1
                        #   curasset.levmax = curasset.levmax * 1.1
                           
                     #if runmode=='REAL' and curasset.symbol in ("BTCBUSD","ETHBUSD","BTCUSDT"):
                     #   curasset.levdefault = 1.095
                     #   curasset.levmax = 1.125
                     #else:
                     #   if runmode=='REAL':
                     #      curasset.levdefault = 1.20
                     #      curasset.levmax = 1.265
 
                     pos30=len(hhist30m)-1
                     #or (curasset.macd30mlast<0 and float(hhist30m[pos30]) < float(hhist30m[pos30-1])) or (float(hhist30m[pos30]) < float(hhist30m[pos30-1]) and float(hhist30m[pos30-1]) < float(hhist30m[pos30-2])):
                     minor=0  
                     
                     for x in range(5):
                        if float(hhist30m[pos30-x])*1000000 < Decimal(hhist30m[pos30-x-1]) * 1000000:
                           minor=minor+1
                           #print(x, pos30, minor, float(hhist30m[pos30-x])*1000000, float(hhist30m[pos30-x-1])*1000000)
                        
               if checkOrders and runmode=="REAL":
                  try:
                     orders = client.get_all_margin_orders(symbol=curasset.symbol,  isIsolated='TRUE', limit=90)
                     oldx=0
                     x=0
                     for order in orders:
                        if (order['type'] == 'LIMIT'):
                           if (order['status'] == 'FILLED'):
                              x=round(time.time(),0)
                              #print(x)
                              if float(order['time']) > oldx:
                                 #print(order['orderId'],order['side'],'price:', order['price'], x-round(float(order['time'])/1000,0), 'secs')
                                 oldx=float(order['time'])
                                 if (order['side'] == 'SELL'):
                                    curasset.sellseconds = x-round(float(order['time'])/1000,0)
                                    curasset.lastsellprice = float(order['price'])
                                    
                                 if (order['side'] == 'BUY'):
                                    curasset.buyseconds = x-round(float(order['time'])/1000,0)
                                    curasset.lastbuyprice = float(order['price'])
                     #print(asset[0]['symbol'], 'lastsell', sellseconds, 'lastbuy', buyseconds)
                     #sys.stdout.flush()
                  except:
                     print('error getting orders') 

               lastprice=round(float(price['price']),curasset.decplaces)
               curasset.lastprice=lastprice
               #sys.stdout.flush()

               if checkOrders and runmode=="SIMUL":
                  a=[]
                  
                  for o in curasset.orders:
                      x=bot4_bin_orders.execute(client, curasset, o[1], float(o[2]), float(o[3]) )
                      if x==0:
                         #print('pending order', curasset.lastprice, o)
                         a.append(o)
                      #else:
                      #   print(df.index[len(df.close)-1])
                     
                  curasset.orders=a
                  curasset.sellcount=len(a)
                  #print('count', curasset.sellcount)
                            
               # -----------------------------------------------------------------------------
               if openOrders and runmode=="REAL":
                  try:
                     orders = client.get_open_margin_orders(symbol=curasset.symbol,  isIsolated='TRUE')
                  except:
                     print('error getting orders') 
                     break
                  
                  for order in orders: # find orders <15 and with 2 nines at end of quatntity
                     if (order['type'] == 'LIMIT'):
                        if (order['side'] == 'SELL'):
                           curasset.sellcount=curasset.sellcount+1
                           curasset.sellamount=curasset.sellamount+float(order['price']) * float(order['origQty'])
                           # findind low order 
                           if (curasset.minsellammount > float(order['price']) or curasset.minsellammount==0):
                              curasset.sellOrder=order['orderId']
                              curasset.sellPrice=order['price']
                              curasset.minsellammount = float(order['price'])

                        if (order['side'] == 'BUY'):
                           if (curasset.margin < curasset.levcritical):
                              #print('!!!!! MARGIN --------------------------------', curasset.margin, curasset.levcritical)
                              try:
                                 curasset.buyOrder = order['orderId']
                                 bot4_bin_orders.cancel( client,curasset, curasset.buyOrder,'MARGIN!!!!')
                                 curasset.buyOrdersCancelled = True
                                 curasset.buyOrder = 0
                              except:
                                 print('erro cancel order')
                           else:
                              curasset.buycount=curasset.buycount+1
                              curasset.buyamount=curasset.buyamount+float(order['price']) * float(order['origQty'])
                              # findind low order 
                           
                           if (curasset.maxbuyammount < float(order['price']) or curasset.maxbuyammount==0):
                              curasset.buyOrder=order['orderId']
                              curasset.sellPrice=order['price']
                              curasset.maxbuyammount = float(order['price'])

                        if (float(order['price']) * float(order['origQty'])  <= 15) :
                           last_char = str(round(float(order['price']),0))[-2:]
                           if (last_char == '99'):
                              print('Control from BIN:',last_char)
                              curasset.autoControl=False
               if True and printdebug:   
                  if runmode=="REAL":
                     print(now.strftime("%Y-%m-%d %H:%M:%S"), curasset.currency, curasset.symbol,numpy.format_float_positional(round(float(price['price']),curasset.decplaces)).rjust(10, ' '), curasset.marginLevelStatus, numpy.format_float_positional(curasset.liqprice).rjust(10, ' '), 'margin',str(round(curasset.margin,3)).ljust(5, '0'), 'critical', str(round(curasset.levcritical,3)).ljust(5, '0'),str(round(curasset.levmin,3)).ljust(5, '0'),'def', str(round(curasset.levdefault,3)).ljust(5, '0'),'max',str(round(curasset.levmax,3)).ljust(5, '0'),'diff', numpy.format_float_positional(round(diff,curasset.decplaces)).rjust(10, ' '),'rsi', str(curasset.rsi14).ljust(5,'0'), curasset.rsi7h ,'sma', numpy.format_float_positional(curasset.sma14).rjust(10, ' '), 'Bal', str(round(float(curasset.freeAsset),2)).rjust(6, '0'),'free', round(float(curasset.netasset),curasset.decplacesqtd),'val',round(totalInvest,0),'s', curasset.sellseconds,'b',curasset.buyseconds,'1d', round(curasset.macd1dlast,2),'4h',round(curasset.macd4hlast,2),'12h',  round(curasset.macd12hlast,2), '1h', curasset.macd1hlast,'3d', curasset.macd3dlast, '1w',curasset.macd1wlast, 'SellCount', curasset.sellcount,'sellseconds',curasset.sellseconds,curasset.lastsellprice, 'BuyCount',curasset.buycount,'buyseconds',curasset.buyseconds, curasset.lastbuyprice, 'reg', round(curasset.regression,2), round(curasset.regressionDay,2), curasset.path, curasset.negative, 'd14', curasset.ema1d14, 'd30', curasset.ema1d30, 'd100', curasset.ema1d100 )
                  
               curasset.stopOrder=0
               # logic ............................. #
               
               #print('seconds',curasset.buyseconds)
               if executeRules and runmode=="REAL":
                     try:
                        for order in orders:
                           #print(order['orderId'], order['price'], order['side'], order['type'], order['status'])
                           if ( order['type'] == 'STOP_LOSS_LIMIT' and order['status'] == 'NEW'):
                              #print(order['orderId'], order['price'], order['side'], order['type'],order['stopPrice'])
                              curasset.stopOrder=order['orderId']
                              if (float(order['stopPrice']) > curasset.maxstop ):
                                 curasset.maxstop=float(order['stopPrice'])
                           else:
                              if False: 
                                 print(order['orderId'], order['price'], order['side'], order['type'])

                           if  ( order['type'] == 'LIMIT' and curasset.autoControl ):
                                 x=round(time.time(),0)
                                 if (x-round(float(order['time'])/1000,0)) > 129600 :  #cancel if > 36 hours
                                    #cancel 
                                    anyOrder=order['orderId']
                                    anyPrice=order['price']
                                    #print('cancel limit ANY order > 129600', anyOrder, curasset.symbol, anyPrice)
                                    
                                    bot4_bin_orders.cancel(client,curasset,anyOrder,'cancel limit ANY order > 129600')
                                 else:
                                    if (order['side'] == 'BUY' ):
                                       curasset.buyOrder=order['orderId']
                                       curasset.buyPrice=order['price']
                                       # ------------- cancel to recreate low order ---------------------
                                       #newPrice=round(float(lastprice) - diff * racio*0.5, curasset.decplaces)
                                       newPrice=round(float(lastprice) - diff * racio, curasset.decplaces)
                                       curasset.newPrice=newPrice
                                       #print('cancel limit BUY order', buyPrice, ' vs ', float(buyPrice) * 0.99, '>',newPrice)
                                       if (newPrice < float(curasset.buyPrice) * 0.99 and float(curasset.buyOrder)>0 and False and curasset.buyPrice != curasset.priceresere ):
                                          bot4_bin_orders.cancel(client,curasset,curasset.buyOrder, 'cancel limit BUY order');
                                          curasset.buyOrder=0
                     except Exception as e:
                           print ('ERRO GRAVE orders',e)
               #print('logic', datetime.now() )

               if curasset.runmode=='SIMUL':
                  totalbal=round(curasset.netasset,5)*lastprice + round(curasset.freeAsset,0)
                  if curasset.borrowed == 0:
                     mrg=2
                  else:   
                     mrg=(totalbal-round(curasset.borrowed,2))/curasset.borrowed+1
                  curasset.margin=mrg
                  curasset.atualasset=totalbal-curasset.borrowed
                  valtoloan = curasset.atualasset / (curasset.levdefault-1)
                  if valtoloan - curasset.borrowed >0:
                     curasset.freeLoan = valtoloan - curasset.borrowed
                  #print('BALANCE',totalbal,mrg, curasset.netasset, curasset.freeAsset, curasset.freeLoan,'#####',curasset.atualasset,'#####')
                  #sleep(2)
               
               if useSafe:
                     rules.safe1(client, df, curasset, change, millseconds_next)
                    
                     
               if True: 
                     #print(curasset.symbol, curasset.run)
                     if curasset.run:
                        try:
                           #print('pay', curasset.margin, curasset.sellseconds)
                           rules.pay(client,df, curasset, change, millseconds_next)    
                           curasset.getbuy = False
                           rules.get(client, df, curasset)      
                        except Exception as e:
                           print ('ERRO GRAVE loan',e)
                  
                     #if True:
                     try:
                        if runmode == "REAL":
                           bot2_stop.cancel(client, df, curasset)
                           bot2_stop.create(client, df, curasset)
                     except Exception as e:
                           print ('ERRO GRAVE stop',e)

                     if runmode=='REAL' and curasset.run:
                        try:
                           #bot4_rsi.cancel(client,df,curasset)
                           #bot4_rsi.sell(client,df, curasset)
                           #bot4_rsi.buy(client,df,curasset)
                           #bot4_dips.auto(client, df, curasset, hhist30m, hhist3d)
                           #bot4_dips.dips(client, df, curasset, hhist30m, hhist3d)
                           #print('> st:',curasset.path)
                           
                           rules.st1(client, df, curasset, hhist1h, hhist12h,change)
                              
                        except Exception as e:
                           print ('ERRO GRAVE ',e)
                     if runmode=='SIMUL':
                           #print('p position', curasset.lastposition)
                           #bot6_newway.st1(client, df, curasset, hhist30m, hhist3d)
                           #bot6_newway.st2(client, df, curasset, hhist30m, hhist3d,sma1d9A, sma1d20A)
                           rules.st1(client, df, curasset, hhist1h, hhist12h,change)

               
               if runReport and runmode == "REAL":
                  #report=report+ "<table border=\"1\">
                  report=report + "<tr><td>" + curasset.symbol  + "<br><p>" + str(lastprice) + "</p>"
                  if change>0:
                     report=report +curasset.path+ "<p style=\"color:green;\">"+str(timeperiod) + 'h:' + str(change) + "%</p></td>"
                  else:
                        report=report +curasset.path+"<p style=\"color:orange;\">" +str(timeperiod) + 'h:' + str(change) + "%</p></td>"

                  if asset[0]['marginLevelStatus'][0:6] ==  'EXCESS':
                     report=report+"<td><p style=\"color:green;\">"+str(margin)+"<br>" + str(curasset.levcritical) +"<br>" + str(curasset.levmin)+"<br>" + str(curasset.levdefault)+"<br>" + str(curasset.levmax)+ "</p></td>"

                  else:
                     if asset[0]['marginLevelStatus'][0:6] ==  'NORMAL':
                        report=report+"<td><p style=\"color:orange;\">"+str(margin)+"<br>" + str(curasset.levcritical)+"<br>" + str(curasset.levmin)+"<br>" + str(curasset.levdefault)+"<br>" + str(curasset.levmax) + "</p></td>"
                     else:
                        report=report+"<td><p style=\"color:red;\">"+str(margin)+"<br>" + str(curasset.levcritical)+"<br>" + str(curasset.levmin)+"<br>" + str(curasset.levdefault)+"<br>" + str(curasset.levmax)+ "</p></td>"
                     
                  report=report+"<td><p style=\"color:red;\">"+str(round(float(curasset.netasset),curasset.decplacesqtd))+ '<br><br>' + str(round(float(curasset.atualasset),0))+"</p></td>"
                  report=report+"<td><p style=\"color:red;\">"+str(round(float(curasset.freeAsset),2))+"</p></td>"
                  if (float(curasset.sma30m7) < float(curasset.sma30m50)):  # give more importance to average price 
                        report=report+"<td><span style=\"color:#FF0000\">" + str(curasset.sma30m50) + "</span><br>"
                  else:
                        report=report+"<td><span style=\"color:#66CC66\">" + str(curasset.sma30m50) + "</span><br>"

                  if (lastprice < float(curasset.sma1h50)):
                        #report=report+"<span style=\"color:#FF0000\">"+str(curasset.sma1h50) + "<br>1h:" + str(rsi1h) + "</span><span style=\"color:black\"> M:" + str(curasset.smarsi1h) + "</span></td>"
                        report=report+"<span style=\"color:#FF0000\">"+str(curasset.sma1h50) + "<br></span><span style=\"color:black\">1h:" + str(curasset.rsi1h) + " M:" + str(curasset.smarsi1h) + "</span></td>"
                  else:
                        report=report+"<span style=\"color:#66CC66\">"+str(curasset.sma1h50) + "<br></span><span style=\"color:black\">1h:" + str(curasset.rsi1h) + " M:" + str(curasset.smarsi1h) + "</span></td>"

                  if (lastprice < float(curasset.sma4h30)):
                        #report=report+"<td><span style=\"color:#FF0000\">"+str(curasset.sma4h30)+"<br>4h:" + str(curasset.rsi4h) + " M:" + str(curasset.smarsi4h) + "</span><br>"
                        report=report+"<td><span style=\"color:#FF0000\">"+str(curasset.sma4h30) + "<br></span><span style=\"color:black\">4h:" + str(curasset.rsi4h)  + " M:" + str(curasset.smarsi4h) + "</span><br>"   
                  else:
                        report=report+"<td><span style=\"color:#66CC66\">"+str(curasset.sma4h30) + "<br></span><span style=\"color:black\">4h:" + str(curasset.rsi4h)  + " M:" + str(curasset.smarsi4h) + "</span><br>"   
                  
                  if (lastprice < float(curasset.sma1d20)):
                        report=report+"<span style=\"color:#FF0000\">"+str(curasset.sma1d20)+"<br></span><span style=\"color:black\">1d:" + str(curasset.rsi1d)  + " M:" + str(curasset.smarsi1d) +"</span></td>"
                  else:
                        report=report+"<span style=\"color:#66CC66\">"+str(curasset.sma1d20)+"<br></span><span style=\"color:black\">1d:" + str(curasset.rsi1d)  + " M:" + str(curasset.smarsi1d) +"</span></td>"

                  if (lastprice < float(curasset.sma3d14)):
                        report=report+"<td><span style=\"color:#FF0000\">"+str(curasset.sma3d14)+"</span><br>"
                  else:
                        report=report+"<td><span style=\"color:#66CC66\">"+str(curasset.sma3d14)+"</span><br>"

                  if (lastprice < float(curasset.sma1w7)):
                        report=report+"<span style=\"color:#FF0000\">"+str(curasset.sma1w7)+"</span></td></tr>"
                  else:
                        report=report+"<span style=\"color:#66CC66\">"+str(curasset.sma1w7)+"</span></td></tr>"
                              
                  #print(now.strftime("%Y-%m-%d %H:%M:%S"),'End symbol', curasset.symbol)
               millseconds_last = millseconds_next
               millseconds_next=millseconds_next + 900
               
               #print(df[-1:])
               if runmode=="REAL":
                  with open(curasset.symbol+'.safe', 'w') as z:
                        print(str(round(float(curasset.lastposition),2)).strip(' '), ";", str(round(float(curasset.safe),2)).strip(' '), ";", str(round(float(curasset.maxsafe),2)).strip(' '), ";", str(round(float(curasset.lastsafeuse),2)).strip(' '), file=z)
                  z.close()

                  sleep(5)
               sys.stdout.flush()
               
               #else:
                  #print(millseconds_last, millseconds_next)
                  #sleep(5)
                  #if (curasset.sellseconds < 3000 or curasset.buyseconds < 3000):
                  #   print(df.index[len(df.close)-1], curasset.symbol,numpy.format_float_positional(round(float(price['price']),curasset.decplaces)).rjust(10, ' '), curasset.sellcount, curasset.rsi1h , curasset.millseconds_next, 'B:',curasset.buyseconds , 'S:',curasset.sellseconds,curasset.borrowed, round(curasset.margin,3), round(curasset.netasset,5), round(curasset.freeAsset,0), totalbal, '### ',curasset.atualasset,' ####')
                  
                  #if totalrec==len(df.close):
                  #    print('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
                  #    print(df.index[len(df.close)-1], curasset.symbol,numpy.format_float_positional(round(float(price['price']),curasset.decplaces)).#rjust(10, ' '), curasset.sellcount, curasset.rsi1h , curasset.millseconds_next, 'B:',curasset.buyseconds , 'S:',curasset.sellseconds,curasset.borrowed, round(curasset.margin,3), round(curasset.netasset,5), round(curasset.freeAsset,0), totalbal)
                  #    quit() 

                  #progress=len(df)
                  #if curasset.margin > curasset.levmax:
                  #   curasset.freeAsset = curasset.freeAsset+curasset.borrowed*0.05
                  #   curasset.borrowed= curasset.borrowed + curasset.borrowed*0.05
                  #   print(df.index[len(df.close)-1], curasset.symbol,numpy.format_float_positional(round(float(price['price']),curasset.decplaces)).rjust(10, ' '), curasset.sellcount, curasset.rsi1h , curasset.millseconds_next, 'B:',curasset.buyseconds , 'S:',curasset.sellseconds,curasset.borrowed, round(curasset.margin,3), round(curasset.netasset,5), round(curasset.freeAsset,0), totalbal)
                 
               #print('END LOOP', datetime.now() )
               
               #print(round(curasset.atualasset,2))
               
         if runReport and runmode == "REAL":   
            report=report+ "</tr></table>"     
      if printdebug:
         if runmode=="REAL":
            print(now.strftime("%Y-%m-%d %H:%M:%S"),'Balance','----------- ',balance,' ------------')
            
      if True and runmode=="SIMUL":
         #   print('----------- ',balance,' ------------')
             #print(df.index[len(df.close)-1], curasset.symbol,numpy.format_float_positional(round(float(price['price']),curasset.decplaces)).rjust(10, ' '), curasset.sellcount, curasset.rsi1h , curasset.millseconds_next, 'B:',curasset.buyseconds , 'S:',curasset.sellseconds,'BB', round(curasset.borrowed,2), 'C',change,'Margin', round(curasset.margin,3), curasset.levcritical, curasset.levmin, curasset.levdefault, curasset.levmax, round(curasset.netasset,5), round(curasset.freeAsset,0),round(trendadjust,2),  round(totalbal,2), '### ',round(curasset.atualasset,2),' ####')
             #print(df.index[len(df.close)-1],round(float(curasset.netasset),5), round(float(curasset.atualass),0), curasset.symbol,numpy.format_float_positional(round(float(price['price']),curasset.decplaces)).rjust(10, ' '), 'RSI',curasset.rsi7h,curasset.rsi1h, 'MACD', curasset.macd30mlast, curasset.macd1hlast, curasset.macd4hlast, curasset.macd4hlast,curasset.macd3dlast, round(curasset.margin,2), curasset.levdefault )
             
             # , round(millseconds_last,0), ';'
             print(df.index[len(df.close)-1], ';',numpy.format_float_positional(round(float(price['price']), curasset.decplaces)).rjust(10,' '), ';',curasset.rsi7h, ';',curasset.rsi1h, ';', curasset.macd1hlast, ';', curasset.macd4hlast, ';', curasset.macd12hlast, ';', curasset.macd1dlast, ';',curasset.macd3dlast, ';',curasset.macd1wlast, ';', change, '% ;', round(curasset.margin,2), ';',round(curasset.levdefault,2), ';',  round(float(curasset.netasset),5) , ';P;',round(float(curasset.atualasset),0), ';', round(float(curasset.safe) , 0),  ';', round(curasset.regression,0), ';', round(curasset.regressionDay,0), ';', curasset.ema1w7, ';',curasset.ema1w14, ';',  curasset.ema1d100,';', curasset.ema1d200,';', curasset.ema1d14, ';', curasset.path) 
             #, curasset.path )  
             
             #,'p', curasset.path 
             #* curasset.lastprice       -  , round(curasset.safe,4), round(curasset.maxsafe,4),
             #  'p', curasset.path,'sec', curasset.buyseconds,
             
             #';B;',round(float(curasset.borrowed),2), 
                      
      if runReport and runmode == "REAL":
         with open('static/index.html', 'w') as f:
               #print("<p>------------------------------------------------</p>", file=f)
               print(report, file=f)    
               print("<p>" + now.strftime("%Y-%m-%d %H:%M:%S") + ' ' + str(balance) + "</p>", file=f)
               #print("<p>------------------------------------------------</p>", file=f)
         f.close()
      sys.stdout.flush()
      if runmode=="REAL":
         sleep(20)      
      if False and runmode == 'SIMUL' and totalrec!=0:   
      #   print('Progress', round(progress/totalrec*100,2) )
         print('Progress', round(progress/totalrec*100,0), round(curasset.atualasset,2), df.index[len(df.close)-1], curasset.margin, curasset.levcritical, curasset.levmin, curasset.levdefault, curasset.levmax, end='\r')
      if runmode == 'SIMUL' and progress==0:
         #print(round(curasset.atualasset,2))
         with open('do.log', 'a') as z:
            #print('B1',B1,'B2', B2, 'B3', B3,'C1',C1,'C2',C2, 'C3',C3,'D1',D1,'D2', D2, file=z)
            print('Progress', round(progress/totalrec*100,0), round(curasset.atualasset,2), df.index[len(df.close)-1], curasset.margin, curasset.levcritical, curasset.levmin, curasset.levdefault, curasset.levmax, file=z)
         z.close()
         
         quit()
      #else:
      #   sleep(0.1)
