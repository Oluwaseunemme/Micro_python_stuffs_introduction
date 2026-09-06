import time

time_tupple=(2025, 7, 22, 4, 20, 0, 3, 203, 0)
time.mktime(time_tupple)# note this is only required if the device isn't connected to PC else it will automatically get localtime
def current_time():
    ct=time.localtime()
    formatted_time=f"{ct[0]}Y:{ct[1]}M:{ct[2]}d:{ct[3]}h:{ct[4]}m:{ct[5]}s"
    print(formatted_time)
while 1:
    current_time()
    

