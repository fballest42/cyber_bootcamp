#!/usr/bin/env python3.7
import sys

def not_int(s):
    i = len(s) - 1
    while (i >= 1):
        if not (s[i] >= '0')