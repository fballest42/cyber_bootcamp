#!/usr/bin/env python3

""" TinyStatytician class

"""

import numpy as np
import sys
import math

class TinyStatistician:
  """ A class that include some statyticians methods """
  def __init__(self):
    pass
    @staticmethod          def mean(x):
    """ Method of the class TinyStatytician that calculate
        the mean of a list or matrix """
    if x == None or len(x) == 0:
      return None
    try:
      mean = 0
      for i in x:
        mean += i
      return mean / len(x)
    except Exception as exc:
      print(exc)
      return None

  @staticmethod   def median(x):
    """Method of the class TinyStatytician that calculate
       the median of a list or matrix """
    return TinyStatistician.percentile(x, 50)

  @staticmethod
  def quantile(x):
    return [TinyStatistician.percentile(x, 25), TinyStatistician.percentile(x,75)]

  @staticmethod
  def percentile(x, per):
    ln = len(x)
    if x == None or ln == 0:
      return None
    try:
      sorted_x = np.sort(x)
      return sorted_x[math.ceil((ln * per) / 100) - 1]
    except Exception as exc:
      print(exc)
      return None

  @staticmethod
  def var(x):
    if x == None or len(x) == 0:
        return None
    try:
      mean = TinyStatistician.mean(x)
      var = 0
      for elem in x:
        var += (elem - mean) ** 2
        return var / len(x)
    except Exception as exc:
      print(exc)
      return None

  @staticmethod
  def std(x):
    if x == None or len(x) == 0:
      return None
    try:
      var = TinyStatistician.var(x) ** 0.5
      return var
    except Exception as exc:
      print(exc)
      return None

ts = TinyStatistician()
lst1 = ["a", "b", "c"]
lst2 = [1.0, 2.0, 3.0]
lst3 = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
lst4 = [17, 56, 38, 19, 11, 10, 8, 41]
lst5 = [57, 47, 37, 27, 17, 13, 1]
lst6 = [1, 3, 501, 270, 69]

LST = [lst1, lst2, lst3, lst4, lst5, lst6]
for l in LST:
  print("MEAN =", ts.mean(l))
  print("MEDIAN =", ts.median(l))
  print("PERCENTILE =", ts.percentile(l, 50))
  print("QUANTILE =", ts.quantile(l))
  print("VAR =", ts.var(l))
  print("STD =", ts.std(l))
  print()
