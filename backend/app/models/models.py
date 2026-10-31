from datetime import date, datetime
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, Date, Numeric, Boolean, ForeignKey,
    DateTime, Text, JSON
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(100), nullable=False, unique=True)
    department_code = Column(String(20), nullable=False, unique=True)
    hod_name = Column(String(100), nullable=False)
    building = Column(String(50))
    contact_email = Column(String(100))

    students = relationship("Student", back_populates="department")
    faculty = relationship("Faculty", back_populates="department")
    subjects = relationship("Subject", back_populates="department")


class Faculty(Base):
    __tablename__ = "faculty"

    faculty_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(30), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=False)
    designation = Column(String(50), nullable=False)
    experience_years = Column(Integer, nullable=False, default=1)
    specialization = Column(String(100))

    department = relationship("Department", back_populates="faculty")
    enrollments = relationship("Enrollment", back_populates="faculty")


class Semester(Base):
    __tablename__ = "semesters"

    semester_id = Column(Integer, primary_key=True, index=True)
    academic_year = Column(String(20), nullable=False)
    semester_number = Column(Integer, nullable=False)
    semester_name = Column(String(50), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)

    enrollments = relationship("Enrollment", back_populates="semester")
    marks = relationship("Mark", back_populates="semester")
    attendance = relationship("Attendance", back_populates="semester")


class Subject(Base):
    __tablename__ = "subjects"

    subject_id = Column(Integer, primary_key=True, index=True)
    subject_code = Column(String(30), nullable=False, unique=True, index=True)
    subject_name = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=False)
    credits = Column(Integer, nullable=False, default=4)
    semester = Column(Integer, nullable=False)
    subject_type = Column(String(20), nullable=False)

    department = relationship("Department", back_populates="subjects")
    enrollments = relationship("Enrollment", back_populates="subject")
    marks = relationship("Mark", back_populates="subject")
    attendance = relationship("Attendance", back_populates="subject")


class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)
    usn = Column(String(30), nullable=False, unique=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=False, index=True)
    admission_year = Column(Integer, nullable=False)
    current_year = Column(Integer, nullable=False)
    current_semester = Column(Integer, nullable=False, index=True)
    section = Column(String(5), nullable=False, default="A")
    cgpa = Column(Numeric(4, 2), nullable=False, default=0.0, index=True)
    backlogs = Column(Integer, nullable=False, default=0)
    city = Column(String(50), nullable=False)
    scholarship_status = Column(String(20), nullable=False, default="None")

    department = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")
    marks = relationship("Mark", back_populates="student")
    attendance = relationship("Attendance", back_populates="student")


class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.subject_id"), nullable=False, index=True)
    semester_id = Column(Integer, ForeignKey("semesters.semester_id"), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculty.faculty_id"))
    enrollment_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default="ACTIVE")

    student = relationship("Student", back_populates="enrollments")
    subject = relationship("Subject", back_populates="enrollments")
    semester = relationship("Semester", back_populates="enrollments")
    faculty = relationship("Faculty", back_populates="enrollments")


class Mark(Base):
    __tablename__ = "marks"

    mark_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.subject_id"), nullable=False, index=True)
    semester_id = Column(Integer, ForeignKey("semesters.semester_id"), nullable=False, index=True)
    internal_marks = Column(Numeric(5, 2), nullable=False)
    external_marks = Column(Numeric(5, 2), nullable=False)
    total_marks = Column(Numeric(5, 2), nullable=False, index=True)
    grade = Column(String(5), nullable=False)
    grade_point = Column(Numeric(4, 2), nullable=False)
    result_status = Column(String(10), nullable=False, index=True)

    student = relationship("Student", back_populates="marks")
    subject = relationship("Subject", back_populates="marks")
    semester = relationship("Semester", back_populates="marks")


class Attendance(Base):
    __tablename__ = "attendance"

    attendance_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.subject_id"), nullable=False, index=True)
    semester_id = Column(Integer, ForeignKey("semesters.semester_id"), nullable=False)
    classes_conducted = Column(Integer, nullable=False)
    classes_attended = Column(Integer, nullable=False)
    attendance_percentage = Column(Numeric(5, 2), nullable=False, index=True)
    attendance_status = Column(String(20), nullable=False)

    student = relationship("Student", back_populates="attendance")
    subject = relationship("Subject", back_populates="attendance")
    semester = relationship("Semester", back_populates="attendance")


class QueryHistory(Base):
    __tablename__ = "query_history"

    query_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), nullable=False, default="default_session", index=True)
    natural_language_question = Column(Text, nullable=False)
    intent = Column(String(50))
    detected_filters = Column(JSON, default=dict)
    generated_sql = Column(Text, nullable=False)
    execution_time_ms = Column(Numeric(10, 2), nullable=False, default=0.0)
    row_count = Column(Integer, nullable=False, default=0)
    explanation = Column(Text)
    error_message = Column(Text)
    status = Column(String(20), nullable=False, default="SUCCESS")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)
