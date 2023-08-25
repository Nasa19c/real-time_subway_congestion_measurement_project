import cv2
import numpy as np
from ultralytics import YOLO

from flask import Flask, Response, render_template

app = Flask(__name__)

model = YOLO("yolov8m.pt")
cap = cv2.VideoCapture("/Users/82108/Desktop/공개sw 개발자/workplace/flask/video1.mp4")



@app.route('/')
def video_show():
    return render_template('example1.html')

def gen_frames():
    people_bbox = []  # 감지된 사람의 수를 저장할 리스트
    while True:
        ret, frame = cap.read()
        if not ret:
            print("NONNO")
            break
        else:
            results = model(frame, device="mps")
            result = results[0]
            bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
            classes = np.array(result.boxes.cls.cpu(), dtype="int")

            persons_mask = classes == 0  # 0은 persons 클래스의 인덱스
            frame_persons_bboxes = bboxes[persons_mask]

            num_persons = frame_persons_bboxes.shape[0]  # 현재 프레임에서 감지된 사람의 수
            people_bbox.append(num_persons)

            for bbox in frame_persons_bboxes:
                (x, y, x2, y2) = bbox
                cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 225), 2)
                cv2.putText(frame, "Person", (x, y-5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 225), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            print("people_bbox:", people_bbox)  # 각 프레임에서 감지된 사람의 수를 출력
            last_people = people_bbox[-1]
            print("Last People:", last_people)  # 마지막 프레임에서 감지된 사람의 수 출력

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
        
        
@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)