from random import random
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

dt = 0.5
A1 = [1,2,3]
A2 = [4,5,6]
A3 = [7,8,9]
A = np.matrix([A1,A2,A3])

def solve(randomness=0.5):
    Ap = np.zeros((3,3))
    res = [np.linalg.norm(Ap-A)]
    for i in range(200):
        # optimize on first set of residuals
        s1 = [random(),random(),random()]
        s2 = [random(),random(),random()]
        s3 = [random(),random(),random()]
        S1 = np.matrix([s1,s2,s3]).transpose()
        s1r = 1+(random()-0.5)*randomness
        s2r = 1+(random()-0.5)*randomness
        s3r = 1+(random()-0.5)*randomness
        S1Noisy = np.matrix([[s1r,0,0],[0,s2r,0],[0,0,s3r]])*S1
        S2 = A*S1Noisy*dt
        Aappx = S2*np.linalg.inv(S1)/dt;
        Ap = (Ap*(i-1)+Aappx)/i if i>0 else Aappx
        # check residuals of second set of residuals
        s1 = [random(),random(),random()]
        s2 = [random(),random(),random()]
        s3 = [random(),random(),random()]
        S1 = np.matrix([s1,s2,s3]).transpose()
        res.append(np.linalg.norm((Ap-A)*S1))
    return (Ap,res)

# get results
Aps = []
residuals = []
randomness = []
for i in range(5):
    r = i/4
    Ap, res = solve(r)
    Aps.append(Ap)
    residuals.append(res)
    randomness.append(r)

# plot results
for i,Ap in enumerate(Aps):
    print(randomness[i],"\n",Ap,"\n")
plot = sb.lineplot(data=residuals)
plot.set_title("Residual Norms of Simple Algorithm")
plot.set_xlabel("Iteration Number")
plot.set_ylabel("Residuals (2-Norm)")
leg = plot.legend(randomness)
leg.set_title("Noise Ratio")
plt.show()
