from curses import termattrs
from click import password_option
from flask import Flask, render_template, request, jsonify, send_file
import sqlite3

app = Flask(__name__)

DB_PATH = 'assignment3.db'
SQL_INIT_PATH = 'initialise.sql'

def connect_db():
    global db
    db = sqlite3.connect(DB_PATH, check_same_thread = False)
    return db


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
        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute('''
                INSERT INTO User (UtorID, First_Name, Middle_Name, Last_Name, Status, Password)
                VALUES({}, {}, {}, {}, {}, {})
            '''.format(castSQL(UtorID),
                    castSQL(First_Name),
                    castSQL(Middle_Name),
                    castSQL(Last_Name),
                    castSQL(Status),
                    castSQL(Password)))
            db.commit()
            cursor.close()
            return 'User successfully added.'
        except:
            db.rollback()
            return 'An error occured. Make sure the UtorID is unique.'
    if request.method == 'GET':
        try:
            db = connect_db()
            cursor = db.cursor()
            sqlite_select_query = """SELECT * from User"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to read data from table", error)
        finally:
            if db:
                db.close()
    a = records
    return jsonify(a)

@app.route('/api/session', methods = ['POST', 'GET'])
def api_session():
    if request.method == 'POST':
        # Name
        # Instructor
        # Year
        # Term
        req = request.form

        Name = req.get('Name')
        Instructor = req.get('Instructor')
        Year = req.get('Year')
        Term = req.get('Term')

        global db
        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute('''
                INSERT INTO Session (Name, Instructor, Year, Term)
                VALUES({}, {}, {}, {})
            '''.format(castSQL(Name),
                    castSQL(Instructor),
                    castSQL(Year),
                    castSQL(Term)))
            db.commit()
            cursor.close()
        except:
            db.rollback()
            return 'An error occured.'
    if request.method == 'GET':
        # Name
        req = request.form
        name = req.get('Name')
        if name != None:
            # return row with primary key name
            db = connect_db()
            post = db.execute('SELECT * FROM Session WHERE Name = ?',
                                (name)).fetchone()
            db.close()
            return post
        else:
            try:
                db = connect_db()
                cursor = db.cursor()
                sqlite_select_query = """SELECT * from Session"""
                cursor.execute(sqlite_select_query)
                records = cursor.fetchall()
                cursor.close()
            except sqlite3.Error as error:
                print("Failed to read data from table", error)
            finally:
                if db:
                    db.close()
        a = records
        return jsonify(a)

@app.route('/api/grade', methods = ['POST', 'GET'])
def api_grade():
    if request.method == 'POST':
        # UtorID
        # Assignment_ID
        req = request.form

        UtorID = req.get('UtorID')
        Assignment_ID = req.get('Assignment_ID')

        global db
        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute('''
                INSERT INTO Grade (UtorID, Assignment_ID)
                VALUES({}, {})
            '''.format(castSQL(UtorID),
                    castSQL(Assignment_ID)))
            db.commit()
            cursor.close()
        except:
            db.rollback()
            return 'An error occured.'
    if request.method == 'GET':
        # ID
        req = request.form
        name = req.get('ID')
        if name != None:
            db = connect_db()
            post = db.execute('SELECT * FROM Grade WHERE Id = ?',
                                (name)).fetchone()
            db.close()
            return post
        else:
            try:
                db = connect_db()
                cursor = db.cursor()
                sqlite_select_query = """SELECT * from Grade"""
                cursor.execute(sqlite_select_query)
                records = cursor.fetchall()
                cursor.close()
            except sqlite3.Error as error:
                print("Failed to read data from table", error)
            finally:
                if db:
                    db.close()
    a = records
    return jsonify(a)

@app.route('/api/assignment', methods = ['POST', 'GET'])
def api_assignment():
    if request.method == 'POST':
        # Name
        # Description
        # Session_ID
        req = request.form

        Name = req.get('Name')
        Description = req.get('Description')
        Session_ID = req.get('Session_ID')

        global db
        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute('''
                INSERT INTO Assignment (Name, Description, Session_ID)
                VALUES({}, {}, {})
            '''.format(castSQL(Name),
                    castSQL(Description),
                    castSQL(Session_ID)))
            db.commit()
            cursor.close()
        except:
            db.rollback()
            return 'An error occured.'
    if request.method == 'GET':
         # ID
        req = request.form
        name = req.get('Id')
        if name != None:
            db = connect_db()
            post = db.execute('SELECT * FROM Assignment WHERE Id = ?',
                                (name)).fetchone()
            db.close()
            return post
        else:
            try:
                db = connect_db()
                cursor = db.cursor()
                sqlite_select_query = """SELECT * from Assignment"""
                cursor.execute(sqlite_select_query)
                records = cursor.fetchall()
                cursor.close()
            except sqlite3.Error as error:
                print("Failed to read data from table", error)
            finally:
                if db:
                    db.close()
    a = records
    return jsonify(a)

@app.route('/api/assignment/student', methods = ['POST', 'GET'])
def api_student_assignment():
    if request.method == 'POST':
        # UtorID
        # Assignment_ID
        req = request.form

        UtorID = req.get('UtorID')
        Assignment_ID = req.get('Assignment_ID')

        global db
        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute('''
                INSERT INTO Student_Assignments (UtorID, Assignment_ID)
                VALUES({}, {})
            '''.format(castSQL(UtorID),
                    castSQL(Assignment_ID)))
            db.commit()
            cursor.close()
        except:
            db.rollback()
            return 'An error occured.'
    if request.method == 'GET':
        # return all
        try:
            db = connect_db()
            cursor = db.cursor()
            sqlite_select_query = """SELECT * from Student_Assignments"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to read data from table", error)
        finally:
            if db:
                db.close()
    a = records
    return jsonify(a)

