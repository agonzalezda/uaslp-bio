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
    msg = {'trigger':2}
    pub.send_info(msg)
    print('Signal Handler, you pressed Ctrl+C!')
    print('Exit in 2 seconds...')
    time.sleep(2)
    sys.exit()
    
# New signal handler    
signal.signal(signal.SIGINT, signal_handler)

lan = launcher()
lan.launch("camera1.py")
lan.launch("camera2.py")
lan.launch("ATM_node.py")

time.sleep(5)
y = raw_input("Press ENTER to start comunication")
print ("....")

pub = publisher("/trigger", True)
##sub1 = subscriber("/force_plate", False)
sub1 = subscriber("/camera1", False)
sub2 = subscriber("/camera2", False)
sub3 = subscriber("/force_plate", False)

# Test comunication, not change ----
msg = {'trigger':3}
pub.send_info(msg)
time.sleep(.2)
pub.send_info(msg)
time.sleep(.2)
pub.send_info(msg)
# ----------------------------------

y = raw_input("Press ENTER to start acquisition")


msg = {'trigger':0}
pub.send_info(msg)
start = time.time()


while True:

    success1, info1 = sub1.listen_info(True)
    if success1:
        end = time.time()
        #print(end - start)
        start = time.time()
        time.sleep(.01)
        camera1_time = str(info1['time'])
        pub.send_info(msg)


    success2, info2 = sub2.listen_info(False)
    if success2:
        start = time.time()
        camera2_time = str(info2['time'])

    success3, info3 = sub3.listen_info(False)
    if success3:
        force_time = str(info3['time'])


    if(success1 and success2):
        print "cameras:"
        time_diference(camera1_time,camera2_time)

    if(success1 and success3):
        print "force:"
        time_diference(camera1_time,force_time)




        
        

    
    
