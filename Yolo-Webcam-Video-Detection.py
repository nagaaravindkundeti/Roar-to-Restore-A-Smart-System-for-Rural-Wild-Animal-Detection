from ultralytics import YOLO
import cv2
import cvzone
import math
import time

import pygame

audio_path = r"D:\PROJECT_EXPO\music\2.wav"

# cap = cv2.VideoCapture(1)  # For Webcam
# cap.set(3, 1280)
# cap.set(4, 720)
cap = cv2.VideoCapture("../Videos/9.mp4")  # ForVideo

model = YOLO("../Yolo-Weights/yolov8x.pt")

classNames = ["person", "", "car", "motorbike", "", "Tiger", "train", "truck", "",
              "", "", "", "", "", "", "Tiger",
              "Tiger", "", "", "Cow", "Elephant", "Bear", "Tiger", "Leopard", "", "",]

prev_frame_time = 0
new_frame_time = 0

while True:
    new_frame_time = time.time()
    success, img = cap.read()
    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h))
            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])
            cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

            # Check if class name is "Tiger"
            if classNames[cls] == "Tiger" and conf > 0.70 or classNames[cls] == "Elephant" and conf > 0.70:
                pygame.mixer.init()
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play(-1)
                pygame.time.wait(100)
            else:
                pygame.mixer.init()
                pygame.mixer.music.stop()


    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    print(fps)
    # cls = int(box.cls[0])

    cv2.imshow("Image", img)
    cv2.waitKey(2)
