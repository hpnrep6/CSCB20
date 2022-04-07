from ast import Pass
from curses import termattrs
from click import password_option
from flask import Flask, redirect, render_template, request, jsonify, send_file, session
import sqlite3
from flask_bcrypt import Bcrypt
from flask_session import Session

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = 'TACOPACOPACO'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)


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

        pw_hash = bcrypt.generate_password_hash(Password).decode('utf-8')
        if not bcrypt.check_password_hash(pw_hash, Password):
             # returns True
            return 'An error occured while hashing the password.'

        Password = pw_hash
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

            if req.get('Instructor_ID') != None:
                sqlite_select_query = """SELECT * from User
                                         WHERE Instructor = {}
                """.format(castSQL(req.get('Instructor_ID')))
            else:
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

@app.route('/api/utorid')
def api_utorid():
    a = {}
    if (session.get('UtorID')):
        a['UtorID'] = session['UtorID']
    return jsonify(a)

@app.route('/api/instructor')
def api_instructor():
    utorid = ''
    if (session.get('UtorID')):
        utorid = session['UtorID']
    else:
        return jsonify({})

    db = connect_db()
    cursor = db.cursor()

      
    sqlite_select_query = """SELECT u2.UtorID, u2.First_Name, u2.Middle_Name, u2.Last_Name 
                            FROM User as u1
                            LEFT JOIN User as u2 ON u1.Instructor = u2.UtorID
                            WHERE u1.UtorID = {}
    """.format(castSQL(utorid))

    cursor.execute(sqlite_select_query)
    instructor = cursor.fetchone()
    cursor.close()

    return jsonify(instructor)

@app.route('/api/instructors', methods = ['GET'])
def api_instructors():
    req = request.form
    if request.method == 'GET':
        try:
            db = connect_db()
            cursor = db.cursor()

            sqlite_select_query = """SELECT UtorID, First_Name, Middle_Name, Last_Name, Status, Instructor FROM User
                                        WHERE Status = 'Instructor'
            """

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
        
        name = session.get('UtorID')

        if name != None:
            db = connect_db()
            post = db.execute('''
                            SELECT u.UtorID, u.First_Name, u.Middle_Name, u.Last_Name, g.Assignment, g.Grade
                            FROM Grade as g LEFT JOIN User as u
                            ON g.Student_Id = u.UtorID
                            WHERE u.Instructor = {}
                            '''.format(castSQL(name))).fetchall()
            db.close()
            return jsonify(post)
        else:
            return 'Invalid'

    return 'Invalid'

@app.route('/api/assignment', methods = ['POST', 'GET'])
def api_assignment():
    if request.method == 'POST':
        # Name
        # Description
        # Session_ID
        req = request.form

        Name = req.get('Name')
        Description = req.get('Description')
        Instructor = req.get('Instructor')

        global db
        db = connect_db()
        cursor = db.cursor()
        # try:
        cursor.execute('''
            INSERT INTO Assignment (Name, Description, Instructor)
            VALUES({}, {}, {})
        '''.format(castSQL(Name),
                castSQL(Description),
                castSQL(Instructor)))

        cursor.execute('SELECT UtorID FROM User WHERE Status = \'Student\' AND Instructor = {}'.format(castSQL(Instructor)))
        students = cursor.fetchall()
        print(students)
        for student in students:
            utorid = student[0]
            
            cursor.execute('''
            INSERT INTO Grade(Assignment, Student_Id)
            VALUES ({}, {})
            '''.format(castSQL(Name), castSQL(utorid)))

        records = {}
        

        db.commit()
        cursor.close()
        db.close()
        # except:
        #     db.rollback()
        #     return 'An error occured.'
    if request.method == 'GET':
         # ID
        req = request.form
        name = req.get('UtorID')

        if name != None:
            db = connect_db()
            post = db.execute('SELECT * FROM Assignment WHERE Id = {}').format(castSQL(name)).fetchall()

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

@app.route('/api/feedback', methods = ['POST', 'GET'])
def api_feedback():
    if request.method == 'POST':
        # Student_ID
        # Assignment
        req = request.form

        Content = req.get('Content')
        Instructor = req.get('Instructor')

        global db
        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute('''
                INSERT INTO Feedback (Content, Instructor)
                VALUES({}, {})
            '''.format(castSQL(Content),
                    castSQL(Instructor)))
            db.commit()
            cursor.close()
        except:
            db.rollback()
            return 'An error occured.'
        finally:
            return 'Success'
    else: # request.method == 'GET':
        # ID
        name = session.get('UtorID')
        if name != None:
            # return row with primary key id
            db = connect_db()
            post = db.execute('SELECT Content FROM Feedback WHERE Instructor = {}'.format(castSQL(name))).fetchall()
            db.close()
            return jsonify(post)


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

@app.route('/login', methods = ['POST'])
def login():
    req = request.form
    utorid = None
    try:
        db = connect_db()
        cursor = db.cursor()

        sqlite_select_query = """SELECT UtorID, Password FROM User
                                    WHERE UtorID = {}
        """.format(castSQL(req.get('UtorID')))

        cursor.execute(sqlite_select_query)
        user = cursor.fetchone()
        cursor.close()

        password = user[1]

        if not bcrypt.check_password_hash(password, req.get('Password')):
            if db:
                db.close()
        else:
            utorid = req.get('UtorID')
        

    except sqlite3.Error as error:
        print(error)
    finally:
        if db:
            db.close()
    
    if utorid != None:
        session['UtorID'] = utorid
    
    return redirect('/')


@app.route('/register', methods = ['POST'])
def register():
    req = request.form
    UtorID = req.get('UtorID')
    First_Name = req.get('First_Name')
    Middle_Name = req.get('Middle_Name')
    Last_Name = req.get('Last_Name')
    Status = req.get('Status')
    Password = req.get('Password')

    hash = bcrypt.generate_password_hash(Password).decode('utf-8')
    if not bcrypt.check_password_hash(hash, Password):
        return 'An error occured while hashing the password.'

    Password = hash
    global db
    db = connect_db()
    cursor = db.cursor()

    instructor = req.get('Instructor')
    if instructor == None:
        instructor = 'NULL'
    else:
        instructor = castSQL(instructor)

    try:
        cursor.execute('''
            INSERT INTO User (UtorID, First_Name, Middle_Name, Last_Name, Status, Password, Instructor)
            VALUES({}, {}, {}, {}, {}, {}, {})
        '''.format(castSQL(UtorID),
                castSQL(First_Name),
                castSQL(Middle_Name),
                castSQL(Last_Name),
                castSQL(Status),
                castSQL(Password),
                instructor))
        db.commit()
        cursor.close()
        return 'User successfully added.'
    except:
        db.rollback()
        return 'An error occured. Make sure the UtorID is unique.'

@app.route('/logout')
def logout():
    if session.get('UtorID'):
        session['UtorID'] = None
    
    return redirect('/')

@app.route('/favicon.ico')
def favicon():
    return send_file('./static/favicon.ico', mimetype='image/svg+xml')

@app.route('/')
def root():
    if (session.get('UtorID')):
        return render_template('index.html')
    else:
        return render_template('login.html')

@app.route('/<file>')
def home(file):
    if (not session.get('UtorID')):
        return redirect('/')

    return render_template(file)

@app.teardown_appcontext
def close_db(exception):
    global db
    db.close()