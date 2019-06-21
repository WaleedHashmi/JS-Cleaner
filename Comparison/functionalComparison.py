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
    return (img)

def imageCompare(one, two):

    # img1 is the core image
    # img2 will be broken down into components
    # then the components will be checked against img1

    img1 = cv2.imread (one)
    img2 = cv2.imread (two)

    # print ("Normalising Image 1:" end = "\t")
    # img1 = normalise(img1)
    # print ("Done")

    print ("Normalising Image 2:", end = "")
    img2 = normalise(img2)
    print ("Done")

    print (img2[0])

    # cv2.imshow('image',img2)
    # a = input ("close?")
    # cv2.destroyAllWindows()

    cv2.imwrite( "img2.jpg", img2 )





imageCompare ("ss/faa-gov/0/screenshotnav-class-hNav.png","ss/faa-gov/1/screenshotnav-class-hNav.png")
