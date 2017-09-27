#!/usr/bin/env python

# ------------------------ Force plate ATM node  ---------------------------
# Description: Get and publish the sensory data from a AMT force plate
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of ay kind.
# Autor: Luis Enrique Coronado Zuniga


from ctypes import*     # Para rpgramar en C
import time             # Libreria de tiempos
import signal           # Excepciones del teclado
import sys
import ATM as atm       # Libreria de la plataforma de fuerza
from nep import*        # Libreria para comunicacion entre procesos
import datetime as dt   # Obtener el tiempo actual
import thread           # Libreria de hilos de ejecucion

# Ejecutar una funcion al presionar Ctrl+C (Excepcion)
def signal_handler(signal, frame):
    """Signal handler used to close the app"""
    print('Signal Handler, you pressed Ctrl+C!')
    print('Exit in 2 seconds...')
    time.sleep(2)
    s_file.close()
    atm.fmBroadcastStop()
    atm.fmBroadcastZero()
    sys.exit()
    
# New signal handler (Definiendo la expcion)    
signal.signal(signal.SIGINT, signal_handler) # signal_handler es el nombre de la funcion que se ejecuta cuando se lance la expecion


s_file = open("datos_plataforma.txt","w") 

# New publisher instance
sub = subscriber("/trigger", True)
pub = publisher("/force_plate", False)

# Init comunication with force plate
value = atm.fmDLLInit()
time.sleep(1)
countdown = 20

# Esperar la inicializacion de la plataforma, si no cerrar
while atm.DeviceInitComplete() == 0:
    time.sleep(.25)
    countdown =  countdown - 1
    if (countdown <= 0):
        print  "The initialization process took longer than normal, please try again"
        time.sleep(5)
        print "closing application"
        exit()

## CONFIG
acqRate = 1000;
atm.fmBroadcastAcquisitionRate(acqRate)
atm.fmBroadcastZero()               # Initialize value of the sensors in cero
atm.fmDLLPostDataReadyMessages(0)   # Do not post data ready messages
##fmDLLSetUSBPacketSize(512);       # Set the packet size to 512
##fmBroadcastGenlock(0);            # Make sure Genlock is off
atm.fmBroadcastRunMode(1)           # Set collection mode to metric
atm.fmDLLSetDataFormat(0)           # 0-Six channel format, 1 eight channel format
atm.fmBroadcastResetSoftware()      # put the configuration parameters on the force platform

##PLATAFORM ERRORS CHECK
ptr =  POINTER(c_float)()

print "Start acquisition test"
atm.fmBroadcastStart(); #start acquisition
time.sleep(.250); # Tiempo en segundos
ret = 0 # Checar si la adquiscion se realizo de manera correcta, si es 0 no se realizo correctamente
while (ret == 0): 
    ret = atm.fmDLLTransferFloatData(byref(ptr)) # En la funcion fmDLLTransferFloatData uno adquier la informacion, se guarda en el apuntado ptr
    print "Fx= ", ptr[0]
    print "Fy= ", ptr[1]
    print "Fz= ", ptr[2]
    print "Mx= ", ptr[3]
    print "My= ", ptr[4]
    print "Mz= ", ptr[5]
    print "No errors in the acquisition"
    
time.sleep(1)
print ("Sensing force plate data...")
print ("Press Ctrl+C to exit")

# Funcion que se ejecuta en otro hilo
def onSendSignal(count):
    start = time.time()
    getInfo = True
    while getInfo:
        # success te indica si recibio datos o no, info es el valor que recibe
        success, info = sub.listen_info(False) # Recibes el trigger
        n1= dt.datetime.now() # Medir dia, hora con microsegundos de la adquicion
        if success:
            option = str(info['trigger'])
            if option == "0":
                end = time.time()
                print(end - start) # Imprimir datos entre cada adquicicion
                start = time.time()
                #print n1          # Imprimir el tiempo actual
                count = count + 1
                msg = {'Fx': ptr[0], 'Fy': ptr[1], 'Fz': ptr[2], 'Mx': ptr[3], 'My': ptr[4], 'Mz': ptr[5], 'time':str(n1)}
                s_file.write(str(count)+","+str(ptr[0])+","+str(ptr[1])+","+str(ptr[2])+","+str(ptr[3])+","+str(ptr[4])+","+str(ptr[5])+","+ str(n1)+"\n") 
                pub.send_info(msg)
            if option == "2":
                getInfo =  False

    print ("Exit... waiting Ctrl + C... ")
      
count = 0 
thread.start_new_thread ( onSendSignal, (count,))

#PUBLISH DATA
while True:
    ret = atm.fmDLLTransferFloatData(byref(ptr));
    if (ret != 0):
        pass # pass indica que no haga nada
        #print Fz


       




