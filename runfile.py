import os
import talib
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np

import json
import sys


from datetime import datetime
from time import sleep
import time
import numpy


#import dic
from decimal import Decimal, getcontext
import math

import mpmath

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

runmode='SIMUL'
print('storing data', datetime.now() )
klines    = getklinefile(runmode+'klines')
i=0

                         


millseconds_last=0
millseconds_next=1677628800


while True:
                         if i==0:
                            klines_aux=klines
                            print(len(klines) )
                            #klines_pos=klines_pos
                            #print(klines)
                            
                         data=[]
                            #print(millseconds_last, millseconds_next)
                         pos=0
                         for line in klines_aux:
                               #if i==5:
                               #   print(i, millseconds_last, '>', round(float(line[0])/1000,0), '<', millseconds_next, datetime.fromtimestamp(float(line[0])/1000), line[1])
                                 
                               if runmode=="SIMUL" and round(float(line[0])/1000,0) >= millseconds_last and round(float(line[0])/1000,0) < millseconds_next:
                                  data.append([datetime.fromtimestamp(float(line[0])/1000), line[1], line[2], line[3], line[4],line[5]])
                                  pos=pos+1 
                                  #if i==5:
                                  #   print(i, millseconds_last, millseconds_next, round(float(line[0])/1000,0), datetime.fromtimestamp(float(line[0])/1000), line[1])
                         print(pos)
                         df_aux=pd.DataFrame(data) 
                 
                         print(df_aux)
                         if len(data)>0:
                               df_aux.columns = ['date','open','high','low','close','volume']
                               df_aux.set_index(['date'], inplace=True)
                            #else:   
                            #   break
                            
                         try:
                            if i==0:
                               klines = klines_aux[pos:]
                               try:
                                  if len(df.close)>0:    
                                     df = pd.concat([df, df_aux])
                                     totalrec=len(klines_aux)
                                    
                               except Exception as e:
                                  print ('error creating df',e)
                                  df = pd.DataFrame(data)  
                                  df.columns = ['date','open','high','low','close','volume']
                                  df.set_index(['date'], inplace=True)
                         except:
                            print('erro')  
                         millseconds_last = millseconds_next
                         millseconds_next=millseconds_next + 900
                         #sleep(5)