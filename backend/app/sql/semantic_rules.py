import re
from typing import Dict, Any, Optional, List


class SemanticRuleGenerator:
    """
    Synthesizes valid PostgreSQL SQL queries directly from structured NLP entities,
    intent classification, and relational constraints.
    Guarantees deterministic, zero-hallucination SQL execution.
    """
    def __init__(self):
        pass

    def generate(
        self,
        question: str,
        intent: str,
        entities: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        q_lower = question.lower()
        depts = entities.get("departments", [])
        subjects = entities.get("subjects", [])
        conditions = entities.get("conditions", [])
        limit = entities.get("limit")
        city = entities.get("city")
        sem = entities.get("semester")
        year = entities.get("year")
        primary = entities.get("primary_entity", "students")

        # -------------------------------------------------------------
        # 1. COMPARISON (e.g. Compare average CGPA / marks between CSE and AIML, or subjects)
        # -------------------------------------------------------------
        if intent == "COMPARISON" or (len(depts) >= 2 and ("compare" in q_lower or "between" in q_lower)) or (len(subjects) >= 2):
            if subjects and len(subjects) >= 2:
                sub_likes = " OR ".join(f"sub.subject_name ILIKE '%{s}%'" for s in subjects)
                return (
                    f"SELECT sub.subject_name, ROUND(AVG(m.total_marks), 2) AS average_marks, COUNT(m.mark_id) AS student_evaluations\n"
                    f"FROM subjects sub\n"
                    f"JOIN marks m ON sub.subject_id = m.subject_id\n"
                    f"WHERE {sub_likes}\n"
                    f"GROUP BY sub.subject_id, sub.subject_name\n"
                    f"ORDER BY average_marks DESC;"
                )
            dept_list_sql = ", ".join(f"'{d}'" for d in depts) if depts else "'CSE', 'AIML'"
            if "mark" in q_lower or "score" in q_lower:
                return (
                    f"SELECT d.department_code, d.department_name, ROUND(AVG(m.total_marks), 2) AS average_marks\n"
                    f"FROM departments d\n"
                    f"JOIN subjects sub ON d.department_id = sub.department_id\n"
                    f"JOIN marks m ON sub.subject_id = m.subject_id\n"
                    f"WHERE d.department_code IN ({dept_list_sql})\n"
                    f"GROUP BY d.department_id, d.department_code, d.department_name\n"
                    f"ORDER BY average_marks DESC;"
                )
            elif "attendance" in q_lower:
                return (
                    f"SELECT d.department_code, d.department_name, ROUND(AVG(a.attendance_percentage), 2) AS average_attendance\n"
                    f"FROM departments d\n"
                    f"JOIN students s ON d.department_id = s.department_id\n"
                    f"JOIN attendance a ON s.student_id = a.student_id\n"
                    f"WHERE d.department_code IN ({dept_list_sql})\n"
                    f"GROUP BY d.department_id, d.department_code, d.department_name\n"
                    f"ORDER BY average_attendance DESC;"
                )
            elif "student" in q_lower or "count" in q_lower or "enrolled" in q_lower:
                return (
                    f"SELECT d.department_code, d.department_name, COUNT(s.student_id) AS student_count\n"
                    f"FROM departments d\n"
                    f"JOIN students s ON d.department_id = s.department_id\n"
                    f"WHERE d.department_code IN ({dept_list_sql})\n"
                    f"GROUP BY d.department_id, d.department_code, d.department_name\n"
                    f"ORDER BY student_count DESC;"
                )
            else: # default CGPA comparison
                return (
                    f"SELECT d.department_code, d.department_name, ROUND(AVG(s.cgpa), 2) AS average_cgpa, COUNT(s.student_id) AS total_students\n"
                    f"FROM departments d\n"
                    f"JOIN students s ON d.department_id = s.department_id\n"
                    f"WHERE d.department_code IN ({dept_list_sql})\n"
                    f"GROUP BY d.department_id, d.department_code, d.department_name\n"
                    f"ORDER BY average_cgpa DESC;"
                )

        # -------------------------------------------------------------
        # 2. TOP_N / RANKING
        # -------------------------------------------------------------
        if intent == "TOP_N" or limit is not None:
            n_limit = limit if limit else 10
            # Top faculty by student count
            if primary == "faculty" or "faculty" in q_lower or "teach" in q_lower:
                return (
                    f"SELECT f.employee_id, f.first_name || ' ' || f.last_name AS faculty_name, d.department_code, COUNT(e.student_id) AS student_count\n"
                    f"FROM faculty f\n"
                    f"JOIN departments d ON f.department_id = d.department_id\n"
                    f"JOIN enrollments e ON f.faculty_id = e.faculty_id\n"
                    f"GROUP BY f.faculty_id, f.employee_id, f.first_name, f.last_name, d.department_code\n"
                    f"ORDER BY student_count DESC\n"
                    f"LIMIT {n_limit};"
                )

            # Top students by attendance
            if any(c.get("attribute") == "attendance" for c in conditions) or "attendance" in q_lower:
                where_clause = f"WHERE d.department_code = '{depts[0]}'\n" if depts else ""
                return (
                    f"SELECT s.usn, s.first_name || ' ' || s.last_name AS student_name, d.department_code, ROUND(AVG(a.attendance_percentage), 2) AS average_attendance\n"
                    f"FROM students s\n"
                    f"JOIN departments d ON s.department_id = d.department_id\n"
                    f"JOIN attendance a ON s.student_id = a.student_id\n"
                    f"{where_clause}"
                    f"GROUP BY s.student_id, s.usn, s.first_name, s.last_name, d.department_code\n"
                    f"ORDER BY average_attendance DESC\n"
                    f"LIMIT {n_limit};"
                )

            # Default: Top students by CGPA
            where_parts = []
            if depts:
                where_parts.append(f"d.department_code = '{depts[0]}'")
            if year:
                where_parts.append(f"s.current_year = {year}")
            if sem:
                where_parts.append(f"s.current_semester = {sem}")

            where_clause = f"WHERE {' AND '.join(where_parts)}\n" if where_parts else ""
            return (
                f"SELECT s.usn, s.first_name, s.last_name, d.department_code, s.cgpa, s.current_semester\n"
                f"FROM students s\n"
                f"JOIN departments d ON s.department_id = d.department_id\n"
                f"{where_clause}"
                f"ORDER BY s.cgpa DESC\n"
                f"LIMIT {n_limit};"
            )

        # -------------------------------------------------------------
        # 3. AVERAGE & AGGREGATIONS
        # -------------------------------------------------------------
        if intent == "AVERAGE":
            # "Show average marks for each subject" or "average marks of each subject"
            if "subject" in q_lower or "course" in q_lower:
                return (
                    "SELECT sub.subject_code, sub.subject_name, ROUND(AVG(m.total_marks), 2) AS average_marks\n"
                    "FROM subjects sub\n"
                    "JOIN marks m ON sub.subject_id = m.subject_id\n"
                    "GROUP BY sub.subject_id, sub.subject_code, sub.subject_name\n"
                    "ORDER BY average_marks DESC\n"
                    "LIMIT 50;"
                )
            # "Average marks by department"
            if ("mark" in q_lower or "score" in q_lower) and "department" in q_lower:
                return (
                    "SELECT d.department_code, d.department_name, ROUND(AVG(m.total_marks), 2) AS average_marks\n"
                    "FROM departments d\n"
                    "JOIN subjects sub ON d.department_id = sub.department_id\n"
                    "JOIN marks m ON sub.subject_id = m.subject_id\n"
                    "GROUP BY d.department_id, d.department_code, d.department_name\n"
                    "ORDER BY average_marks DESC;"
                )
            # "Average CGPA of each department"
            if "each department" in q_lower or "by department" in q_lower or "all departments" in q_lower:
                return (
                    "SELECT d.department_code, d.department_name, ROUND(AVG(s.cgpa), 2) AS average_cgpa, COUNT(s.student_id) AS total_students\n"
                    "FROM departments d\n"
                    "JOIN students s ON d.department_id = s.department_id\n"
                    "GROUP BY d.department_id, d.department_code, d.department_name\n"
                    "ORDER BY average_cgpa DESC;"
                )
            # "Average CGPA of AIML"
            if depts:
                return (
                    f"SELECT d.department_code, d.department_name, ROUND(AVG(s.cgpa), 2) AS average_cgpa, COUNT(s.student_id) AS student_count\n"
                    f"FROM departments d\n"
                    f"JOIN students s ON d.department_id = s.department_id\n"
                    f"WHERE d.department_code = '{depts[0]}'\n"
                    f"GROUP BY d.department_id, d.department_code, d.department_name;"
                )
            # Overall average CGPA
            return (
                "SELECT ROUND(AVG(cgpa), 2) AS average_cgpa, COUNT(*) AS total_students FROM students;"
            )

        # -------------------------------------------------------------
        # 4. MAXIMUM / HIGHEST
        # -------------------------------------------------------------
        if intent == "MAXIMUM":
            # "Which department has the highest average CGPA?"
            if "department" in q_lower and ("cgpa" in q_lower or "gpa" in q_lower):
                return (
                    "SELECT d.department_code, d.department_name, ROUND(AVG(s.cgpa), 2) AS highest_average_cgpa\n"
                    "FROM departments d\n"
                    "JOIN students s ON d.department_id = s.department_id\n"
                    "GROUP BY d.department_id, d.department_code, d.department_name\n"
                    "ORDER BY highest_average_cgpa DESC\n"
                    "LIMIT 1;"
                )
            # "Which department has the highest average attendance?"
            if "department" in q_lower and "attendance" in q_lower:
                return (
                    "SELECT d.department_code, d.department_name, ROUND(AVG(a.attendance_percentage), 2) AS highest_average_attendance\n"
                    "FROM departments d\n"
                    "JOIN students s ON d.department_id = s.department_id\n"
                    "JOIN attendance a ON s.student_id = a.student_id\n"
                    "GROUP BY d.department_id, d.department_code, d.department_name\n"
                    "ORDER BY highest_average_attendance DESC\n"
                    "LIMIT 1;"
                )
            # "Which semester has highest average marks?"
            if "semester" in q_lower:
                return (
                    "SELECT sem.semester_number, sem.semester_name, ROUND(AVG(m.total_marks), 2) AS average_marks\n"
                    "FROM marks m\n"
                    "JOIN semesters sem ON m.semester_id = sem.semester_id\n"
                    "GROUP BY sem.semester_number, sem.semester_name\n"
                    "ORDER BY average_marks DESC\n"
                    "LIMIT 1;"
                )

        # -------------------------------------------------------------
        # 5. MINIMUM / LOWEST
        # -------------------------------------------------------------
        if intent == "MINIMUM":
            # "Which subject has the lowest average marks?"
            if "subject" in q_lower:
                return (
                    "SELECT sub.subject_code, sub.subject_name, ROUND(AVG(m.total_marks), 2) AS lowest_average_marks\n"
                    "FROM subjects sub\n"
                    "JOIN marks m ON sub.subject_id = m.subject_id\n"
                    "GROUP BY sub.subject_id, sub.subject_code, sub.subject_name\n"
                    "ORDER BY lowest_average_marks ASC\n"
                    "LIMIT 1;"
                )
            # "Which department has the lowest average CGPA?"
            if "department" in q_lower:
                return (
                    "SELECT d.department_code, d.department_name, ROUND(AVG(s.cgpa), 2) AS lowest_average_cgpa\n"
                    "FROM departments d\n"
                    "JOIN students s ON d.department_id = s.department_id\n"
                    "GROUP BY d.department_id, d.department_code, d.department_name\n"
                    "ORDER BY lowest_average_cgpa ASC\n"
                    "LIMIT 1;"
                )

        # -------------------------------------------------------------
        # 6. COUNT & GROUP_BY
        # -------------------------------------------------------------
        if intent in ["COUNT", "GROUP_BY"]:
            # "How many students are enrolled in each department?" / "Students per department"
            if "department" in q_lower and ("each" in q_lower or "by" in q_lower or "per" in q_lower):
                return (
                    "SELECT d.department_code, d.department_name, COUNT(s.student_id) AS student_count\n"
                    "FROM departments d\n"
                    "LEFT JOIN students s ON d.department_id = s.department_id\n"
                    "GROUP BY d.department_id, d.department_code, d.department_name\n"
                    "ORDER BY student_count DESC;"
                )
            # "Show number of students in each semester"
            if "semester" in q_lower:
                return (
                    "SELECT current_semester, COUNT(student_id) AS student_count\n"
                    "FROM students\n"
                    "GROUP BY current_semester\n"
                    "ORDER BY current_semester ASC;"
                )
            # "Distribution of grades in Machine Learning"
            if subjects and "grade" in q_lower:
                return (
                    f"SELECT m.grade, COUNT(*) AS count\n"
                    f"FROM marks m\n"
                    f"JOIN subjects sub ON m.subject_id = sub.subject_id\n"
                    f"WHERE sub.subject_name ILIKE '%{subjects[0]}%'\n"
                    f"GROUP BY m.grade\n"
                    f"ORDER BY count DESC;"
                )
            # "How many students scored above 90 in Data Structures?"
            if subjects and any(c.get("attribute") == "marks" for c in conditions):
                m_cond = next(c for c in conditions if c.get("attribute") == "marks")
                return (
                    f"SELECT COUNT(DISTINCT m.student_id) AS student_count\n"
                    f"FROM marks m\n"
                    f"JOIN subjects sub ON m.subject_id = sub.subject_id\n"
                    f"WHERE sub.subject_name ILIKE '%{subjects[0]}%' AND m.total_marks {m_cond['operator']} {m_cond['value']};"
                )
            # "How many students have attendance below 75%?"
            if any(c.get("attribute") == "attendance" for c in conditions):
                a_cond = next(c for c in conditions if c.get("attribute") == "attendance")
                where_dept = f"AND d.department_code = '{depts[0]}' " if depts else ""
                return (
                    f"SELECT COUNT(DISTINCT s.student_id) AS student_count\n"
                    f"FROM students s\n"
                    f"JOIN departments d ON s.department_id = d.department_id\n"
                    f"JOIN attendance a ON s.student_id = a.student_id\n"
                    f"WHERE a.attendance_percentage {a_cond['operator']} {a_cond['value']} {where_dept};"
                )
            # "How many students failed more than two subjects?"
            if any(c.get("attribute") == "backlogs" for c in conditions) or "failed" in q_lower:
                limit_val = 2
                for c in conditions:
                    if c.get("attribute") == "backlogs":
                        limit_val = c.get("value", 2)
                return (
                    f"SELECT COUNT(*) AS student_count FROM (\n"
                    f"    SELECT s.student_id\n"
                    f"    FROM marks m\n"
                    f"    JOIN students s ON m.student_id = s.student_id\n"
                    f"    WHERE m.result_status = 'FAIL'\n"
                    f"    GROUP BY s.student_id\n"
                    f"    HAVING COUNT(m.mark_id) > {limit_val}\n"
                    f") subquery;"
                )
            # Simple count
            where_clause = f"WHERE d.department_code = '{depts[0]}'" if depts else ""
            return (
                f"SELECT COUNT(s.student_id) AS total_students\n"
                f"FROM students s\n"
                f"JOIN departments d ON s.department_id = d.department_id\n"
                f"{where_clause};"
            )

        # -------------------------------------------------------------
        # 7. RELATIONAL FILTERS & JOINS
        # -------------------------------------------------------------
        # "Which students failed more than two subjects?" / "Students who failed Machine Learning"
        if "failed" in q_lower or any(c.get("attribute") == "backlogs" for c in conditions):
            if subjects: # Failed a specific subject
                return (
                    f"SELECT s.usn, s.first_name, s.last_name, d.department_code, sub.subject_name, m.total_marks, m.grade\n"
                    f"FROM marks m\n"
                    f"JOIN students s ON m.student_id = s.student_id\n"
                    f"JOIN subjects sub ON m.subject_id = sub.subject_id\n"
                    f"JOIN departments d ON s.department_id = d.department_id\n"
                    f"WHERE sub.subject_name ILIKE '%{subjects[0]}%' AND m.result_status = 'FAIL'\n"
                    f"ORDER BY s.usn\n"
                    f"LIMIT 50;"
                )
            else: # Failed more than N subjects
                min_failed = 2
                for c in conditions:
                    if c.get("attribute") == "backlogs":
                        min_failed = c.get("value", 2)
                return (
                    f"SELECT s.usn, s.first_name || ' ' || s.last_name AS student_name, d.department_code, COUNT(m.mark_id) AS failed_subjects_count\n"
                    f"FROM marks m\n"
                    f"JOIN students s ON m.student_id = s.student_id\n"
                    f"JOIN departments d ON s.department_id = d.department_id\n"
                    f"WHERE m.result_status = 'FAIL'\n"
                    f"GROUP BY s.student_id, s.usn, s.first_name, s.last_name, d.department_code\n"
                    f"HAVING COUNT(m.mark_id) > {min_failed}\n"
                    f"ORDER BY failed_subjects_count DESC\n"
                    f"LIMIT 50;"
                )

        # Subject marks filter: "Show students who scored above 80 in Machine Learning"
        if subjects and any(c.get("attribute") == "marks" for c in conditions):
            m_cond = next(c for c in conditions if c.get("attribute") == "marks")
            dept_clause = f"AND d.department_code = '{depts[0]}' " if depts else ""
            return (
                f"SELECT s.usn, s.first_name, s.last_name, d.department_code, sub.subject_name, m.total_marks, m.grade\n"
                f"FROM marks m\n"
                f"JOIN students s ON m.student_id = s.student_id\n"
                f"JOIN subjects sub ON m.subject_id = sub.subject_id\n"
                f"JOIN departments d ON s.department_id = d.department_id\n"
                f"WHERE sub.subject_name ILIKE '%{subjects[0]}%' AND m.total_marks {m_cond['operator']} {m_cond['value']} {dept_clause}\n"
                f"ORDER BY m.total_marks DESC\n"
                f"LIMIT 50;"
            )

        # Multi-condition: "Which students have both CGPA above 8.5 and attendance above 85%?"
        cgpa_c = next((c for c in conditions if c.get("attribute") == "cgpa"), None)
        att_c = next((c for c in conditions if c.get("attribute") == "attendance"), None)
        if cgpa_c and att_c:
            dept_filter = f"AND d.department_code = '{depts[0]}' " if depts else ""
            return (
                f"SELECT s.usn, s.first_name, s.last_name, d.department_code, s.cgpa, ROUND(AVG(a.attendance_percentage), 2) AS avg_attendance\n"
                f"FROM students s\n"
                f"JOIN departments d ON s.department_id = d.department_id\n"
                f"JOIN attendance a ON s.student_id = a.student_id\n"
                f"WHERE s.cgpa {cgpa_c['operator']} {cgpa_c['value']} {dept_filter}\n"
                f"GROUP BY s.student_id, s.usn, s.first_name, s.last_name, d.department_code, s.cgpa\n"
                f"HAVING AVG(a.attendance_percentage) {att_c['operator']} {att_c['value']}\n"
                f"ORDER BY s.cgpa DESC\n"
                f"LIMIT 50;"
            )

        # Attendance filter: "Which students have attendance below 75%?"
        if att_c:
            dept_filter = f"AND d.department_code = '{depts[0]}' " if depts else ""
            year_filter = f"AND s.current_year = {year} " if year else ""
            return (
                f"SELECT DISTINCT s.usn, s.first_name, s.last_name, d.department_code, a.attendance_percentage, a.attendance_status\n"
                f"FROM attendance a\n"
                f"JOIN students s ON a.student_id = s.student_id\n"
                f"JOIN departments d ON s.department_id = d.department_id\n"
                f"WHERE a.attendance_percentage {att_c['operator']} {att_c['value']} {dept_filter}{year_filter}\n"
                f"ORDER BY a.attendance_percentage ASC\n"
                f"LIMIT 50;"
            )

        # CGPA filter: "Show AIML students with CGPA above 8"
        if cgpa_c:
            dept_filter = f"AND d.department_code = '{depts[0]}' " if depts else ""
            city_filter = f"AND s.city = '{city}' " if city else ""
            return (
                f"SELECT s.usn, s.first_name, s.last_name, d.department_code, s.cgpa, s.current_semester, s.city\n"
                f"FROM students s\n"
                f"JOIN departments d ON s.department_id = d.department_id\n"
                f"WHERE s.cgpa {cgpa_c['operator']} {cgpa_c['value']} {dept_filter}{city_filter}\n"
                f"ORDER BY s.cgpa DESC\n"
                f"LIMIT 50;"
            )

        # City filter: "Show students from Bangalore"
        if city:
            dept_filter = f"AND d.department_code = '{depts[0]}' " if depts else ""
            return (
                f"SELECT s.usn, s.first_name, s.last_name, d.department_code, s.city, s.cgpa\n"
                f"FROM students s\n"
                f"JOIN departments d ON s.department_id = d.department_id\n"
                f"WHERE s.city = '{city}' {dept_filter}\n"
                f"ORDER BY s.cgpa DESC\n"
                f"LIMIT 50;"
            )

        # General Department filter: "Show all students from AIML"
        if depts:
            return (
                f"SELECT s.usn, s.first_name, s.last_name, d.department_code, s.cgpa, s.current_semester\n"
                f"FROM students s\n"
                f"JOIN departments d ON s.department_id = d.department_id\n"
                f"WHERE d.department_code = '{depts[0]}'\n"
                f"ORDER BY s.usn\n"
                f"LIMIT 50;"
            )

        # Default fallback: recent students
        return (
            "SELECT s.usn, s.first_name, s.last_name, d.department_code, s.cgpa, s.current_semester\n"
            "FROM students s\n"
            "JOIN departments d ON s.department_id = d.department_id\n"
            "ORDER BY s.student_id ASC\n"
            "LIMIT 50;"
        )


semantic_rule_generator = SemanticRuleGenerator()
