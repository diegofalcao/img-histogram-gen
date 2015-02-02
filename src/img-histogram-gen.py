import sys
import math
import collections

from PIL import Image
from PIL import ImageDraw

# It returns the region of an specific point considering that the image was
# divided into 5 regions.
def getRegion(width, height, x, y):
    imgWBorder = width * 0.10
    imgHBorder = height * 0.10

    if (x <= (width / 2) and y <= imgHBorder) or (x <= imgWBorder and y <= height / 2):
        return "A"

    if (x > (width / 2) and y <= imgHBorder) or (x > (width - imgWBorder) and y <= height / 2):
        return "B"

    if (x <= (width / 2) and y > (height - imgHBorder)) or (x <= imgWBorder and y > height / 2):
        return "D"

    if (x > (width / 2) and y > (height - imgHBorder)) or (x > (width - imgWBorder) and y > height / 2):
        return "E"

    # It belongs to the square in the center of the image
    return "C"

# This program breaks the image into 1296 blocks and 5 regions and generates histograms to each block. After that, each
# histogram block becomes words that can be used as terms in a vector model. So that, it can be used together with a
# vector model to do CBIR (Content Based Information Retrieval).
def main(argv):

    # if len(sys.argv) < 2 or len(sys.argv) > 2:
    #     print "This program breaks the image into 1296 blocks and 5 regions and generates histograms to each block. "
    #     print "After that, each histogram block becomes words that can be used as terms in a vector model. So that, "
    #     print "it can be used together with a vector model to do CBIR (Content Based Information Retrieval)."
    #     print "\nImage Histogram Generator usage:"
    #     print sys.argv[0], '<image_path>'
    #     sys.exit()

    #im = sys.argv[1]
    im = Image.open('../lena.jpg')

    im256 = im.convert('P', palette=Image.ADAPTIVE, colors=255)

    width = im.size[0]
    height = im.size[1]

    draw = ImageDraw.Draw(im256)

    print getRegion(width, height, 52, 196)

    imgWBorder = width * 0.11
    imgHBorder = height * 0.11

    draw.line((width/2, 0, width/2, imgHBorder), fill=255) # UP
    draw.line((0, height/2, imgWBorder, height/2), fill=255) # LEFT
    draw.line((width - imgWBorder, height/2, width, height/2), fill=255) # RIGHT
    draw.line((width/2, height - imgHBorder, width/2, height), fill=255) # BOTTOM

    NUMBER_OF_BLOCKS = 1296

    blockSize = math.sqrt((width * height) / NUMBER_OF_BLOCKS)

    yleft = 0
    yright = blockSize

    for i in range(0, 37):
        xleft = 0
        xright = blockSize

        for j in range(0, 37):
            draw.rectangle((xleft, yleft, xright, yright), outline=0)

            # tmpImg = im256.crop((xleft, yleft, xright, yright))
            # tmpHistogram = tmpImg.histogram()
            # tmpSortedHistogram = collections.OrderedDict(sorted(tmpHistogram.items(), reverse=True))
            # len95percent = len(sortedHistogram) * 0.95

            xleft = xleft + blockSize
            xright = xright + blockSize

        yleft = yleft + blockSize
        yright = yright + blockSize

    draw.rectangle((imgWBorder, imgHBorder, width - imgWBorder, height - imgHBorder), outline=255)

    im256.convert('RGB').save('../lena256.jpg')
if __name__ == '__main__':
    main(sys.argv)