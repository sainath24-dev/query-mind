#!/usr/bin/env python3
"""
Comprehensive Automated Test Suite for QueryMind Backend
Executes NLP, Security, Schema, API, and Execution tests.
"""

import asyncio
import sys
from httpx import AsyncClient, ASGITransport
from backend.app.main import app
from backend.app.nlp.entity_extractor import entity_extractor
from backend.app.nlp.intent_classifier import intent_classifier
from backend.app.nlp.schema_matcher import schema_matcher
from backend.app.sql.safety import safety_checker
from backend.app.sql.validator import sql_validator


async def run_all_tests():
    print("=" * 65)
    print("Running QueryMind Backend Automated Tests")
    print("=" * 65)

    passed = 0
    failed = 0

    def check(name, condition, details=""):
        nonlocal passed, failed
        if condition:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name} - FAILED: {details}")
            failed += 1

    # -------------------------------------------------------------
    # 1. NLP Tests
    # -------------------------------------------------------------
    print("\n[Group 1] Natural Language Processing Pipeline:")
    e1 = entity_extractor.extract("Who are the top 10 students by CGPA?")
    check("Extract Limit (top 10)", e1["limit"] == 10)
    i1, _ = intent_classifier.classify("Who are the top 10 students by CGPA?", e1)
    check("Classify Intent TOP_N", i1 == "TOP_N")

    e2 = entity_extractor.extract("Which AIML students have attendance below 75%?")
    check("Extract Department (AIML)", "AIML" in e2["departments"])
    check("Extract Attendance Condition (< 75)", any(c["attribute"] == "attendance" and c["operator"] == "<" and c["value"] == 75.0 for c in e2["conditions"]))

    e3 = entity_extractor.extract("What is the average salary of AIML students?")
    check("Detect Out-of-Scope Attribute (salary)", len(e3["unsupported_attributes"]) > 0)

    # -------------------------------------------------------------
    # 2. SQL Security & AST Safety Tests
    # -------------------------------------------------------------
    print("\n[Group 2] SQL Safety & Injection Protection:")
    safe_ok, _ = safety_checker.check_safety("SELECT * FROM students LIMIT 10;")
    check("Allow valid SELECT query", safe_ok)

    drop_safe, err_drop = safety_checker.check_safety("DROP TABLE students;")
    check("Block DROP TABLE", not drop_safe and "DROP" in err_drop)

    delete_safe, err_del = safety_checker.check_safety("DELETE FROM students WHERE student_id = 1;")
    check("Block DELETE FROM", not delete_safe and "DELETE" in err_del)

    multi_safe, err_multi = safety_checker.check_safety("SELECT 1; DROP TABLE students;")
    check("Block multiple semicolon-separated statements", not multi_safe)

    valid_ok, sanitized, _ = sql_validator.validate_and_sanitize("SELECT usn, cgpa FROM students WHERE cgpa > 8.0")
    check("Sanitize and enforce LIMIT on un-limited queries", "LIMIT" in sanitized)

    # -------------------------------------------------------------
    # 3. HTTP API Endpoints Integration Tests
    # -------------------------------------------------------------
    print("\n[Group 3] FastAPI Endpoints & Relational Execution:")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Root health check
        r_root = await client.get("/")
        check("GET / (Health check)", r_root.status_code == 200 and r_root.json()["status"] == "online")

        # Schema introspection
        r_schema = await client.get("/api/schema")
        check("GET /api/schema", r_schema.status_code == 200 and len(r_schema.json()["tables"]) >= 8)

        # Dashboard metrics (from database)
        r_dash = await client.get("/api/dashboard")
        dash = r_dash.json()
        check("GET /api/dashboard (Real 5000+ students)", r_dash.status_code == 200 and dash["total_students"] >= 5000)
        check("GET /api/dashboard (10 departments)", dash["total_departments"] == 10)
        check("GET /api/dashboard (Average CGPA computed)", dash["average_cgpa"] > 6.0)

        # Live Query 1: Top students
        r_q1 = await client.post("/api/query", json={"question": "Who are the top 10 students by CGPA?"})
        q1_data = r_q1.json()
        check("POST /api/query: Top 10 Students", r_q1.status_code == 200 and q1_data["row_count"] == 10 and q1_data["status"] == "SUCCESS")
        check("Explanation generated", len(q1_data["explanation"]) > 10)

        # Live Query 2: Department Count & Visualization
        r_q2 = await client.post("/api/query", json={"question": "How many students are enrolled in each department?"})
        q2_data = r_q2.json()
        check("POST /api/query: Department Count", r_q2.status_code == 200 and q2_data["row_count"] == 10)
        check("Automatic Bar Chart recommendation", q2_data["visualization"]["recommended_chart"] == "bar")

        # Live Query 3: Attendance Filter
        r_q3 = await client.post("/api/query", json={"question": "Which students have attendance below 75%?"})
        q3_data = r_q3.json()
        check("POST /api/query: Attendance filter", r_q3.status_code == 200 and q3_data["row_count"] > 0)

        # Live Query 4: Cross-table Marks & Subject Join
        r_q4 = await client.post("/api/query", json={"question": "Show all AIML students who scored above 80 in Machine Learning."})
        q4_data = r_q4.json()
        check("POST /api/query: Relational Join (Students + Subjects + Marks)", r_q4.status_code == 200 and q4_data["status"] == "SUCCESS")

        # Live Query 5: Out of Scope Question
        r_q5 = await client.post("/api/query", json={"question": "What is the average salary of employees?"})
        q5_data = r_q5.json()
        check("POST /api/query: Graceful rejection of missing schema (salary)", q5_data["is_answerable"] is False)

        # Live Query 6: Malicious Destructive Request
        r_q6 = await client.post("/api/query", json={"question": "Delete all students."})
        q6_data = r_q6.json()
        check("POST /api/query: Reject destructive prompt", q6_data["status"] in ["ERROR", "UNANSWERABLE"] or "prohibited" in q6_data["explanation"].lower() or "rejected" in q6_data["explanation"].lower())

        # Query History Check
        r_hist = await client.get("/api/query-history")
        hist_data = r_hist.json()
        check("GET /api/query-history: Audit trail logged", r_hist.status_code == 200 and hist_data["total_count"] > 0)

    print("\n" + "=" * 65)
    print(f"TEST RESULTS: {passed} PASSED, {failed} FAILED")
    print("=" * 65)

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
