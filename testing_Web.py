from flask import Flask, render_template, Response, redirect, request, session
import cv2
import numpy as np
from ultralytics import YOLO
import pandas as pd
from read_csv import draw_si_station_chart, draw_si_station_weekday_chart, draw_jong_station_chart, draw_jong_station_weekday_chart, draw_se_station_chart, draw_se_station_weekday_chart, draw_station_chart, draw_station_weekday_chart


app = Flask(__name__)
app.secret_key = 'supersecretkey'
cap = cv2.VideoCapture("video1.mp4")
model = YOLO("yolov8m.pt")

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

def gen_frames():
    global paused, last_people  # paused 변수를 전역 변수로 선언

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

@app.route('/toggle_pause')
def toggle_pause(): #특정 키를 누르면 last_people에 특정 키를 누른 시점의 값을 저장하도록 하자.
    global paused, last_people
    paused = not paused
    if paused:
        last_people = people_bbox[-1] if people_bbox else 0
        print("Last People:", last_people)
    return "Paused" if paused else "Playing" 

#s키 눌렀을때
'''@app.route('/save_people_bbox')
def save_people_bbox():
    global people_bbox
    current_people = people_bbox[-1] if people_bbox else 0
    saved_people = current_people
    print("current people: ", current_people)
    return str(saved_people)'''

@app.route('/save_people_bbox', methods=['GET'])
def save_people_bbox_get():
    current_people = people_bbox[-1] if people_bbox else 0
    saved_people = current_people
    return str(saved_people)


def calculate_progress_values(current_people):
    progress_value_platform = (current_people / 30) * 100
    progress_value_inside = (current_people / 30) * 100
    return progress_value_platform, progress_value_inside

@app.route("/")
def index():
    return render_template('index.html')

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

@app.route("/index2", methods=['GET', 'POST'])
def index2():
    progress_value_platform = 0
    progress_value_inside = 0    # 초기 값으로 설정

    if request.method == 'POST':
        for station_info in topics:
            if request.form['Station'] == station_info['id']:
                return render_template('index2.html', last_station=station_info['last'], next_station=station_info['next'],
                                       arrive1=station_info['arrive1'], arrive2=station_info['arrive2'],
                                       progress_value_platform=progress_value_platform,
                                       progress_value_inside=progress_value_inside)
    else:
        return render_template('index2.html', progress_value_platform=progress_value_platform,
                               progress_value_inside=progress_value_inside)


'''@app.route("/index2", methods =['GET','POST'])
def index2(): #여기에 특정 값을 저장한 변수를 넣기
    progress_value_platform = random.randrange(0,100)
    progress_value_inside = random.randrange(0,100)
    if request.method =='POST':
        for station_info in topics:
            if request.form['Station'] == station_info['id']:
                return render_template('index2.html', last_station = station_info['last'], next_station = station_info['next'], arrive1 = station_info['arrive1'], arrive2 = station_info['arrive2'],progress_value_platform = progress_value_platform, progress_value_inside = progress_value_inside)
    else:
        return render_template('index2.html',progress_value_platform = progress_value_platform, progress_value_inside = progress_value_inside)
'''

# @app.route("/index2/1/", methods=['GET','POST'])
# def index2_1():
#     progress_value_platform = random.randrange(0,100)
#     progress_value_inside = random.randrange(0,100)
#     for station_info in topics:
#         if station_info['id'] == '종각역':
#             return render_template('index2.html', last_station = station_info['last'], next_station = station_info['next'], arrive1 = station_info['arrive1'], arrive2 = station_info['arrive2'],progress_value_platform = progress_value_platform, progress_value_inside = progress_value_inside)


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
    app.run()


# 지도는 request로 불러와야함