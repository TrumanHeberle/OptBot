from utils.vector import Vector
from copy import copy
from math import pi, atan, isclose

TOLERANCE = 0.00000001;

def test_init():
    """vector initialization"""
    v = Vector(1,2,3)
    assert v.x==1 and v.roll==1
    assert v.y==2 and v.pitch==2
    assert v.z==3 and v.yaw==3

def test_setters():
    """vector property setters"""
    v = Vector(1,2,3)
    v.x = 4
    assert v.x==4 and v.y==2 and v.z==3
    v.y = 5
    assert v.x==4 and v.y==5 and v.z==3
    v.z = 6
    assert v.x==4 and v.y==5 and v.z==6

def test_copy():
    """vector deep copying"""
    v = Vector(1,2,3)
    vcopy = copy(v)
    assert v.x==vcopy.x
    assert v.y==vcopy.y
    assert v.z==vcopy.z
    vcopy.x = 4
    vcopy.y = 5
    vcopy.z = 6
    assert v.x != vcopy.x
    assert v.y != vcopy.y
    assert v.z != vcopy.z

def test_to_string():
    """vector to string"""
    assert str(Vector(1,2,3))=="(1,2,3)"

def test_to_list():
    """vector to list"""
    assert list(Vector(1,2,3))==[1,2,3]
    assert list(Vector(-1,0,1))==[-1,0,1]
    assert list(Vector(-1,-2,-3))==[-1,-2,-3]

def test_equality():
    """vector equality"""
    v1 = Vector(1,2,3)
    v2 = Vector(1,2,3)
    assert v1==v2
    v2.z = 1
    assert v1!=v2
    v2.z = 3
    v2.y = 3
    assert v1!=v2
    v2.y = 2
    v2.x = 2
    assert v1!=v2
    v2.x = 1
    assert v1==v2

def test_addition():
    """vector addition"""
    # vector addition
    assert Vector(1,2,3)+Vector(-1,-2,-3)==Vector(0,0,0)
    assert Vector(1,2,3)+Vector(1,-2,-3)==Vector(2,0,0)
    assert Vector(1,2,3)+Vector(1,2,3)==Vector(2,4,6)
    # scalar addition
    assert Vector(1,2,3)+2==Vector(3,4,5)
    assert Vector(1,2,3)+(-2)==Vector(-1,0,1)
    assert Vector(1,2,3)+0==Vector(1,2,3)
    # inplace vector addition
    v = Vector(1,2,3)
    v += Vector(1,2,3)
    assert v==Vector(2,4,6)
    # inplace scalar addition
    v = Vector(1,2,3)
    v += 2
    assert v==Vector(3,4,5)

def test_subtraction():
    """vector subtraction"""
    # vector subtraction
    assert Vector(1,2,3)-Vector(-1,-2,-3)==Vector(2,4,6)
    assert Vector(1,2,3)-Vector(1,-2,-3)==Vector(0,4,6)
    assert Vector(1,2,3)-Vector(1,2,3)==Vector(0,0,0)
    # scalar subtraction
    assert Vector(1,2,3)-2==Vector(-1,0,1)
    assert Vector(1,2,3)-(-2)==Vector(3,4,5)
    assert Vector(1,2,3)-0==Vector(1,2,3)
    # inplace vector subtraction
    v = Vector(1,2,3)
    v -= Vector(1,2,3)
    assert v==Vector(0,0,0)
    # inplace scalar subtraction
    v = Vector(1,2,3)
    v -= 2
    assert v==Vector(-1,0,1)

def test_negation():
    """vector negation"""
    assert -Vector(1,2,3)==Vector(-1,-2,-3)
    assert -Vector(-1,-2,-3)==Vector(1,2,3)
    assert -Vector(-1,0,1)==Vector(1,0,-1)

def test_multiplication():
    """vector multiplication"""
    # vector multiplication
    assert Vector(1,2,3)*Vector(-1,-2,-3)==Vector(-1,-4,-9)
    assert Vector(1,2,3)*Vector(1,-2,-3)==Vector(1,-4,-9)
    assert Vector(1,2,3)*Vector(0,0,0)==Vector(0,0,0)
    # scalar multiplication
    assert Vector(1,2,3)*2==Vector(2,4,6)
    assert Vector(1,2,3)*(-2)==Vector(-2,-4,-6)
    assert Vector(1,2,3)*0==Vector(0,0,0)
    # inplace vector multiplication
    v = Vector(1,2,3)
    v *= Vector(1,2,3)
    assert v==Vector(1,4,9)
    # inplace scalar multiplication
    v = Vector(1,2,3)
    v *= 2
    assert v==Vector(2,4,6)

