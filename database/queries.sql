-- ==============================================================================
-- QueryMind Benchmark & Sample SQL Queries
-- Demonstrating Level 1 through Level 8 Complexity
-- ==============================================================================

-- 1. "Show all students from AIML."
SELECT s.usn, s.first_name, s.last_name, d.department_code, s.cgpa, s.current_semester
FROM students s
JOIN departments d ON s.department_id = d.department_id
WHERE d.department_code = 'AIML'
ORDER BY s.usn
LIMIT 50;

-- 2. "Show AIML students with CGPA above 8."
SELECT s.usn, s.first_name, s.last_name, s.cgpa, s.current_semester
FROM students s
JOIN departments d ON s.department_id = d.department_id
WHERE d.department_code = 'AIML' AND s.cgpa > 8.0
ORDER BY s.cgpa DESC;

-- 3. "Who are the top 10 students by CGPA?"
SELECT s.usn, s.first_name || ' ' || s.last_name AS student_name, d.department_code, s.cgpa
FROM students s
JOIN departments d ON s.department_id = d.department_id
ORDER BY s.cgpa DESC
LIMIT 10;

-- 4. "Show students with attendance below 75%."
SELECT DISTINCT s.usn, s.first_name, s.last_name, d.department_code, a.attendance_percentage, a.attendance_status
FROM attendance a
JOIN students s ON a.student_id = s.student_id
JOIN departments d ON s.department_id = d.department_id
WHERE a.attendance_percentage < 75.0
ORDER BY a.attendance_percentage ASC
LIMIT 50;

-- 5. "How many students are enrolled in each department?"
SELECT d.department_code, d.department_name, COUNT(s.student_id) AS student_count
FROM departments d
LEFT JOIN students s ON d.department_id = s.department_id
GROUP BY d.department_id, d.department_code, d.department_name
ORDER BY student_count DESC;

-- 6. "What is the average CGPA of each department?"
SELECT d.department_code, d.department_name, ROUND(AVG(s.cgpa), 2) AS average_cgpa
FROM departments d
JOIN students s ON d.department_id = s.department_id
GROUP BY d.department_id, d.department_code, d.department_name
ORDER BY average_cgpa DESC;

-- 7. "Which department has the highest average CGPA?"
SELECT d.department_code, d.department_name, ROUND(AVG(s.cgpa), 2) AS average_cgpa
FROM departments d
JOIN students s ON d.department_id = s.department_id
GROUP BY d.department_id, d.department_code, d.department_name
ORDER BY average_cgpa DESC
LIMIT 1;

-- 8. "Show the average marks for each subject."
SELECT sub.subject_code, sub.subject_name, ROUND(AVG(m.total_marks), 2) AS average_marks
FROM subjects sub
JOIN marks m ON sub.subject_id = m.subject_id
GROUP BY sub.subject_id, sub.subject_code, sub.subject_name
ORDER BY average_marks DESC
LIMIT 50;

-- 9. "Which students failed more than two subjects?"
SELECT s.usn, s.first_name || ' ' || s.last_name AS student_name, d.department_code, COUNT(m.mark_id) AS failed_subjects_count
FROM marks m
JOIN students s ON m.student_id = s.student_id
JOIN departments d ON s.department_id = d.department_id
WHERE m.result_status = 'FAIL'
GROUP BY s.student_id, s.usn, s.first_name, s.last_name, d.department_code
HAVING COUNT(m.mark_id) > 2
ORDER BY failed_subjects_count DESC;

-- 10. "Show students who scored above 80 in Machine Learning."
SELECT s.usn, s.first_name, s.last_name, d.department_code, sub.subject_name, m.total_marks, m.grade
FROM marks m
JOIN students s ON m.student_id = s.student_id
JOIN subjects sub ON m.subject_id = sub.subject_id
JOIN departments d ON s.department_id = d.department_id
WHERE sub.subject_name ILIKE '%Machine Learning%' AND m.total_marks > 80.0
ORDER BY m.total_marks DESC
LIMIT 50;

