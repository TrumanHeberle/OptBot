import numpy as np
from math import sqrt, sin, cos

### THIS FILE CONTAINS STATIC FUNCTIONS FOR MANIPULATING VECTORS (3D)

def mag(vec: np.ndarray) -> float:
    return sqrt(np.inner(vec,vec))

def normalize(vec: np.ndarray) -> np.ndarray:
    m = mag(vec)
    return vec if np.all(vec==0) or m==1 else vec/m

def rotation_matrix(roll: float, pitch: float, yaw: float) -> np.matrix:
    cp = cos(pitch); cy = cos(yaw); cr = cos(roll)
    sp = sin(pitch); sy = sin(yaw); sr = sin(roll)
    return np.matrix([[cp*cy, cr*sy-cy*sp*sr, -cr*cy*sp-sr*sy],
        [cp*sy, -cr*cy-sp*sr*sy, cy*sr-cr*sp*sy],[sp, cp*sr, cp*cr]])

def scalar_project(vec,axis) -> float:
    return np.dot(vec,normalize(axis))

def project(vec,axis) -> np.ndarray:
    axis = normalize(axis)
    return np.dot(vec,axis)*axis

def transform(vec: np.ndarray, tmat: np.matrix) -> np.ndarray:
    return np.squeeze(np.asarray(np.matmul(tmat,vec)))

def mag_normalize(vec: np.ndarray, mmax: float) -> np.ndarray:
    vm = mag(vec)
    if vm>mmax:
        return vec*mmax/vm
    return vec
