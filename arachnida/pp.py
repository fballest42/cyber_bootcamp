#!/usr/bin/env python3

import sys

class prueba:
    def __init__(self, name, years):
        self.name = name
        self.years = years

    def printer(self):
        print(self.name, self.years)

class prueba2:
    def __init__(self):
        self

    def printer2(self):
        print(self)

p1 = prueba("Juan", 33)
p1.printer()
p2 = prueba2()
p2.printer2()
