#!/usr/bin/env python3
""" Vector tests

"""
from random import randint

def generator(text, sep=None, option=None):
    """A generator that splits text according to 'sep' and 'option', and yields the results"""
    if not isinstance(text, str) or option not in [None, "shuffle", "unique", "ordered"] or len(sep) == 0:
        yield "ERROR"
    else:
        if option is None:
            listy = text.split(sep)
        elif option == "shuffle":
            listy = []
            tmp = list(text.split(sep))
            while len(tmp) > 0 and tmp[0] != []:
                a = randint(0, len(tmp) - 1)
                listy.append(tmp[a])
                tmp.remove(tmp[a])
        elif option == "unique":
            listy = list(dict.fromkeys(text.split(sep)))
        elif option == "ordered":
            listy = sorted(text.split(sep))
        for item in listy:
            yield item 

# if __name__ == '__main__':
#     TEXT = "Le Lorem Ipsum est simplement du faux texte Le Lorem Ipsum est ."

#     print("Regular split :")
#     for i in generator(TEXT, sep=" "):
#         print(i)
#     print()

#     print("Regular split with sep 'Ipsum':")
#     for i in generator(TEXT, sep="Ipsum"):
#         print(i)
#     print()

#     print("Regular Split with sep 'a':")
#     for i in generator(TEXT, sep="a"):
#         print(i)
#     print()

#     print("Shuffle split :")
#     for i in generator(TEXT, sep=" ", option="shuffle"):
#         print(i)
#     print()

#     print("Unique split :")
#     for i in generator(TEXT, sep=" ", option="unique"):
#         print(i)
#     print()

#     print("Ordered split :")
#     for i in generator(TEXT, sep=" ", option="ordered"):
#         print(i)
#     print()

#     print("Invalid option :")
#     for i in generator(TEXT, sep=" ", option=""):
#         print(i)
#     print()

#     print("Invalid split :")
#     for i in generator(6, sep=" "):
#         print(i)
#     print()

#     print("Invalid separator 1:", sep="")
#     for i in generator(TEXT,  sep=""):
#         print(i)
#     print()
