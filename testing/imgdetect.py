from ultralytics import YOLO
import cv2, os

model = YOLO('yolov8m.pt')
imgpath = "images/orig/"

for imgname in os.listdir(imgpath):
    img = cv2.imread(imgpath + imgname)
    results = model.predict(imgpath + imgname)
    result = results[0]

    for box in result.boxes:
        class_id = result.names[box.cls[0].item()]
        cords = box.xyxy[0].tolist()
        cords = [round(x) for x in cords]
        conf = round(box.conf[0].item(), 2)
        # print("Object type:", class_id)
        # print("Coordinates:", cords)
        # print("Probability:", conf)
        # print("---")

        img = cv2.rectangle(img, (cords[0], cords[1]), (cords[2], cords[3]), (0, 0, 255), 1)
        img = cv2.putText(img, class_id + " " + str(conf), (cords[0], cords[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("Captcha", img)
    cv2.waitKey(0)