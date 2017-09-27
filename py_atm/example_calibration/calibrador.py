import matplotlib.pyplot as plt
from numpy import*
from numpy.linalg import*
from lineal_calib import*

#Load 2d information
p2D_cam1 = loadtxt('data2D_cam1.txt',  delimiter = ",")
p2D_cam2 = loadtxt('data2D_cam2.txt',  delimiter = ",")


#Load 3d information
p3D = loadtxt('data3D.txt', delimiter = ",")

#More than 2000 correspondences can cause memory error

n,m = p3D.shape  # n =  number of correscpondences

if n > 2000:
    n = 2000
    p3D = p3D[0:2000,:]
    p2D_cam1 = p2D_cam1[0:2000,:]
    p2D_cam2 = p2D_cam2[0:2000,:]


#New calibration instance
calib1 = lineal_calib(p2D_cam1,p3D,False)
calib2 = lineal_calib(p2D_cam2,p3D,False)

#Calculate the parameters
p1 = calib1.parameters()
p2 = calib2.parameters()

print
print "Parameters camera 1"
print p1

print
print "Parameters camera 2"
print p2

savetxt('parameters_cam1.txt', p1, delimiter = ",",  fmt = '%1.10f' )
savetxt('parameters_cam2.txt', p2, delimiter = ",",  fmt = '%1.10f' )

param = [p1,p2]
p2D = [p2D_cam1,p2D_cam2]

k = 0
for p in param:
    # Test of errors, fill the matrix A
    A1 = [p[0,0],p[1,0],p[2,0],p[3,0]]
    A2 = [p[4,0],p[5,0],p[6,0],p[7,0]]
    A3 = [p[8,0],p[9,0],p[10,0],1]
    A = array([A1,A2,A3])


    n,m = shape(p2D[k])
    error = 0;

    #Show the 3D to 2D proyection

    print "3D to 2D proyection"
    for i in range(n):
        p3 = array([[p3D[i,0]],[p3D[i,1]],[p3D[i,2]],[1]])
        p2 = dot(A,p3)

        #print p2[0]/p2[2],  p2[1]/p2[2]
        error = error + ((p2D[k][i,0]  - p2[0]/p2[2])**2 + (p2D[k][i,1] - p2[1]/p2[2])**2) **.5

    k = k + 1
    print ("Camera " + str(k)) 
    print ("Sum square errors = ", error/n)
