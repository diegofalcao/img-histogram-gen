import sys
import math
import operator

from PIL import Image

# This represents the space between the boundary of the image and the square region
# in the center of the image.
BORDER_PERCENT = 0.11

# Number of blocks to crop the image.
NUMBER_OF_BLOCKS = 1296

# It returns the region of an specific point considering that the image was
# divided into 5 regions.
def getRegion(width, height, x, y):
    imgWBorder = width * BORDER_PERCENT
    imgHBorder = height * BORDER_PERCENT

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
# Example:
#  ___________
# |A  __|__  B|
# |__|C    |__|
# |D |_____| E|
# |_____|_____|
#
def main(argv):

    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print "This program breaks the image into 1296 blocks and 5 regions and generates histograms to each block. "
        print "After that, each histogram block becomes words that can be used as terms in a vector model. So that, "
        print "it can be used together with a vector model to do CBIR (Content Based Information Retrieval)."
        print "\nImage Histogram Generator usage:"
        print sys.argv[0], '<image_path>'
        sys.exit()

    imagePath = sys.argv[1]
    
    try:    
        im = Image.open(imagePath)
    except:
        sys.exit() # The image was not found or is corrupted.

    # Decreasing the quantization of the image to 256 colors
    img256 = im.convert('P', palette=Image.ADAPTIVE, colors=255)

    imgWidth = im.size[0]
    imgHeight = im.size[1]

    blockSize = math.sqrt((imgWidth * imgHeight) / NUMBER_OF_BLOCKS)

    yleft = 0
    yright = blockSize

    blockWords = []

    # 36x36 = 1296 blocks
    for i in range(0, 36):
        xleft = 0
        xright = blockSize

        for j in range(0, 36):
            tmpImg = img256.transform((36, 36), Image.EXTENT, (xleft, yleft, xright, yright))
            tmpHistogram = tmpImg.histogram() #Generates the histogram to the current block

            tmpDictHistogram = {}

            for key, value in enumerate(tmpHistogram):
                tmpDictHistogram[key] = value

            tmpSortedHistogram = sorted(tmpDictHistogram.items(), key = operator.itemgetter(1), reverse=True)

            len95percent = int(len(tmpSortedHistogram) * 0.95)

            blockWord = ''

            x = 0

            for value in tmpSortedHistogram:
                if x == len95percent:
                    break

                blockWord = blockWord + 'x' + str(value[0])

                x = x + 1

            blockWord =  getRegion(imgWidth, imgHeight, xright, yright) + blockWord

            blockWords.append(blockWord)

            xleft = xleft + blockSize
            xright = xright + blockSize

        yleft = yleft + blockSize
        yright = yright + blockSize

    print ' '.join(blockWords)

    sys.exit()

if __name__ == '__main__':
    main(sys.argv)