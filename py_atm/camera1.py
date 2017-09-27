from __future__ import absolute_import, print_function, division
from pymba import *
import numpy as np
import cv2
import time
import signal
import sys
import datetime as dt
from nep import*

sub = subscriber("/trigger", True)
pub = publisher("/camera1", False)

def signal_handler(signal, frame):
    """Signal handler used to close the app"""
    print('Signal Handler, you pressed Ctrl+C!')
    # clean up after capture
    camera0.revokeAllFrames()
    # close camera
    camera0.closeCamera()
    print ('Saving images ....')
    for img in images:
        count  =  img['image_number']
        img_ = img['img']
        #rgb = cv2.cvtColor(img['img'], cv2.COLOR_BAYER_RG2RGB)  # La imagen que adquires esta
        print ("count = " + str(count))
        #cv2.imshow('frame',img_)
        #cv2.waitKey(10)
        cv2.imwrite("images/camera_1_" + str(count) + ".jpg", img_)
        
    print('Exit in 2 seconds...')
    time.sleep(2)
    sys.exit()

def get_image_mako():                
    camera0.startCapture()
    frame0.queueFrameCapture()
    camera0.runFeatureCommand('AcquisitionStart')
    camera0.runFeatureCommand('AcquisitionStop')
    frame0.waitFrameCapture() # Aqui terminas de obtener una imagen desde la camara

    # Cambiar el formato de la imagen de Vimba a OpenCV
    moreUsefulImgData = np.ndarray(buffer = frame0.getBufferByteData(),dtype = np.uint8,shape = (frame0.height,frame0.width,1))

    # get image data...
    rgb = cv2.cvtColor(moreUsefulImgData, cv2.COLOR_BAYER_RG2RGB)  # La imagen que adquires esta en escala de grises, aqui la conviertes a RGB  para visualizarla
    return rgb
    
    
# New signal handler    
signal.signal(signal.SIGINT, signal_handler)


# start Vimba
with Vimba() as vimba:
    # get system object
    system = vimba.getSystem()

    # list available cameras (after enabling discovery for GigE cameras)
    if system.GeVTLIsPresent:
        system.runFeatureCommand("GeVDiscoveryAllOnce")
        time.sleep(0.2)
    cameraIds = vimba.getCameraIds()
    for cameraId in cameraIds:
        print('Camera ID:', cameraId)

    # get and open a camera
    camera0 = vimba.getCamera(cameraIds[0]) #-------------------- ID de la camara
    camera0.openCamera()

    # list camera features
    cameraFeatureNames = camera0.getFeatureNames()
    for name in cameraFeatureNames:
        print('Camera feature:', name)

    # read info of a camera feature
    #featureInfo = camera0.getFeatureInfo('AcquisitionMode')
    #for field in featInfo.getFieldNames():
    #    print field, '--', getattr(featInfo, field)

    # get the value of a feature
    print(camera0.AcquisitionMode)

    # set the value of a feature
    camera0.AcquisitionMode = 'SingleFrame'

    # create new frames for the camera
    frame0 = camera0.getFrame()    # creates a frame
    frame1 = camera0.getFrame()    # creates a second frame

    # announce frame
    frame0.announceFrame()

    # capture a camera image
    count = 0
    start = time.time()
    success = True
    images = []

    getImages =  True
    while getImages:
        
        success, info = sub.listen_info(False) # Trigger
        if success:
            # If trigger == 0, adquire datos para experimentos
            option = str(info['trigger'])
            if option == "0":
                end = time.time()
                print(end - start)
                start = time.time()
                rgb = get_image_mako() 
                count += 1
                img_info = {'image_number':count, 'img':rgb}
                images.append(img_info)

                
                #cv2.imshow('frame',rgb) # Visualizas la imagen
                camera0.endCapture()
                #cv2.waitKey(10) # Aqui es un sleep para mostrar la imagen
                # Send acquisition time
                n1= dt.datetime.now() # Tiempo en el que termina la adquisicion y conversion a opencv
                print (n1)
                msg = {'time':str(n1)}
                pub.send_info(msg)

            if option == "1":
                # Else adquire y guarda imagenes para calibracion
                rgb = get_image_mako() 
                count += 1

                cv2.imshow('frame',rgb) # Visualizas la imagen
                camera0.endCapture()
                cv2.waitKey(10) # Aqui es un sleep para mostrar la imagen

                print ("Image saved = " + str(count))
                cv2.imwrite("images/calib_cam1_" + str(count) + ".jpg", rgb)

            if option == "2":
                getImages =  False

                
    # clean up after capture
    camera0.revokeAllFrames()
    # close camera
    camera0.closeCamera()
    print ('Saving images ....')
    for img in images:
        count  =  img['image_number']
        img_ = img['img']
        #rgb = cv2.cvtColor(img['img'], cv2.COLOR_BAYER_RG2RGB)  # La imagen que adquires esta
        print ("count = " + str(count))
        #cv2.imshow('frame',img_)
        #cv2.waitKey(10)
        cv2.imwrite("images/camera_1_" + str(count) + ".jpg", img_)
        
    print('Exit in 5 seconds...')
    time.sleep(5)

