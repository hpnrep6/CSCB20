from ctypes import cast
from flask import Flask, redirect, render_template, request, jsonify, send_file, session
import sqlite3
from flask_bcrypt import Bcrypt
from flask_session import Session
from itsdangerous import json

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = 'TACOPACOPACO'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

DB_PATH = 'assignment3.db'
SQL_INIT_PATH = 'initialise.sql'

def connect_db():
    return sqlite3.connect(DB_PATH, check_same_thread = False)


def create_db():
    db = connect_db()

    file = open(SQL_INIT_PATH, 'r')
    query = file.read()
    file.close()

    query = query.split(';\n')

    for q in query:
        db.execute(q)
    db.commit()
    db.close()

connect_db()
create_db()

def castSQL(str):
    if str == None:
        return 'null'
    str = str.replace('\'', '\'\'')
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
            req = request.form
            sqlite_select_query = """SELECT UtorID, First_Name, Middle_Name, Last_Name, Status, Instructor from User
                                    WHERE UtorID = {}
                                    """.format(castSQL(session.get('UtorID')))
            cursor.execute(sqlite_select_query)
            records = cursor.fetchone()
            cursor.close()
            if db:
                db.close()
            return jsonify(records)
        except sqlite3.Error as error:
            return 'Error'

@app.route('/api/utorid')
def api_utorid():
    a = {}
    if (session.get('UtorID')):
        a['UtorID'] = session['UtorID']
    return jsonify(a)

@app.route('/api/status')
def api_status():
    utorid = session.get('UtorID')

    db = connect_db()
    cursor = db.cursor()


    status = cursor.execute('''
                SELECT Status
                FROM User
                WHERE UtorID = {}'''.format(castSQL(utorid))).fetchone()
   
    cursor.close()
    db.close()
    return jsonify(status[0])


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
            return 'Error'
        finally:
            if db:
                db.close()
    a = records
    return jsonify(a)

@app.route('/api/grade', methods = ['POST', 'GET'])
def api_grade():
    if request.method == 'POST':
        # UtorID
        # Assignment
        req = request.form

        UtorID = req.get('UtorID')
        Assignment = req.get('Assignment')
        Grade = req.get('Grade')

        db = connect_db()
        cursor = db.cursor()

        result = cursor.execute('''
            SELECT *
            FROM Grade
            WHERE Assignment = {} AND Student_ID = {}
        '''.format(castSQL(Assignment), castSQL(UtorID))).fetchone()

        if result == None:
            try:
                cursor.execute('''
                    INSERT INTO Grade (Student_Id, Assignment)
                    VALUES({}, {})
                '''.format(castSQL(UtorID),
                        castSQL(Assignment)))
                db.commit()
                cursor.close()
            except:
                db.rollback()
                return 'An error occured.'
        else:
            try:
                cursor.execute('''
                    UPDATE Grade
                    SET Grade = {}
                    WHERE Assignment = {} AND Student_ID = {}
                '''.format(Grade, castSQL(Assignment), castSQL(UtorID)))
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
            assignments = db.execute('''
            SELECT Name
            FROM Assignment
            WHERE Instructor = {}
            GROUP BY Name
            '''.format(castSQL(name))).fetchall()
            db.close()

            names = {}

            names['_assignments'] = assignments

            for entry in post:
                if not entry[0] in names:
                    names[entry[0]] = []
                names[entry[0]].append([entry[1:]])
            return jsonify(names)
        else:
            return 'Error'

    return 'Error'

@app.route('/api/grade/aggregate')
def api_grade_aggregate():
    UtorID = session.get('UtorID')

    db = connect_db()
    cursor = db.cursor()

    result = cursor.execute('''
    SELECT Assignment, AVG(Grade)
    FROM Grade
    GROUP BY Assignment
    '''.format(UtorID)).fetchall()

    cursor.close()
    db.close()

    return jsonify(result)