def test_division():
    """vector division"""
    # vector division
    assert Vector(1,2,3)/Vector(-1,-2,-3)==Vector(-1,-1,-1)
    assert Vector(1,2,3)/Vector(1,-2,-3)==Vector(1,-1,-1)
    assert Vector(0,0,0)/Vector(1,2,3)==Vector(0,0,0)
    # scalar division
    assert Vector(1,2,3)/2==Vector(0.5,1,1.5)
    assert Vector(1,2,3)/(-2)==Vector(-0.5,-1,-1.5)
    assert Vector(1,2,3)/0.5==Vector(2,4,6)
    # inplace vector division
    v = Vector(1,2,3)
    v /= Vector(1,2,3)
    assert v==Vector(1,1,1)
    # inplace scalar division
    v = Vector(1,2,3)
    v /= 2
    assert v==Vector(0.5,1,1.5)

def test_modulo():
    """vector modulo"""
    # vector modulo
    assert Vector(10,11,12)%Vector(2,4,6)==Vector(0,3,0)
    assert Vector(10,-11,12)%Vector(3,5,7)==Vector(1,4,5)
    assert Vector(10,-11,-12)%Vector(-7,-5,-3)==Vector(-4,-1,0)
    # scalar modulo
    assert Vector(10,11,12)%5==Vector(0,1,2)
    assert Vector(10,-11,12)%6==Vector(4,1,0)
    assert Vector(10,-11,-12)%-5==Vector(0,-1,-2)
    # inplace vector modulo
    v = Vector(10,-11,12)
    v %= Vector(3,5,7)
    assert v==Vector(1,4,5)
    # inplace scalar modulo
    v = Vector(10,-11,12)
    v %= 6
    assert v==Vector(4,1,0)

def test_magnitude():
    """vector magnitude"""
    assert Vector(0,0,0).mag()==0
    assert Vector(1,0,0).mag()==1
    assert Vector(0,1,0).mag()==1
    assert Vector(0,0,1).mag()==1
    assert Vector(1,0,1).mag()==2**0.5
    assert Vector(1,1,0).mag()==2**0.5
    assert Vector(0,1,1).mag()==2**0.5
    assert Vector(1,1,1).mag()==3**0.5
    assert Vector(1,2,3).mag()==14**0.5

def test_dot():
    """vector dot product"""
    assert Vector(0,0,0).dot(Vector(0,0,0))==0
    assert Vector(1,2,3).dot(Vector(0,0,0))==0
    assert Vector(0,0,0).dot(Vector(1,2,3))==0
    assert Vector(1,2,3).dot(Vector(1,0,0))==1
    assert Vector(1,2,3).dot(Vector(0,1,0))==2
    assert Vector(1,2,3).dot(Vector(0,0,1))==3
    assert Vector(1,2,3).dot(Vector(2,3,4))==20
    assert Vector(2,3,4).dot(Vector(1,2,3))==20

def test_cross():
    """vector cross product"""
    zero = Vector(0,0,0)
    x = Vector(1,0,0)
    y = Vector(0,1,0)
    z = Vector(0,0,1)
    xy = Vector(1,2,0)
    yz = Vector(0,2,1)
    # zero vector cases
    assert zero.cross(zero)==Vector(0,0,0)
    assert x.cross(zero)==Vector(0,0,0)
    assert zero.cross(x)==Vector(0,0,0)
    assert y.cross(zero)==Vector(0,0,0)
    assert zero.cross(x)==Vector(0,0,0)
    assert z.cross(zero)==Vector(0,0,0)
    assert zero.cross(z)==Vector(0,0,0)
    assert xy.cross(zero)==Vector(0,0,0)
    assert zero.cross(xy)==Vector(0,0,0)
    # orthonormal cases
    assert x.cross(y)==Vector(0,0,1)
    assert x.cross(z)==Vector(0,-1,0)
    assert y.cross(z)==Vector(1,0,0)
    assert y.cross(x)==Vector(0,0,-1)
    assert z.cross(x)==Vector(0,1,0)
    assert z.cross(y)==Vector(-1,0,0)
    # general cases
    assert xy.cross(x)==Vector(0,0,-2)
    assert x.cross(xy)==Vector(0,0,2)
    assert xy.cross(yz)==Vector(2,-1,2)
    assert yz.cross(xy)==Vector(-2,1,-2)

