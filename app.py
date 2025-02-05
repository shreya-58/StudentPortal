import os
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "studentportal.sqlite3") 
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()
# app.config['SECRET_KEY'] = 'your_secret_key_here'

db = SQLAlchemy()

class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # student, teacher, admin

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    course_desc = db.Column(db.String)
    semester = db.Column(db.Integer, db.ForeignKey('student.sem'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'))

class Student(db.Model):
    __tablename__ = 'student'
    stud_id = db.Column(db.Integer, primary_key=True)
    stud_name = db.Column(db.String(100), nullable=False)
    stud_mob = db.Column(db.Integer, unique=True, nullable=False)
    stud_email = db.Column(db.String(60), unique=True)
    stud_addr = db.Column(db.String)
    semester = db.Column(db.Integer)

class Teacher(db.Model):
    __tablename__ = 'teacher'
    teacher_id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(100), nullable=False)

class Assignment(db.Model):
    ass_id = db.Column(db.Integer, primary_key=True)
    ass_title = db.Column(db.String(100), nullable=False)
    ass_description = db.Column(db.Text, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course.id'))
    ass_marks = db.Column(db.Integer)

class Attendance(db.Model):
    lect_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.stud.id'))
    lec_date = db.Column(db.Date, nullable=False)
    lec_time = db.Column(db.String(30), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course.id'))
    status = db.Column(db.String(1), nullable=False)  # Present-P/Absent-A

class Result(db.Model):
    res_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    marks = db.Column(db.Integer, nullable=False)


@app.route("/", methods=['GET', 'POST'])
def loginpage():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
        login = Login.query.filter_by(id = id, password = password)
        print(id, password)
        if login:
            if login.id == id and login.password == password:
                # session['id'] = id
                # session['password'] = password
                if login.role == 'student':
                    return redirect(url_for(student_dashboard))
                elif login.role == 'teacher':
                    return redirect(url_for(teacher_dashboard))
                elif login.role == 'admin':
                    return redirect(url_for(admin_dashboard))
        return render_template(error.html)
    return render_template("login.html")


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)