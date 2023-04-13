#!/usr/bin/env python3
t = (5, 10, 15, 20 , 25)

if (isinstance(t, tuple) and len(t) != 0):
    i = 0
    s = ""
    while (i < len(t) - 1):
        s += "{}, ".format(t[i])
        i += 1
    print("The {} numbers are: {}{}".format(i + 1, s, t[-1]), end="")
else:
    print("ERROR")
