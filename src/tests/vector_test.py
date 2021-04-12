from utils.vector import Vector
from copy import copy

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

def test_division():
    """vector division"""

def test_modulo():
    """vector modulo"""

def test_magnitude():
    """vector magnitude"""

def test_dot():
    """vector dot product"""

def test_cross():
    """vector cross product"""

def test_angle():
    """vector angles"""

def test_project():
    """vector projection"""

def test_normalize():
    """vector normalization"""

def test_rotation():
    """vector rotation"""
