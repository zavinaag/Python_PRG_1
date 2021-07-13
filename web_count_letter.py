from flask import Flask, render_template, request, redirect, escape
from datetime import date, datetime
from count_letter import ccount

app = Flask(__name__)

now = datetime.now()
logging_meta = dict()

def log_request(req: 'flask_request', res: str) -> None:
    datetimen = now.strftime("%Y:%m:%d") + " " + now.strftime("%H:%M:%S")
    with open('log.txt', 'a') as log:
        print('date: ' + datetimen, req.form, req.remote_addr, req.user_agent, req.form['PhraseInput'], res, file=log, sep='|')

def view_the_log() -> str:
    try:
        with open('log.txt') as log:
            contents = log.readlines()
        return escape(''.join(contents))
    except FileNotFoundError:
        print("No such file log.txt")


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

if __name__ == '__main__':
    app.run(debug=True)
