#!/usr/bin/env python3

import sys
import exiftool

def getExif(image_name):
    with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(image_name)
    for dic in metadata:
        print("\n{:*>80s}".format("*"))
        print("* METADATOS DEL ARCHIVO {:>>53s} *".format(dic['SourceFile'].upper()))
        print("{:*>80s}".format("*"))
        for key in dic:
            print("{:-<40s}> {}".format(key, dic[key]))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        getExif(sys.argv[1:])
    else:
        print("you must provide at least an image")
