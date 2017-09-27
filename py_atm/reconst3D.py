from numpy import*
from numpy.linalg import*
from lsm import lsm_lineal

class reconst3D:

    def fill_A (self,c1,c2,p1,p2,n):
        A = zeros((4,3))
    
        A[0,0] = c1[n,0]*p1[8,0] - p1[0,0];
        A[0,1] = c1[n,0]*p1[9,0] - p1[1,0];
        A[0,2] = c1[n,0]*p1[10,0] - p1[2,0];

        A[1,0] = c1[n,1]*p1[8,0] - p1[4,0];
        A[1,1] = c1[n,1]*p1[9,0] - p1[5,0];
        A[1,2] = c1[n,1]*p1[10,0] - p1[6,0];

        A[2,0] = c2[n,0]*p2[8,0] - p2[0,0];
        A[2,1] = c2[n,0]*p2[9,0] - p2[1,0];
        A[2,2] = c2[n,0]*p2[10,0] - p2[2,0];

        A[3,0] = c2[n,1]*p2[8,0] - p2[4,0];
        A[3,1] = c2[n,1]*p2[9,0] - p2[5,0];
        A[3,2] = c2[n,1]*p2[10,0] - p2[6,0];
        
        return A

    def fill_B(self,c1,c2,p1,p2,n):

        b = zeros((4,1))
        b[0,0] = p1[3,0] - c1[n,0];
        b[1,0] = p1[7,0] - c1[n,1];
        b[2,0] = p2[3,0] - c2[n,0];
        b[3,0] = p2[7,0] - c2[n,1]

        return b

    def get3D(self,c1,c2,n=0):
        A = self.fill_A(c1,c2,self.p1,self.p2,n)
        b = self.fill_B(c1,c2,self.p1,self.p2,n)
        x = lsm_lineal(A,b)
        return x

    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2
        
        


