import os
import subprocess
import sys
from time import sleep
import psutil
# Iterate over all running process


print('python bot4.py SIMUL FILE 1.5 1.2 1.03 C1 C2 C3 D1 D2 Timer')
for c1 in range(100, 130):
  print('1 . c1',str(c1/100))
  for c2 in range(100, 130):
    print('2 . c2',str(c2/100))
    for c3 in range(100, 130):
        print('c3',str(c3/100))
        for D1 in range(0, 5):
          for D2 in range(7, 9):
        # os.system('python3 bot4.py SIMUL FILE 1.5 1.1 1.03 ' + str(c2/100)+' '+str(c3/100) )
        #                       0       1     2    3  4          5                   6                7
                  argum = 'start /min python bot5.py SIMUL FILE 1.5 1.2 1.03 ' + str(c1/100) + ' ' + str(c2/100) + ' ' + str(c3/100) + ' ' + str(float(D1)*50) + ' ' + str(float(D2)*50) 
                  #result = subprocess.getoutput(argum)
                  
                  
                
                  #with open('do.log', 'a') as f:
                  #       print(result, file=f)    
                  #f.close()
                  tot=10

                  while (tot > 4) : 
                    
                    tot1=0
                    for proc in psutil.process_iter():
                      try:
                        
                        processName = proc.name()
                        #print(processName)
                        if "pyth" in processName:
                            #print(processName)
                            tot1=tot1+1
                      except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        print('erro')
                        #pass
                      print('tot' , tot)
                    tot=tot1
                    if tot>4:
                        print('Wait a litle')
                        sleep(5)
                    #else:
                    #     tot=10
                      
                  print(argum)
                  #
                  subprocess.call(argum , shell=True)
                  #sleep(tot * 20)
    