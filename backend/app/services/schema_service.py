from typing import Dict, List, Any, Optional
from backend.app.database.connection import execute_query_async
from backend.app.schemas.schemas import SchemaTableInfo, SchemaColumnInfo, SchemaResponse

TABLE_DESCRIPTIONS = {
    "students": "Stores personal, demographic, and academic profile of students including USN, department, CGPA, year, semester, and backlogs.",
    "departments": "Academic departments offering degree programs, with department codes (CSE, AIML, etc.) and HOD details.",
    "subjects": "Course catalog across semesters and departments, specifying subject codes, credits, and subject types (CORE, ELECTIVE, LAB).",
    "faculty": "Teaching staff members, designations, department affiliation, experience, and academic specializations.",
    "semesters": "Academic calendar periods mapping academic years (e.g. 2023-24) to semester numbers (1-8).",
    "enrollments": "Registration records linking students with specific subjects, faculty instructors, and semesters.",
    "marks": "Evaluation scores for students per subject and semester, with internal marks (0-40), external marks (0-60), total marks (0-100), letter grade, and PASS/FAIL result status.",
    "attendance": "Class attendance records per student, subject, and semester, tracking classes conducted, classes attended, percentage, and eligibility status.",
    "query_history": "Audit log of natural language queries, generated SQL, execution metrics, and performance timestamps."
}

COLUMN_DESCRIPTIONS = {
    "students": {
        "student_id": "Primary key identifier for a student",
        "usn": "University Seat Number / Unique registration code (e.g. 1MS22AIML042)",
        "first_name": "Student's first name",
        "last_name": "Student's last name / surname",
        "gender": "Gender ('Male', 'Female', 'Other')",
        "date_of_birth": "Birth date of the student",
        "email": "Official student email address",
        "phone": "Contact telephone number",
        "department_id": "Foreign key referencing departments.department_id",
        "admission_year": "Year the student was admitted (e.g. 2022)",
        "current_year": "Current academic year of study (1 to 4)",
        "current_semester": "Current semester of study (1 to 8)",
        "section": "Class division / section letter ('A', 'B', 'C')",
        "cgpa": "Cumulative Grade Point Average on a 10.0 scale (e.g. 8.45)",
        "backlogs": "Count of currently uncleared / failed course backlogs (0 or higher)",
        "city": "Home residential city of the student (e.g. Bangalore, Mysore)",
        "scholarship_status": "Scholarship awarded ('None', 'Merit', 'Need-based', 'Sports')"
    },
    "departments": {
        "department_id": "Primary key identifier for a department",
        "department_name": "Full name of the engineering department (e.g. Artificial Intelligence and Machine Learning)",
        "department_code": "Standard abbreviated code (CSE, AIML, ISE, ECE, EEE, ME, CIVIL, DS, CS, IT)",
        "hod_name": "Name of the Head of the Department",
        "building": "Campus building location",
        "contact_email": "Department administrative email"
    },
    "subjects": {
        "subject_id": "Primary key identifier for a subject",
        "subject_code": "Unique course code (e.g. AIML501, CS204)",
        "subject_name": "Official title of the subject (e.g. Machine Learning, Operating Systems)",
        "department_id": "Foreign key referencing departments.department_id",
        "credits": "Credit value assigned to the course (1 to 6)",
        "semester": "Semester number when the subject is offered (1 to 8)",
        "subject_type": "Classification: 'CORE', 'ELECTIVE', or 'LAB'"
    },
    "faculty": {
        "faculty_id": "Primary key identifier for a faculty member",
        "employee_id": "Unique employee identification code",
        "first_name": "Faculty member's first name",
        "last_name": "Faculty member's last name",
        "email": "Faculty official email address",
        "department_id": "Foreign key referencing departments.department_id",
        "designation": "Academic rank: Professor, Associate Professor, Assistant Professor, Visiting Faculty",
        "experience_years": "Total years of teaching/research experience",
        "specialization": "Primary academic domain (e.g. Machine Learning, VLSI, Distributed Systems)"
    },
    "semesters": {
        "semester_id": "Primary key identifier for a semester period",
        "academic_year": "Academic year designation (e.g. 2023-24)",
        "semester_number": "Semester number (1 through 8)",
        "semester_name": "Display title (e.g. Semester 1, Semester 5)",
        "start_date": "Term starting date",
        "end_date": "Term ending date"
    },
    "enrollments": {
        "enrollment_id": "Primary key identifier for course registration",
        "student_id": "Foreign key referencing students.student_id",
        "subject_id": "Foreign key referencing subjects.subject_id",
        "semester_id": "Foreign key referencing semesters.semester_id",
        "faculty_id": "Foreign key referencing faculty.faculty_id (instructor)",
        "enrollment_date": "Date student enrolled in course",
        "status": "Course enrollment status: 'ACTIVE', 'COMPLETED', 'DROPPED'"
    },
    "marks": {
        "mark_id": "Primary key identifier for an examination score record",
        "student_id": "Foreign key referencing students.student_id",
        "subject_id": "Foreign key referencing subjects.subject_id",
        "semester_id": "Foreign key referencing semesters.semester_id",
        "internal_marks": "Continuous internal assessment score (0.0 to 40.0)",
        "external_marks": "Semester end exam score (0.0 to 60.0)",
        "total_marks": "Combined final score = internal + external (0.0 to 100.0)",
        "grade": "Letter grade: 'O' (>=90), 'A+' (80-89), 'A' (70-79), 'B+' (60-69), 'B' (55-59), 'C' (50-54), 'P' (40-49), 'F' (<40)",
        "grade_point": "Numerical grade point corresponding to letter grade (10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 0.0)",
        "result_status": "Final course outcome: 'PASS' or 'FAIL'"
    },
    "attendance": {
        "attendance_id": "Primary key identifier for attendance track",
        "student_id": "Foreign key referencing students.student_id",
        "subject_id": "Foreign key referencing subjects.subject_id",
        "semester_id": "Foreign key referencing semesters.semester_id",
        "classes_conducted": "Total number of class sessions held during the term",
        "classes_attended": "Number of class sessions attended by the student",
        "attendance_percentage": "Calculated percentage: (attended / conducted) * 100",
        "attendance_status": "Eligibility category: 'ELIGIBLE' (>=85%), 'WARNING' (75-84.9%), 'CONDONED' (65-74.9%), 'DETAINED' (<65%)"
    }
}


