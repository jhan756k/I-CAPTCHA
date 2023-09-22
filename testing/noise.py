import cv2, os, random
import numpy as np
from copy import deepcopy

for img in os.listdir("images/orig"):
    image = cv2.imread("images/orig/" + img)
    res = deepcopy(image)

    # Salt and pepper noise
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            for z in range(image.shape[2]):
                if random.random() < 0.1:
                    res[x][y][z] =  random.randint(0, 255)
    cv2.imwrite("images/attack/random/" + img, res)

    # Gaussian noise
    # mean = 0
    # var = 1000
    # sigma = var ** 0.5
    # gauss = np.random.normal(mean, sigma, (image.shape[0], image.shape[1], image.shape[2]))
    # gauss = gauss.reshape(image.shape[0], image.shape[1], image.shape[2])
    # res = res + gauss
    # cv2.imwrite("images/attack/gaussian/" + img, res)

    # Shot noise
    # for x in range(image.shape[0]):
    #     for y in range(image.shape[1]):
    #         for z in range(image.shape[2]):
    #             if random.random() < 0.1:
    #                 res[x][y][z] = 0
    # cv2.imwrite("images/attack/shot/" + img, res)

    print("Done with " + img)