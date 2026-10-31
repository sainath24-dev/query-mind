#!/usr/bin/env python3
"""
QueryMind Synthetic Dataset Generator
Generates realistic university relational data and populates PostgreSQL.
Deterministic random seeding for reproducible benchmarks.
"""

import os
import sys
import random
import math
from datetime import date, timedelta
import psycopg2
from psycopg2.extras import execute_batch

# Set deterministic random seed
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "querymind")

FIRST_NAMES_MALE = [
    "Aarav", "Aditya", "Rohan", "Vikram", "Karthik", "Siddharth", "Rahul", "Nikhil",
    "Arjun", "Varun", "Abhishek", "Manish", "Gautam", "Pranav", "Harish", "Deepak",
    "Sachin", "Kunal", "Anand", "Rajesh", "Suraj", "Akash", "Vivek", "Suresh", "Manoj",
    "Dev", "Rishi", "Samar", "Kabir", "Dhruv", "Ayush", "Tanmay", "Yash", "Rajat", "Alok"
]

FIRST_NAMES_FEMALE = [
    "Priya", "Sneha", "Ananya", "Divya", "Pooja", "Kavya", "Deepika", "Shreya",
    "Meera", "Swati", "Neha", "Ritu", "Anushka", "Isha", "Tanvi", "Aditi",
    "Pavithra", "Lakshmi", "Bhavana", "Keerthi", "Nandini", "Aishwarya", "Shruti",
    "Preeti", "Rashmi", "Varsha", "Jyothi", "Sanjana", "Radhika", "Meenakshi"
]

LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Iyer", "Nair", "Rao", "Kulkarni", "Reddy", "Hegde",
    "Joshi", "Deshmukh", "Bhat", "Shenoy", "Shetty", "Prasad", "Gupta", "Menon",
    "Pillai", "Choudhury", "Mukherjee", "Banerjee", "Singh", "Das", "Bose", "Kumar",
    "Pai", "Kamath", "Acharya", "Pandey", "Mishra", "Naik", "Gowda", "Patil"
]

CITIES = [
    "Bangalore", "Mysore", "Mangalore", "Hubli", "Belgaum", "Shimoga", "Udupi",
    "Tumkur", "Davangere", "Chennai", "Hyderabad", "Mumbai", "Pune", "Delhi", "Coimbatore"
]

DEPARTMENTS_DATA = [
    ("Computer Science and Engineering", "CSE", "Dr. Ramesh Chandra", "Turing Block", "cse@univ.edu"),
    ("Artificial Intelligence and Machine Learning", "AIML", "Dr. Sangeetha Rao", "Shannon Hall", "aiml@univ.edu"),
    ("Information Science and Engineering", "ISE", "Dr. Prabhakar Murthy", "Lovelace Wing", "ise@univ.edu"),
    ("Electronics and Communication Engineering", "ECE", "Dr. K. V. Raman", "Maxwell Complex", "ece@univ.edu"),
    ("Electrical and Electronics Engineering", "EEE", "Dr. Meenakshi Sundaram", "Tesla Tower", "eee@univ.edu"),
    ("Mechanical Engineering", "ME", "Dr. Arvind Kulkarni", "Newton Pavilion", "me@univ.edu"),
    ("Civil Engineering", "CIVIL", "Dr. Visvesvaraya Sastry", "Smeaton Block", "civil@univ.edu"),
    ("Data Science", "DS", "Dr. Anand Joshi", "Shannon Hall", "ds@univ.edu"),
    ("Cyber Security", "CS", "Dr. Suresh Narayanan", "Turing Block", "cs@univ.edu"),
    ("Information Technology", "IT", "Dr. Rekha Hegde", "Lovelace Wing", "it@univ.edu"),
]

FACULTY_SPECIALIZATIONS = [
    "Distributed Systems", "Machine Learning", "Computer Vision", "Natural Language Processing",
    "Cryptography", "Database Internals", "Robotics & Controls", "VLSI Design",
    "Embedded Systems", "Power Electronics", "Structural Dynamics", "Big Data Analytics",
    "Cloud Computing", "Software Architecture", "Quantum Computing", "Deep Learning"
]

