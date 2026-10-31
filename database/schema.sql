-- ==============================================================================
-- QueryMind — Relational Database Schema
-- Academic University Management System
-- ==============================================================================

-- Drop tables if re-initializing in order of foreign key dependencies
DROP TABLE IF EXISTS attendance CASCADE;
DROP TABLE IF EXISTS marks CASCADE;
DROP TABLE IF EXISTS enrollments CASCADE;
DROP TABLE IF EXISTS subjects CASCADE;
DROP TABLE IF EXISTS faculty CASCADE;
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS semesters CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
DROP TABLE IF EXISTS query_history CASCADE;

-- 1. DEPARTMENTS
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    department_code VARCHAR(20) NOT NULL UNIQUE,
    hod_name VARCHAR(100) NOT NULL,
    building VARCHAR(50) DEFAULT 'Main Academic Block',
    contact_email VARCHAR(100)
);

-- 2. FACULTY
CREATE TABLE faculty (
    faculty_id SERIAL PRIMARY KEY,
    employee_id VARCHAR(30) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    department_id INTEGER NOT NULL REFERENCES departments(department_id) ON DELETE RESTRICT,
    designation VARCHAR(50) NOT NULL CHECK (designation IN ('Professor', 'Associate Professor', 'Assistant Professor', 'Visiting Faculty')),
    experience_years INTEGER NOT NULL DEFAULT 1 CHECK (experience_years >= 0),
    specialization VARCHAR(100)
);

-- 3. SEMESTERS
CREATE TABLE semesters (
    semester_id SERIAL PRIMARY KEY,
    academic_year VARCHAR(20) NOT NULL, -- e.g. '2023-24'
    semester_number INTEGER NOT NULL CHECK (semester_number BETWEEN 1 AND 8),
    semester_name VARCHAR(50) NOT NULL,  -- e.g. 'Semester 1'
    start_date DATE,
    end_date DATE,
    CONSTRAINT uq_academic_year_sem UNIQUE (academic_year, semester_number)
);

-- 4. SUBJECTS
CREATE TABLE subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_code VARCHAR(30) NOT NULL UNIQUE,
    subject_name VARCHAR(100) NOT NULL,
    department_id INTEGER NOT NULL REFERENCES departments(department_id) ON DELETE RESTRICT,
    credits INTEGER NOT NULL DEFAULT 4 CHECK (credits BETWEEN 1 AND 6),
    semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 8),
    subject_type VARCHAR(20) NOT NULL CHECK (subject_type IN ('CORE', 'ELECTIVE', 'LAB'))
);

-- 5. STUDENTS
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    usn VARCHAR(30) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('Male', 'Female', 'Other')),
    date_of_birth DATE NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    department_id INTEGER NOT NULL REFERENCES departments(department_id) ON DELETE RESTRICT,
    admission_year INTEGER NOT NULL CHECK (admission_year >= 2018),
    current_year INTEGER NOT NULL CHECK (current_year BETWEEN 1 AND 4),
    current_semester INTEGER NOT NULL CHECK (current_semester BETWEEN 1 AND 8),
    section VARCHAR(5) NOT NULL DEFAULT 'A',
    cgpa NUMERIC(4, 2) NOT NULL DEFAULT 0.0 CHECK (cgpa BETWEEN 0.0 AND 10.0),
    backlogs INTEGER NOT NULL DEFAULT 0 CHECK (backlogs >= 0),
    city VARCHAR(50) NOT NULL,
    scholarship_status VARCHAR(20) NOT NULL DEFAULT 'None' CHECK (scholarship_status IN ('None', 'Merit', 'Need-based', 'Sports'))
);

-- 6. ENROLLMENTS
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    subject_id INTEGER NOT NULL REFERENCES subjects(subject_id) ON DELETE RESTRICT,
    semester_id INTEGER NOT NULL REFERENCES semesters(semester_id) ON DELETE RESTRICT,
    faculty_id INTEGER REFERENCES faculty(faculty_id) ON DELETE SET NULL,
    enrollment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'COMPLETED', 'DROPPED')),
    CONSTRAINT uq_student_subject_sem UNIQUE (student_id, subject_id, semester_id)
);

