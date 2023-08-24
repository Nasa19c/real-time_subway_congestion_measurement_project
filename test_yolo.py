from flask import Flask, render_template, Response
import cv2
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)

cap = cv2.VideoCapture("video1.mp4")
model = YOLO("yolov8m.pt")

people_bbox = []  # 감지된 사람의 수를 저장할 리스트
paused = False  # 동영상 일시 정지 여부를 저장하는 변수

def gen_frames():
    global paused  # paused 변수를 전역 변수로 선언

    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                break
            
            results = model(frame, device="mps")
            result = results[0]
            bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
            classes = np.array(result.boxes.cls.cpu(), dtype="int")
            
            persons_mask = classes == 0  # 0은 persons 클래스의 인덱스
            frame_persons_bboxes = bboxes[persons_mask]
            
            num_persons = frame_persons_bboxes.shape[0]  # 현재 프레임에서 감지된 사람의 수
            people_bbox.append(num_persons)
            
            last_people = 0  # 기본값을 0으로 설정

            for bbox in frame_persons_bboxes:
                (x, y, x2, y2) = bbox
                cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 225), 2)
                cv2.putText(frame, "Person", (x, y-5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 225), 2)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        key = cv2.waitKey(1)
    
        if key == 27:  # ESC 키를 누르면 동영상 일시 정지/재생
            paused = not paused
            print("people_bbox:", people_bbox)  # 각 프레임에서 감지된 사람의 수를 출력
            last_people = people_bbox[-1]
            print("Last People:", last_people)  # 마지막 프레임에서 감지된 사람의 수 출력
        elif paused and key != -1:  # 정지 상태에서 다른 키를 누르면 다시 재생
            paused = False
        
        if key == 27 and not paused:  # ESC 키를 누르면서 동시에 재생 중이면 종료
            break
    last_people = people_bbox[-1] if people_bbox else 0 


@app.route('/')
def index():
    return render_template('video_show.html')

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
