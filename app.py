from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from enum import Enum 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    utorid = db.Column(db.String(32), primary_key = True)
    first_name = db.Column(db.String(128), nullable = False)
    middle_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    status = db.Column(db.Enum('Student', 'Instructor'), nullable = False)
    password = db.Column(db.String(256))

class Session(db.Model):
    name = db.Column(db.String(16), primary_key = True)
    instructor = db.relationship('User')
    year = db.Column(db.Integer, nullable = False)
    term = db.Column(db.Enum('Winter', 'Summer', 'Fall'), nullable = False)

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(256), nullable = False)
    instructor = db.relationship('User')
    term = db.relationship('Session')

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    item = db.relationship('Evaluation')
    student_id = db.relationship('User')
    session = db.relationship('Session')
    grade = db.Column(db.Float, nullable = False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    feedback = db.Column(db.String(2048), nullable = False)
    instructor = db.relationship('User')

class Regrade(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    request = db.Column(db.String(2048))
    grade = db.relationship('Grade')

def setup_db():
    db.create_all()

setup_db()

@app.route('/api/user', methods = ['POST', 'GET'])
def api_user():
    return 'Hello, World!'

@app.route('/api/session', methods = ['POST', 'GET'])
def api_session():
    return 'Hello, World!'

@app.route('/api/grade', methods = ['POST', 'GET'])
def api_grade():
    return 'Hello, World!'

@app.route('/api/feedback', methods = ['POST', 'GET'])
def api_feedback():
    return 'Hello, World!'

@app.route('/api/evaluations', methods = ['POST', 'GET'])
def api_evaluations():
    return 'Hello, World!'

@app.route('/api/remark')
def api_remark():
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
def home():
    return render_template('index.html')

@app.route('/<file>')
def hom(file):
    return render_template(file)