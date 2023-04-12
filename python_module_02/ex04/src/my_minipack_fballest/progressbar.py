""" A progress bar funtion for my_minipack """

import time
import sys

def progressbar(list):
    start = time.time()
    mval = len(list)
    length = len(str(max(list)))
    eta = 0
    barsize = 40
    for i in list:
        per = i / mval * 100
        bar = int(i / mval * barsize)
        t = time.time() - start
        if not per == 0:
            eta = t / per * 100
        if per < 70:
            color = "\033[31m"
        elif per < 95:
            color = "\033[33m" 
        else:
            color = "\033[32m"
        sys.stdout.write("ETA: %.2fs [%3d%%] |%s%-*.*s%s| %*d/%d | elapsed time %.2fs %s" % (eta, per + 1, color, barsize, barsize, "█"*(bar + 1), "\033[0m", length, i + 1, mval, t, "\r"))
        sys.stdout.flush()
        yield i
