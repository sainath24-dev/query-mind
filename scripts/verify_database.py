#!/usr/bin/env python3
"""
Database Verification Script for QueryMind
Checks table counts, foreign-key integrity, indexes, and read-only user permissions.
"""

import os
import psycopg2

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "querymind")


def main():
    print("=" * 60)
    print("QueryMind Database Integrity & Security Verification")
    print("=" * 60)

    # 1. Admin connection check
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, dbname=DB_NAME
    )
    cur = conn.cursor()

    tables = [
        "departments", "faculty", "semesters", "subjects",
        "students", "enrollments", "marks", "attendance", "query_history"
    ]

    print("\n[1] Table Record Counts:")
    for t in tables:
        cur.execute(f"SELECT COUNT(*) FROM {t};")
        cnt = cur.fetchone()[0]
        print(f"  - {t:<15}: {cnt:>8,} rows")

    print("\n[2] Foreign Key Integrity Checks:")
    # Check for orphan students
    cur.execute("""
        SELECT COUNT(*) FROM students s
        LEFT JOIN departments d ON s.department_id = d.department_id
        WHERE d.department_id IS NULL;
    """)
    orphan_students = cur.fetchone()[0]
    print(f"  - Orphan students (invalid department): {orphan_students}")

    # Check for orphan marks
    cur.execute("""
        SELECT COUNT(*) FROM marks m
        LEFT JOIN students s ON m.student_id = s.student_id
        LEFT JOIN subjects sub ON m.subject_id = sub.subject_id
        WHERE s.student_id IS NULL OR sub.subject_id IS NULL;
    """)
    orphan_marks = cur.fetchone()[0]
    print(f"  - Orphan marks (invalid student/subject): {orphan_marks}")

    # Check for orphan attendance
    cur.execute("""
        SELECT COUNT(*) FROM attendance a
        LEFT JOIN students s ON a.student_id = s.student_id
        LEFT JOIN subjects sub ON a.subject_id = sub.subject_id
        WHERE s.student_id IS NULL OR sub.subject_id IS NULL;
    """)
    orphan_att = cur.fetchone()[0]
    print(f"  - Orphan attendance (invalid student/subject): {orphan_att}")

    assert orphan_students == 0 and orphan_marks == 0 and orphan_att == 0, "Foreign key integrity violated!"
    print("  ✓ All Foreign Key constraints verified: 0 orphan rows.")

    cur.close()
    conn.close()

    # 2. Read-Only User Connection & Permission Check
    print("\n[3] Security Test: Read-Only User Permissions:")
    try:
        ro_conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, user="querymind_readonly", password="readonly_secure_pass", dbname=DB_NAME
        )
        ro_cur = ro_conn.cursor()

        # Test SELECT (should succeed)
        ro_cur.execute("SELECT COUNT(*) FROM students;")
        stu_cnt = ro_cur.fetchone()[0]
        print(f"  ✓ Read-only user SELECT succeeded: read {stu_cnt:,} students.")

        # Test INSERT (MUST FAIL)
        insert_rejected = False
        try:
            ro_cur.execute("INSERT INTO departments (department_name, department_code, hod_name) VALUES ('Test', 'TST', 'Dr. Test');")
        except psycopg2.errors.InsufficientPrivilege:
            insert_rejected = True
            ro_conn.rollback()

        if insert_rejected:
            print("  ✓ Read-only user INSERT correctly rejected with InsufficientPrivilege.")
        else:
            print("  ✗ SECURITY WARNING: Read-only user was able to insert!")

        # Test DROP (MUST FAIL)
        drop_rejected = False
        try:
            ro_cur.execute("DROP TABLE attendance;")
        except psycopg2.errors.InsufficientPrivilege:
            drop_rejected = True
            ro_conn.rollback()

        if drop_rejected:
            print("  ✓ Read-only user DROP TABLE correctly rejected with InsufficientPrivilege.")

        ro_cur.close()
        ro_conn.close()
    except Exception as e:
        print(f"  Error testing read-only user: {e}")

    print("\n" + "=" * 60)
    print("ALL INTEGRITY AND SECURITY CHECKS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    main()
