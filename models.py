from flask_sqlalchemy import SQLAlchemy

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
    stud_mob = db.Column(db.Integer(10), unique=True, nullable=False)
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
