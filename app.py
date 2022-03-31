from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)

DB_PATH = 'assignment3.db'
SQL_INIT_PATH = 'initialise.sql'

def connect_db():
    global db
    db = sqlite3.connect(DB_PATH)


def create_db():
    global db

    file = open(SQL_INIT_PATH, 'r')
    query = file.read()
    file.close()

    query = query.split(';\n')

    for q in query:
        db.execute(q)

connect_db()
create_db()

@app.route('/api/user', methods = ['POST', 'GET'])
def api_user():
    if request.method == 'POST':
        pass
        # except Exception as e:
        #     print(e)
    if request.method == 'GET':
        pass
    return 'Hello, World!'

@app.route('/api/session', methods = ['POST', 'GET'])
def api_session():
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return 'Hello, World!'

@app.route('/api/grade', methods = ['POST', 'GET'])
def api_grade():
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return 'Hello, World!'

@app.route('/api/feedback', methods = ['POST', 'GET'])
def api_feedback():
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return 'Hello, World!'

@app.route('/api/evaluations', methods = ['POST', 'GET'])
def api_evaluations():
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return 'Hello, World!'

@app.route('/api/remark', methods = ['POST', 'GET'])
def api_remark():
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return 'Hello, World!'

@app.route('/instructor/class')
def instructor_class():
    return 'Hello, World!'

@app.route('/instructor/remark')
def instructor_remark():
    return 'Hello, World!'

@app.route('/login')
def login():
    return 'Hello, World!'

@app.route('/register')
def register():
    return 'Hello, World!'

@app.route('/grades')
def grades():
    return 'Hello, World!'

@app.route('/user')
def user():
    return 'Hello, World!'

@app.route('/feedback')
def feedback():
    return 'Hello, World!'

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/<file>')
def home(file):
    return render_template(file)

@app.teardown_appcontext
def close_db():
    db.close()