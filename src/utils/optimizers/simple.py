import numpy as np

# solves a system using simple linear regression

def R(X):
    """returns an adjusted sample input for the form: R=[X,1]'"""
    return np.vstack((X,np.ones((1,X.shape[1]))))

def solve(X,Y):
    """return the constant matrix B for the form: Y = B*R"""
    Rm = R(X)
    RmT = Rm.transpose()
    return Y@RmT@np.linalg.inv(Rm@RmT)
