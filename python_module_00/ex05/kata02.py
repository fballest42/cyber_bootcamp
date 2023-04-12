#!/usr/bin/env python3
t = (3, 30, 2019, 9, 25)

if (len(t) >= 5):
	print("{:>02}/{:>02}/{} {:>02}:{:>2}" 
    	.format(t[0], t[1], t[2], t[3], t[4]))
else:
    print("Tuple needs at least five parameters.")
