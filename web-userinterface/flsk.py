from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2
import cvzone
import math
import pygame
import mysql.connector
from flask import jsonify




# mydb = mysql.connector.connect(
#      host="localhost",
#      user="root",
#      password="apple.CLOUD@2001",
#      database="wildanimals")

app = Flask(__name__)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
hand = 0
model = YOLO("../Yolo-Weights/facehand.pt")
classNames = ['Face', 'Hand']
audio_path = r"D:\PROJECT_EXPO\music\2.wav"

def count_hands(frame):
    count = 0
    results = model(frame, stream=True)
    for r in results:
        boxes = r.boxes
        for i, box in enumerate(boxes):
            cls = int(box.cls[0])
            class_type = classNames[cls]
            conf = math.ceil((box.conf[0] * 100)) / 100

            if class_type == "Hand" and conf > 0.65:
                count += 1

    return count

def gen_frames():
    def count_hands(frame):
        count = 0
        results = model(frame, stream=True)
        for r in results:
            boxes = r.boxes
            for i, box in enumerate(boxes):
                cls = int(box.cls[0])
                class_type = classNames[cls]
                conf = math.ceil((box.conf[0] * 100)) / 100

                if class_type == "Hand" and conf > 0.65:
                    count += 1

        return count

    while True:
        success, img = cap.read()
        if not success:
            break
        else:


            # hand_count = count_hands(img)
            # values = ('Hand', hand_count)
            # cursor = mydb.cursor()
            # cursor.execute(sql, values)
            # mydb.commit()

            results = model(img, stream=True)
            for r in results:
                boxes = r.boxes
                for i, box in enumerate(boxes):
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    #cls = int(box.cls[0])
                    conf = math.ceil((box.conf[0] * 100)) / 100



                    hand_count = count_hands(img)


                    if conf > 0.60:
                        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                        cls = int(box.cls[0])
                        cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

                    # Check if class name is "Hand" and confidence is greater than 0.70
                    cls = int(box.cls[0])
                    if classNames[cls] == "Hand" and conf > 0.70 :
                        pygame.mixer.init()
                        pygame.mixer.music.load(audio_path)
                        pygame.mixer.music.play(-1)
                        pygame.time.wait(100)

                    else:
                        pygame.mixer.init()
                        pygame.mixer.music.stop()

            #cvzone.putTextRect(img, f'Hands: {hand_count}', (10, 20), scale=1, thickness=1)
            #sql = "INSERT INTO wild_animal_count (class, count) VALUES (%s, %s)"



            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            print("Number of hands detected:", hand_count)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signal')
def signal():
    return render_template('signal.html')

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/his')
def his():
    return render_template('History.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
