# import the necessary packages
from skimage.measure import compare_ssim as ssim
import cv2, os
import numpy as np
from subImageSearch import find_image
from PIL import Image


def RemoveTempFolders(someList):
    for item in someList:
        if item[0] == ".":
            someList.remove(item)
        if item == "normalised.jpg":
            someList.remove(item)

    return someList

def imageCompare(imageA, imageB):
    if imageA.shape != imageB.shape:
        return 0
    try:
        return ssim(imageA, imageB, multichannel=True)
    except:
        return 0


websites = os.listdir("components")
imageMatrix = []
websites = RemoveTempFolders(websites)

for website in ['faa-gov']: #in websites:
    classes = os.listdir("components/"+website)
    classes = RemoveTempFolders(classes)

    for cls in classes:
        varients = os.listdir("components/"+website+"/"+cls)
        varients = RemoveTempFolders(varients)

        for varient in ["/1","/2"]:
            reference = cv2.imread ("components/"+website+"/"+cls+"/0/normalised.jpg",0)
            reference_mask = cv2.imread ("components/"+website+"/"+cls+"/0/normalised.jpg")

            components = os.listdir("components/"+website+"/"+cls+"/"+varient)
            components = RemoveTempFolders(components)

            notFound=0
            found = 0

            output = open("scores/" + website + "_" + cls + "_varient" + varient[-1] + ".csv", "a+")

            for c in components:
                comp = cv2.imread ("components/"+website+"/"+cls+"/"+varient+"/"+c,0)
                result = find_image (reference,comp)
                if result == False:
                    cropped = comp [50:(comp.shape[0]-50),50:(comp.shape[1]-50)]
                    cv2.imwrite('temp.jpg', cropped)
                    cropped = cv2.imread ('temp.jpg',0)
                    result = find_image (reference,cropped)
                    print (result)
                    notFound+=1
                elif result != False:
                    print (True)
                    found +=1
                    cv2.rectangle(reference_mask, (result[1],result[0]), (result[1]+comp.shape[1], result[0]+comp.shape[0]), (255,0,0), 2)


                output.write (("original: "+c) + "," + ("matched: "+ str(result)))
                output.write("\n")

            cv2.imwrite("components/"+website+"/"+cls+"/"+varient+"/ref_mask.jpg", reference_mask)
            print (notFound,found)
