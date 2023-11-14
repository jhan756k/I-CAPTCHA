import cv2, os, random
import numpy as np
from copy import deepcopy
from ultralytics import YOLO

model = YOLO('yolov8m.pt')

for img in os.listdir("images/orig"):
    image = cv2.imread("images/orig/" + img)
    results = model.predict(image)
    result = results[0]
    detected = []

    for box in result.boxes:
        class_id = result.names[box.cls[0].item()]
        if class_id not in "motorcycles":
            continue
        cords = box.xyxy[0].tolist()
        detected.append(cords)
        class_id = result 

    for i in detected:
        x1, y1, x2, y2 = i
        for x in range(int(x1), int(x2)):
            for y in range(int(y1), int(y2)):
                tmp = np.array([0.0, 0.0, 0.0])
                for a in range(-2, 3):
                    for b in range(-2, 3):
                        tmp += image[y + b][x + a]
                tmp /= 25
                image[y][x] = tmp

    secondres = model.predict(image)
    secondres = secondres[0]

    for box in secondres.boxes:
        class_id = secondres.names[box.cls[0].item()]
        if class_id not in "motorcycles":
            continue
        cords = box.xyxy[0].tolist()
        cords = [round(x) for x in cords]
        conf = round(box.conf[0].item(), 2)

        image = cv2.rectangle(image, (cords[0], cords[1]), (cords[2], cords[3]), (0, 0, 255), 1)
        image = cv2.putText(image, class_id + " " + str(conf), (cords[0], cords[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)    

    cv2.imshow("Captcha", image)    
    cv2.waitKey(0)