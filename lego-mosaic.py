#Algorithms for determining dominant color of tile inspired by http://charlesleifer.com/blog/using-python-and-k-means-to-find-the-dominant-colors-in-images/
import sys, random, argparse, math
from PIL import Image
from legoColors import lColors
from collections import namedtuple
from colorTesting import colorz

Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

def get_points(imgTile, tileSize):
    points = []
    for count, color in imgTile.getcolors(tileSize ** 2):
        points.append(Point(color, 1, count))

    return points

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))
rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

def findDominant(imgTile, tileSize, n=1):
    points = get_points(imgTile, tileSize)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    print(list(rgbs))
    return map(rtoh, rgbs)

def euclidean(p1, p2):
    return math.sqrt(sum([(p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)]))

def calculate_center(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)

def kmeans(points, k, min_diff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while 1:
        plists = [[] for i in range(k)]

        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break
    return clusters

def closestColor(tileRGB):
    minDifference = 1000 #255*3 is the max difference between two colors
    colorMatch = 0

    for key,val in lColors.items():
        #color weighting used
        colorDifference = math.sqrt((((val[0]-tileRGB[0]) * .3)**2) + ((val[1]-tileRGB[1]) * .59)**2) + ((val[2]-tileRGB[2]) * .11)**2
        if(colorDifference < minDifference):
            minDifference = colorDifference
            colorMatch = key

    return colorMatch



#hard code in the columns for now - should be entered by user
cols = 50

sourceImage = Image.open("test-image.jpg")

imageW, imageH = sourceImage.size[0], sourceImage.size[1]
print("Image height: " + str(imageH))

#tiles are square (lego pieces)
tileSize = int(imageW/cols)

#determine how many vertical tiles can fit in image
croppedH = math.floor(imageH/tileSize) * tileSize
print("Cropped height: " + str(croppedH))

baseImage = None

if croppedH != imageH:
    #crops the height towards the center if the image height and cropped height do not match
    area = (0, (imageH - croppedH) / 2,imageW, (imageH + croppedH) / 2)
    baseImage = sourceImage.crop(area)
    imageH = int(sourceImage.size[1])
else:
    baseImage = sourceImage

#calculate number of rows
rows = int(imageH/tileSize)



tileColors = []
for i in range(rows):
    rowColorList = []

    y1 = int(i * tileSize)
    y2 = int((i + 1) * tileSize)
    if i == rows - 1:
        y2 = imageH

    for j in range(cols):
        x1 = int(j * tileSize)
        x2 = int((j + 1) * tileSize)
        if j == rows - 1:
            x2 = imageW

        #print(str(tileSize))
        currTile = baseImage.crop((x1, y1, x2, y2))
        #domColor = findDominant(currTile, tileSize)
        print(list(colorz(currTile)))

        #print(list(domColor))




#TODO
#Create 2d Array of color keys
#Create dictionary of lego id color to lego brick code
#Create a count of each color (number of pieces needed) and tie to brick code
#Create image from a 2d array of lego color ids
#Create a manual for creating lego color ids?

print(lColors[1][0])


baseImage.show()


