from numpy import*
from scipy.linalg import*

def lsm_lineal (A,b):
    x = dot (pinv(A),b)
    return x


