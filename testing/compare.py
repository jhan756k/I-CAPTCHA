import cv2, os, random
import numpy as np
from copy import deepcopy

for img in os.listdir("images/orig"):
    orig = cv2.imread("images/orig/" + img)
    attack = cv2.imread("images/attack/random/" + img)
    res = deepcopy(orig)

    for x in range(orig.shape[0]):
        for y in range(orig.shape[1]):
            for z in range(orig.shape[2]):
                if orig[x][y][z] != attack[x][y][z]:
                    res[x][y][z] = 255

    cv2.imwrite("images/attack/compare/" + img, res)
    print("Done with " + img)

    # calculate difference ratio

    # Test denoising methods

