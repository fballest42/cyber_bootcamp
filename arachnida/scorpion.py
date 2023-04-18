#!/usr/bin/env python3


import sys
import os
import io
import piexif
from PIL import Image, ExifTags

def getExif(image_name):
    file_name, file_ext = os.path.splitext(image_name)
    file_ext = file_ext.lstrip('.')
    img = Image.open(image_name)
    # if file_ext == "png":
    #     img_exif = {"EXIF": piexif.load(img.info.get('png'))}
    if file_ext in "jpg":
        img_exif = img.getexif()
    # elif file_ext == "jpeg":
    #     img_exif = piexif.load(img.info)
    if img_exif is None:
        print('Sorry, image has no exif data.')
    else:
        for key, val in img_exif.items():
            if key in ExifTags.TAGS:
                print(f'{ExifTags.TAGS[key]}: {val}')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for ar in sys.argv[1:]:
            getExif(ar)
    else:
        print("you must provide at least an image")
