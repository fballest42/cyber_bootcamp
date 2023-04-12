#!/usr/bin/env python3
t = (12, 24, 36)

if (isinstance(t, tuple) and len(t) == 0):
    print("There are no numbers.")
elif (isinstance(t, (int, str, list, dict))):
    print("Error is not a tuple")
elif (len(t) > 1):
    s = "{}".format(t[0])
    i = 1
    while (i < len(t)):
        s += ", {}".format(t[i])
        i += 1
    print("The {} numbers are: {}".format(i, s), end="") 
