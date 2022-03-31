from flask import Flask, render_template, request, jsonify, send_file
import sqlite3

app = Flask(__name__)

DB_PATH = 'assignment3.db'
SQL_INIT_PATH = 'initialise.sql'

def connect_db():
    global db
    db = sqlite3.connect(DB_PATH, check_same_thread = False)


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

def castSQL(str):
    return '\'' + str + '\''

@app.route('/api/user', methods = ['POST', 'GET'])
def api_user():

    if request.method == 'POST':
        # UtorID
        # First_Name
        # Middle_Name
        # Last_Name
        # Status
        # Password
        req = request.form

        UtorID = req.get('UtorID')
        First_Name = req.get('First_Name')
        Middle_Name = req.get('Middle_Name')
        Last_Name = req.get('Last_Name')
        Status = req.get('Status')
        Password = req.get('Password')

        global db
        cursor = db.cursor()
        # try:
        cursor.execute('''
            INSERT INTO User (UtorID, First_Name, Middle_Name, Last_Name, Status, Password)
            VALUES({}, {}, {}, {}, {}, {})
        '''.format(castSQL(UtorID),
                   castSQL(First_Name),
                   castSQL(Middle_Name),
                   castSQL(Last_Name),
                   castSQL(Status),
                   castSQL(Password)))
        cursor.close()
        # except E:
        #     return 'owo'
    if request.method == 'GET':
        pass
    a = {}
    a['as'] = 2
    return jsonify(a)

@app.route('/api/session', methods = ['POST', 'GET'])
def api_session():
    if request.method == 'POST':
        # Name
        # Instructor
        # Year
        # Term
        pass
    if request.method == 'GET':
        # Name
        req = request.form
        name = req.get('Name')
        if name != None:
            # return row with primary key name
            pass
        else:
            # return all
            pass
    return 'Hello, World!'

@app.route('/api/grade', methods = ['POST', 'GET'])
def api_grade():
    if request.method == 'POST':
        # UtorID
        # Assignment_ID
        pass
    if request.method == 'GET':
        # ID
        req = request.form
        name = req.get('ID')
        if name != None:
            # return row with primary key id
            pass
        else:
            # return all
            pass
    return 'Hello, World!'

@app.route('/api/assignment', methods = ['POST', 'GET'])
def api_assignment():
    if request.method == 'POST':
        # Name
        # Description
        # Session_ID
        pass
    if request.method == 'GET':
         # ID
        req = request.form
        name = req.get('ID')
        if name != None:
            # return row with primary key id
            pass
        else:
            # return all
            pass
    return 'Hello, World!'

@app.route('/api/assignment/student', methods = ['POST', 'GET'])
def api_student_assignment():
    if request.method == 'POST':
        # UtorID
        # Assignment_ID
        pass
    if request.method == 'GET':
        # return all
        pass
    return 'Hello, World!'

@app.route('/api/feedback', methods = ['POST', 'GET'])
def api_feedback():
    if request.method == 'POST':
        # Student_ID
        # Assignment
        pass
    if request.method == 'GET':
        # ID
        req = request.form
        name = req.get('ID')
        if name != None:
            # return row with primary key id
            pass
        else:
            # return all
            pass
    return 'Hello, World!'

@app.route('/api/regrade', methods = ['POST', 'GET'])
def api_remark():
    if request.method == 'POST':
        # Grade_ID
        # Content
        pass
    if request.method == 'GET':
        # ID
        req = request.form
        name = req.get('ID')
        if name != None:
            # return row with primary key id
            pass
        else:
            # return all
            pass
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

@app.route('/favicon.ico')
def favicon():
    return send_file('./static/favicon.ico', mimetype='image/svg+xml')

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/<file>')
def home(file):
    return render_template(file)

@app.teardown_appcontext
def close_db(exception):
    global db
    db.close()