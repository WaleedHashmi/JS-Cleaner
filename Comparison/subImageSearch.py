import cv2, os
import numpy as np

def find_image(im, tpl):
    im = np.atleast_3d(im)
    tpl = np.atleast_3d(tpl)
    H, W, D = im.shape[:3]
    h, w = tpl.shape[:2]

    # Integral image and template sum per channel
    sat = im.cumsum(1).cumsum(0)
    tplsum = np.array([tpl[:, :, i].sum() for i in range(D)])

    # Calculate lookup table for all the possible windows
    iA, iB, iC, iD = sat[:-h, :-w], sat[:-h, w:], sat[h:, :-w], sat[h:, w:]
    lookup = iD - iB - iC + iA
    # Possible matches
    possible_match = np.where(np.logical_and.reduce([lookup[..., i] == tplsum[i] for i in range(D)]))

    # Find exact match
    for y, x in zip(*possible_match):
        if np.all(im[y+1:y+h+1, x+1:x+w+1] == tpl):
            return (y+1, x+1)

    return False 
    raise Exception("Image not found")


# img0 = cv2.imread ("/Users/waleed/Desktop/JS-Reseach/Comparison/ss/faa-gov/2/screenshotdiv-id-faaModal.png")
# img1 = cv2.imread ("/Users/waleed/Desktop/screenshoth2-class-visuallyHidden.png")
#
# print (img0)
# print (img1)
#
# result = find_image (img0,img1)
# print (result)
# # cv2.rectangle(img0, (result[0],result[1]), (result[0]+img1.shape[0], result[1]+img1.shape[1]), (255,0,0), 2)
#
# cv2.rectangle(img0, (result[1],result[0]),(result[1]+img1.shape[1],result[0]+img1.shape[0]) , (255,0,0), 2)
#
# cv2.imwrite("1.jpg", img0)
