from flask import Flask

app = Flask(__name__)
@app.route('/')
def hello() -> str:
    return 'Hello from Flask'

@app.route('/about')
def about() -> str:
    return '<h1>About page</h1>'

app.run()
