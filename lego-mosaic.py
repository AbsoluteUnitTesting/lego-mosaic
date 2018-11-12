import sys, random, argparse, math
from PIL import Image
#hard code in the columns for now - should be entered by user
cols = 50

sourceImage = Image.open("test-image.jpg")

imageW, imageH = sourceImage.size[0], sourceImage.size[1]
print("Image height: " + str(imageH))

tileW = tileH = imageW/cols
#determine how many vertical tiles can fit in image
croppedH = math.floor(imageH/tileH) * tileH
print("Cropped height: " + str(croppedH))

baseImage = None

if croppedH != imageH:
    #crops the height towards the center if the image height and cropped height do not match
    area = (0, (imageH - croppedH) / 2,imageW, (imageH + croppedH) / 2)
    baseImage = sourceImage.crop(area)
else:
    baseImage = sourceImage

baseImage.show()
