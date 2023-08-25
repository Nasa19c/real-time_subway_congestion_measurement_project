from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = 'mysecretkey'  # 세션 보안을 위한 시크릿 키

# 예시 사용자 정보 (실제로는 데이터베이스나 인증 시스템을 사용해야 함)
USERS = {
    'user1': 'password1',
    'user2': 'password2'
}

@app.route('/')
def index():
    return "Welcome to the public page!"

@app.route('/hidden')
def hidden_page():
    if 'username' in session:
        return "Welcome to the hidden page!"
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('hidden_page'))
        else:
            return "Login failed."

    return render_template('login.html')

if __name__ == "__main__":
    app.run()
