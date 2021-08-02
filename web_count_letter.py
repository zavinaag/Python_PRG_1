from flask import Flask, render_template, request, redirect, escape, session
from datetime import datetime
from count_letter import ccount
from dbinterface import log_event_ins, log_event_get, log_event_ins_dbcm
from m_checker import check_logged_in
from user_login_form import Login_form

app = Flask(__name__)

now = datetime.now()
logging_meta = dict()

app.secret_key = '30 82 01 0a 02 82 01 01 00 df 90 d2 ae 90 5a 80 11 c1 df 78 75 9a f9 ee 3c a7 54 44 bb a7 8e 2b 92 29 ef dc e5 0a 57 3b 31 07 6c 1d 14 f5 fe d3 ef 25 9c fe c8 8a e0 0c b2 e7 78 61 f8 5d 1f 0e 87 d8 7f 06 f5 4a ec df da 82 da 1f d8 99 ed 26 be d0 55 79 19 bd 88 69 33 f4 62 4d 84 65 af 4d cb ac 8d e4 37 45 a6 de 1c 94 99 1e b7 eb b5 ab 96 76 af b2 38 08 f9 55 f0 13 a1 fa d3 5a af df ff 0a 2d e7 d7 f2 cd 4c bc f5 d6 ff 8e 0f 87 f1 55 c6 92 51 cf 4d 35 81 86 0f 9a 22 a0 76 0b 54 7e 97 8b 22 28 4e e7 53 ff ec 23 08 2d c9 29 1e 3c 37 f4 7b 6e 03 cc c8 95 c0 3e e1 29 24 71 1e 7a 10 a3 4b e6 c6 63 d0 ae 44 18 8d 82 8f 5f 91 1a ae 8a fe 70 22 b7 5a 1e 1f b8 a6 e5 08 00 25 68 97 7c 73 16 c7 86 f1 18 81 1b 5a ee c8 96 a6 64 a4 58 9b 0b 0d a2 53 9d bd f1 d8 ff 4b c3 be 3b 6d 68 5b 45 c2 19 c5 39 02 03 01 00 01'

app.config['dbconfig'] = {'database': 'webapp.db'}


def get_datetimen() -> str:
    return str(now.strftime("%Y:%m:%d") + " " + now.strftime("%H:%M:%S"))


def get_session_user() -> str:
    return session['user']


def log_request(req, res) -> None:
    with open('log.txt', 'a') as log:
        print(get_datetimen(), req.remote_addr, req.user_agent.browser, req.form['PhraseInput'], res, file=log, sep='|')
    log_event_ins(get_datetimen(), req.form['PhraseInput'], res, req.remote_addr, req.user_agent.browser)


def log_request_dbcm(req, res) -> None:
    log_event_ins_dbcm(get_datetimen(), req.form['PhraseInput'], res, req.remote_addr, req.user_agent.browser,
                       app.config['dbconfig'])


def set_session(user: str = 'Anonimous', password: str = 'pass', logged_in: bool = True) -> None:
    session['logged_in'] = logged_in
    session['password'] = password
    session['user'] = user
    return session


@app.route('/')
def hello_flask() -> '302':
    return redirect('/index')


@app.route('/index')
def index_page():
    if 'logged_in' and 'user' in session:
        return render_template("entry.html", the_title='Подсчет вхождений букв в слово или фразу',
                               user=get_session_user())
    else:
        return redirect('/lgf')


@app.route('/countthis', methods=['POST'])
@check_logged_in
def web_count() -> str:
    try:
        if request.form['PhraseInput'].strip() != '':
            the_result = ccount(request.form['PhraseInput'])
            log_request(request, the_result)
            log_request_dbcm(request, the_result)

            if 'logged_in' and 'user' in session:
                return render_template('result.html', the_title='Результат обработки',
                                       the_word=request.form['PhraseInput'],
                                       the_result=the_result, user=session['user'])
            else:
                return render_template('result.html', the_title='Результат обработки',
                                       the_word=request.form['PhraseInput'],
                                       the_result=the_result, user='Guest')
        else:
            return redirect('/index')
    except FileNotFoundError:
        print("No such file log.txt")


@app.route('/viewlog')
@check_logged_in
def get_log() -> 'html':
    try:
        contents = []
        with open('log.txt') as log:
            for line in log:
                contents.append([])
                for item in line.split('|'):
                    contents[-1].append(escape(item))
        return render_template('log.html', the_title='Log View', the_data=contents, user=get_session_user())
    except FileNotFoundError:
        print("No such file log.txt")


@app.route('/viewlogdb')
@check_logged_in
def get_log_db() -> 'html':
    res = log_event_get()
    return render_template('log.html', the_title='Log View DB', the_data=res, user=get_session_user())


@app.route('/lgf', methods=['GET'])
def user_login_form():
    ulf = Login_form()
    return render_template('user_login_form.html', title="Авторизация пользователя", form=ulf)


@app.route('/lgf2', methods=['GET'])
def user_login_form_wtf():
    ulfw = Login_form()
    return render_template('ulfw.html', form=ulfw)


@app.route('/login', methods=['POST'])
def set_session_user():
    if (not request.form['user']):
        set_session()
    else:
        set_session(password=request.form['password'], user=request.form['user'])
    return redirect('/index')


@app.route('/login2', methods=['POST', 'GET'])
def set_session_user2():
    ulfw = Login_form()
    if ulfw.validate_on_submit():
        if (not ulfw.user.data):
            return redirect('/lgf2')
        else:
            set_session(password=ulfw.password.data, user=ulfw.user.data)
        return redirect('/index')
    else:
        set_session()
        return redirect('/index')


@app.route('/logout', methods=['GET'])
@check_logged_in
def logout() -> '302':
    if 'logged_in' and 'user' in session:
        session.pop('logged_in')
        session.pop('user')
    return redirect('/')


@app.route('/accden')
def accden() -> 'html':
    return render_template("accden.html", the_title='')


@app.route('/status')
def check_status() -> str:
    if 'logged_in' and 'user' in session:
        return 'You logged in currently as ' + session['user']
    return 'You are not logged in currently'


if __name__ == '__main__':
    app.run(debug=True)
