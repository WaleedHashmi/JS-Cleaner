#####
#####  1. Aim:
#####           a/ Normalise -> Set background as 0 and everything else in their primary colors
#####           b/ find disconnected components
#####

# import the necessary packages
import cv2, os
import numpy as np
import skimage
from matplotlib import pyplot as plt


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


def breakIntoComponents (img = "ss/faa-gov/0/screenshotnav-class-hNav.png"):
    img0 = cv2.imread (img)

    print ("Normalising Image: \t", img)
    img0_norm = normalise(img0)

    img0_dil = cv2.dilate (img0_norm,np.ones((15, 15)))

    labels, markers = cv2.connectedComponents(img0_dil.astype(np.uint8),connectivity=8)

    img0_mask = skimage.measure.label(markers, background = 0).flatten()

    for i in range (labels):
        component = np.where(img0_mask==i)[0]
        print ("Saving Comp", i)
        saveComponent(component,markers.shape,i)

def removeLeadingZeros(mask):
    for i in range (len(mask)):
        if np.count_nonzero (mask[0]) == 0:
            mask = np.delete(mask, 0,0)
        else:
            continue
    return mask

def removeTailingZeros(mask):
    for i in range (len(mask)-1,0,-1):
        if np.count_nonzero (mask[len(mask)-1]) == 0:
            mask = np.delete(mask,len(mask)-1,0)
        else:
            continue
    return mask

def crop (mask):
    print ("Cropping")
    mask = removeLeadingZeros(mask)
    mask = removeTailingZeros(mask)
    mask = np.transpose(mask)
    mask = removeLeadingZeros(mask)
    mask = removeTailingZeros(mask)
    mask = np.transpose(mask)
    return mask

def saveComponent (comp,shape,label):
    sizeForFlatten = shape[0]*shape[1]

    mask = np.zeros(sizeForFlatten)
    for c in comp:
        mask[c] = 1

    # mask = cv2.erode(mask, np.ones((50, 50)))

    mask = mask.reshape(shape[0],shape[1])

    mask = crop(mask)

    if len(mask.flatten()) < 20:
        print ("component too small")
    else:
        print ("writing image")

        ##### Converting to three channel 3d array to save with cv2
        mask_write = mask.tolist()

        for i in range(len(mask_write)):
            for j in range(len(mask_write[0])):
                if mask_write[i][j] == 1:
                    mask_write[i][j] = [255,255,255]
                else:
                    mask_write[i][j] = [0,0,0]

        mask_write = np.array (mask_write)

        cv2.imwrite("1/"+str(label)+".jpg", mask_write)



breakIntoComponents("ss/faa-gov/0/screenshotnav-class-hNav.png")
