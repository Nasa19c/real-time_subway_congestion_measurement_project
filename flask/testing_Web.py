import random

from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

users = {
    'bean': '1234'
}

종각역 = {'last':'', 'next': '시청역'}
시청역 = {'last':'종각역', 'next': '서울역'}
서울역 = {'last':'시청역', 'next': ''}

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


@app.route("/index2")
def index2():
    progress_value = random.randrange(0,100)
    return render_template('index2.html', last_station = 시청역['last'], next_station = 시청역['next'], progress_value = progress_value)



@app.route("/data")
def data():
    return render_template('data.html')

if __name__=="__main__":
    app.run(debug=True)

# 지도는 request로 불러와야함