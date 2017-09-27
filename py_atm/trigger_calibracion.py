import time
from nep import*
import signal
import sys
import datetime as dt


def time_diference(str_t1,str_t2):

    try:
        y = dt.datetime.strptime(str_t1, "%Y-%m-%d %H:%M:%S.%f")
    except:
        y = dt.datetime.strptime(str_t1, "%Y-%m-%d %H:%M:%S")
        
    try:
        x = dt.datetime.strptime(str_t2, "%Y-%m-%d %H:%M:%S.%f")
    except:
        x = dt.datetime.strptime(str_t2, "%Y-%m-%d %H:%M:%S")

    diff_h = abs(x.hour - y.hour)
    diff_min = abs(x.minute - y.minute)
    diff_sec = abs(x.second - y.second)
    diff_micro = abs(x.microsecond - y.microsecond)
    
    print str(diff_h) + ":" +  str(diff_min) + ":" + str(diff_sec) + "." + str(diff_micro)
    
    

def signal_handler(signal, frame):
    """Signal handler used to close the app"""
    print('Signal Handler, you pressed Ctrl+C!')
    print('Exit in 2 seconds...')
    time.sleep(2)
    sys.exit()
    
# New signal handler    
signal.signal(signal.SIGINT, signal_handler)


lan = launcher()
lan.launch("camera1.py")
lan.launch("camera2.py")


time.sleep(5)
y = raw_input("Press ENTER to start comunication")
print ("....")

pub = publisher("/trigger", True)
##sub1 = subscriber("/force_plate", False)
sub1 = subscriber("/camera1", False)
sub2 = subscriber("/camera2", False)


# Test comunication, not change ----
msg = {'trigger':3}
pub.send_info(msg)
time.sleep(.2)
pub.send_info(msg)
time.sleep(.2)
pub.send_info(msg)
# ----------------------------------

print 
y = raw_input("Press ENTER to get a new image || Press c + enter to finish")
msg = {'trigger':1}
pub.send_info(msg)

new = True
while new:

    y =  raw_input("Waiting new enter ....")
    if(y == "c"):
        msg = {'trigger':2}
        pub.send_info(msg)
        new =  False
    else:
        pub.send_info(msg)


print('Exit in 2 seconds...')
time.sleep(2)
sys.exit()
        

    
    
