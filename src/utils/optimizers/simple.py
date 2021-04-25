#from numba import njit
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

# solves a system using simple linear regression

#@njit
def sample(n,m):
    """returns a sample input of X"""
    return np.random.uniform(-1,1,(n,m))

#@njit
def R(X):
    """returns an adjusted sample input for the form: R=[X,1]'"""
    return np.vstack((X,np.ones((1,X.shape[1]))))

#@njit
def solve(X,Y):
    """return the constant matrix B for the form: Y = B*R"""
    Rm = R(X)
    RmT = Rm.transpose()
    Y += np.random.uniform(-100,100,Y.shape) # randomness
    return Y@RmT@np.linalg.inv(Rm@RmT)

# true constants
n = 60
A = np.random.uniform(-1,1,(n,n))
b = np.random.uniform(-1,1,(n,1))
B = np.hstack((A,b))

# numerical prediction
ms = [n*2**(i+1) for i in range(16)]
results = []
for m in ms:
    print(f"solving for {n*(n+1)} constants using {m} samples...")
    X = sample(n,m)
    results.append(solve(X,B@R(X)))

# validation sample
X = sample(n,n)
Rm = R(X)
Y = B@Rm

# residuals
resBr = [np.mean(abs((B-Bp)/B)) for Bp in results] # relative
resNr = [np.mean(abs((Y-Bp@Rm)/Y)) for Bp in results] # relative
resBa = [np.mean(abs(B-Bp)) for Bp in results] # absolute
resNa = [np.mean(abs(Y-Bp@Rm)) for Bp in results] # absolute

# residual graphs
plot = sb.lineplot(x=ms,y=resBr)
plot = sb.lineplot(x=ms,y=resBa)
plot = sb.lineplot(x=ms,y=resNr)
plot = sb.lineplot(x=ms,y=resNa)
plot.set_title("Accuracy vs Sample Number")
plot.set_xlabel("Number of Samples")
plot.set_ylabel("Average Residual")
plot.legend(labels=["B (relative)","B (absolute)","net (relative)","net (absolute)"])
plt.show()
