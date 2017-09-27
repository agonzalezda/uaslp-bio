
from pylab import *
from numpy import *
from numpy import linalg as LA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2

def preLUT(img,a,b):
    lut = np.arange(256)
    lut = lut.astype(np.uint8)
    lut = 255-lut
    for x in range(256):
        if x < a:
            lut[x] = 255
        elif x > b:
            lut[x] = 0
        if (x >= a) and (x <= b):
            valor = (float(x-b)/float(a-b))
            lut[x] = int(255*valor)
    img2 = cv2.LUT(img,lut)

    return img2

def preProccesing(img,view=False, bilateral=True, algorithm = 'canny', vlut = 150 ):
    #img2 = preLUT(img,0,vlut)
    #img2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img2 = img
    if bilateral:
        img2 = cv2.bilateralFilter(img2,9,75,75)
    if algorithm == 'canny':
        img_seg = cv2.Canny(img2,50,150)
    if algorithm == 'th':
        ret,img_seg = cv2.threshold(img2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    if view:
        cv2.namedWindow('segmentation',0)
        cv2.imshow('segmentation', img_seg)
        cv2.waitKey(0)
    
    return img,img_seg
    
def massCenter(cnt):
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return cx, cy

def findVisualCue(img, area_min, area_max, r):
    contours, jr = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    bool, cx, cy, nc = findCircle(contours,area_min,area_max,r)
    return cx,cy,nc #nc = numero de circulos

def circle(roundness, roundness_desired, area_actual, area_min, area_max):
    # If the roundness is greater than .85 and have the correct relation
    if(roundness > roundness_desired and area_actual > area_min  and area_actual < area_max):
        return True
    else:
        return False

def findCircle(contours, a_min, a_max, roundness_desired):
    i = 0
    nc = 0
    cx = np.arange(50)
    cy = np.arange(50)
    while i < len(contours):
        cnt = contours[i]
        
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt,True)
        
        if(perimeter > 80):
            roundness = 4.0*3.1416*area/(perimeter**2)
            if(circle(roundness, roundness_desired , area, a_min, a_max)):
                cx[nc], cy[nc] = massCenter(cnt)
                nc = nc +1
        i = i + 1

    if nc > 0:
        return True, cx[:nc], cy[:nc], nc
    return False, -1, -1, -1

#quitar? solo para el de knn ?
def getCenters(imgc):
    img = preProccesing(imgc,False,True,'th',120)
    cx,cy,nc = findVisualCue(img,0,10000,.8)
    center = np.zeros((nc,2))

    for j in range(nc):
            center[j,0] = cx[j]
            center[j,1] = cy[j]
    n = 1
    while(n<nc):
        distance = ((center[n,0] - center[n-1,0])**2 + (center[n,1] - center[n-1,1] )**2 )**.5
        if distance < 10:
            center = delete(center,n,axis=0)
            nc -=1
        else:
            n+=1

    return center

def drawImage(imgc1,imgc2,matches,labels,time):
    for j in labels-1:
        cv2.circle(imgc1,(int(matches[j,0]),int(matches[j,1])),18,(255,255,0),-1)
        cv2.circle(imgc1,(int(matches[j,0]),int(matches[j,1])),10,(255,0,0),-1)
        cv2.putText(imgc1,str(j+1),(int(matches[j,0]),int(matches[j,1])),cv2.FONT_HERSHEY_SIMPLEX, 4.0, (255,255,0),3)
    for j in labels-1:
        cv2.circle(imgc2,(int(matches[j,2]),int(matches[j,3])),18,(255,255,0),-1)
        cv2.circle(imgc2,(int(matches[j,2]),int(matches[j,3])),10,(255,0,0),-1)
        cv2.putText(imgc2,str(j+1),(int(matches[j,2]),int(matches[j,3])),cv2.FONT_HERSHEY_SIMPLEX, 4.0, (255,255,0),3)

    cv2.namedWindow('result1',0)
    cv2.namedWindow('result2',0)
    cv2.imshow('result1', imgc1)
    cv2.imshow('result2', imgc2)
    if time == 0:
        cv2.waitKey()
    else:
        cv2.waitKey(time)
                                        
    return imgc1, imgc2


def drawImage2(imgc1,imgc2,matches1, matches2,labels1, labels2,time):
    i = 0 
    for j in labels1-1:
        cv2.circle(imgc1,(int(matches1[i,0]),int(matches1[i,1])),18,(255,255,0),-1)
        cv2.circle(imgc1,(int(matches1[i,0]),int(matches1[i,1])),10,(255,0,0),-1)
        cv2.putText(imgc1,str(j+1),(int(matches1[i,0]),int(matches1[i,1])),cv2.FONT_HERSHEY_SIMPLEX, 4.0, (255,255,0),3)
        i = i+1
    i = 0 
    for j in labels2-1:
        cv2.circle(imgc2,(int(matches2[i,0]),int(matches2[i,1])),18,(255,255,0),-1)
        cv2.circle(imgc2,(int(matches2[i,0]),int(matches2[i,1])),10,(255,0,0),-1)
        cv2.putText(imgc2,str(j+1),(int(matches2[i,0]),int(matches2[i,1])),cv2.FONT_HERSHEY_SIMPLEX, 4.0, (255,255,0),3)
        i = i+1

    cv2.namedWindow('result1',0)
    cv2.namedWindow('result2',0)
    cv2.imshow('result1', imgc1)
    cv2.imshow('result2', imgc2)
    if time == 0:
        cv2.waitKey()
    else:
        cv2.waitKey(time)
                                        
    return imgc1, imgc2