-- 11. "How many students scored above 90 in Data Structures?"
SELECT COUNT(DISTINCT m.student_id) AS count_students_above_90
FROM marks m
JOIN subjects sub ON m.subject_id = sub.subject_id
WHERE sub.subject_name ILIKE '%Data Structures%' AND m.total_marks > 90.0;

-- 12. "Compare the average CGPA of AIML and CSE."
SELECT d.department_code, d.department_name, ROUND(AVG(s.cgpa), 2) AS average_cgpa
FROM departments d
JOIN students s ON d.department_id = s.department_id
WHERE d.department_code IN ('AIML', 'CSE')
GROUP BY d.department_id, d.department_code, d.department_name;

-- 13. "Show the top 5 students in AIML."
SELECT s.usn, s.first_name, s.last_name, s.cgpa, s.current_semester
FROM students s
JOIN departments d ON s.department_id = d.department_id
WHERE d.department_code = 'AIML'
ORDER BY s.cgpa DESC
LIMIT 5;

-- 14. "Which subject has the lowest average marks?"
SELECT sub.subject_code, sub.subject_name, ROUND(AVG(m.total_marks), 2) AS lowest_average_marks
FROM subjects sub
JOIN marks m ON sub.subject_id = m.subject_id
GROUP BY sub.subject_id, sub.subject_code, sub.subject_name
ORDER BY lowest_average_marks ASC
LIMIT 1;

-- 15. "Which students have both CGPA above 8.5 and attendance above 85%?"
SELECT s.usn, s.first_name, s.last_name, d.department_code, s.cgpa, ROUND(AVG(a.attendance_percentage), 2) AS avg_attendance
FROM students s
JOIN departments d ON s.department_id = d.department_id
JOIN attendance a ON s.student_id = a.student_id
WHERE s.cgpa > 8.5
GROUP BY s.student_id, s.usn, s.first_name, s.last_name, d.department_code, s.cgpa
HAVING AVG(a.attendance_percentage) > 85.0
ORDER BY s.cgpa DESC
LIMIT 50;

-- 16. "Show the number of students in each semester."
SELECT current_semester, COUNT(student_id) AS student_count
FROM students
GROUP BY current_semester
ORDER BY current_semester ASC;

-- 17. "Which faculty teaches the most students?"
SELECT f.employee_id, f.first_name || ' ' || f.last_name AS faculty_name, d.department_code, COUNT(e.student_id) AS student_count
FROM faculty f
JOIN departments d ON f.department_id = d.department_id
JOIN enrollments e ON f.faculty_id = e.faculty_id
GROUP BY f.faculty_id, f.employee_id, f.first_name, f.last_name, d.department_code
ORDER BY student_count DESC
LIMIT 1;

-- 18. "Show average marks by department."
SELECT d.department_code, d.department_name, ROUND(AVG(m.total_marks), 2) AS avg_marks
FROM departments d
JOIN subjects sub ON d.department_id = sub.department_id
JOIN marks m ON sub.subject_id = m.subject_id
GROUP BY d.department_id, d.department_code, d.department_name
ORDER BY avg_marks DESC;

-- 19. "Show the distribution of grades in Machine Learning."
SELECT m.grade, COUNT(*) AS count
FROM marks m
JOIN subjects sub ON m.subject_id = sub.subject_id
WHERE sub.subject_name ILIKE '%Machine Learning%'
GROUP BY m.grade
ORDER BY count DESC;

-- 20. "Which semester has the highest average marks?"
SELECT sem.semester_number, sem.semester_name, ROUND(AVG(m.total_marks), 2) AS avg_marks
FROM marks m
JOIN semesters sem ON m.semester_id = sem.semester_id
GROUP BY sem.semester_number, sem.semester_name
ORDER BY avg_marks DESC
LIMIT 1;
