import cv2, os, random
import numpy as np
from copy import deepcopy

for img in os.listdir("images/orig"):
    image = cv2.imread("images/orig/" + img)
    res = deepcopy(image)

    # for x in range(image.shape[0]):
    #     for y in range(image.shape[1]):
    #         for z in range(image.shape[2]):
    #             temp = random.randint(0, 50)
    #             if res[x][y][z] + temp > 255:
    #                 res[x][y][z] -= temp
    #             res[x][y][z] += temp

    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            for z in range(image.shape[2]):
                if random.random() < 0.1:
                    res[x][y][z] =  random.randint(0, 255)

    cv2.imwrite("images/attack/random/" + img, res)
    print("Done with " + img)