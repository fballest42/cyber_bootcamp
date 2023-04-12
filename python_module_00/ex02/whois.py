#!/usr/bin/env python3.7
import sys

if len(sys.argv) == 2:
    argum = sys.argv[1].lstrip("+-")
    try:
        int(argum)
        if (int(argum) == 0):
            print("I'm Zero.")
        elif (int(argum) % 2 == 0):
            print("I'm Even.")
        elif (int(argum) % 2 == 1):
                print("I'm Odd.")
    except:
        print("AssertionError: argument is not an integer.")
elif len(sys.argv) > 2:
    print("AssertionError: more than one argument are provided.")
