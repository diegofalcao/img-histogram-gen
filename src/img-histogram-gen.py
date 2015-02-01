import sys
from PIL import Image
from PIL import ImageDraw


# Generates K Folds with FAILURE and PASS instances.
#def generateKFolds(numberOfFolds, numberOfPassInstancesPerFold, passInstances,
#                   numberOfFailureInstancesPerFold, failureInstances):

# Combines folds to generate the training and testing sets
#def generateTrainingAndTestingSetsCombiningFolds(folds, header, trainingPrefixName, testingPrefixName, verbose):

# This script generates folds using StratifiedKFold. It means that
# it preserves the class distribution of the original file in the generated
# folds.
def main(argv):

    # if len(sys.argv) < 5 or len(sys.argv) > 5:
    #     print "This script generates folds using StratifiedKFold. It means that it preserves the class distribution"
    #     print "of the original file in the generated folds."
    #     print "\nCross-validation Stratifield KFold Generator usage:"
    #     print sys.argv[0], '<csv_file_name> <KFold> <training_output_prefix_name> <testing_output_prefix_name>'
    #     sys.exit()

    im = Image.open('../lena.jpg')

    im256 = im.convert('P', palette=Image.ADAPTIVE, colors=255)

    width = im.size[0]
    height = im.size[1]

    draw = ImageDraw.Draw(im256)

    imgWBorder = width * 0.11
    imgHBorder = height * 0.11

    draw.line((width/2, 0, width/2, imgWBorder), fill=255) # UP
    draw.line((0, height/2, imgWBorder, height/2), fill=255) # LEFT
    draw.line((width - imgWBorder, height/2, width, height/2), fill=255) # RIGHT
    draw.line((width/2, height - imgHBorder, width/2, height), fill=255) # BOTTOM

    space = 14.2

    yleft = 0
    yright = space

    for i in range(0, 37):
        xleft = 0
        xright = space

        for j in range(0, 37):
            draw.rectangle((xleft, yleft, xright, yright), outline=0)

            xleft = xleft + space
            xright = xright + space

        yleft = yleft + space
        yright = yright + space

    draw.rectangle((imgWBorder, imgHBorder, width - imgWBorder, height - imgHBorder), outline=255)

    im256.convert('RGB').save('../lena256.jpg')
if __name__ == '__main__':
    main(sys.argv)