-- 7. MARKS
CREATE TABLE marks (
    mark_id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    subject_id INTEGER NOT NULL REFERENCES subjects(subject_id) ON DELETE RESTRICT,
    semester_id INTEGER NOT NULL REFERENCES semesters(semester_id) ON DELETE RESTRICT,
    internal_marks NUMERIC(5, 2) NOT NULL CHECK (internal_marks BETWEEN 0.0 AND 40.0),
    external_marks NUMERIC(5, 2) NOT NULL CHECK (external_marks BETWEEN 0.0 AND 60.0),
    total_marks NUMERIC(5, 2) NOT NULL CHECK (total_marks BETWEEN 0.0 AND 100.0),
    grade VARCHAR(5) NOT NULL CHECK (grade IN ('O', 'A+', 'A', 'B+', 'B', 'C', 'P', 'F')),
    grade_point NUMERIC(4, 2) NOT NULL CHECK (grade_point BETWEEN 0.0 AND 10.0),
    result_status VARCHAR(10) NOT NULL CHECK (result_status IN ('PASS', 'FAIL')),
    CONSTRAINT uq_marks_student_subject_sem UNIQUE (student_id, subject_id, semester_id)
);

-- 8. ATTENDANCE
CREATE TABLE attendance (
    attendance_id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    subject_id INTEGER NOT NULL REFERENCES subjects(subject_id) ON DELETE RESTRICT,
    semester_id INTEGER NOT NULL REFERENCES semesters(semester_id) ON DELETE RESTRICT,
    classes_conducted INTEGER NOT NULL CHECK (classes_conducted > 0),
    classes_attended INTEGER NOT NULL CHECK (classes_attended >= 0 AND classes_attended <= classes_conducted),
    attendance_percentage NUMERIC(5, 2) NOT NULL CHECK (attendance_percentage BETWEEN 0.0 AND 100.0),
    attendance_status VARCHAR(20) NOT NULL CHECK (attendance_status IN ('ELIGIBLE', 'DETAINED', 'WARNING', 'CONDONED')),
    CONSTRAINT uq_attendance_student_subject_sem UNIQUE (student_id, subject_id, semester_id)
);

-- 9. QUERY HISTORY
CREATE TABLE query_history (
    query_id SERIAL PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL DEFAULT 'default_session',
    natural_language_question TEXT NOT NULL,
    intent VARCHAR(50),
    detected_filters JSONB DEFAULT '{}'::jsonb,
    generated_sql TEXT NOT NULL,
    execution_time_ms NUMERIC(10, 2) NOT NULL DEFAULT 0.0,
    row_count INTEGER NOT NULL DEFAULT 0,
    explanation TEXT,
    error_message TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'SUCCESS' CHECK (status IN ('SUCCESS', 'ERROR')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================================================
-- INDEXES FOR OPTIMAL QUERY PERFORMANCE
-- ==============================================================================
CREATE INDEX idx_students_dept ON students(department_id);
CREATE INDEX idx_students_cgpa ON students(cgpa DESC);
CREATE INDEX idx_students_sem ON students(current_semester);
CREATE INDEX idx_students_year ON students(current_year);
CREATE INDEX idx_students_usn ON students(usn);
CREATE INDEX idx_students_city ON students(city);

CREATE INDEX idx_faculty_dept ON faculty(department_id);
CREATE INDEX idx_subjects_dept ON subjects(department_id);
CREATE INDEX idx_subjects_sem ON subjects(semester);
CREATE INDEX idx_subjects_code ON subjects(subject_code);

CREATE INDEX idx_enrollments_student ON enrollments(student_id);
CREATE INDEX idx_enrollments_subject ON enrollments(subject_id);
CREATE INDEX idx_enrollments_faculty ON enrollments(faculty_id);

CREATE INDEX idx_marks_student ON marks(student_id);
CREATE INDEX idx_marks_subject ON marks(subject_id);
CREATE INDEX idx_marks_semester ON marks(semester_id);
CREATE INDEX idx_marks_total ON marks(total_marks);
CREATE INDEX idx_marks_status ON marks(result_status);

CREATE INDEX idx_attendance_student ON attendance(student_id);
CREATE INDEX idx_attendance_subject ON attendance(subject_id);
CREATE INDEX idx_attendance_pct ON attendance(attendance_percentage);
CREATE INDEX idx_attendance_status ON attendance(attendance_status);

CREATE INDEX idx_query_history_created ON query_history(created_at DESC);
CREATE INDEX idx_query_history_session ON query_history(session_id);

-- ==============================================================================
-- SECURITY: READ-ONLY DATABASE USER CONFIGURATION
-- ==============================================================================
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'querymind_readonly') THEN
        CREATE ROLE querymind_readonly WITH LOGIN PASSWORD 'readonly_secure_pass';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE querymind TO querymind_readonly;
GRANT USAGE ON SCHEMA public TO querymind_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO querymind_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO querymind_readonly;

-- Revoke dangerous permissions explicitly from read-only user
REVOKE CREATE ON SCHEMA public FROM querymind_readonly;
REVOKE INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER ON ALL TABLES IN SCHEMA public FROM querymind_readonly;
