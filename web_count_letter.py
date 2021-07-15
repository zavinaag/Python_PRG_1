from flask import Flask, render_template, request, redirect, escape
from datetime import date, datetime
from count_letter import ccount
from dbinterface import log_event_ins, log_event_get

app = Flask(__name__)

now = datetime.now()
logging_meta = dict()


def log_request(req: 'flask_request', res: str) -> None:
    datetimen = now.strftime("%Y:%m:%d") + " " + now.strftime("%H:%M:%S")
    with open('log.txt', 'a') as log:
        print(datetimen, req.remote_addr, req.user_agent.browser, req.form['PhraseInput'], res, file=log, sep='|')
    log_event_ins(datetimen, req.form['PhraseInput'], res, req.remote_addr, req.user_agent.browser)


def view_the_log() -> str:
    try:
        contents = []
        with open('log.txt') as log:
            for line in log:
                contents.append([])
                for item in line.split('|'):
                    contents[-1].append(escape(item))
        return render_template('log.html', the_title='Log View', the_data=contents)

    except FileNotFoundError:
        print("No such file log.txt")


def view_the_log_db() -> str:
    res = log_event_get()
    return render_template('log.html', the_title='Log View DB', the_data=res)


@app.route('/')
def hello_flask() -> '302':
    return redirect('/index')


@app.route('/index')
def index_page() -> 'html':
    return render_template("entry.html", the_title='Подсчет вхождений букв в слово или фразу')


@app.route('/countthis', methods=['POST'])
def web_count() -> str:
    try:
        the_result = ccount(request.form['PhraseInput'])
        log_request(request, the_result)
        if request.form['PhraseInput'] != '':
            return render_template('result.html', the_title='Результат обработки', the_word=request.form['PhraseInput'],
                                   the_result=the_result)
        else:
            return redirect('/index')
    except FileNotFoundError:
        print("No such file log.txt")


@app.route('/viewlog')
def get_log() -> str:
    return view_the_log()


@app.route('/viewlogdb')
def get_log_db() -> str:
    return view_the_log_db()


if __name__ == '__main__':
    app.run(debug=True)
