#!/usr/bin/env python3
import time
import sys


def ft_progress(list):
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
        sys.stdout.write('\r')
        sys.stdout.write("ETA: %.2fs [%3d%%] |%s%-*.*s%s| %*d/%d | elapsed time %.2fs" % (eta, per + 1, color, barsize, barsize, "█"*(bar + 1), "\033[0m", length, i + 1, mval, t))
        sys.stdout.flush()
        yield i

if __name__ == "__main__":
    listy = range(1000)
    ret = 0
    for elem in ft_progress(listy):
        ret += (elem + 3) % 5
        time.sleep(0.005)
    print()
    print(ret)
    # listy = range(3333)
    # ret = 0
    # for elem in ft_progress(listy):
    #     ret += elem
    #     time.sleep(0.005)
    # print()
    # print(ret) 
