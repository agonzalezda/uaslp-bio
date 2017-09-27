from numpy import*
from numpy.linalg import*
from lsm import lsm_lineal

class lineal_calib:


    def A_matrix (self,points2D, points3D):

        n,m = shape(points2D)
        A = self.fill_A (points3D[0,0],points3D[0,1],points3D[0,2],points2D[0,0],points2D[0,1])
        
        for i in range(1,n):
            At = self.fill_A (points3D[i,0],points3D[i,1],points3D[i,2],points2D[i,0],points2D[i,1])
            A = concatenate((A ,At),axis=0)
        
        return A

    def fill_A (self,Xw,Yw,Zw,xi,yi):
        At = zeros((2,11))
    
	At[0,0] = Xw;
	At[0,1] = Yw;
	At[0,2] = Zw;
	At[0,3] = 1;
	At[0,8] = -xi*Xw;
	At[0,9] = -xi*Yw;
	At[0,10] = -xi*Zw;

	At[1,4] = Xw;
	At[1,5] = Yw;
	At[1,6] = Zw;
	At[1,7] = 1;
	At[1,8] = -yi*Xw;
	At[1,9] = -yi*Yw;
	At[1,10] = -yi*Zw;
        
        return At

    def B_matrix (self,points2D):
    
        n,m = shape(points2D)
        B = zeros((n*2,1))

        for i in range(n):
            B[2*i+0] = points2D[i,0]
            B[2*i+1] = points2D[i,1]        
        return B

    def parameters(self):
        return self.x


    def __init__(self,points2D, points3D,use_arma = False):
        A = self.A_matrix(points2D, points3D)
        b = self.B_matrix(points2D)
        self.x = lsm_lineal(A,b)
        
        