@app.route('/api/grade/student', methods = ['GET'])
def api_grade_student():
    name = session.get('UtorID')

    if name != None:
        db = connect_db()
        post = db.execute('''
                        SELECT g.Assignment, g.Grade, a.Description
                        FROM (Grade as g LEFT JOIN User as u
                        ON g.Student_Id = u.UtorID)
                        LEFT JOIN Assignment as a
                        ON g.Assignment = a.Name
                        WHERE g.Student_Id = {}
                        '''.format(castSQL(name))).fetchall()

        db.close()

        return jsonify(post)
    else:
        return 'Error'


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

        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute('''
                INSERT INTO Assignment (Name, Description, Instructor)
                VALUES({}, {}, {})
            '''.format(castSQL(Name),
                    castSQL(Description),
                    castSQL(Instructor)))

            cursor.execute('SELECT UtorID FROM User WHERE Status = \'Student\' AND Instructor = {}'.format(castSQL(Instructor)))
            students = cursor.fetchall()

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
            return redirect('/instructor.html')
        except:
            db.rollback()
            return 'An error occured.'
    if request.method == 'GET':
         # ID
        req = request.form
        name = req.get('UtorID')

        if name != None:
            db = connect_db()
            post = db.execute('SELECT * FROM Assignment WHERE Id = {} ORDER BY Name DESC').format(castSQL(name)).fetchall()

            db.close()
            return jsonify(post)
        else:
            try:
                db = connect_db()
                cursor = db.cursor()
                sqlite_select_query = """SELECT * from Assignment"""
                cursor.execute(sqlite_select_query)
                records = cursor.fetchall()
                cursor.close()
                db.close()
                return jsonify(records)
            except sqlite3.Error as error:
                return 'Error'

@app.route('/api/feedback', methods = ['POST', 'GET'])
def api_feedback():
    if request.method == 'POST':
        # Student_ID
        # Assignment
        req = request.form

        Content = req.get('Content')
        Instructor = req.get('Instructor')

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
        # Assignment
        # Content
        req = request.form

        utorid = session.get('UtorID')

        Assignment = req.get('Assignment')
        Content = req.get('Content')

        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute('''
                INSERT INTO Regrade_Request (Student_ID, Assignment, Content)
                VALUES({}, {}, {})
            '''.format(castSQL(utorid),
                    castSQL(Assignment),
                    castSQL(Content)))
            db.commit()
            cursor.close()
            return 'Success'
        except:
            db.rollback()
            return 'An error occured.'
    if request.method == 'GET':
        # ID
        name = session.get('UtorID')
        if name != None:
            # return row with primary key id
            db = connect_db()
            regrades = db.execute('''
                            SELECT Assignment, UtorID, First_Name, Last_Name, Content
                            FROM Regrade_Request LEFT JOIN User
                            ON Student_ID = UtorID
                            WHERE Instructor = {}
                            '''.format(castSQL(name))).fetchall()

            assignments = db.execute('''
                            SELECT Name
                            FROM Assignment
                            WHERE Instructor = {}
                            '''.format(castSQL(name))).fetchall()
            db.close()

            regrade_dict = {}

            for regrade in regrades:
                if regrade[0] not in regrade_dict:
                    regrade_dict[regrade[0]] = []
                regrade_dict[regrade[0]].append(regrade[1:])

            for assignment in assignments:
                if assignment[0] not in regrade_dict:
                    regrade_dict[assignment[0]] = []


            return jsonify(regrade_dict)

    return 'Error'

@app.route('/login', methods = ['POST'])
def login():
    req = request.form
    utorid = None
    # try:
    db = connect_db()
    cursor = db.cursor()

    sqlite_select_query = """SELECT UtorID, Password FROM User
                                WHERE UtorID = {}
    """.format(castSQL(req.get('UtorID')))

    cursor.execute(sqlite_select_query)
    user = cursor.fetchone()

    if user == None:
        db.close()
        return 'Incorrect UtorID or Password'

    cursor.close()

    password = user[1]

    if not bcrypt.check_password_hash(password, req.get('Password')):
        if db:
            db.close()
        return 'Incorrect UtorID or Password'
    else:
        utorid = req.get('UtorID')
        
    if db:
        db.close()
    
    if utorid != None:
        session['UtorID'] = utorid
    
    return 'Success'


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

        if instructor != 'NULL':
            assignments = cursor.execute('''
                SELECT Name
                FROM Assignment
                WHERE Instructor = {}
            '''.format(instructor)).fetchall()

            for assignment in assignments:
                cursor.execute('''
                    INSERT INTO Grade (Assignment, Student_ID, Grade)
                    VALUES({}, {}, NULL)
                '''.format(castSQL(assignment[0]), castSQL(UtorID)))
            db.commit()
        cursor.close()
        db.close()
        return redirect('/')
    except:
        db.rollback()
        return render_template('register.html', message='Your username may not be unique or another error occured. Please try again.')


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
    if not session.get('UtorID'):
        if file == 'register.html':
            return render_template(file)
        return redirect('/')

    return render_template(file)