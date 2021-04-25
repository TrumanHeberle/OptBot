from copy import copy
from math import sin, cos, acos

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
    def y(self):
        return self.x2
    @property
    def z(self):
        return self.x3
    @x.setter
    def x(self, val: float):
        self.x1 = val
    @y.setter
    def y(self, val: float):
        self.x2 = val
    @z.setter
    def z(self, val: float):
        self.x3 = val
    @property
    def roll(self):
        return self.x
    @property
    def pitch(self):
        return self.y
    @property
    def yaw(self):
        return self.z
    @roll.setter
    def roll(self, val: float):
        self.x = val
    @pitch.setter
    def pitch(self, val: float):
        self.y = val
    @yaw.setter
    def yaw(self, val: float):
        self.z = val
    def __copy__(self):
        return Vector(self.x,self.y,self.z)
    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+","+str(self.z)+")"
    def __repr__(self):
        return str(self)
    def __getitem__(self, i):
        return (self.x,self.y,self.z)[i]
    def __eq__(self, other):
        return self.x==other.x and self.y==other.y and self.z==other.z
    def __ne__(self, other):
        return self.x!=other.x or self.y!=other.y or self.z!=other.z
    def __add__(self, other):
        try:
            # vector addition
            return Vector(self.x+other.x,self.y+other.y,self.z+other.z)
        except:
            # scalar addition
            return Vector(self.x+other,self.y+other,self.z+other)
    def __radd__(self, other):
        try:
            # vector addition
            return Vector(other.x+self.x,other.y+self.y,other.z+self.z)
        except:
            # scalar addition
            return Vector(other+self.x,other+self.y,other+self.z)
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
    def __rsub__(self, other):
        try:
            # vector subtraction
            return Vector(other.x-self.x,other.y-self.y,other.z-self.z)
        except:
            # scalar subtraction
            return Vector(other-self.x,other-self.y,other-self.z)
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
    def __rmul__(self, other):
        try:
            # elementwise multiplication
            return Vector(other.x*self.x,other.y*self.y,other.z*self.z)
        except:
            # scalar multiplication
            return Vector(other*self.x,other*self.y,other*self.z)
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
    def __imod__(self, other):
        try:
            # elementwise modulo
            self.x %= other.x
            self.y %= other.y
            self.z %= other.z
        except:
            # scalar modulo
            self.x %= other
            self.y %= other
            self.z %= other
        return self
    def __truediv__(self, other):
        try:
            # elementwise division
            return Vector(self.x/other.x,self.y/other.y,self.z/other.z)
        except:
            # scalar division
            return Vector(self.x/other,self.y/other,self.z/other)
    def __rtruediv__(self, other):
        try:
            # elementwise division
            return Vector(other.x/self.x,other.y/self.y,other.z/self.z)
        except:
            # scalar division
            return Vector(other/self.x,other/self.y,other/self.z)
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
    def approx(self, other, tolerance=0.000001):
        """Returns whether two vectors are similar enough"""
        return (self-other).mag() < tolerance
    def mag(self) -> float:
        """Returns the magnitude of the vector"""
        return (self.x**2+self.y**2+self.z**2)**0.5
    def dot(self, other) -> float:
        """Returns the dot product of two vectors"""
        return self.x*other.x+self.y*other.y+self.z*other.z
    def scalar_project(self, axis) -> float:
        """Returns the magnitude of the vector projected onto an axis"""
        return self.dot(axis.normalize())
    def angle(self, other) -> float:
        """Returns the angle between two vectors"""
        return acos(self.dot(other)/(self.mag()*other.mag()))
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
        "Returns the vector rotated by euler angles"
        cr = cos(other.roll); cp = cos(other.pitch); cy = cos(other.yaw)
        sr = sin(other.roll); sp = sin(other.pitch); sy = sin(other.yaw)
        x = self.x*(cp*cy)+self.y*(cy*sp*sr-cr*sy)+self.z*(-cr*cy*sp-sr*sy)
        y = self.x*(cp*sy)+self.y*(cr*cy+sp*sr*sy)+self.z*(cy*sr-cr*sp*sy)
        z = self.x*(sp)+self.y*(-cp*sr)+self.z*(cp*cr)
        return Vector(x,y,z)
