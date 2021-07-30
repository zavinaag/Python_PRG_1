from flask import Flask, session, redirect, render_template
from m_checker import check_logged_in

app = Flask(__name__)
app.secret_key = 'secret'


@app.route('/')
@app.route('/inx')
def hello():
    return 'Hello it is a index page'


@app.route('/accden')
def accden():
    return render_template("accden.html", the_title='')


@app.route('/p1')
@check_logged_in
def pg1() -> str:
    print('pg1 from simpleapp')
    return 'it is a page 1'


@app.route('/p2')
@check_logged_in
def pg2() -> str:
    return 'it is a page 2'


@app.route('/p3')
def pg3() -> str:
    return 'it is a page 3'


@app.route('/login')
def login():
    session['logged_in'] = True
    session['user'] = 'Anonim'
    return 'You are logged in'


@app.route('/login/<user>')
def login_user(user: str):
    session['logged_in'] = True
    session['user'] = user
    return 'You are logged in'


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
        return 'You are logged out'
    else:
        pass


@app.route('/status')
def check_status() -> str:
    if 'logged_in' in session:
        return 'You logged in currently as ' + session['user']
    return 'You are not logged in currently'


if __name__ == '__main__':
    app.run(debug=True)
