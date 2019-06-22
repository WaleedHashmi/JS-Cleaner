#####
#####  1. Aim:
#####           a/ Normalise -> Set background as 0 and everything else in their primary colors
#####           b/ find disconnected components
#####

# import the necessary packages
import cv2, os
import numpy as np

def RemoveTempFolders(someList):
    for item in someList:
        if item[0] == ".":
            someList.remove(item)
    return someList

def normalise(img, background = [255,255,255]):
    # change background to black(0)
    # transorm the rest of the pixels to
    # monotone for easier comparison later

    black = 0
    white = 255
    k = 0
    l=0
    for i in range(len(img)):
        for j in range(len(img[0])):
            if list(img[i][j]) == background:
                img[i][j] = black
                l+=1
            else:
                img[i][j] = white
                k+=1
    print (k,l)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def imageCompare(one, two):
    # img1 is the core image
    # img2 will be broken down into components
    # then the components will be checked against img1

    img1 = cv2.imread (one)
    img2 = cv2.imread (two)

    # print ("Normalising Image 1:" end = "\t")
    # img1 = normalise(img1)
    # print ("Done")

    print ("Normalising Image 2")
    img2Mask = normalise(img2)
    cv2.imwrite( "img2mask.jpg", img2)

    # print ("Dilating Image 2")
    # img2Mask_dilated = cv2.dilate(img2Mask, kernel = np.ones((5,5),np.uint8))
    # cv2.imwrite( "img2Mask_dilated.jpg", img2Mask_dilated)

    connectivity = 4
    output = cv2.connectedComponentsWithStats(img2Mask,connectivity)
    nLabels = output[0]
    labels = output[1]
    stats = output[2]
    centroids = output[3]

    print (nLabels)
    print (labels)
    print (centroids)
    print (stats)

    # print (output)

    # cv2.imshow('image',img2)
    # a = input ("close?")
    # cv2.destroyAllWindows()

    cv2.imwrite( "img2mask.jpg", img2 )





imageCompare ("ss/faa-gov/0/screenshotnav-class-hNav.png","ss/faa-gov/1/screenshotnav-class-hNav.png")
