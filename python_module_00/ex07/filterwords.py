#!/usr/bin/env python3
import sys
import string


if (len(sys.argv) == 3):
    try:
        length = int(sys.argv[2])
    except ValueError:
        print("Invalid length parameter.")
        sys.exit()
elif (len(sys.argv) < 3):
    print("Too few arguments.")
    sys.exit()
elif (len(sys.argv) > 3):
    print("Too many arguments.")
    sys.exit()

s = sys.argv[1].translate(str.maketrans('', '', string.punctuation))
t = [word for word in s.split(' ') if len(word) > length]
print(t)

