#!/usr/bin/env python3
t = (1971, 2, 28, 18, 35)

if (len(t) == 5):
	print("{:>02}/{:>02}/{:>04} {:>02}:{:>2}".format(t[2], t[1], t[0], t[3], t[4]))
else:
    print("Tuple needs at least five parameters.")
