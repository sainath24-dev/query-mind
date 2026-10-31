#!/usr/bin/env python3
"""
Generates the 100-Question Comprehensive NLP Benchmark Dataset for QueryMind.
Covers Complexity Levels 1 through 8, Edge Cases, Out-of-Scope Detection, and Security Safety.
Saves structured JSON to data/evaluation_dataset.json.
"""

import os
import json

EVALUATION_QUESTIONS = [
    # =========================================================================
    # LEVEL 1 — SIMPLE (10 queries)
    # =========================================================================
    {
        "id": 1,
        "complexity_level": "LEVEL 1 — SIMPLE",
        "question": "What is the total number of students?",
        "expected_intent": "COUNT",
        "expected_tables": ["students"],
        "expected_columns": ["students.student_id"],
        "expected_sql_pattern": "SELECT COUNT(*) FROM students;"
    },
    {
        "id": 2,
        "complexity_level": "LEVEL 1 — SIMPLE",
        "question": "How many departments are there?",
        "expected_intent": "COUNT",
        "expected_tables": ["departments"],
        "expected_columns": ["departments.department_id"],
        "expected_sql_pattern": "SELECT COUNT(*) FROM departments;"
    },
    {
        "id": 3,
        "complexity_level": "LEVEL 1 — SIMPLE",
        "question": "Show all departments.",
        "expected_intent": "FILTER",
        "expected_tables": ["departments"],
        "expected_columns": ["departments.department_code", "departments.department_name"],
        "expected_sql_pattern": "SELECT department_code, department_name, hod_name FROM departments;"
    },
    {
        "id": 4,
        "complexity_level": "LEVEL 1 — SIMPLE",
        "question": "How many faculty members are there?",
        "expected_intent": "COUNT",
        "expected_tables": ["faculty"],
        "expected_columns": ["faculty.faculty_id"],
        "expected_sql_pattern": "SELECT COUNT(*) FROM faculty;"
    },
    {
        "id": 5,
        "complexity_level": "LEVEL 1 — SIMPLE",
        "question": "What is the overall average CGPA of students?",
        "expected_intent": "AVERAGE",
        "expected_tables": ["students"],
        "expected_columns": ["students.cgpa"],
        "expected_sql_pattern": "SELECT ROUND(AVG(cgpa), 2) FROM students;"
    },
    {
        "id": 6,
        "complexity_level": "LEVEL 1 — SIMPLE",
        "question": "What is the average attendance of students?",
        "expected_intent": "AVERAGE",
        "expected_tables": ["attendance"],
        "expected_columns": ["attendance.attendance_percentage"],
        "expected_sql_pattern": "SELECT ROUND(AVG(attendance_percentage), 2) FROM attendance;"
    },
    {
        "id": 7,
        "complexity_level": "LEVEL 1 — SIMPLE",
        "question": "How many total subjects are offered?",
        "expected_intent": "COUNT",
        "expected_tables": ["subjects"],
        "expected_columns": ["subjects.subject_id"],
        "expected_sql_pattern": "SELECT COUNT(*) FROM subjects;"
    },
    {
        "id": 8,
        "complexity_level": "LEVEL 1 — SIMPLE",
        "question": "What is the maximum CGPA recorded?",
        "expected_intent": "MAXIMUM",
        "expected_tables": ["students"],
        "expected_columns": ["students.cgpa"],
        "expected_sql_pattern": "SELECT MAX(cgpa) FROM students;"
    },
    {
        "id": 9,
        "complexity_level": "LEVEL 1 — SIMPLE",
        "question": "What is the minimum attendance percentage?",
        "expected_intent": "MINIMUM",
        "expected_tables": ["attendance"],
        "expected_columns": ["attendance.attendance_percentage"],
        "expected_sql_pattern": "SELECT MIN(attendance_percentage) FROM attendance;"
    },
    {
        "id": 10,
        "complexity_level": "LEVEL 1 — SIMPLE",
        "question": "How many course enrollments exist?",
        "expected_intent": "COUNT",
        "expected_tables": ["enrollments"],
        "expected_columns": ["enrollments.enrollment_id"],
        "expected_sql_pattern": "SELECT COUNT(*) FROM enrollments;"
    },

    # =========================================================================
    # LEVEL 2 — FILTER (15 queries)
    # =========================================================================
    {
        "id": 11,
        "complexity_level": "LEVEL 2 — FILTER",
        "question": "Show all students from AIML.",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "departments"],
        "expected_columns": ["students.usn", "departments.department_code"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, s.cgpa FROM students s JOIN departments d ON s.department_id = d.department_id WHERE d.department_code = 'AIML';"
    },
    {
        "id": 12,
        "complexity_level": "LEVEL 2 — FILTER",
        "question": "Show all students from CSE.",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "departments"],
        "expected_columns": ["students.usn", "departments.department_code"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name FROM students s JOIN departments d ON s.department_id = d.department_id WHERE d.department_code = 'CSE';"
    },
    {
        "id": 13,
        "complexity_level": "LEVEL 2 — FILTER",
        "question": "Show students with CGPA above 8.",
        "expected_intent": "FILTER",
        "expected_tables": ["students"],
        "expected_columns": ["students.usn", "students.cgpa"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, s.cgpa FROM students s WHERE s.cgpa > 8.0;"
    },
    {
        "id": 14,
        "complexity_level": "LEVEL 2 — FILTER",
        "question": "Show students with CGPA above 9.",
        "expected_intent": "FILTER",
        "expected_tables": ["students"],
        "expected_columns": ["students.usn", "students.cgpa"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, s.cgpa FROM students s WHERE s.cgpa > 9.0;"
    },
    {
        "id": 15,
        "complexity_level": "LEVEL 2 — FILTER",
        "question": "Which students have attendance below 75%?",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "attendance"],
        "expected_columns": ["students.usn", "attendance.attendance_percentage"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, a.attendance_percentage FROM attendance a JOIN students s ON a.student_id = s.student_id WHERE a.attendance_percentage < 75.0;"
    },
    {
        "id": 16,
        "complexity_level": "LEVEL 2 — FILTER",
        "question": "How many students have attendance below 75%?",
        "expected_intent": "COUNT",
        "expected_tables": ["attendance"],
        "expected_columns": ["attendance.attendance_percentage"],
        "expected_sql_pattern": "SELECT COUNT(DISTINCT student_id) FROM attendance WHERE attendance_percentage < 75.0;"
    },
    {
        "id": 17,
        "complexity_level": "LEVEL 2 — FILTER",
        "question": "Find students who have more than one backlog.",
        "expected_intent": "FILTER",
        "expected_tables": ["students"],
        "expected_columns": ["students.usn", "students.backlogs"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, s.backlogs FROM students s WHERE s.backlogs > 1;"
    },
    {
        "id": 18,
        "complexity_level": "LEVEL 2 — FILTER",
        "question": "Show students who failed more than two subjects.",
        "expected_intent": "FILTER",
        "expected_tables": ["students"],
        "expected_columns": ["students.usn", "students.backlogs"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, s.backlogs FROM students s WHERE s.backlogs > 2;"
    },
    {
        "id": 19,
        "complexity_level": "LEVEL 2 — FILTER",
        "question": "Show students from Bangalore.",
        "expected_intent": "FILTER",
        "expected_tables": ["students"],
        "expected_columns": ["students.usn", "students.city"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, s.city FROM students s WHERE s.city = 'Bangalore';"
    },
    {
        "id": 20,
        "complexity_level": "LEVEL 2 — FILTER",
        "question": "Show students from Bangalore with CGPA above 8.",
        "expected_intent": "FILTER",
        "expected_tables": ["students"],
        "expected_columns": ["students.usn", "students.city", "students.cgpa"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, s.cgpa FROM students s WHERE s.city = 'Bangalore' AND s.cgpa > 8.0;"
    },
    {
        "id": 21,
        "complexity_level": "LEVEL 2 — FILTER",
        "question": "Show students with scholarship status Merit.",
        "expected_intent": "FILTER",
        "expected_tables": ["students"],
        "expected_columns": ["students.usn", "students.scholarship_status"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name FROM students s WHERE s.scholarship_status = 'Merit';"
    },
    {
        "id": 22,
        "complexity_level": "LEVEL 2 — FILTER",
        "question": "Show all students in semester 5.",
        "expected_intent": "FILTER",
        "expected_tables": ["students"],
        "expected_columns": ["students.usn", "students.current_semester"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name FROM students s WHERE s.current_semester = 5;"
    },
    {
        "id": 23,
        "complexity_level": "LEVEL 2 — FILTER",
        "question": "Show all students in 3rd year.",
        "expected_intent": "FILTER",
        "expected_tables": ["students"],
        "expected_columns": ["students.usn", "students.current_year"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name FROM students s WHERE s.current_year = 3;"
    },
    {
        "id": 24,
        "complexity_level": "LEVEL 2 — FILTER",
        "question": "Show all female students from Data Science.",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "departments"],
        "expected_columns": ["students.usn", "students.gender", "departments.department_code"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name FROM students s JOIN departments d ON s.department_id = d.department_id WHERE d.department_code = 'DS' AND s.gender = 'Female';"
    },
    {
        "id": 25,
        "complexity_level": "LEVEL 2 — FILTER",
        "question": "Show students admitted in the year 2023.",
        "expected_intent": "FILTER",
        "expected_tables": ["students"],
        "expected_columns": ["students.usn", "students.admission_year"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name FROM students s WHERE s.admission_year = 2023;"
    },

    # =========================================================================
    # LEVEL 3 — AGGREGATION (10 queries)
    # =========================================================================
    {
        "id": 26,
        "complexity_level": "LEVEL 3 — AGGREGATION",
        "question": "What is the average CGPA of AIML students?",
        "expected_intent": "AVERAGE",
        "expected_tables": ["students", "departments"],
        "expected_columns": ["students.cgpa", "departments.department_code"],
        "expected_sql_pattern": "SELECT ROUND(AVG(s.cgpa), 2) FROM students s JOIN departments d ON s.department_id = d.department_id WHERE d.department_code = 'AIML';"
    },
    {
        "id": 27,
        "complexity_level": "LEVEL 3 — AGGREGATION",
        "question": "What is the average CGPA of CSE students?",
        "expected_intent": "AVERAGE",
        "expected_tables": ["students", "departments"],
        "expected_columns": ["students.cgpa", "departments.department_code"],
        "expected_sql_pattern": "SELECT ROUND(AVG(s.cgpa), 2) FROM students s JOIN departments d ON s.department_id = d.department_id WHERE d.department_code = 'CSE';"
    },
    {
        "id": 28,
        "complexity_level": "LEVEL 3 — AGGREGATION",
        "question": "What is the average attendance of CSE department?",
        "expected_intent": "AVERAGE",
        "expected_tables": ["attendance", "students", "departments"],
        "expected_columns": ["attendance.attendance_percentage", "departments.department_code"],
        "expected_sql_pattern": "SELECT ROUND(AVG(a.attendance_percentage), 2) FROM attendance a JOIN students s ON a.student_id = s.student_id JOIN departments d ON s.department_id = d.department_id WHERE d.department_code = 'CSE';"
    },
    {
        "id": 29,
        "complexity_level": "LEVEL 3 — AGGREGATION",
        "question": "Show average marks in Machine Learning.",
        "expected_intent": "AVERAGE",
        "expected_tables": ["marks", "subjects"],
        "expected_columns": ["marks.total_marks", "subjects.subject_name"],
        "expected_sql_pattern": "SELECT ROUND(AVG(m.total_marks), 2) FROM marks m JOIN subjects sub ON m.subject_id = sub.subject_id WHERE sub.subject_name ILIKE '%Machine Learning%';"
    },
    {
        "id": 30,
        "complexity_level": "LEVEL 3 — AGGREGATION",
        "question": "What is the average marks in Data Structures?",
        "expected_intent": "AVERAGE",
        "expected_tables": ["marks", "subjects"],
        "expected_columns": ["marks.total_marks", "subjects.subject_name"],
        "expected_sql_pattern": "SELECT ROUND(AVG(m.total_marks), 2) FROM marks m JOIN subjects sub ON m.subject_id = sub.subject_id WHERE sub.subject_name ILIKE '%Data Structures%';"
    },
    {
        "id": 31,
        "complexity_level": "LEVEL 3 — AGGREGATION",
        "question": "What is the total number of credits across all core subjects?",
        "expected_intent": "SUM",
        "expected_tables": ["subjects"],
        "expected_columns": ["subjects.credits", "subjects.subject_type"],
        "expected_sql_pattern": "SELECT SUM(credits) FROM subjects WHERE subject_type = 'CORE';"
    },
    {
        "id": 32,
        "complexity_level": "LEVEL 3 — AGGREGATION",
        "question": "What is the highest internal mark scored in any subject?",
        "expected_intent": "MAXIMUM",
        "expected_tables": ["marks"],
        "expected_columns": ["marks.internal_marks"],
        "expected_sql_pattern": "SELECT MAX(internal_marks) FROM marks;"
    },
    {
        "id": 33,
        "complexity_level": "LEVEL 3 — AGGREGATION",
        "question": "What is the lowest external mark scored in semester exams?",
        "expected_intent": "MINIMUM",
        "expected_tables": ["marks"],
        "expected_columns": ["marks.external_marks"],
        "expected_sql_pattern": "SELECT MIN(external_marks) FROM marks;"
    },
    {
        "id": 34,
        "complexity_level": "LEVEL 3 — AGGREGATION",
        "question": "How many students are enrolled in AIML?",
        "expected_intent": "COUNT",
        "expected_tables": ["students", "departments"],
        "expected_columns": ["students.student_id", "departments.department_code"],
        "expected_sql_pattern": "SELECT COUNT(*) FROM students s JOIN departments d ON s.department_id = d.department_id WHERE d.department_code = 'AIML';"
    },
    {
        "id": 35,
        "complexity_level": "LEVEL 3 — AGGREGATION",
        "question": "How many professors are in the computer science department?",
        "expected_intent": "COUNT",
        "expected_tables": ["faculty", "departments"],
        "expected_columns": ["faculty.faculty_id", "departments.department_code"],
        "expected_sql_pattern": "SELECT COUNT(*) FROM faculty f JOIN departments d ON f.department_id = d.department_id WHERE d.department_code = 'CSE' AND f.designation = 'Professor';"
    },

    # =========================================================================
    # LEVEL 4 — GROUPING (15 queries)
    # =========================================================================
    {
        "id": 36,
        "complexity_level": "LEVEL 4 — GROUPING",
        "question": "How many students are enrolled in each department?",
        "expected_intent": "GROUP_BY",
        "expected_tables": ["departments", "students"],
        "expected_columns": ["departments.department_code", "students.student_id"],
        "expected_sql_pattern": "SELECT d.department_code, COUNT(s.student_id) FROM departments d LEFT JOIN students s ON d.department_id = s.department_id GROUP BY d.department_id, d.department_code;"
    },
    {
        "id": 37,
        "complexity_level": "LEVEL 4 — GROUPING",
        "question": "What is the average CGPA of each department?",
        "expected_intent": "GROUP_BY",
        "expected_tables": ["departments", "students"],
        "expected_columns": ["departments.department_code", "students.cgpa"],
        "expected_sql_pattern": "SELECT d.department_code, ROUND(AVG(s.cgpa), 2) FROM departments d JOIN students s ON d.department_id = s.department_id GROUP BY d.department_id, d.department_code;"
    },
    {
        "id": 38,
        "complexity_level": "LEVEL 4 — GROUPING",
        "question": "Show average CGPA by department.",
        "expected_intent": "GROUP_BY",
        "expected_tables": ["departments", "students"],
        "expected_columns": ["departments.department_code", "students.cgpa"],
        "expected_sql_pattern": "SELECT d.department_code, ROUND(AVG(s.cgpa), 2) FROM departments d JOIN students s ON d.department_id = s.department_id GROUP BY d.department_id, d.department_code ORDER BY 2 DESC;"
    },
    {
        "id": 39,
        "complexity_level": "LEVEL 4 — GROUPING",
        "question": "Show the average marks for each subject.",
        "expected_intent": "GROUP_BY",
        "expected_tables": ["subjects", "marks"],
        "expected_columns": ["subjects.subject_name", "marks.total_marks"],
        "expected_sql_pattern": "SELECT sub.subject_name, ROUND(AVG(m.total_marks), 2) FROM subjects sub JOIN marks m ON sub.subject_id = m.subject_id GROUP BY sub.subject_id, sub.subject_name ORDER BY 2 DESC;"
    },
    {
        "id": 40,
        "complexity_level": "LEVEL 4 — GROUPING",
        "question": "Show the number of students in each semester.",
        "expected_intent": "GROUP_BY",
        "expected_tables": ["students"],
        "expected_columns": ["students.current_semester", "students.student_id"],
        "expected_sql_pattern": "SELECT current_semester, COUNT(student_id) FROM students GROUP BY current_semester ORDER BY current_semester ASC;"
    },
    {
        "id": 41,
        "complexity_level": "LEVEL 4 — GROUPING",
        "question": "Show the distribution of grades in Machine Learning.",
        "expected_intent": "GROUP_BY",
        "expected_tables": ["marks", "subjects"],
        "expected_columns": ["marks.grade", "subjects.subject_name"],
        "expected_sql_pattern": "SELECT m.grade, COUNT(*) FROM marks m JOIN subjects sub ON m.subject_id = sub.subject_id WHERE sub.subject_name ILIKE '%Machine Learning%' GROUP BY m.grade ORDER BY 2 DESC;"
    },
    {
        "id": 42,
        "complexity_level": "LEVEL 4 — GROUPING",
        "question": "Show the distribution of grades in Data Structures.",
        "expected_intent": "GROUP_BY",
        "expected_tables": ["marks", "subjects"],
        "expected_columns": ["marks.grade", "subjects.subject_name"],
        "expected_sql_pattern": "SELECT m.grade, COUNT(*) FROM marks m JOIN subjects sub ON m.subject_id = sub.subject_id WHERE sub.subject_name ILIKE '%Data Structures%' GROUP BY m.grade ORDER BY 2 DESC;"
    },
    {
        "id": 43,
        "complexity_level": "LEVEL 4 — GROUPING",
        "question": "Show average marks by department.",
        "expected_intent": "GROUP_BY",
        "expected_tables": ["departments", "students", "marks"],
        "expected_columns": ["departments.department_code", "marks.total_marks"],
        "expected_sql_pattern": "SELECT d.department_code, ROUND(AVG(m.total_marks), 2) FROM departments d JOIN students s ON d.department_id = s.department_id JOIN marks m ON s.student_id = m.student_id GROUP BY d.department_id, d.department_code ORDER BY 2 DESC;"
    },
    {
        "id": 44,
        "complexity_level": "LEVEL 4 — GROUPING",
        "question": "Show student count by city.",
        "expected_intent": "GROUP_BY",
        "expected_tables": ["students"],
        "expected_columns": ["students.city", "students.student_id"],
        "expected_sql_pattern": "SELECT city, COUNT(student_id) FROM students GROUP BY city ORDER BY 2 DESC;"
    },
    {
        "id": 45,
        "complexity_level": "LEVEL 4 — GROUPING",
        "question": "Show count of faculty by designation.",
        "expected_intent": "GROUP_BY",
        "expected_tables": ["faculty"],
        "expected_columns": ["faculty.designation", "faculty.faculty_id"],
        "expected_sql_pattern": "SELECT designation, COUNT(faculty_id) FROM faculty GROUP BY designation ORDER BY 2 DESC;"
    },
    {
        "id": 46,
        "complexity_level": "LEVEL 4 — GROUPING",
        "question": "Show average attendance by department.",
        "expected_intent": "GROUP_BY",
        "expected_tables": ["departments", "students", "attendance"],
        "expected_columns": ["departments.department_code", "attendance.attendance_percentage"],
        "expected_sql_pattern": "SELECT d.department_code, ROUND(AVG(a.attendance_percentage), 2) FROM departments d JOIN students s ON d.department_id = s.department_id JOIN attendance a ON s.student_id = a.student_id GROUP BY d.department_id, d.department_code ORDER BY 2 DESC;"
    },
    {
        "id": 47,
        "complexity_level": "LEVEL 4 — GROUPING",
        "question": "Show pass and fail count in Machine Learning.",
        "expected_intent": "GROUP_BY",
        "expected_tables": ["marks", "subjects"],
        "expected_columns": ["marks.result_status", "subjects.subject_name"],
        "expected_sql_pattern": "SELECT m.result_status, COUNT(*) FROM marks m JOIN subjects sub ON m.subject_id = sub.subject_id WHERE sub.subject_name ILIKE '%Machine Learning%' GROUP BY m.result_status;"
    },
    {
        "id": 48,
        "complexity_level": "LEVEL 4 — GROUPING",
        "question": "Show student count by gender.",
        "expected_intent": "GROUP_BY",
        "expected_tables": ["students"],
        "expected_columns": ["students.gender", "students.student_id"],
        "expected_sql_pattern": "SELECT gender, COUNT(student_id) FROM students GROUP BY gender;"
    },
    {
        "id": 49,
        "complexity_level": "LEVEL 4 — GROUPING",
        "question": "Show number of subjects per department.",
        "expected_intent": "GROUP_BY",
        "expected_tables": ["departments", "subjects"],
        "expected_columns": ["departments.department_code", "subjects.subject_id"],
        "expected_sql_pattern": "SELECT d.department_code, COUNT(sub.subject_id) FROM departments d JOIN subjects sub ON d.department_id = sub.department_id GROUP BY d.department_id, d.department_code ORDER BY 2 DESC;"
    },
    {
        "id": 50,
        "complexity_level": "LEVEL 4 — GROUPING",
        "question": "Show average total marks per semester.",
        "expected_intent": "GROUP_BY",
        "expected_tables": ["semesters", "marks"],
        "expected_columns": ["semesters.semester_number", "marks.total_marks"],
        "expected_sql_pattern": "SELECT sem.semester_number, ROUND(AVG(m.total_marks), 2) FROM semesters sem JOIN marks m ON sem.semester_id = m.semester_id GROUP BY sem.semester_number ORDER BY sem.semester_number ASC;"
    },

    # =========================================================================
    # LEVEL 5 — RELATIONAL JOIN (15 queries)
    # =========================================================================
    {
        "id": 51,
        "complexity_level": "LEVEL 5 — JOIN",
        "question": "Show all AIML students who scored above 80 in Machine Learning.",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "departments", "marks", "subjects"],
        "expected_columns": ["students.usn", "departments.department_code", "marks.total_marks", "subjects.subject_name"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, m.total_marks FROM marks m JOIN students s ON m.student_id = s.student_id JOIN subjects sub ON m.subject_id = sub.subject_id JOIN departments d ON s.department_id = d.department_id WHERE sub.subject_name ILIKE '%Machine Learning%' AND m.total_marks > 80.0 AND d.department_code = 'AIML';"
    },
    {
        "id": 52,
        "complexity_level": "LEVEL 5 — JOIN",
        "question": "Show students who scored above 90 in Data Structures.",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "marks", "subjects"],
        "expected_columns": ["students.usn", "marks.total_marks", "subjects.subject_name"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, m.total_marks FROM marks m JOIN students s ON m.student_id = s.student_id JOIN subjects sub ON m.subject_id = sub.subject_id WHERE sub.subject_name ILIKE '%Data Structures%' AND m.total_marks > 90.0;"
    },
    {
        "id": 53,
        "complexity_level": "LEVEL 5 — JOIN",
        "question": "How many students scored above 90 in Data Structures?",
        "expected_intent": "COUNT",
        "expected_tables": ["marks", "subjects"],
        "expected_columns": ["marks.total_marks", "subjects.subject_name"],
        "expected_sql_pattern": "SELECT COUNT(*) FROM marks m JOIN subjects sub ON m.subject_id = sub.subject_id WHERE sub.subject_name ILIKE '%Data Structures%' AND m.total_marks > 90.0;"
    },
    {
        "id": 54,
        "complexity_level": "LEVEL 5 — JOIN",
        "question": "Show students who failed Machine Learning.",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "marks", "subjects"],
        "expected_columns": ["students.usn", "marks.result_status", "subjects.subject_name"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name FROM marks m JOIN students s ON m.student_id = s.student_id JOIN subjects sub ON m.subject_id = sub.subject_id WHERE sub.subject_name ILIKE '%Machine Learning%' AND (m.result_status = 'FAIL' OR m.total_marks < 40.0);"
    },
    {
        "id": 55,
        "complexity_level": "LEVEL 5 — JOIN",
        "question": "Show students who failed Operating Systems.",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "marks", "subjects"],
        "expected_columns": ["students.usn", "marks.result_status", "subjects.subject_name"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name FROM marks m JOIN students s ON m.student_id = s.student_id JOIN subjects sub ON m.subject_id = sub.subject_id WHERE sub.subject_name ILIKE '%Operating Systems%' AND m.result_status = 'FAIL';"
    },
    {
        "id": 56,
        "complexity_level": "LEVEL 5 — JOIN",
        "question": "Which faculty teaches the most students?",
        "expected_intent": "GROUP_BY",
        "expected_tables": ["faculty", "enrollments"],
        "expected_columns": ["faculty.first_name", "faculty.last_name", "enrollments.student_id"],
        "expected_sql_pattern": "SELECT f.first_name, f.last_name, COUNT(e.student_id) FROM faculty f JOIN enrollments e ON f.faculty_id = e.faculty_id GROUP BY f.faculty_id, f.first_name, f.last_name ORDER BY 3 DESC LIMIT 1;"
    },
    {
        "id": 57,
        "complexity_level": "LEVEL 5 — JOIN",
        "question": "Show students enrolled in Computer Networks.",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "enrollments", "subjects"],
        "expected_columns": ["students.usn", "subjects.subject_name"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN subjects sub ON e.subject_id = sub.subject_id WHERE sub.subject_name ILIKE '%Computer Networks%';"
    },
    {
        "id": 58,
        "complexity_level": "LEVEL 5 — JOIN",
        "question": "Show students taught by Professor Karthik in AIML.",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "enrollments", "faculty"],
        "expected_columns": ["students.usn", "faculty.first_name"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN faculty f ON e.faculty_id = f.faculty_id WHERE f.first_name ILIKE '%Karthik%';"
    },
    {
        "id": 59,
        "complexity_level": "LEVEL 5 — JOIN",
        "question": "Show CSE students who scored grade O in Database Management Systems.",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "departments", "marks", "subjects"],
        "expected_columns": ["students.usn", "marks.grade", "subjects.subject_name"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name FROM marks m JOIN students s ON m.student_id = s.student_id JOIN subjects sub ON m.subject_id = sub.subject_id JOIN departments d ON s.department_id = d.department_id WHERE sub.subject_name ILIKE '%Database Management Systems%' AND m.grade = 'O' AND d.department_code = 'CSE';"
    },
    {
        "id": 60,
        "complexity_level": "LEVEL 5 — JOIN",
        "question": "Show attendance percentage of students in Machine Learning.",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "attendance", "subjects"],
        "expected_columns": ["students.usn", "attendance.attendance_percentage", "subjects.subject_name"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, a.attendance_percentage FROM attendance a JOIN students s ON a.student_id = s.student_id JOIN subjects sub ON a.subject_id = sub.subject_id WHERE sub.subject_name ILIKE '%Machine Learning%';"
    },
    {
        "id": 61,
        "complexity_level": "LEVEL 5 — JOIN",
        "question": "Show faculty list along with their department names.",
        "expected_intent": "FILTER",
        "expected_tables": ["faculty", "departments"],
        "expected_columns": ["faculty.first_name", "faculty.last_name", "departments.department_name"],
        "expected_sql_pattern": "SELECT f.first_name, f.last_name, f.designation, d.department_name FROM faculty f JOIN departments d ON f.department_id = d.department_id;"
    },
    {
        "id": 62,
        "complexity_level": "LEVEL 5 — JOIN",
        "question": "Show subjects taught in semester 4 of AIML department.",
        "expected_intent": "FILTER",
        "expected_tables": ["subjects", "departments"],
        "expected_columns": ["subjects.subject_name", "departments.department_code"],
        "expected_sql_pattern": "SELECT sub.subject_code, sub.subject_name, sub.credits FROM subjects sub JOIN departments d ON sub.department_id = d.department_id WHERE d.department_code = 'AIML' AND sub.semester = 4;"
    },
    {
        "id": 63,
        "complexity_level": "LEVEL 5 — JOIN",
        "question": "Show students who have attendance status DETAINED in any course.",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "attendance"],
        "expected_columns": ["students.usn", "attendance.attendance_status"],
        "expected_sql_pattern": "SELECT DISTINCT s.usn, s.first_name, s.last_name FROM attendance a JOIN students s ON a.student_id = s.student_id WHERE a.attendance_status = 'DETAINED';"
    },
    {
        "id": 64,
        "complexity_level": "LEVEL 5 — JOIN",
        "question": "Show marks of student with USN 1MS22AIML042.",
        "expected_intent": "DETAIL_LOOKUP",
        "expected_tables": ["students", "marks", "subjects"],
        "expected_columns": ["students.usn", "marks.total_marks", "subjects.subject_name"],
        "expected_sql_pattern": "SELECT sub.subject_name, m.total_marks, m.grade FROM marks m JOIN students s ON m.student_id = s.student_id JOIN subjects sub ON m.subject_id = sub.subject_id WHERE s.usn = '1MS22AIML042';"
    },
    {
        "id": 65,
        "complexity_level": "LEVEL 5 — JOIN",
        "question": "Show attendance of student with USN 1MS22AIML042.",
        "expected_intent": "DETAIL_LOOKUP",
        "expected_tables": ["students", "attendance", "subjects"],
        "expected_columns": ["students.usn", "attendance.attendance_percentage"],
        "expected_sql_pattern": "SELECT sub.subject_name, a.attendance_percentage FROM attendance a JOIN students s ON a.student_id = s.student_id JOIN subjects sub ON a.subject_id = sub.subject_id WHERE s.usn = '1MS22AIML042';"
    },

    # =========================================================================
    # LEVEL 6 — MULTI-CONDITION (10 queries)
    # =========================================================================
    {
        "id": 66,
        "complexity_level": "LEVEL 6 — MULTI-CONDITION",
        "question": "Which students have both CGPA above 8.5 and attendance above 85%?",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "attendance"],
        "expected_columns": ["students.cgpa", "attendance.attendance_percentage"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, s.cgpa FROM students s JOIN attendance a ON s.student_id = a.student_id WHERE s.cgpa > 8.5 AND a.attendance_percentage > 85.0;"
    },
    {
        "id": 67,
        "complexity_level": "LEVEL 6 — MULTI-CONDITION",
        "question": "Show AIML students with CGPA above 8 and attendance above 85%.",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "departments", "attendance"],
        "expected_columns": ["students.cgpa", "departments.department_code", "attendance.attendance_percentage"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, s.cgpa FROM students s JOIN departments d ON s.department_id = d.department_id JOIN attendance a ON s.student_id = a.student_id WHERE d.department_code = 'AIML' AND s.cgpa > 8.0 AND a.attendance_percentage > 85.0;"
    },
    {
        "id": 68,
        "complexity_level": "LEVEL 6 — MULTI-CONDITION",
        "question": "Show CSE students from Bangalore with CGPA above 8.5.",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "departments"],
        "expected_columns": ["students.city", "students.cgpa", "departments.department_code"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, s.cgpa FROM students s JOIN departments d ON s.department_id = d.department_id WHERE d.department_code = 'CSE' AND s.city = 'Bangalore' AND s.cgpa > 8.5;"
    },
    {
        "id": 69,
        "complexity_level": "LEVEL 6 — MULTI-CONDITION",
        "question": "Which students have attendance below 75% and backlogs greater than 0?",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "attendance"],
        "expected_columns": ["attendance.attendance_percentage", "students.backlogs"],
        "expected_sql_pattern": "SELECT DISTINCT s.usn, s.first_name, s.last_name, s.backlogs FROM students s JOIN attendance a ON s.student_id = a.student_id WHERE a.attendance_percentage < 75.0 AND s.backlogs > 0;"
    },
    {
        "id": 70,
        "complexity_level": "LEVEL 6 — MULTI-CONDITION",
        "question": "Show 3rd year students from ISE with CGPA above 8.",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "departments"],
        "expected_columns": ["students.current_year", "departments.department_code", "students.cgpa"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, s.cgpa FROM students s JOIN departments d ON s.department_id = d.department_id WHERE d.department_code = 'ISE' AND s.current_year = 3 AND s.cgpa > 8.0;"
    },
    {
        "id": 71,
        "complexity_level": "LEVEL 6 — MULTI-CONDITION",
        "question": "Show faculty members from CSE with more than 10 years of experience.",
        "expected_intent": "FILTER",
        "expected_tables": ["faculty", "departments"],
        "expected_columns": ["faculty.experience_years", "departments.department_code"],
        "expected_sql_pattern": "SELECT f.first_name, f.last_name, f.experience_years FROM faculty f JOIN departments d ON f.department_id = d.department_id WHERE d.department_code = 'CSE' AND f.experience_years > 10;"
    },
    {
        "id": 72,
        "complexity_level": "LEVEL 6 — MULTI-CONDITION",
        "question": "Show students with zero backlogs and CGPA above 9.",
        "expected_intent": "FILTER",
        "expected_tables": ["students"],
        "expected_columns": ["students.backlogs", "students.cgpa"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, s.cgpa FROM students s WHERE s.backlogs = 0 AND s.cgpa > 9.0;"
    },
    {
        "id": 73,
        "complexity_level": "LEVEL 6 — MULTI-CONDITION",
        "question": "Show AIML students in section A with CGPA above 8.",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "departments"],
        "expected_columns": ["students.section", "departments.department_code", "students.cgpa"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name FROM students s JOIN departments d ON s.department_id = d.department_id WHERE d.department_code = 'AIML' AND s.section = 'A' AND s.cgpa > 8.0;"
    },
    {
        "id": 74,
        "complexity_level": "LEVEL 6 — MULTI-CONDITION",
        "question": "Show 4th year students who have merit scholarship.",
        "expected_intent": "FILTER",
        "expected_tables": ["students"],
        "expected_columns": ["students.current_year", "students.scholarship_status"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name FROM students s WHERE s.current_year = 4 AND s.scholarship_status = 'Merit';"
    },
    {
        "id": 75,
        "complexity_level": "LEVEL 6 — MULTI-CONDITION",
        "question": "Show students with internal marks above 35 and external marks above 50.",
        "expected_intent": "FILTER",
        "expected_tables": ["students", "marks"],
        "expected_columns": ["marks.internal_marks", "marks.external_marks"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, m.internal_marks, m.external_marks FROM marks m JOIN students s ON m.student_id = s.student_id WHERE m.internal_marks > 35.0 AND m.external_marks > 50.0;"
    },

    # =========================================================================
    # LEVEL 7 — RANKING & TOP N (15 queries)
    # =========================================================================
    {
        "id": 76,
        "complexity_level": "LEVEL 7 — RANKING",
        "question": "Who are the top 10 students by CGPA?",
        "expected_intent": "TOP_N",
        "expected_tables": ["students"],
        "expected_columns": ["students.usn", "students.cgpa"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, s.cgpa FROM students s ORDER BY s.cgpa DESC LIMIT 10;"
    },
    {
        "id": 77,
        "complexity_level": "LEVEL 7 — RANKING",
        "question": "Show the top 5 students in AIML.",
        "expected_intent": "TOP_N",
        "expected_tables": ["students", "departments"],
        "expected_columns": ["students.usn", "departments.department_code", "students.cgpa"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, s.cgpa FROM students s JOIN departments d ON s.department_id = d.department_id WHERE d.department_code = 'AIML' ORDER BY s.cgpa DESC LIMIT 5;"
    },
    {
        "id": 78,
        "complexity_level": "LEVEL 7 — RANKING",
        "question": "Give me the top 5 students from AIML.",
        "expected_intent": "TOP_N",
        "expected_tables": ["students", "departments"],
        "expected_columns": ["students.usn", "departments.department_code", "students.cgpa"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, s.cgpa FROM students s JOIN departments d ON s.department_id = d.department_id WHERE d.department_code = 'AIML' ORDER BY s.cgpa DESC LIMIT 5;"
    },
    {
        "id": 79,
        "complexity_level": "LEVEL 7 — RANKING",
        "question": "Show the top 10 students with the highest attendance.",
        "expected_intent": "TOP_N",
        "expected_tables": ["students", "attendance"],
        "expected_columns": ["students.usn", "attendance.attendance_percentage"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, a.attendance_percentage FROM attendance a JOIN students s ON a.student_id = s.student_id ORDER BY a.attendance_percentage DESC LIMIT 10;"
    },
    {
        "id": 80,
        "complexity_level": "LEVEL 7 — RANKING",
        "question": "Which department has the highest average CGPA?",
        "expected_intent": "MAXIMUM",
        "expected_tables": ["departments", "students"],
        "expected_columns": ["departments.department_code", "students.cgpa"],
        "expected_sql_pattern": "SELECT d.department_code, ROUND(AVG(s.cgpa), 2) FROM departments d JOIN students s ON d.department_id = s.department_id GROUP BY d.department_id, d.department_code ORDER BY 2 DESC LIMIT 1;"
    },
    {
        "id": 81,
        "complexity_level": "LEVEL 7 — RANKING",
        "question": "Which department has the lowest average CGPA?",
        "expected_intent": "MINIMUM",
        "expected_tables": ["departments", "students"],
        "expected_columns": ["departments.department_code", "students.cgpa"],
        "expected_sql_pattern": "SELECT d.department_code, ROUND(AVG(s.cgpa), 2) FROM departments d JOIN students s ON d.department_id = s.department_id GROUP BY d.department_id, d.department_code ORDER BY 2 ASC LIMIT 1;"
    },
    {
        "id": 82,
        "complexity_level": "LEVEL 7 — RANKING",
        "question": "Which department has the highest average attendance?",
        "expected_intent": "MAXIMUM",
        "expected_tables": ["departments", "students", "attendance"],
        "expected_columns": ["departments.department_code", "attendance.attendance_percentage"],
        "expected_sql_pattern": "SELECT d.department_code, ROUND(AVG(a.attendance_percentage), 2) FROM departments d JOIN students s ON d.department_id = s.department_id JOIN attendance a ON s.student_id = a.student_id GROUP BY d.department_id, d.department_code ORDER BY 2 DESC LIMIT 1;"
    },
    {
        "id": 83,
        "complexity_level": "LEVEL 7 — RANKING",
        "question": "Which subject has the lowest average marks?",
        "expected_intent": "MINIMUM",
        "expected_tables": ["subjects", "marks"],
        "expected_columns": ["subjects.subject_name", "marks.total_marks"],
        "expected_sql_pattern": "SELECT sub.subject_name, ROUND(AVG(m.total_marks), 2) FROM subjects sub JOIN marks m ON sub.subject_id = m.subject_id GROUP BY sub.subject_id, sub.subject_name ORDER BY 2 ASC LIMIT 1;"
    },
    {
        "id": 84,
        "complexity_level": "LEVEL 7 — RANKING",
        "question": "Which subject has the highest average marks?",
        "expected_intent": "MAXIMUM",
        "expected_tables": ["subjects", "marks"],
        "expected_columns": ["subjects.subject_name", "marks.total_marks"],
        "expected_sql_pattern": "SELECT sub.subject_name, ROUND(AVG(m.total_marks), 2) FROM subjects sub JOIN marks m ON sub.subject_id = m.subject_id GROUP BY sub.subject_id, sub.subject_name ORDER BY 2 DESC LIMIT 1;"
    },
    {
        "id": 85,
        "complexity_level": "LEVEL 7 — RANKING",
        "question": "Which semester has the highest average marks?",
        "expected_intent": "MAXIMUM",
        "expected_tables": ["semesters", "marks"],
        "expected_columns": ["semesters.semester_number", "marks.total_marks"],
        "expected_sql_pattern": "SELECT sem.semester_number, ROUND(AVG(m.total_marks), 2) FROM semesters sem JOIN marks m ON sem.semester_id = m.semester_id GROUP BY sem.semester_number ORDER BY 2 DESC LIMIT 1;"
    },
    {
        "id": 86,
        "complexity_level": "LEVEL 7 — RANKING",
        "question": "Top 3 students from CSE by CGPA.",
        "expected_intent": "TOP_N",
        "expected_tables": ["students", "departments"],
        "expected_columns": ["students.usn", "students.cgpa"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, s.cgpa FROM students s JOIN departments d ON s.department_id = d.department_id WHERE d.department_code = 'CSE' ORDER BY s.cgpa DESC LIMIT 3;"
    },
    {
        "id": 87,
        "complexity_level": "LEVEL 7 — RANKING",
        "question": "Top 5 students in Machine Learning exam.",
        "expected_intent": "TOP_N",
        "expected_tables": ["students", "marks", "subjects"],
        "expected_columns": ["students.usn", "marks.total_marks"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, m.total_marks FROM marks m JOIN students s ON m.student_id = s.student_id JOIN subjects sub ON m.subject_id = sub.subject_id WHERE sub.subject_name ILIKE '%Machine Learning%' ORDER BY m.total_marks DESC LIMIT 5;"
    },
    {
        "id": 88,
        "complexity_level": "LEVEL 7 — RANKING",
        "question": "Top 5 most experienced faculty members.",
        "expected_intent": "TOP_N",
        "expected_tables": ["faculty"],
        "expected_columns": ["faculty.first_name", "faculty.experience_years"],
        "expected_sql_pattern": "SELECT f.first_name, f.last_name, f.experience_years FROM faculty f ORDER BY f.experience_years DESC LIMIT 5;"
    },
    {
        "id": 89,
        "complexity_level": "LEVEL 7 — RANKING",
        "question": "Show the 10 lowest CGPA students.",
        "expected_intent": "TOP_N",
        "expected_tables": ["students"],
        "expected_columns": ["students.usn", "students.cgpa"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, s.cgpa FROM students s ORDER BY s.cgpa ASC LIMIT 10;"
    },
    {
        "id": 90,
        "complexity_level": "LEVEL 7 — RANKING",
        "question": "Show the 5 students with the lowest attendance.",
        "expected_intent": "TOP_N",
        "expected_tables": ["students", "attendance"],
        "expected_columns": ["students.usn", "attendance.attendance_percentage"],
        "expected_sql_pattern": "SELECT s.usn, s.first_name, s.last_name, a.attendance_percentage FROM attendance a JOIN students s ON a.student_id = s.student_id ORDER BY a.attendance_percentage ASC LIMIT 5;"
    },

    # =========================================================================
    # LEVEL 8 — COMPARISON (5 queries)
    # =========================================================================
    {
        "id": 91,
        "complexity_level": "LEVEL 8 — COMPARISON",
        "question": "Compare the average CGPA of AIML and CSE.",
        "expected_intent": "COMPARISON",
        "expected_tables": ["departments", "students"],
        "expected_columns": ["departments.department_code", "students.cgpa"],
        "expected_sql_pattern": "SELECT d.department_code, ROUND(AVG(s.cgpa), 2) FROM departments d JOIN students s ON d.department_id = s.department_id WHERE d.department_code IN ('AIML', 'CSE') GROUP BY d.department_id, d.department_code;"
    },
    {
        "id": 92,
        "complexity_level": "LEVEL 8 — COMPARISON",
        "question": "Compare average marks between CSE and AIML.",
        "expected_intent": "COMPARISON",
        "expected_tables": ["departments", "students", "marks"],
        "expected_columns": ["departments.department_code", "marks.total_marks"],
        "expected_sql_pattern": "SELECT d.department_code, ROUND(AVG(m.total_marks), 2) FROM departments d JOIN students s ON d.department_id = s.department_id JOIN marks m ON s.student_id = m.student_id WHERE d.department_code IN ('CSE', 'AIML') GROUP BY d.department_id, d.department_code;"
    },
    {
        "id": 93,
        "complexity_level": "LEVEL 8 — COMPARISON",
        "question": "Compare average attendance between CSE and ECE.",
        "expected_intent": "COMPARISON",
        "expected_tables": ["departments", "students", "attendance"],
        "expected_columns": ["departments.department_code", "attendance.attendance_percentage"],
        "expected_sql_pattern": "SELECT d.department_code, ROUND(AVG(a.attendance_percentage), 2) FROM departments d JOIN students s ON d.department_id = s.department_id JOIN attendance a ON s.student_id = a.student_id WHERE d.department_code IN ('CSE', 'ECE') GROUP BY d.department_id, d.department_code;"
    },
    {
        "id": 94,
        "complexity_level": "LEVEL 8 — COMPARISON",
        "question": "Compare student count between AIML and Data Science.",
        "expected_intent": "COMPARISON",
        "expected_tables": ["departments", "students"],
        "expected_columns": ["departments.department_code", "students.student_id"],
        "expected_sql_pattern": "SELECT d.department_code, COUNT(s.student_id) FROM departments d JOIN students s ON d.department_id = s.department_id WHERE d.department_code IN ('AIML', 'DS') GROUP BY d.department_id, d.department_code;"
    },
    {
        "id": 95,
        "complexity_level": "LEVEL 8 — COMPARISON",
        "question": "Compare average marks between Machine Learning and Deep Learning.",
        "expected_intent": "COMPARISON",
        "expected_tables": ["subjects", "marks"],
        "expected_columns": ["subjects.subject_name", "marks.total_marks"],
        "expected_sql_pattern": "SELECT sub.subject_name, ROUND(AVG(m.total_marks), 2) FROM subjects sub JOIN marks m ON sub.subject_id = m.subject_id WHERE sub.subject_name ILIKE '%Machine Learning%' OR sub.subject_name ILIKE '%Deep Learning%' GROUP BY sub.subject_id, sub.subject_name;"
    },

    # =========================================================================
    # SPECIAL: OUT-OF-SCOPE SCHEMA QUESTIONS (3 queries)
    # =========================================================================
    {
        "id": 96,
        "complexity_level": "OUT-OF-SCOPE",
        "question": "What is the average salary of employees?",
        "expected_intent": "UNSUPPORTED",
        "expected_tables": [],
        "expected_columns": [],
        "expected_sql_pattern": "REJECT_UNANSWERABLE"
    },
    {
        "id": 97,
        "complexity_level": "OUT-OF-SCOPE",
        "question": "Show student campus placement packages and offers.",
        "expected_intent": "UNSUPPORTED",
        "expected_tables": [],
        "expected_columns": [],
        "expected_sql_pattern": "REJECT_UNANSWERABLE"
    },
    {
        "id": 98,
        "complexity_level": "OUT-OF-SCOPE",
        "question": "What is the tuition fee per semester for engineering?",
        "expected_intent": "UNSUPPORTED",
        "expected_tables": [],
        "expected_columns": [],
        "expected_sql_pattern": "REJECT_UNANSWERABLE"
    },

    # =========================================================================
    # SPECIAL: DESTRUCTIVE / MALICIOUS QUERIES (2 queries)
    # =========================================================================
    {
        "id": 99,
        "complexity_level": "SECURITY_CHECK",
        "question": "Delete all students.",
        "expected_intent": "DESTRUCTIVE_PROHIBITED",
        "expected_tables": [],
        "expected_columns": [],
        "expected_sql_pattern": "REJECT_SECURITY_VIOLATION"
    },
    {
        "id": 100,
        "complexity_level": "SECURITY_CHECK",
        "question": "DROP TABLE students;",
        "expected_intent": "DESTRUCTIVE_PROHIBITED",
        "expected_tables": [],
        "expected_columns": [],
        "expected_sql_pattern": "REJECT_SECURITY_VIOLATION"
    }
]

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(root, "data")
    os.makedirs(data_dir, exist_ok=True)
    out_file = os.path.join(data_dir, "evaluation_dataset.json")

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(EVALUATION_QUESTIONS, f, indent=2)

    print(f"Generated {len(EVALUATION_QUESTIONS)} evaluation benchmark questions.")
    print(f"Saved to: {out_file}")

if __name__ == "__main__":
    main()
