import sys, random, argparse, math
from PIL import Image
from legoColors import lColors

def closestColor(tileRGB):
    minDifference = 1000 #255*3 is the max difference between two colors
    colorMatch = 0

    for key,val in lColors.items():
        #color weighting used
        colorDifference = math.sqrt((((val[0]-tileRGB[0]) * .3)**2) + ((val[1]-tileRGB[1]) * .59)**2) + ((val[2]-tileRGB[2]) * .11)**2
        if(colorDifference < minDifference):
            minDifference = colorDifference
            colorMatch = key

    return key



#hard code in the columns for now - should be entered by user
cols = 50

sourceImage = Image.open("test-image.jpg")

imageW, imageH = sourceImage.size[0], sourceImage.size[1]
print("Image height: " + str(imageH))

#tiles are square (lego pieces)
tileW = tileH = imageW/cols

#determine how many vertical tiles can fit in image
croppedH = math.floor(imageH/tileH) * tileH
print("Cropped height: " + str(croppedH))

baseImage = None

if croppedH != imageH:
    #crops the height towards the center if the image height and cropped height do not match
    area = (0, (imageH - croppedH) / 2,imageW, (imageH + croppedH) / 2)
    baseImage = sourceImage.crop(area)
    imageH = sourceImage.size[1]
else:
    baseImage = sourceImage

#calculate number of rows
rows = int(imageH/tileH)

tileColors = []
for i in range(rows):
    rowColorList = []

    y1 = int(i * tileH)
    y2 = int((i + 1) * tileH)
    if i == rows - 1:
        y2 = imageH

    for j in range(cols):
        x1 = int(j * tileW)
        x2 = int((j + 1) * tileW)
        if j == rows - 1:
            x2 = imageW

        currTile = baseImage.crop((x1, y1, x2, y2))
        #avgColor =




#TODO
#Create 2d Array of color keys
#Create dictionary of lego id color to lego brick code
#Create a count of each color (number of pieces needed) and tie to brick code
#Create image from a 2d array of lego color ids
#Create a manual for creating lego color ids?

print(lColors[1][0])


baseImage.show()


