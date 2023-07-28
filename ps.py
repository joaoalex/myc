import psutil
# Iterate over all running process
tot=0
for proc in psutil.process_iter():
    try:
        # Get process name & pid from process object.
        processName = proc.name()
        #processID = proc.pid
        if "pyth" in processName:
           tot=tot+1
           #print(processName , ' ::: ', processID)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass