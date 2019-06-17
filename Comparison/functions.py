def imageCompare(img1,img2):
    img1 = cv2.imread(img1)
    img2 = cv2.imread(img2)

    diff = cv2.subtract(img1,img2)
    r,g,b = cv2.split(diff)

    if cv2.countNonZero(r)==cv2.countNonZero(g)==cv2.countNonZero(b)==0:
        return True
    else:
        return False
