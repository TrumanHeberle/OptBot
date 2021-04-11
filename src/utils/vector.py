from typing import List
from copy import copy
import numpy as np
from math import sqrt, sin, cos

### THIS FILE CONTAINS STATIC FUNCTIONS FOR MANIPULATING VECTORS (3D)

class Vector:
    def __init__(self,x,y,z):
        self.x1 = x
        self.x2 = y
        self.x3 = z
    @property
    def x(self):
        return self.x1
    @property
    def roll(self):
        return self.x1
    @property
    def y(self):
        return self.x2
    @property
    def pitch(self):
        return self.x2
    @property
    def z(self):
        return self.x3
    @property
    def yaw(self):
        return self.x3
    @x.setter
    def x(self, val: float):
        self.x1 = val
    @roll.setter
    def roll(self, val: float):
        self.x1 = val
    @y.setter
    def y(self, val: float):
        self.x2 = val
    @pitch.setter
    def pitch(self, val: float):
        self.x2 = val
    @z.setter
    def z(self, val: float):
        self.x3 = val
    @yaw.setter
    def yaw(self, val: float):
        self.x3 = val
    def __copy__(self):
        return Vector(self.x,self.y,self.z)
    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+", "+str(self.z)+")"
    def as_list(self) -> List[float]:
        """Returns the vector as a list"""
        return [self.x,self.y,self.z]
    def __add__(self, other):
        try:
            # vector addition
            return Vector(self.x+other.x,self.y+other.y,self.z+other.z)
        except:
            # scalar addition
            return Vector(self.x-other,self.y-other,self.z-other)
    def __iadd__(self, other):
        try:
            # vector addition
            self.x += other.x
            self.y += other.y
            self.z += other.z
        except:
            # scalar addition
            self.x += other
            self.y += other
            self.z += other
        return self
    def __sub__(self, other):
        try:
            # vector subtraction
            return Vector(self.x-other.x,self.y-other.y,self.z-other.z)
        except:
            # scalar subtraction
            return Vector(self.x-other,self.y-other,self.z-other)
    def __isub__(self, other):
        try:
            # vector subtraction
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
        except:
            # scalar subtraction
            self.x -= other
            self.y -= other
            self.z -= other
        return self
    def __mul__(self, other):
        try:
            # elementwise multiplication
            return Vector(self.x*other.x,self.y*other.y,self.z*other.z)
        except:
            # scalar multiplication
            return Vector(self.x*other,self.y*other,self.z*other)
    def __imul__(self, other):
        try:
            # elementwise multiplication
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        except:
            # scalar multiplication
            self.x *= other
            self.y *= other
            self.z *= other
        return self
    def __neg__(self):
        return Vector(-self.x,-self.y,-self.z)
    def __mod__(self, other):
        try:
            # elementwise modulo
            return Vector(self.x%other.x,self.y%other.y,self.z%other.z)
        except:
            # scalar modulo
            return Vector(self.x%other,self.y%other,self.z%other)
    def __truediv__(self, other):
        try:
            # elementwise division
            return Vector(self.x/other.x,self.y/other.y,self.z/other.z)
        except:
            # scalar division
            return Vector(self.x/other,self.y/other,self.z/other)
    def __itruediv__(self, other):
        try:
            # elementwise division
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
        except:
            # scalar division
            self.x /= other
            self.y /= other
            self.z /= other
        return self
    def mag(self) -> float:
        """Returns the magnitude of the vector"""
        return (self.x**2+self.y**2+self.z**2)**0.5
    def dot(self, other) -> float:
        """Returns the dot product of two vectors"""
        return self.x*other.x+self.y*other.y+self.z*other.z
    def scalar_project(self, axis) -> float:
        """Returns the magnitude of the vector projected onto an axis"""
        return self.dot(axis.normalize())
    def normalize(self):
        """Returns the vector normalized to magnitude 1"""
        m = self.mag()
        if m==0:
            return Vector(0,0,0)
        if m==1:
            return copy(self)
        return copy(self)/m
    def mag_normalize(self, mx: float):
        """Returns the vector normalized to have a magnitude <= mx"""
        m = self.mag()
        if m==0:
            return Vector(0,0,0)
        if m<=mx:
            return copy(self)
        return copy(self)*mx/m
    def project(self, axis):
        """Returns the vector projected onto an axis"""
        axis = axis.normalize()
        return axis*self.dot(axis)
    def cross(self, other):
        """Returns the cross product of two vectors"""
        x = self.y*other.z-self.z*other.y
        y = self.z*other.x-self.x*other.z
        z = self.x*other.y-self.y*other.x
        return Vector(x,y,z)
    def rpy(self, other):
        """Returns the vector rotated by euler angles"""
        cp = cos(other.pitch); cy = cos(other.yaw); cr = cos(other.roll)
        sp = sin(other.pitch); sy = sin(other.yaw); sr = sin(other.roll)
        x = self.x*(cp*cy)+self.y*(cr*sy-cy*sp*sr)+self.z*(-cr*cy*sp-sr*sy)
        y = self.x*(cp*sy)+self.y*(-cr*cy-sp*sr*sy)+self.z*(cy*sr-cr*sp*sy)
        z = self.x*(sp)+self.y*(cp*sr)+self.z*(cp*cr)
        return Vector(x,y,z)
