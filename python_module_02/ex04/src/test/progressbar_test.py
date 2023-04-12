#!/usr/bin/env python3
""" A file to test the progressbar funtion """
import time
from random import randint
from my_minipack.progressbar import progressbar

if __name__ == "__main__":
    listy = range(1000)
    ret = 0
    for elem in progressbar(listy):
        ret += (elem + 3) % 5
        time.sleep(0.005)
    print(ret, end="")