@app.route('/api/feedback', methods = ['POST', 'GET'])
def api_feedback():
    if request.method == 'POST':
        # Student_ID
        # Assignment
        req = request.form

        Student_ID = req.get('Student_ID')
        Assignment = req.get('Assignment')

        global db
        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute('''
                INSERT INTO Feedback (Student_ID, Assignment)
                VALUES({}, {})
            '''.format(castSQL(Student_ID),
                    castSQL(Assignment)))
            db.commit()
            cursor.close()
        except:
            db.rollback()
            return 'An error occured.'
    if request.method == 'GET':
        # ID
        req = request.form
        name = req.get('Id')
        if name != None:
            # return row with primary key id
            db = connect_db()
            post = db.execute('SELECT * FROM Feedback WHERE Id = ?',
                                (name)).fetchone()
            db.close()
            return post
        else:
            try:
                db = connect_db()
                cursor = db.cursor()
                sqlite_select_query = """SELECT * from Feedback"""
                cursor.execute(sqlite_select_query)
                records = cursor.fetchall()
                cursor.close()
            except sqlite3.Error as error:
                print("Failed to read data from table", error)
            finally:
                if db:
                    db.close()
    a = records
    return jsonify(a)

@app.route('/api/regrade', methods = ['POST', 'GET'])
def api_remark():
    if request.method == 'POST':
        # Grade_ID
        # Content
        req = request.form

        Grade_ID = req.get('Grade_ID')
        Content = req.get('Content')

        global db
        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute('''
                INSERT INTO Regrade_Request (Student_ID, Assignment)
                VALUES({}, {})
            '''.format(castSQL(Grade_ID),
                    castSQL(Content)))
            db.commit()
            cursor.close()
        except:
            db.rollback()
            return 'An error occured.'
    if request.method == 'GET':
        # ID
        req = request.form
        name = req.get('Id')
        if name != None:
            # return row with primary key id
            db = connect_db()
            post = db.execute('SELECT * FROM Regrade_Request WHERE Id = ?',
                                (name)).fetchone()
            db.close()
            return post
        else:
            try:
                db = connect_db()
                cursor = db.cursor()
                sqlite_select_query = """SELECT * from Regrade_Request"""
                cursor.execute(sqlite_select_query)
                records = cursor.fetchall()
                cursor.close()
            except sqlite3.Error as error:
                print("Failed to read data from table", error)
            finally:
                if db:
                    db.close()
    a = records
    return jsonify(a)

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