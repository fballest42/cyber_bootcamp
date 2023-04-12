#!/usr/bin/env python3

from vector import Vector

def test_vector(test: str, arg):
    print(test)
    try:
        v = Vector(arg)
        print(v.values)
        print(v.shape)
        return (v)
    except Exception as e:
        print(e)
        return None


def test_multiplication(test: str, v: Vector, scalar):
    print(test)
    try:
        v1 = v * scalar
        v2 = scalar * v
        print(str(v1) + " == " + str(v2))
        return (v1)
    except Exception as e:
        print(e)
        return None


def test_dot(test: str, v1: Vector, v2: Vector):
    print(test)
    try:
        vA = v1.dot(v2)
        vB = v2.dot(v1)
        print(v1, v2, str(vA) + " == " + str(vB))
        return (vA)
    except Exception as e:
        print(e)
        return None


def test_add_sub(test: str, v1: Vector, v2: Vector):
    print(test)
    try:
        v1A = v1 + v2
        v1B = v2 + v1
        v2A = v1 - v2
        v2B = -1 * (v2 - v1)
        v3A = -1 * v1 - v2
        v3B = -1 * v2 - v1
        print(str(v1A) + " == " + str(v1B))
        print(str(v2A) + " == " + str(v2B))
        print(str(v3A) + " == " + str(v3B))
        return (v1A)
    except Exception as e:
        print(e)
        return None


def test_division(test: str, v: Vector, scalar):
    print(test)
    v1 = None
    try:
        v1 = v / scalar
        print(str(v1))
    except Exception as e:
        print(e)
    try:
        v2 = scalar / v
        print(str(v2))
        return v1
    except Exception as e:
        print(e)
        return v1


v1 = test_vector("\033[33mFour list in list:\033[0m",
                 [[0.0], [1.0], [2.0], [3.0]])
v2 = test_vector("\n\033[33mSingle list:\033[0m", [0.0, 1.0, 2.0, 3.0])
v3 = test_vector("\n\033[33m[2x2]:\033[0m", [[0.0, 1.0], [2.0, 3.0]])
test_vector("\n\033[33mSingle list 2:\033[0m", [0., 1.131, 1e5, 3.0])
test_vector("\n\033[33mSingle list in list:\033[0m",
            [[0.0, 1.0, 2.0, 3.0]])
test_vector("\n\033[33mSingle list in list in list:\033[0m",
            [[[0.0, 1.0, 2.0, 3.0]]])
test_vector("\n\033[33mSize negative\033[0m", -1)
v0 = test_vector("\n\033[33mSize zero\033[0m", 0)
v = test_vector("\n\033[33mSize positive\033[0m", 4)
test_vector("\n\033[33mTuple with same number\033[0m", (0, 0))
test_vector("\n\033[33mTuple increasing\033[0m", (0, 10))
test_vector("\n\033[33mTuple decreasing\033[0m", (10, 0))
test_vector("\n\033[33mTuple error\033[0m", (0, 1.1))

print("\n\033[35mMULTIPLICATION\033[0m")
test_multiplication("\n\033[33m" + str(v1) + " * " + str(5)
                    + "\033[0m", v1, 5)
test_multiplication("\n\033[33m" + str(v1) + " * " + str(3.5)
                    + "\033[0m", v1, 3.5)
test_multiplication("\n\033[33m" + str(v1) + " * " + str(0)
                    + "\033[0m", v1, 0)
test_multiplication("\n\033[33m" + str(v1) + " * " + str(-4)
                    + "\033[0m", v1, -4)
test_multiplication("\n\033[33m" + str(v2) + " * " + str(5)
                    + "\033[0m", v2, 5)
test_multiplication("\n\033[33m" + str(v2) + " * " + str(3.5)
                    + "\033[0m", v2, 3.5)
test_multiplication("\n\033[33m" + str(v2) + " * " + str(0)
                    + "\033[0m", v2, 0)
test_multiplication("\n\033[33m" + str(v2) + " * " + str(-4)
                    + "\033[0m", v2, -4)
test_multiplication("\n\033[33m" + str(v0) + " * " + str(-4)
                    + "\033[0m", v0, -4)

print("\n\033[35mDOT PRODUCT\033[0m")
test_dot("", v1, v1)
test_dot("", v2, v2)
test_dot("", v2, v1.T())
test_dot("", v0, v0)
test_dot("", Vector([1.0]), Vector([0.5]))
test_dot("", Vector([2.0, 0.5, 1/3]), Vector([1.5, 6.0, 9.0]))
test_dot("", Vector([[2.0], [0.5], [1/3]]), Vector([[1.5], [6.0], [9.0]]))
test_dot("", Vector([[1.0, 3.0]]), Vector([[2.0, 4.0]]))

print("\n\033[35mADDITION & SUBSTRACTION\033[0m")
test_add_sub("", v1, v1)
test_add_sub("", v2, v2)
test_add_sub("", v0, v0)

print("\n\033[35mDIVISION\033[0m")
test_division("\n\033[33m" + str(v1) + " / " + str(3) + "\033[0m", v1, 3)
test_division("\n\033[33m" + str(v1) + " / " + str(0.33) + "\033[0m", v1, 0.33)
test_division("\n\033[33m" + str(v1) + " / " + str(0) + "\033[0m", v1, 0)
test_division("\n\033[33m" + str(v1) + " / " + str(None) + "\033[0m", v1, None)
test_division("\n\033[33m" + str(v0) + " / " + str(3) + "\033[0m", v0, 3)

print("\n\033[35m\033[0m")
print(repr(v1 * +3.14))
print(v1)
print(v1.shape)
print(v1.T())
print(v1.T().shape)

print("\n\033[35m Correction:\033[0m")
print(Vector([1., 2e-3, 3.14, 5.]).values)
print(Vector(4).values)
print(Vector((10, 12)).values)
try:
    Vector(-1)
except Exception as e:
    print(e)
print(Vector((3, 1)).values)
print(Vector((1, 1)).values)
try:
    Vector((4, 7.1))
except Exception as e:
    print(e)
print(Vector(4) * 4)
print(4.0 * Vector(4))
try:
    print(Vector(4) * "hi")
except Exception as e:
    print(e)
print(Vector(4) / 2)
print(Vector(4) / 3.14)