SUBJECT_TEMPLATES = [
    # Common Foundation (Sem 1-2)
    ("Mathematics - I", 4, 1, "CORE"),
    ("Engineering Physics", 4, 1, "CORE"),
    ("Basic Electrical Engineering", 3, 1, "CORE"),
    ("Elements of Civil Engineering", 3, 1, "CORE"),
    ("C Programming and Problem Solving", 4, 1, "CORE"),
    ("C Programming Lab", 2, 1, "LAB"),
    ("Mathematics - II", 4, 2, "CORE"),
    ("Engineering Chemistry", 4, 2, "CORE"),
    ("Basic Electronics Engineering", 3, 2, "CORE"),
    ("Elements of Mechanical Engineering", 3, 2, "CORE"),
    ("Data Structures and Algorithms", 4, 2, "CORE"),
    ("Data Structures Lab", 2, 2, "LAB"),

    # Sem 3-4 (CS / IT / AIML / DS / ISE)
    ("Database Management Systems", 4, 3, "CORE"),
    ("DBMS Laboratory", 2, 3, "LAB"),
    ("Computer Organization and Architecture", 4, 3, "CORE"),
    ("Discrete Mathematical Structures", 3, 3, "CORE"),
    ("Object Oriented Programming with Java", 4, 3, "CORE"),
    ("Operating Systems", 4, 4, "CORE"),
    ("Design and Analysis of Algorithms", 4, 4, "CORE"),
    ("Algorithms Lab", 2, 4, "LAB"),
    ("Microcontrollers and Embedded Systems", 3, 4, "CORE"),
    ("Theory of Computation", 3, 4, "CORE"),

    # Sem 5-6
    ("Computer Networks", 4, 5, "CORE"),
    ("Computer Networks Lab", 2, 5, "LAB"),
    ("Software Engineering", 3, 5, "CORE"),
    ("Machine Learning", 4, 5, "CORE"),
    ("Machine Learning Lab", 2, 5, "LAB"),
    ("Web Technology and Frameworks", 3, 5, "ELECTIVE"),
    ("Artificial Intelligence", 4, 6, "CORE"),
    ("Cloud Computing", 3, 6, "ELECTIVE"),
    ("Compiler Design", 4, 6, "CORE"),
    ("Cyber Security and Cryptography", 3, 6, "CORE"),
    ("Digital Image Processing", 3, 6, "ELECTIVE"),

    # Sem 7-8
    ("Deep Learning", 4, 7, "CORE"),
    ("Natural Language Processing", 4, 7, "ELECTIVE"),
    ("Big Data Analytics", 3, 7, "CORE"),
    ("Internet of Things", 3, 7, "ELECTIVE"),
    ("Computer Vision", 3, 7, "ELECTIVE"),
    ("Distributed Systems", 4, 8, "CORE"),
    ("Information Retrieval", 3, 8, "ELECTIVE"),
    ("Major Project and Viva", 6, 8, "CORE"),
]

# Department specific specialized subjects
DEPT_SPECIALIZED_SUBJECTS = {
    "AIML": [
        ("Reinforcement Learning", 4, 6, "CORE"),
        ("Neural Networks & Deep Architectures", 4, 6, "CORE"),
        ("Generative AI Systems", 3, 7, "ELECTIVE"),
        ("Speech and Audio Processing", 3, 8, "ELECTIVE")
    ],
    "DS": [
        ("Statistical Inference for Data Science", 4, 4, "CORE"),
        ("Data Mining and Warehousing", 4, 5, "CORE"),
        ("Predictive Analytics", 3, 6, "CORE"),
        ("Data Visualization and Storytelling", 3, 7, "ELECTIVE")
    ],
    "CS": [
        ("Ethical Hacking and Penetration Testing", 4, 5, "CORE"),
        ("Network Security Protocols", 4, 6, "CORE"),
        ("Digital Forensics", 3, 7, "ELECTIVE"),
        ("Blockchain and Smart Contracts", 3, 8, "ELECTIVE")
    ],
    "ECE": [
        ("Signals and Systems", 4, 3, "CORE"),
        ("Analog Circuit Design", 4, 4, "CORE"),
        ("Digital Signal Processing", 4, 5, "CORE"),
        ("VLSI Design and Verification", 4, 6, "CORE")
    ],
    "EEE": [
        ("Electric Machines - I", 4, 3, "CORE"),
        ("Power Systems Engineering", 4, 4, "CORE"),
        ("Control Systems Engineering", 4, 5, "CORE"),
        ("Power Electronics and Drives", 4, 6, "CORE")
    ],
    "ME": [
        ("Mechanics of Materials", 4, 3, "CORE"),
        ("Thermodynamics", 4, 4, "CORE"),
        ("Fluid Mechanics and Machinery", 4, 5, "CORE"),
        ("Finite Element Analysis", 4, 6, "CORE")
    ],
    "CIVIL": [
        ("Surveying and Geomatics", 4, 3, "CORE"),
        ("Strength of Materials", 4, 4, "CORE"),
        ("Structural Analysis", 4, 5, "CORE"),
        ("Transportation Engineering", 4, 6, "CORE")
    ],
}


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        dbname=DB_NAME
    )


