import cv2 as cv
import numpy as np


def detect_collage(pil_image):
    # a factor for middle search
    bf = 4
    cannyThres1 = 250
    cannyThres2 = 400

    src = cv.cvtColor(np.array(pil_image), cv.COLOR_RGB2GRAY)

    height, width = src.shape
    thres = int(min(width, height) / 3)

    dst = cv.Canny(src, cannyThres1, cannyThres2, None, 3)

    lines = cv.HoughLines(dst, 1, np.pi / 2, thres, None, 0, 0)

    thetaDlist = []
    rholist = []
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            thetaD = int(180 * theta / np.pi)
            if (((thetaD == 0) & ((rho < (bf - 1) * (width / bf)) & (rho > (width / bf)))) | (
                    (thetaD == 90) & ((rho < (bf - 1) * (height / bf)) & (rho > (height / bf))))):
                thetaDlist.append(thetaD)
                rholist.append(rho)

    numLines = len(thetaDlist)
    if numLines > 1:
        return True

    elif numLines == 1:
        rhot = rholist[0]
        thetat = thetaDlist[0]
        if (((thetat == 0) & ((rhot < (2 * bf - 3) * (width / (2 * bf))) & (rhot > 3 * (width / (2 * bf))))) | (
                (thetat == 90) & ((rhot < (2 * bf - 3) * (height / (2 * bf))) & (rhot > 3 * (height / (2 * bf)))))):
            return True
        else:
            return False
    else:
        return False