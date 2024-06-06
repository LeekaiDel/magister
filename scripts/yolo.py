import cv2
import time
from ultralytics import YOLO

img = cv2.imread('1.png')

model = YOLO("best.pt")

results = model.predict(img)

boxes = results[0].boxes.xyxy.tolist()

print(boxes)

res_plotted = results[0].plot()

cv2.imshow('', res_plotted)

cv2.waitKey(0)