class SchemaService:
    def __init__(self):
        self._cached_schema: Optional[SchemaResponse] = None
        self._table_metadata: Dict[str, SchemaTableInfo] = {}
        self._foreign_keys: List[Dict[str, str]] = []

    async def get_schema(self, force_refresh: bool = False) -> SchemaResponse:
        if self._cached_schema and not force_refresh:
            return self._cached_schema

        # 1. Fetch tables
        _, t_rows = await execute_query_async("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """, readonly=False)
        table_names = [r["table_name"] for r in t_rows]

        # 2. Fetch Foreign Keys
        _, fk_rows = await execute_query_async("""
            SELECT
                tc.table_name AS source_table,
                kcu.column_name AS source_column,
                ccu.table_name AS target_table,
                ccu.column_name AS target_column
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
              AND tc.table_schema = 'public';
        """, readonly=False)

        foreign_keys = []
        fk_map = {}
        for r in fk_rows:
            fk_info = {
                "source_table": r["source_table"],
                "source_column": r["source_column"],
                "target_table": r["target_table"],
                "target_column": r["target_column"],
                "display": f"{r['source_table']}.{r['source_column']} -> {r['target_table']}.{r['target_column']}"
            }
            foreign_keys.append(fk_info)
            fk_map[(r["source_table"], r["source_column"])] = f"{r['target_table']}.{r['target_column']}"

        self._foreign_keys = foreign_keys

        # 3. Introspect each table
        table_infos: List[SchemaTableInfo] = []
        for t_name in table_names:
            _, col_rows = await execute_query_async(f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = '{t_name}'
                ORDER BY ordinal_position;
            """, readonly=False)

            _, pk_rows = await execute_query_async(f"""
                SELECT kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name = kcu.constraint_name
                  AND tc.table_schema = kcu.table_schema
                WHERE tc.constraint_type = 'PRIMARY KEY'
                  AND tc.table_schema = 'public'
                  AND tc.table_name = '{t_name}';
            """, readonly=False)
            pk_cols = set(r["column_name"] for r in pk_rows)

            _, cnt_rows = await execute_query_async(f"SELECT COUNT(*) AS cnt FROM {t_name};", readonly=False)
            row_count = int(cnt_rows[0]["cnt"]) if cnt_rows else 0

            columns_info: List[SchemaColumnInfo] = []
            for col in col_rows:
                c_name = col["column_name"]
                c_type = col["data_type"]
                is_null = (col["is_nullable"] == "YES")
                is_pk = c_name in pk_cols
                is_fk = (t_name, c_name) in fk_map
                target_fk = fk_map.get((t_name, c_name))

                # Samples
                sample_vals: List[Any] = []
                try:
                    _, s_rows = await execute_query_async(
                        f"SELECT DISTINCT {c_name} FROM {t_name} WHERE {c_name} IS NOT NULL LIMIT 4;",
                        readonly=False
                    )
                    sample_vals = [str(list(r.values())[0]) for r in s_rows]
                except Exception:
                    pass

                desc = COLUMN_DESCRIPTIONS.get(t_name, {}).get(c_name, f"Column {c_name} in table {t_name}")

                columns_info.append(SchemaColumnInfo(
                    name=c_name,
                    data_type=c_type,
                    is_nullable=is_null,
                    is_primary_key=is_pk,
                    is_foreign_key=is_fk,
                    foreign_key_target=target_fk,
                    description=desc,
                    sample_values=sample_vals
                ))

            table_desc = TABLE_DESCRIPTIONS.get(t_name, f"Relational table {t_name}")
            t_fks = [fk for fk in foreign_keys if fk["source_table"] == t_name]

            t_info = SchemaTableInfo(
                name=t_name,
                description=table_desc,
                row_count=row_count,
                columns=columns_info,
                foreign_keys=t_fks
            )
            table_infos.append(t_info)
            self._table_metadata[t_name] = t_info

        self._cached_schema = SchemaResponse(tables=table_infos, relationships=foreign_keys)
        return self._cached_schema

    def get_table_names(self) -> List[str]:
        return list(self._table_metadata.keys())

    def get_table_info(self, table_name: str) -> Optional[SchemaTableInfo]:
        return self._table_metadata.get(table_name)

    def format_relevant_schema_prompt(self, relevant_tables: List[str]) -> str:
        if not relevant_tables:
            relevant_tables = list(self._table_metadata.keys())

        lines = ["### DATABASE SCHEMA ###"]
        for t_name in relevant_tables:
            if t_name not in self._table_metadata:
                continue
            t_info = self._table_metadata[t_name]
            lines.append(f"\nTable: {t_name} ({t_info.description})")
            lines.append("Columns:")
            for col in t_info.columns:
                pk_tag = " [PRIMARY KEY]" if col.is_primary_key else ""
                fk_tag = f" [REFERENCES {col.foreign_key_target}]" if col.is_foreign_key else ""
                samples = f" (e.g. {', '.join(col.sample_values[:3])})" if col.sample_values else ""
                lines.append(f"  - {col.name} ({col.data_type}){pk_tag}{fk_tag}: {col.description}{samples}")

        lines.append("\n### FOREIGN KEY RELATIONSHIPS ###")
        for fk in self._foreign_keys:
            if fk["source_table"] in relevant_tables or fk["target_table"] in relevant_tables:
                lines.append(f"  - {fk['display']}")

        return "\n".join(lines)


schema_service = SchemaService()
