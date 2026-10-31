# QueryMind — Natural Language Database Query Assistant

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18.6-blue.svg)](https://www.postgresql.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.2-black.svg)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-3178C6.svg)](https://www.typescriptlang.org/)
[![Evaluation](https://img.shields.io/badge/Benchmark-100%25%20SQL%20Execution-brightgreen.svg)]()

> **QueryMind** is an end-to-end, production-grade Natural Language Database Query Assistant designed for structured relational database exploration. It converts human language questions into syntactically valid, security-checked PostgreSQL SQL queries, executes them against a 135,000+ record relational database, generates dynamic chart visualizations, and returns grounded natural language explanations.

---

## 🌟 Key Highlights & Philosophy

- **Not a Generic Chatbot**: Every query actually interacts with a live PostgreSQL relational cluster. No hardcoded or fake answers.
- **Pure Relational Grounding**: Introspects live database metadata, tables, constraints, and distinct column sample values.
- **Verified Synthetic University Dataset**: Over **5,200 students**, **10 departments**, **438 subjects**, **120 faculty**, and **135,188 marks and attendance records** generated with realistic correlated distributions.
- **Enterprise-Grade Security Sandbox**:
  - AST parsing via `sqlparse` strictly enforces `SELECT` / `WITH` statement types.
  - Immediate rejection of destructive keywords (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `TRUNCATE`, `ALTER`).
  - Separation of privileges: user queries execute exclusively under the restricted PostgreSQL role `querymind_readonly`.
  - Enforced `statement_timeout = 5000ms` and defensive row ceilings (`LIMIT 50`).
- **Dual-Tier Query Engine**:
  - Deterministic high-precision semantic synthesizer covering all complexity levels (L1 Simple to L8 Multi-table Comparison).
  - Abstract OpenAI-compatible LLM provider interface supporting OpenAI, Groq, DeepSeek, Together, LM Studio, and Ollama.
- **Educational & Viva-Ready Transparency**:
  - Collapsible generated SQL drawer with copy and syntax inspection.
  - Interactive 8-Stage NLP Architecture visualizer explaining tokenization, entity extraction, intent classification, TF-IDF cosine similarity schema matching, and data-to-text NLG.
- **Automated Recharts Visualization**: Dynamic detection and rendering of Bar Charts, Line Charts, and Pie/Donut distributions.
- **Conversational Follow-Up Memory**: Contextual understanding across multi-turn queries (e.g., *"Show top 10 AIML students"* followed by *"Only show the top 5"*).

---

## 🏗️ System Architecture

```
USER QUESTION (Plain English)
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. Text Preprocessing & Cleaning (Normalization/Tokenize)   │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Named Entity Extraction (Depts, Subjects, Marks, Limit)   │
│    + Out-of-Scope Detection (Salary, Fees, Placements)      │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Intent Classification (COUNT, TOP_N, COMPARISON, etc.)   │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Semantic Schema Matcher (TF-IDF Cosine Similarity)       │
│    + Relational Bridge Rule Join Path Resolution            │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. SQL Generation (Semantic Rule Synthesizer / LLM Provider)│
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. SQL AST Validator & Security Sandbox (Reject Destructive)│
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Safe Execution on PostgreSQL (Role: querymind_readonly)   │
│    Timeout: 5.0s, Row Limit: 50                             │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. Grounded NLG Explanation & Dynamic Recharts Visualization │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Relational Database Schema

The database `querymind` models a university academic ecosystem with zero orphaned foreign keys:

| Table | Records | Description | Primary Key | Foreign Keys |
| :--- | :---: | :--- | :--- | :--- |
| **`departments`** | 10 | Engineering streams (CSE, AIML, ISE, ECE, EEE, ME, CIVIL, DS, CS, IT) | `department_id` | — |
| **`faculty`** | 120 | Teaching staff, designations, experience, specialization | `faculty_id` | `department_id` |
| **`subjects`** | 438 | Course catalog across semesters 1–8 (Core, Elective, Lab) | `subject_id` | `department_id` |
| **`semesters`** | 8 | Academic term calendar mappings (Sem 1 to Sem 8) | `semester_id` | — |
| **`students`** | 5,200 | Student profiles, USN, section, CGPA (5.0–10.0), backlogs, city | `student_id` | `department_id` |
| **`enrollments`**| 135,188 | Course registrations linking students, subjects, faculty, semester | `enrollment_id` | `student_id`, `subject_id`, `faculty_id`, `semester_id` |
| **`marks`** | 135,188 | Internal (0–40), External (0–60), Total (0–100), Grade, Result | `mark_id` | `student_id`, `subject_id`, `semester_id` |
| **`attendance`** | 135,188 | Classes conducted, attended, percentage, eligibility status | `attendance_id` | `student_id`, `subject_id`, `semester_id` |
| **`query_history`**| Auto | Chronological audit trail of all natural language questions & SQL | `query_id` | — |

---

## 🚀 Quickstart & Installation

### Prerequisites
- macOS / Linux / Windows
- Python 3.10+ (tested with Python 3.13)
- Node.js 18+ & npm
- PostgreSQL 14+ (active on port 5432)

### 1. Clone & Setup Environment

```bash
cd "QueryMind"

# Copy environment configuration
cp .env.example .env
```

### 2. Database Initialization & Seeding

```bash
# 1. Start PostgreSQL
bash scripts/start_postgres.sh

# 2. Populate 5,200 students, 120 faculty, 438 subjects, and 135k+ records
python scripts/generate_dataset.py

# 3. Verify foreign key integrity & distributions
python scripts/verify_database.py
```

### 3. Start Application Services

```bash
# Start both backend and frontend with one command
bash scripts/start_all.sh

# Or start individually:
bash scripts/start_backend.sh   # Listens on http://127.0.0.1:8008
bash scripts/start_frontend.sh  # Listens on http://localhost:3000
```

### 4. Stop Services

```bash
bash scripts/stop_all.sh
```

---

## 📈 Evaluation & Benchmark Results

The system was evaluated against the **100-Question Comprehensive Benchmark Suite** (`data/evaluation_dataset.json`) across Complexity Levels 1 through 8, Out-of-Scope attributes, and Malicious injections:

| Metric | Target | QueryMind Benchmark Result |
| :--- | :---: | :---: |
| **Intent Classification Accuracy** | >= 85.0% | **98.0%** (98/100) |
| **Entity Extraction Accuracy** | >= 85.0% | **100.0%** (100/100) |
| **SQL Execution Accuracy** | >= 90.0% | **100.0%** (100/100) |
| **Average Query Latency** | < 200 ms | **27.90 ms** |

Run the automated evaluation benchmark anytime:
```bash
python scripts/run_evaluation.py
```
*(Detailed markdown report saved to [`docs/evaluation.md`](docs/evaluation.md))*.

---

## 🧪 Automated Test Suite

QueryMind includes comprehensive unit, integration, and security tests:

```bash
PYTHONPATH=. python backend/tests/run_tests.py
```

```text
[Group 1] Natural Language Processing Pipeline:
  ✓ Extract Limit (top 10)
  ✓ Classify Intent TOP_N
  ✓ Extract Department (AIML)
  ✓ Extract Attendance Condition (< 75)
  ✓ Detect Out-of-Scope Attribute (salary)

[Group 2] SQL Safety & Injection Protection:
  ✓ Allow valid SELECT query
  ✓ Block DROP TABLE
  ✓ Block DELETE FROM
  ✓ Block multiple semicolon-separated statements
  ✓ Sanitize and enforce LIMIT on un-limited queries

[Group 3] FastAPI Endpoints & Relational Execution:
  ✓ GET / (Health check)
  ✓ GET /api/schema
  ✓ GET /api/dashboard (Real 5000+ students)
  ✓ GET /api/dashboard (10 departments)
  ✓ GET /api/dashboard (Average CGPA computed)
  ✓ POST /api/query: Top 10 Students
  ✓ Explanation generated
  ✓ POST /api/query: Department Count
  ✓ Automatic Bar Chart recommendation
  ✓ POST /api/query: Attendance filter
  ✓ POST /api/query: Relational Join (Students + Subjects + Marks)
  ✓ POST /api/query: Graceful rejection of missing schema (salary)
  ✓ POST /api/query: Reject destructive prompt
  ✓ GET /api/query-history: Audit trail logged

TEST RESULTS: 24 PASSED, 0 FAILED
```

---

## 💡 Example Queries & Demonstrations

### 1. Level 1 — Simple
- *"What is the total number of students?"*
- *"How many faculty members are there?"*
- *"Show all departments."*

### 2. Level 2 — Filter
- *"Show all students from AIML."*
- *"Show students with CGPA above 8."*
- *"Which students have attendance below 75%?"*
- *"Find students who have more than one backlog."*

### 3. Level 3 — Aggregation
- *"What is the average CGPA of AIML students?"*
- *"What is the average attendance of CSE department?"*
- *"Show average marks in Machine Learning."*

### 4. Level 4 — Grouping
- *"How many students are enrolled in each department?"*
- *"What is the average CGPA of each department?"*
- *"Show the distribution of grades in Machine Learning."*
- *"Show average marks by department."*

### 5. Level 5 — Cross-Table Relational Join
- *"Show all AIML students who scored above 80 in Machine Learning."*
- *"Show students who failed Machine Learning."*
- *"Which faculty teaches the most students?"*
- *"Show attendance percentage of students in Machine Learning."*

### 6. Level 6 — Multi-Condition
- *"Which students have both CGPA above 8.5 and attendance above 85%?"*
- *"Show AIML students with CGPA above 8 and attendance above 85%."*
- *"Show CSE students from Bangalore with CGPA above 8.5."*

### 7. Level 7 — Ranking & Top N
- *"Who are the top 10 students by CGPA?"*
- *"Show the top 5 students in AIML."*
- *"Which department has the highest average CGPA?"*
- *"Which subject has the lowest average marks?"*

### 8. Level 8 — Comparative Inquiries
- *"Compare the average CGPA of AIML and CSE."*
- *"Compare average marks between CSE and AIML."*
- *"Compare average attendance between CSE and ECE."*
- *"Compare average marks between Machine Learning and Deep Learning."*

### 9. Out-of-Scope Rejection (No Hallucination)
- Question: *"What is the average salary of employees?"*
- System Response: *"I cannot answer this question because the university relational database does not contain salary information. The database tracks students, departments, faculty, courses, marks, and attendance."*

### 10. Malicious Destructive Input Rejection
- Question: *"Delete all students."* or *"DROP TABLE students;"*
- System Response: *"Security Policy Violation: Destructive database statements (such as DELETE, DROP, TRUNCATE, ALTER, INSERT, UPDATE) are prohibited. QueryMind operates exclusively in read-only analysis mode."*

---

## 🌐 API Reference

### `POST /api/query`
Executes an end-to-end natural language query:
```json
// Request
{
  "question": "Show the top 5 students in AIML by CGPA.",
  "session_id": "session_abc123"
}

// Response
{
  "question": "Show the top 5 students in AIML by CGPA.",
  "intent": "TOP_N",
  "entities": {
    "departments": ["AIML"],
    "limit": 5,
    "order": "DESC"
  },
  "sql": "SELECT s.usn, s.first_name, s.last_name, d.department_code, s.cgpa FROM students s JOIN departments d ON s.department_id = d.department_id WHERE d.department_code = 'AIML' ORDER BY s.cgpa DESC LIMIT 5;",
  "columns": ["usn", "first_name", "last_name", "department_code", "cgpa"],
  "rows": [
    { "usn": "1MS24AIML346", "first_name": "Harish", "last_name": "Kulkarni", "cgpa": 9.67 }
  ],
  "row_count": 5,
  "execution_time_ms": 8.03,
  "explanation": "Retrieved top 5 records. The highest-ranked student is Harish Kulkarni with a CGPA of 9.67.",
  "visualization": {
    "can_visualize": true,
    "recommended_chart": "bar",
    "x_axis_key": "usn",
    "y_axis_key": "cgpa"
  },
  "tables_used": ["departments", "students"],
  "status": "SUCCESS"
}
```

### Other Endpoints
- `GET /api/dashboard`: Aggregates university metrics (students, depts, pass rate, avg CGPA).
- `GET /api/schema`: Complete schema introspection with table columns, PKs, and foreign keys.
- `GET /api/query-history`: Audit log of past queries and SQL statements.
- `POST /api/query/validate`: Standalone SQL AST security and syntax validator.

---

## 🎓 Viva & Presentation Checklist

For project demonstration and viva presentation:
1. **Show Dashboard**: Highlight that Total Students (5,200), Average CGPA (7.18), and Average Attendance (78.8%) are calculated directly from live PostgreSQL database records.
2. **Execute Single-Table Query**: *"Show all students with CGPA above 9."* (Demonstrates filtering and interactive table grid).
3. **Execute Multi-Table Relational Join**: *"Show all AIML students who scored above 80 in Machine Learning."* (Demonstrates 4-table ANSI JOIN: `students` + `departments` + `marks` + `subjects`).
4. **Demonstrate Dynamic Visualization**: *"How many students are enrolled in each department?"* (Shows automatic Bar Chart recommendation).
5. **Demonstrate Conversational Context**:
   - Query 1: *"Show the top 10 AIML students by CGPA."*
   - Query 2: *"Only show the top 5."* (Demonstrates session memory re-interpreting constraints).
6. **Demonstrate Hallucination Prevention**: *"What is the average salary of employees?"* (Demonstrates graceful out-of-scope schema rejection).
7. **Demonstrate Security Sandbox**: *"Delete all students."* or *"DROP TABLE students;"* (Demonstrates AST security rejection).
8. **Inspect Generated SQL**: Expand the collapsible SQL drawer to demonstrate query transparency.
9. **Show NLP Architecture**: Walk through the 8-stage interactive pipeline in the frontend.

---

## 🔮 Future Scope

- **Multi-Dialect Support**: Extend query synthesizer to support MySQL, SQLite, Snowflake, and BigQuery.
- **Voice Ingestion**: Integrate Web Speech API for voice-driven spoken database queries.
- **Multilingual Support**: Extend tokenization and schema matcher to support Hindi, Kannada, Spanish, and French.
- **Automated Dashboard Generation**: Auto-generate custom multi-chart analytics layouts from complex exploratory queries.

---

## 📄 License

This project is licensed under the MIT License — suitable for academic research, university coursework, and portfolio demonstration.
