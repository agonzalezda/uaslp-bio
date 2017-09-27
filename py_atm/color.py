from pylab import *
from numpy import *
from numpy import linalg as LA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2

def constancy(imgc1):
    b,g,r = cv2.split(imgc1)

    ar =  mean(r)
    ag =  mean(g)
    ab =  mean(b)

    max_c = max(max(ar,ag,ab),128)

    c_r = max_c  / ar
    c_g = max_c  / ag
    c_b = max_c  / ab

    r = cv2.convertScaleAbs(c_r*r)
    g = cv2.convertScaleAbs(c_g*g)
    b = cv2.convertScaleAbs(c_b*b)
	
    img = cv2.merge((b,g,r))

    return img
