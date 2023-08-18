from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/index2")
def index2():
    return render_template('index2.html')

@app.route("/data")
def data():
    return render_template('data.html')

if __name__=="__main__":
    app.run()

# 지도는 request로 불러와야함