def calculate_grade(total_marks, internal_marks, external_marks):
    # Pass criteria: total >= 40, external >= 21 (out of 60), internal >= 16 (out of 40)
    is_pass = (total_marks >= 40.0) and (external_marks >= 21.0) and (internal_marks >= 16.0)
    if not is_pass or total_marks < 40.0:
        return "F", 0.0, "FAIL"
    elif total_marks >= 90.0:
        return "O", 10.0, "PASS"
    elif total_marks >= 80.0:
        return "A+", 9.0, "PASS"
    elif total_marks >= 70.0:
        return "A", 8.0, "PASS"
    elif total_marks >= 60.0:
        return "B+", 7.0, "PASS"
    elif total_marks >= 55.0:
        return "B", 6.0, "PASS"
    elif total_marks >= 50.0:
        return "C", 5.0, "PASS"
    else:
        return "P", 4.0, "PASS"


def main():
    print("=" * 70)
    print("QueryMind: Generating Synthetic Academic Relational Dataset")
    print("=" * 70)

    conn = get_db_connection()
    cur = conn.cursor()

    # 1. Clean existing data in dependency order
    print("[1/9] Cleaning existing tables...")
    cur.execute("""
        TRUNCATE TABLE attendance, marks, enrollments, subjects, faculty,
        students, semesters, departments, query_history RESTART IDENTITY CASCADE;
    """)
    conn.commit()

    # 2. Insert Departments
    print("[2/9] Generating 10 Departments...")
    dept_map = {} # code -> id
    for name, code, hod, bldg, email in DEPARTMENTS_DATA:
        cur.execute(
            """INSERT INTO departments (department_name, department_code, hod_name, building, contact_email)
               VALUES (%s, %s, %s, %s, %s) RETURNING department_id;""",
            (name, code, hod, bldg, email)
        )
        dept_id = cur.fetchone()[0]
        dept_map[code] = dept_id
    conn.commit()
    print(f"      Inserted {len(dept_map)} departments.")

    # 3. Insert Semesters (Multiple academic years, 1 to 8)
    print("[3/9] Generating Semesters...")
    academic_years = ["2022-23", "2023-24", "2024-25", "2025-26", "2026-27"]
    semester_ids = []
    sem_lookup = {} # (academic_year, sem_num) -> semester_id

    for yr in academic_years:
        for s_num in range(1, 9):
            sem_name = f"Semester {s_num}"
            start_m = 8 if s_num % 2 == 1 else 2
            end_m = 12 if s_num % 2 == 1 else 6
            y_start = int(yr.split("-")[0])
            start_dt = date(y_start if start_m == 8 else y_start + 1, start_m, 1)
            end_dt = date(y_start if start_m == 8 else y_start + 1, end_m, 28)

            cur.execute(
                """INSERT INTO semesters (academic_year, semester_number, semester_name, start_date, end_date)
                   VALUES (%s, %s, %s, %s, %s) RETURNING semester_id;""",
                (yr, s_num, sem_name, start_dt, end_dt)
            )
            s_id = cur.fetchone()[0]
            semester_ids.append(s_id)
            sem_lookup[(yr, s_num)] = s_id
    conn.commit()
    print(f"      Inserted {len(semester_ids)} semester periods.")

    # 4. Insert Faculty (120+ faculty across departments)
    print("[4/9] Generating 120 Faculty Members...")
    designations = ["Professor", "Associate Professor", "Assistant Professor", "Visiting Faculty"]
    desig_weights = [0.20, 0.35, 0.35, 0.10]
    faculty_records = []
    faculty_by_dept = {code: [] for code in dept_map}
    fac_counter = 1

    for code, dept_id in dept_map.items():
        # 12 faculty per department = 120 faculty
        for _ in range(12):
            is_female = random.random() < 0.45
            fn = random.choice(FIRST_NAMES_FEMALE if is_female else FIRST_NAMES_MALE)
            ln = random.choice(LAST_NAMES)
            emp_id = f"FAC{dept_id:02d}{fac_counter:04d}"
            email = f"{fn.lower()}.{ln.lower()}{fac_counter}@univ.edu"
            desig = random.choices(designations, weights=desig_weights)[0]
            exp = random.randint(12, 28) if desig == "Professor" else (
                random.randint(7, 15) if desig == "Associate Professor" else (
                    random.randint(2, 8) if desig == "Assistant Professor" else random.randint(1, 10)
                )
            )
            spec = random.choice(FACULTY_SPECIALIZATIONS)

            cur.execute(
                """INSERT INTO faculty (employee_id, first_name, last_name, email, department_id, designation, experience_years, specialization)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING faculty_id;""",
                (emp_id, fn, ln, email, dept_id, desig, exp, spec)
            )
            fac_id = cur.fetchone()[0]
            faculty_by_dept[code].append(fac_id)
            fac_counter += 1
    conn.commit()
    print(f"      Inserted {fac_counter - 1} faculty members.")

    # 5. Insert Subjects (Common + Dept Specific)
    print("[5/9] Generating 75+ Subjects...")
    subject_map = {} # subject_id -> (dept_id, semester, credits)
    dept_subjects = {code: [] for code in dept_map}
    subj_code_counter = 101

    # Base common core subjects
    for code, dept_id in dept_map.items():
        # Add general templates
        for title, credits, sem, stype in SUBJECT_TEMPLATES:
            # Differentiate code per department
            s_code = f"{code}{sem}{subj_code_counter:02d}"
            cur.execute(
                """INSERT INTO subjects (subject_code, subject_name, department_id, credits, semester, subject_type)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   ON CONFLICT (subject_code) DO NOTHING
                   RETURNING subject_id;""",
                (s_code, title, dept_id, credits, sem, stype)
            )
            res = cur.fetchone()
            if res:
                s_id = res[0]
                subject_map[s_id] = (dept_id, sem, credits)
                dept_subjects[code].append(s_id)
                subj_code_counter += 1

        # Add specialized department subjects
        if code in DEPT_SPECIALIZED_SUBJECTS:
            for title, credits, sem, stype in DEPT_SPECIALIZED_SUBJECTS[code]:
                s_code = f"{code}SP{subj_code_counter:02d}"
                cur.execute(
                    """INSERT INTO subjects (subject_code, subject_name, department_id, credits, semester, subject_type)
                       VALUES (%s, %s, %s, %s, %s, %s)
                       ON CONFLICT (subject_code) DO NOTHING
                       RETURNING subject_id;""",
                    (s_code, title, dept_id, credits, sem, stype)
                )
                res = cur.fetchone()
                if res:
                    s_id = res[0]
                    subject_map[s_id] = (dept_id, sem, credits)
                    dept_subjects[code].append(s_id)
                    subj_code_counter += 1

    conn.commit()
    print(f"      Inserted {len(subject_map)} distinct department subjects.")

    # 6. Generate 5,200 Students across Departments and Performance Profiles
    print("[6/9] Generating 5,200 Students with realistic performance profiles...")
    # Performance profiles:
    # 'high': 15% -> CGPA 8.5 - 9.8, backlogs 0
    # 'average': 55% -> CGPA 6.8 - 8.4, backlogs 0 or 1
    # 'struggling': 20% -> CGPA 5.0 - 6.7, backlogs 1 to 4
    # 'inconsistent': 10% -> CGPA 5.5 - 8.0, backlogs 0 to 2
    student_records = []
    student_metadata = {} # student_id -> (profile, dept_code, current_semester, cgpa)

    TOTAL_STUDENTS = 5200
    students_per_dept = TOTAL_STUDENTS // len(dept_map)

    stu_counter = 1
    profiles = ["high", "average", "struggling", "inconsistent"]
    profile_weights = [0.15, 0.55, 0.20, 0.10]
    scholarship_options = ["None", "Merit", "Need-based", "Sports"]

    for code, dept_id in dept_map.items():
        for i in range(students_per_dept):
            prof = random.choices(profiles, weights=profile_weights)[0]
            is_female = random.random() < 0.42
            fn = random.choice(FIRST_NAMES_FEMALE if is_female else FIRST_NAMES_MALE)
            ln = random.choice(LAST_NAMES)
            gender = "Female" if is_female else "Male"

            # Admission year between 2021 and 2024
            # Current year 1 (Sem 1-2), 2 (Sem 3-4), 3 (Sem 5-6), 4 (Sem 7-8)
            curr_year = random.choice([1, 2, 3, 4])
            curr_sem = curr_year * 2 - random.choice([0, 1])
            adm_year = 2025 - curr_year

            # USN format: 1MS{YY}{DEPT}{NUM:03d}
            usn = f"1MS{str(adm_year)[-2:]}{code}{i+1:03d}"
            email = f"{fn.lower()}.{ln.lower()}{stu_counter}@student.univ.edu"
            phone = f"98{random.randint(10000000, 99999999)}"

            # DOB: roughly 18-23 years old
            age_days = random.randint(18 * 365, 23 * 365)
            dob = date(2025, 1, 1) - timedelta(days=age_days)
            sec = random.choice(["A", "B", "C"])
            city = random.choice(CITIES)

            # Profile-guided CGPA & backlogs
            if prof == "high":
                cgpa = round(random.uniform(8.50, 9.85), 2)
                backlogs = 0
                scholarship = "Merit" if random.random() < 0.45 else "None"
            elif prof == "average":
                cgpa = round(random.uniform(6.80, 8.45), 2)
                backlogs = 1 if random.random() < 0.15 else 0
                scholarship = random.choice(["None", "None", "Need-based", "Sports"])
            elif prof == "struggling":
                cgpa = round(random.uniform(5.00, 6.75), 2)
                backlogs = random.choices([1, 2, 3, 4], weights=[0.4, 0.3, 0.2, 0.1])[0]
                scholarship = "None"
            else: # inconsistent
                cgpa = round(random.uniform(5.80, 8.20), 2)
                backlogs = random.choice([0, 1, 2])
                scholarship = "None"

            student_records.append((
                usn, fn, ln, gender, dob, email, phone, dept_id,
                adm_year, curr_year, curr_sem, sec, cgpa, backlogs, city, scholarship
            ))
            stu_counter += 1

    # Batch insert students
    student_insert_query = """
        INSERT INTO students (
            usn, first_name, last_name, gender, date_of_birth, email, phone,
            department_id, admission_year, current_year, current_semester,
            section, cgpa, backlogs, city, scholarship_status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING student_id, usn, department_id, current_semester, cgpa;
    """
    execute_batch(cur, student_insert_query, student_records, page_size=1000)
    conn.commit()

    # Re-query all inserted students for relations
    cur.execute("SELECT student_id, department_id, current_semester, cgpa FROM students;")
    students_db = cur.fetchall()
    print(f"      Inserted {len(students_db)} students.")

    # 7. Generate Enrollments, Marks, and Attendance Records
    # To meet >30,000 enrollments and >100,000 marks and >100,000 attendance records:
    # Every student enrolls in subjects for completed semesters + current semester.
    # An average student in Sem 4 has 4 semesters * ~6 subjects = 24 enrollments/marks.
    # 5,200 * ~22 subjects = ~114,000 records!
    print("[7/9] Generating 110,000+ Enrollments, Marks, and Attendance records...")

    # Organize subjects by (department_id, semester)
    subjects_by_dept_sem = {}
    for s_id, (d_id, sem, cred) in subject_map.items():
        subjects_by_dept_sem.setdefault((d_id, sem), []).append(s_id)

    # Department code by id lookup
    dept_id_to_code = {v: k for k, v in dept_map.items()}

    enrollment_batch = []
    marks_batch = []
    attendance_batch = []

    for s_idx, (stu_id, d_id, curr_sem, cgpa) in enumerate(students_db):
        dept_code = dept_id_to_code[d_id]
        fac_pool = faculty_by_dept.get(dept_code, [])

        # Quality factor derived from CGPA
        perf_factor = (float(cgpa) - 4.5) / 5.5 # scale roughly 0.0 to 1.0

        # Enrolls in semesters 1 up to curr_sem
        for sem_num in range(1, curr_sem + 1):
            # Select corresponding semester_id (e.g. 2023-24 or 2024-25)
            # Find an academic year appropriate for this semester
            acad_yr = "2023-24" if sem_num <= 4 else "2024-25"
            sem_id = sem_lookup.get((acad_yr, sem_num), semester_ids[0])

            subjs = subjects_by_dept_sem.get((d_id, sem_num), [])
            # Pick 4 to 6 subjects for this semester
            for subj_id in subjs:
                fac_id = random.choice(fac_pool) if fac_pool else None
                status = "COMPLETED" if sem_num < curr_sem else "ACTIVE"
                enr_date = date(2023 + (sem_num // 3), 8 if sem_num % 2 == 1 else 2, random.randint(1, 20))

                enrollment_batch.append((
                    stu_id, subj_id, sem_id, fac_id, enr_date, status
                ))

                # Marks generation (aligned with student's academic profile)
                # Base marks mean determined by perf_factor
                target_score = 42 + perf_factor * 50 # 42 to 92
                # Subject specific variation
                actual_total = max(25.0, min(99.0, random.gauss(target_score, 7.5)))
                
                # Split total into internal (0-40, roughly 40%) and external (0-60, roughly 60%)
                internal = round(min(40.0, max(10.0, actual_total * 0.40 + random.gauss(0, 2.0))), 2)
                external = round(min(60.0, max(12.0, actual_total - internal)), 2)
                total = round(internal + external, 2)

                grade, grade_pt, res_status = calculate_grade(total, internal, external)

                marks_batch.append((
                    stu_id, subj_id, sem_id, internal, external, total, grade, grade_pt, res_status
                ))

                # Attendance generation (aligned with student's profile)
                # Classes conducted 50-60
                conducted = random.randint(52, 62)
                base_pct = 60.0 + perf_factor * 35.0 # 60% to 95%
                actual_pct = max(45.0, min(98.5, random.gauss(base_pct, 6.0)))
                attended = min(conducted, int(round((actual_pct / 100.0) * conducted)))
                final_pct = round((attended / conducted) * 100.0, 2)

                if final_pct >= 85.0:
                    att_status = "ELIGIBLE"
                elif final_pct >= 75.0:
                    att_status = "WARNING"
                elif final_pct >= 65.0:
                    att_status = "CONDONED"
                else:
                    att_status = "DETAINED"

                attendance_batch.append((
                    stu_id, subj_id, sem_id, conducted, attended, final_pct, att_status
                ))

        if (s_idx + 1) % 1000 == 0:
            print(f"      Processed {s_idx + 1} students ({len(enrollment_batch)} enrollments queued)...")

    # Fast bulk insertion using execute_batch
    print("[8/9] Writing records to PostgreSQL...")
    print(f"      Inserting {len(enrollment_batch)} enrollments...")
    execute_batch(cur, """
        INSERT INTO enrollments (student_id, subject_id, semester_id, faculty_id, enrollment_date, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (student_id, subject_id, semester_id) DO NOTHING;
    """, enrollment_batch, page_size=2000)
    conn.commit()

    print(f"      Inserting {len(marks_batch)} marks records...")
    execute_batch(cur, """
        INSERT INTO marks (student_id, subject_id, semester_id, internal_marks, external_marks, total_marks, grade, grade_point, result_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (student_id, subject_id, semester_id) DO NOTHING;
    """, marks_batch, page_size=2000)
    conn.commit()

    print(f"      Inserting {len(attendance_batch)} attendance records...")
    execute_batch(cur, """
        INSERT INTO attendance (student_id, subject_id, semester_id, classes_conducted, classes_attended, attendance_percentage, attendance_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (student_id, subject_id, semester_id) DO NOTHING;
    """, attendance_batch, page_size=2000)
    conn.commit()

    # 8. Recalculate and synchronize actual CGPA and backlogs for integrity
    print("[9/9] Synchronizing student CGPA and backlog counters with marks...")
    cur.execute("""
        WITH student_stats AS (
            SELECT
                student_id,
                ROUND(AVG(grade_point), 2) as computed_cgpa,
                COUNT(*) FILTER (WHERE result_status = 'FAIL') as computed_backlogs
            FROM marks
            GROUP BY student_id
        )
        UPDATE students s
        SET
            cgpa = COALESCE(ss.computed_cgpa, s.cgpa),
            backlogs = COALESCE(ss.computed_backlogs, 0)
        FROM student_stats ss
        WHERE s.student_id = ss.student_id;
    """)
    conn.commit()

    # 9. Verify and print comprehensive summary statistics
    print("\n" + "=" * 70)
    print("DATA GENERATION COMPLETE — VALIDATING DATABASE METRICS")
    print("=" * 70)

    cur.execute("SELECT COUNT(*) FROM students;")
    count_students = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM departments;")
    count_depts = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM faculty;")
    count_faculty = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM subjects;")
    count_subjects = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM enrollments;")
    count_enrollments = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM marks;")
    count_marks = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM attendance;")
    count_attendance = cur.fetchone()[0]

    cur.execute("SELECT ROUND(AVG(cgpa), 2) FROM students;")
    avg_cgpa = cur.fetchone()[0]

    cur.execute("SELECT ROUND(AVG(attendance_percentage), 2) FROM attendance;")
    avg_attendance = cur.fetchone()[0]

    cur.execute("""
        SELECT ROUND((COUNT(*) FILTER (WHERE result_status = 'PASS')::numeric / COUNT(*)) * 100, 2)
        FROM marks;
    """)
    pass_pct = cur.fetchone()[0]

    print(f"Students:           {count_students:,}")
    print(f"Departments:        {count_depts}")
    print(f"Faculty:            {count_faculty}")
    print(f"Subjects:           {count_subjects}")
    print(f"Enrollments:        {count_enrollments:,}")
    print(f"Marks:              {count_marks:,}")
    print(f"Attendance Records: {count_attendance:,}")
    print("-" * 70)
    print(f"Average CGPA:       {avg_cgpa}")
    print(f"Average Attendance: {avg_attendance}%")
    print(f"Pass Percentage:    {pass_pct}%")
    print("-" * 70)

    # Department-wise student count and average CGPA
    print("DEPARTMENT-WISE METRICS:")
    cur.execute("""
        SELECT d.department_code, d.department_name, COUNT(s.student_id), ROUND(AVG(s.cgpa), 2)
        FROM departments d
        LEFT JOIN students s ON d.department_id = s.department_id
        GROUP BY d.department_id, d.department_code, d.department_name
        ORDER BY d.department_code;
    """)
    for row in cur.fetchall():
        print(f"  {row[0]:<6} | {row[1]:<45} | Students: {row[2]:>4} | Avg CGPA: {row[3]}")

    print("-" * 70)
    print("TOP 10 STUDENTS OVERALL:")
    cur.execute("""
        SELECT s.usn, s.first_name || ' ' || s.last_name, d.department_code, s.cgpa, s.current_semester
        FROM students s
        JOIN departments d ON s.department_id = d.department_id
        ORDER BY s.cgpa DESC
        LIMIT 10;
    """)
    for rank, row in enumerate(cur.fetchall(), 1):
        print(f"  #{rank:>2} | {row[0]} | {row[1]:<25} | {row[2]:<6} | Sem: {row[4]} | CGPA: {row[3]}")

    print("=" * 70)
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