def test_angle():
    """vector angles"""
    x = Vector(1,0,0)
    y = Vector(0,1,0)
    z = Vector(0,0,1)
    xy = Vector(1,2,0)
    yz = Vector(0,2,1)
    # same angle cases
    assert x.angle(x)==0
    assert y.angle(y)==0
    assert z.angle(z)==0
    # opposite angle cases
    assert x.angle(-x)==pi
    assert (-x).angle(x)==pi
    assert y.angle(-y)==pi
    assert (-y).angle(y)==pi
    assert z.angle(-z)==pi
    assert (-z).angle(z)==pi
    # orthonormal cases
    assert x.angle(y)==pi/2
    assert x.angle(z)==pi/2
    assert y.angle(x)==pi/2
    assert y.angle(z)==pi/2
    assert z.angle(y)==pi/2
    assert z.angle(x)==pi/2
    # general cases
    assert isclose(xy.angle(x),atan(2),abs_tol=TOLERANCE)
    assert isclose(x.angle(xy),atan(2),abs_tol=TOLERANCE)
    assert isclose(xy.angle(y),atan(0.5),abs_tol=TOLERANCE)
    assert isclose(y.angle(xy),atan(0.5),abs_tol=TOLERANCE)

def test_normalize():
    """vector normalization"""
    # zero vector case
    assert Vector(0,0,0).normalize()==Vector(0,0,0)
    # orthonormal cases
    assert Vector(1,0,0).normalize()==Vector(1,0,0)
    assert Vector(0,1,0).normalize()==Vector(0,1,0)
    assert Vector(0,0,1).normalize()==Vector(0,0,1)
    assert Vector(0.4,0,0).normalize()==Vector(1,0,0)
    assert Vector(0,0.5,0).normalize()==Vector(0,1,0)
    assert Vector(0,0,0.6).normalize()==Vector(0,0,1)
    # general cases
    n = Vector(1,1,0).normalize()
    assert isclose(n.x,0.5**0.5,abs_tol=TOLERANCE)
    assert isclose(n.y,0.5**0.5,abs_tol=TOLERANCE)
    assert n.z==0
    n = Vector(0,1,1).normalize()
    assert n.x==0
    assert isclose(n.y,0.5**0.5,abs_tol=TOLERANCE)
    assert isclose(n.z,0.5**0.5,abs_tol=TOLERANCE)
    n = Vector(1,-1,1).normalize()
    assert isclose(n.x,(1/3)**0.5,abs_tol=TOLERANCE)
    assert isclose(n.y,-(1/3)**0.5,abs_tol=TOLERANCE)
    assert isclose(n.z,(1/3)**0.5,abs_tol=TOLERANCE)

def test_project():
    """vector projection"""
    zero = Vector(0,0,0)
    x = Vector(1,0,0)
    y = Vector(0,1,0)
    z = Vector(0,0,1)
    xy = Vector(1,1,0)
    xyz = Vector(1,1,1)
    v = Vector(10,11,12)
    # zero vector cases
    assert x.project(zero)==Vector(0,0,0)
    assert y.project(zero)==Vector(0,0,0)
    assert z.project(zero)==Vector(0,0,0)
    assert zero.project(x)==Vector(0,0,0)
    assert zero.project(y)==Vector(0,0,0)
    assert zero.project(z)==Vector(0,0,0)
    assert x.scalar_project(zero)==0
    assert y.scalar_project(zero)==0
    assert z.scalar_project(zero)==0
    assert zero.scalar_project(x)==0
    assert zero.scalar_project(y)==0
    assert zero.scalar_project(z)==0
    # orthonormal cases
    assert xy.project(x)==Vector(1,0,0)
    assert xy.project(y)==Vector(0,1,0)
    assert xy.project(z)==Vector(0,0,0)
    assert xyz.project(x)==Vector(1,0,0)
    assert xyz.project(y)==Vector(0,1,0)
    assert xyz.project(z)==Vector(0,0,1)
    assert xy.scalar_project(x)==1
    assert xy.scalar_project(y)==1
    assert xy.scalar_project(z)==0
    assert xyz.scalar_project(x)==1
    assert xyz.scalar_project(y)==1
    assert xyz.scalar_project(z)==1
    # general cases
    p = xyz.project(xy)
    assert isclose(p.x,1,abs_tol=TOLERANCE) and isclose(p.y,1,abs_tol=TOLERANCE) and p.z==0
    assert isclose(xyz.scalar_project(xy),2**0.5,abs_tol=TOLERANCE)
    p = v.project(xy)
    assert isclose(p.x,10.5,abs_tol=TOLERANCE) and isclose(p.y,10.5,abs_tol=TOLERANCE) and p.z==0
    assert isclose(v.scalar_project(xy),(2*(10.5**2))**0.5,abs_tol=TOLERANCE)

def test_rotation():
    """vector rotation"""
    # TODO: write rotation test
