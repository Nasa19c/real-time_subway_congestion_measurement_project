import random

from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

users = {
    'bean': '1234'
}
topics = [
    {'id' : '종각역', 'last': '', 'next': '시청역', 'arrive1': '18:40', 'arrive2': '18:45'},
    {'id' : '시청역','last':'종각역', 'next': '서울역', 'arrive1': '18:47', 'arrive2': '18:53'},
    {'id' : '서울역','last':'시청역', 'next': '', 'arrive1': '18:54', 'arrive2': '18:59'}
]

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

@app.route("/index2", methods =['GET','POST'])
def index2():
    progress_value_platform = random.randrange(0,100)
    progress_value_inside = random.randrange(0,100)
    if request.method =='POST':
        for station_info in topics:
            if request.form['Station'] == station_info['id']:
                return render_template('index2.html', last_station = station_info['last'], next_station = station_info['next'], arrive1 = station_info['arrive1'], arrive2 = station_info['arrive2'],progress_value_platform = progress_value_platform, progress_value_inside = progress_value_inside)
    else:
        return render_template('index2.html',progress_value_platform = progress_value_platform, progress_value_inside = progress_value_inside)


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

if __name__=="__main__":
    app.run(debug=True)

# 지도는 request로 불러와야함