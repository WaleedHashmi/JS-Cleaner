# import the necessary packages
from skimage.measure import compare_ssim as ssim
import cv2, os
import numpy as np

def RemoveTempFolders(someList):
    for item in someList:
        if item[0] == ".":
            someList.remove(item)
    return someList

def imageCompare(imageA, imageB):
    if imageA.shape != imageB.shape:
        return 0
    try:
        return ssim(imageA, imageB, multichannel=True)
    except:
        return 0


def score(website,cls,imageMatrix):
    root = "components/" + website + "/" + cls + "/"

    for var in [1]:
        output = open("scores/" + website + "_" + cls + "varient_" + str(var) + ".csv", "a+")

        for img0 in imageMatrix[0]:
            img0_ = cv2.imread(root + "0/" + img0)
            highest = [0,"None"]
            if highest[0]==1: continue

            for img1 in imageMatrix[var]:
                img1_ = cv2.imread(root + str(var) + "/" + img1)
                s = imageCompare(img0_,img1_)

                if s>highest[0]:
                    highest = [s,img1]

            # print (highest)


            output.write (("original: "+img0) + "," + ("matched: "+highest[1])+ "," +("score: "+str(highest[0])))
            output.write("\n")


websites = os.listdir("components")
imageMatrix = []
websites = RemoveTempFolders(websites)

for website in websites:
    classes = os.listdir("components/"+website)
    classes = RemoveTempFolders(classes)

    for cls in classes:
        varients = os.listdir("components/"+website+"/"+cls)
        varients = RemoveTempFolders(varients)

        imageMatrix = []

        for varient in ["/0","/1","/2"]:
            images = os.listdir("components/"+website+"/"+cls+varient)
            images = RemoveTempFolders(images)
            imageMatrix.append(images)

        print ("scoring", cls)
        score (website, cls, imageMatrix)
