# QueryMind Relational Database Architecture

## 1. Relational Schema Design

QueryMind operates on a realistic, multi-table university academic schema in PostgreSQL.

```
                           ┌──────────────┐
                           │ departments  │
                           └──────┬───────┘
                                  │
                 ┌────────────────┼────────────────┐
                 │                │                │
                 ▼                ▼                ▼
          ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
          │   faculty    │ │   students   │ │   subjects   │
          └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
                 │                │                │
                 └───────┐ ┌──────┼──────┐ ┌───────┘
                         ▼ ▼      ▼      ▼ ▼
                     ┌─────────┐  │  ┌─────────┐
                     │enroll-  │  │  │  marks  │
                     │  ments  │  │  └─────────┘
                     └─────────┘  │
                                  ▼
                            ┌───────────┐
                            │attendance │
                            └───────────┘
```

## 2. Table Specifications

### 2.1 `departments` (10 records)
- `department_id`: Primary Key (SERIAL)
- `department_name`: Full department name (VARCHAR 100)
- `department_code`: Abbreviated code (CSE, AIML, ISE, ECE, EEE, ME, CIVIL, DS, CS, IT)
- `hod_name`: Head of Department name
- `building`: Campus building location
- `contact_email`: Official departmental email

### 2.2 `faculty` (120 records)
- `faculty_id`: Primary Key (SERIAL)
- `employee_id`: Unique employee code (e.g., FAC_CSE_001)
- `first_name`, `last_name`: Personal name
- `department_id`: Foreign key -> `departments.department_id`
- `designation`: Professor, Associate Professor, Assistant Professor, Visiting Faculty
- `experience_years`: Years of academic experience (1 to 35)
- `specialization`: Academic domain

### 2.3 `subjects` (438 records)
- `subject_id`: Primary Key (SERIAL)
- `subject_code`: Unique course code (e.g., AIML501)
- `subject_name`: Course title (e.g., Machine Learning, Operating Systems)
- `department_id`: Foreign key -> `departments.department_id`
- `credits`: Academic credits (1 to 6)
- `semester`: Semester offered (1 to 8)
- `subject_type`: CORE, ELECTIVE, LAB

### 2.4 `semesters` (8 records)
- `semester_id`: Primary Key (SERIAL)
- `academic_year`: Academic session (e.g., 2023-24)
- `semester_number`: Semester index (1 through 8)
- `semester_name`: Semester display title
- `start_date`, `end_date`: Calendar bounds

### 2.5 `students` (5,200 records)
- `student_id`: Primary Key (SERIAL)
- `usn`: University Seat Number (e.g., 1MS22AIML042)
- `first_name`, `last_name`, `gender`, `date_of_birth`
- `email`, `phone`, `city`
- `department_id`: Foreign key -> `departments.department_id`
- `admission_year`: Year of admission (2021 to 2024)
- `current_year`: Academic year (1 to 4)
- `current_semester`: Active semester (1 to 8)
- `section`: Section assignment ('A', 'B', 'C')
- `cgpa`: Cumulative Grade Point Average (5.0 to 10.0 scale)
- `backlogs`: Number of active course backlogs (0 to 6)
- `scholarship_status`: 'None', 'Merit', 'Need-based', 'Sports'

### 2.6 `enrollments` (135,188 records)
- `enrollment_id`: Primary Key (SERIAL)
- `student_id`: Foreign key -> `students.student_id`
- `subject_id`: Foreign key -> `subjects.subject_id`
- `semester_id`: Foreign key -> `semesters.semester_id`
- `faculty_id`: Foreign key -> `faculty.faculty_id`
- `enrollment_date`: Enrollment timestamp
- `status`: 'ACTIVE', 'COMPLETED', 'DROPPED'

### 2.7 `marks` (135,188 records)
- `mark_id`: Primary Key (SERIAL)
- `student_id`: Foreign key -> `students.student_id`
- `subject_id`: Foreign key -> `subjects.subject_id`
- `semester_id`: Foreign key -> `semesters.semester_id`
- `internal_marks`: Continuous assessment (0.0 to 40.0)
- `external_marks`: Semester end exam (0.0 to 60.0)
- `total_marks`: Calculated sum = internal + external (0.0 to 100.0)
- `grade`: Letter grade ('O', 'A+', 'A', 'B+', 'B', 'C', 'P', 'F')
- `grade_point`: Grade point (10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 0.0)
- `result_status`: 'PASS' or 'FAIL'

### 2.8 `attendance` (135,188 records)
- `attendance_id`: Primary Key (SERIAL)
- `student_id`: Foreign key -> `students.student_id`
- `subject_id`: Foreign key -> `subjects.subject_id`
- `semester_id`: Foreign key -> `semesters.semester_id`
- `classes_conducted`: Total lecture sessions held (40 to 60)
- `classes_attended`: Lectures attended by student
- `attendance_percentage`: Calculated = (attended / conducted) * 100
- `attendance_status`: 'ELIGIBLE' (>=85%), 'WARNING' (75-84.9%), 'CONDONED' (65-74.9%), 'DETAINED' (<65%)

### 2.9 `query_history` (Audit Log)
- `query_id`: Primary Key (SERIAL)
- `session_id`: Client session ID
- `natural_language_question`: Original user text
- `intent`: Classified query intent
- `detected_filters`: JSON string of extracted filters
- `generated_sql`: Synthesized PostgreSQL query
- `execution_time_ms`: Execution time in milliseconds
- `row_count`: Number of records returned
- `explanation`: Generated natural language summary
- `status`: SUCCESS, ERROR, UNANSWERABLE
- `created_at`: Query execution timestamp

## 3. Database Indexes
- `idx_students_dept_cgpa` on `students(department_id, cgpa DESC)`
- `idx_marks_student_subject` on `marks(student_id, subject_id)`
- `idx_marks_total_grade` on `marks(total_marks DESC, grade)`
- `idx_attendance_student_subject` on `attendance(student_id, subject_id)`
- `idx_attendance_pct` on `attendance(attendance_percentage)`
- `idx_enrollments_student` on `enrollments(student_id, subject_id)`
