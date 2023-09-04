import cv2
import numpy as np
import pandas as pd
from flask import (Flask, Response, jsonify, redirect, render_template,
                   request, session)
from ultralytics import YOLO

from read_csv import (draw_jong_station_chart, draw_jong_station_weekday_chart,
                      draw_se_station_chart, draw_se_station_weekday_chart,
                      draw_si_station_chart, draw_si_station_weekday_chart,
                      draw_station_chart, draw_station_weekday_chart)

app = Flask(__name__)
app.secret_key = 'supersecretkey'
cap = cv2.VideoCapture("video1.mp4")

people_bbox = []  # 감지된 사람의 수를 저장할 리스트
paused = False  # 동영상 일시 정지 여부를 저장하는 변수

users = {
    'bean': '1234'
}
topics = [
    {'id' : '종각역', 'last': '', 'next': '시청역', 'arrive1': '18:40', 'arrive2': '18:45'},
    {'id' : '시청역','last':'종각역', 'next': '서울역', 'arrive1': '18:47', 'arrive2': '18:53'},
    {'id' : '서울역','last':'시청역', 'next': '', 'arrive1': '18:54', 'arrive2': '18:59'}
]
# Load data from CSV file
data = pd.read_csv('SUBWAY_MONTH.csv', encoding='utf-8')  # 변경: 파일 경로 수정

draw_station_chart(data)
draw_station_weekday_chart(data)
draw_si_station_chart(data)
draw_si_station_weekday_chart(data)
draw_jong_station_chart(data)
draw_jong_station_weekday_chart(data)
draw_se_station_chart(data)
draw_se_station_weekday_chart(data)

last_station=None
next_station=None
arrive1=None
arrive2=None

@app.route('/toggle_pause')
def toggle_pause(): #특정 키를 누르면 last_people에 특정 키를 누른 시점의 값을 저장하도록 하자.
    global paused, last_people
    paused = not paused
    if paused:
        last_people = people_bbox[-1] if people_bbox else 0
        print("Last People:", last_people)
    return "Paused" if paused else "Playing"


@app.route('/save_people_bbox', methods=['GET'])
def save_people_bbox_get():
    current_people = people_bbox[-1] if people_bbox else 0
    saved_people = current_people
    return str(saved_people)


@app.route("/")
def index():
    return render_template('index.html',last_station=last_station, next_station = next_station, arrive1 = arrive1, arrive2 = arrive2)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect('/index2')
        else:
            return render_template('404.html', error='Invalid username or password')
    else:
        return render_template('login.html')


@app.route("/index2")
def index2():
    return render_template('index2.html',last_station=last_station, next_station = next_station, arrive1 = arrive1, arrive2 = arrive2)

@app.route('/update_variable', methods=['POST'])
def update_variable():
    global last_station
    global next_station
    global arrive1
    global arrive2
    global cap

    selected_station = request.form.get('Station')
    
    if selected_station == '종각역':
        cap = cv2.VideoCapture("video1.mp4")
    elif selected_station == '시청역':
        cap = cv2.VideoCapture("video2.mp4")
    elif selected_station == '서울역':
        cap = cv2.VideoCapture("video3.mp4")
    else:
        cap = None


    for station_info in topics:
        if selected_station == station_info['id']:
            last_station = station_info['last']
            next_station = station_info['next']
            arrive1 = station_info['arrive1']
            arrive2 = station_info['arrive2']
    
            return jsonify({"last_station":last_station, "next_station": next_station, "arrive1": arrive1, "arrive2": arrive2})

    return jsonify({"last_station":None,
                    "next_station":None,
                    "arrive1":None,
                    "arrive2":None,
                    })

@app.route('/update_variable_1', methods=['POST'])
def update_variable_1():
    global last_station
    global next_station
    global arrive1
    global arrive2
    global cap

    selected_station = request.form.get('Station1')

    if selected_station == '종각역':
        cap = cv2.VideoCapture("video4.mp4")
    elif selected_station == '시청역':
        cap = cv2.VideoCapture("video5.mp4")
    elif selected_station == '서울역':
        cap = cv2.VideoCapture("video6.mp4")
    else:
        cap = None

    for station_info in topics:
        if selected_station == station_info['id']:
            last_station = station_info['last']
            next_station = station_info['next']
            arrive1 = station_info['arrive1']
            arrive2 = station_info['arrive2']
    
            return jsonify({"last_station":last_station, "next_station": next_station, "arrive1": arrive1, "arrive2": arrive2})

    return jsonify({"last_station":None,
                    "next_station":None,
                    "arrive1":None,
                    "arrive2":None,
                    })


model = YOLO("yolov8m.pt")


def gen_frames():
    global paused, last_people, cap  # paused 변수를 전역 변수로 선언

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
            current_people = 0

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

@app.route("/data")
def data():
    return render_template('data.html')

@app.route("/시청_station_daily_data")
def si_station_daily_data():
    return render_template('시청_station_daily_data.html')

@app.route("/종각_station_daily_data")
def jong_station_daily_data():
    return render_template('종각_station_daily_data.html')
    
@app.route("/서울_station_daily_data")
def se_station_daily_data():
    return render_template('서울_station_daily_data.html')

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)


# 지도는 request로 불러와야함