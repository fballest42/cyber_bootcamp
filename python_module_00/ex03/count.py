#!/usr/bin/env python3
import sys
import string

def text_analyzer(*args):
    """This function counts the number of upper characters, lower characters,
        punctuation and spaces in a given text"""
    if len(args) > 1 or not isinstance(args[0], str):
        print("ERROR")
        return
    elif (len(args) == 0):
        print("What is the text to analyse?")
        print(">> ", end="")
        sys.stdout.flush()
        st = sys.stdin.readline()[0:-1]
    else:
        st = args[0]
    upper = 0
    lower = 0
    punct = 0
    space = 0
    for i in range(len(st)):
        if st[i].isupper():
            upper += 1
        elif st[i].islower():
            lower += 1
        elif st[i] in (' ', '\t', '\r', '\v', '\f'):
            space += 1
        elif st[i] in (string.punctuation):
            punct += 1
    print("The text contains {} characters:".format(len(st)))
    print("- {} upper letters".format(upper))
    print("- {} lower letters".format(lower))
    print("- {} punctuation marks".format(punct))
    print("- {} spaces".format(space))

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("ERROR")
    elif len(sys.argv) == 2:
        text_analyzer(sys.argv[1])
    else:
        print("What is the text to analyse?")
        print(">> ", end="")
        sys.stdout.flush()
        str = sys.stdin.readline()[0:-1]
        text_analyzer(str)
