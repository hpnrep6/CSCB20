from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from enum import Enum 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    email = db.Column(db.String(128), primary_key = True)
    username = db.Column(db.String(64), nullable = False)
    first_name = db.Column(db.String(64), nullable = False)
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    status = db.Column(db.Enum('Student', 'Instructor'), nullable = False)
    password = db.Column(db.String(256))

    # sessions = db.relationship('Session', back_populates = 'User')
    # evaluations = db.relationship('Evaluation', back_populates = 'User')
    # grades = db.relationship('Grade', back_populates = 'User')
    # feedback = db.relationship('Feedback', back_populates = 'User')

class Session(db.Model):
    name = db.Column(db.String(16), primary_key = True)
    # instructor = db.Column(db.String(128), db.ForeignKey('User.email'))
    # instructor_rel = db.relationship('User', back_populates = 'Session')
    year = db.Column(db.Integer, nullable = False)
    term = db.Column(db.Enum('Winter', 'Summer', 'Fall'), nullable = False)

    # evaluations = db.relationship('Evaluation')
    # grades = db.relationship('Grade')

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(256), nullable = False)
    # instructor = db.Column(db.String(128), db.ForeignKey('User.email'))
    # instructor_rel = db.relationship('User', back_populates = 'Evaluation')
    # term = db.Column(db.String(16), db.ForeignKey('Session.name'))
    # term_rel = db.relationship('Session', back_populates = 'Evaluation')

    # grades = db.relationship('Grade')

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    # item = db.Column(db.Integer, db.ForeignKey('Evaluation.id'))
    # item_rel = db.relationship('Evaluation', back_populates = 'Grade')
    # student_id = db.Column(db.String(128), db.ForeignKey('User.email'))
    # student_rel = db.relationship('User', back_populates = 'Grade')
    # session = db.Column(db.String(16), db.ForeignKey('Session.name'))
    # session_rel = db.relationship('Session', back_populates = 'Grade')
    grade = db.Column(db.Float, nullable = False)

    # regrades = db.relationship('Regrade')

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    feedback = db.Column(db.String(2048), nullable = False)
    # instructor = db.Column(db.String(128), db.ForeignKey('User.email'))
    # instructor_rel = db.relationship('User', back_populates = 'Feedback')

class Regrade(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    request = db.Column(db.String(2048))
    # grade = db.Column(db.Integer, db.ForeignKey('Grade.id'))
    # grade_rel = db.relationship('Grade', back_populates = 'Regrade')

def setup_db():
    print('Creating database!')
    db.create_all()

setup_db()

@app.route('/api/user', methods = ['POST', 'GET'])
def api_user():
    if request.method == 'POST':
        # try:
        user = User(email = request.form.get('email'),
                    username = request.form.get('username'),
                    first_name = request.form.get('first_name'),
                    middle_name = request.form.get('middle_name'),
                    last_name = request.form.get('last_name'),
                    status = request.form.get('status'),
                    password = 'amogus')
        db.session.add(user)
        db.session.commit()
        print(2)
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