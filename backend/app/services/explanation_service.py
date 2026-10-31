from typing import List, Dict, Any, Optional
from backend.app.llm.provider import get_llm_provider


class ExplanationService:
    def __init__(self):
        self.llm_provider = get_llm_provider()

    async def explain_result(
        self,
        question: str,
        intent: str,
        columns: List[str],
        rows: List[Dict[str, Any]],
        execution_time_ms: float
    ) -> str:
        """
        Produces an accurate, data-grounded natural-language explanation of query results.
        """
        row_count = len(rows)
        if row_count == 0:
            return "The database query executed successfully in {ms}ms, but returned no matching records for the specified criteria.".format(ms=execution_time_ms)

        # 1. Try LLM explanation if configured
        if hasattr(self.llm_provider, "is_configured") and self.llm_provider.is_configured():
            prompt = (
                f"User Question: {question}\n"
                f"SQL Columns: {columns}\n"
                f"Sample Results (up to 3 rows): {rows[:3]}\n"
                f"Total Rows Returned: {row_count}\n"
                f"Provide a direct 1-2 sentence factual summary strictly grounded in this data."
            )
            try:
                llm_explanation = await self.llm_provider.generate_explanation(prompt)
                if llm_explanation:
                    return llm_explanation.strip()
            except Exception:
                pass

        # 2. Deterministic high-precision data-grounded explanation
        first_row = rows[0]

        # Case: Single aggregate value or single department/subject maximum/minimum
        if row_count == 1:
            if "highest_average_cgpa" in first_row:
                dept = first_row.get("department_name") or first_row.get("department_code", "Department")
                return f"Based on the database records, {dept} has the highest average CGPA at {first_row['highest_average_cgpa']}."
            elif "lowest_average_marks" in first_row:
                subj = first_row.get("subject_name", "Subject")
                return f"The subject with the lowest average marks is {subj} ({first_row.get('subject_code', '')}) with an average of {first_row['lowest_average_marks']} marks."
            elif "average_cgpa" in first_row:
                return f"The computed average CGPA is {first_row['average_cgpa']} across {first_row.get('total_students', first_row.get('student_count', 'all'))} students."
            elif "student_count" in first_row or "total_students" in first_row:
                cnt = first_row.get("student_count") or first_row.get("total_students")
                return f"There are currently {cnt:,} students matching this query in the university database."
            elif "faculty_name" in first_row and "student_count" in first_row:
                return f"{first_row['faculty_name']} ({first_row.get('department_code', '')}) instructs the highest number of students ({first_row['student_count']:,} students)."

        # Case: Top N ranking (Students or Faculty)
        if intent == "TOP_N":
            if "student_name" in first_row or "first_name" in first_row:
                lead_name = first_row.get("student_name") or f"{first_row.get('first_name', '')} {first_row.get('last_name', '')}"
                lead_metric = first_row.get("cgpa") or first_row.get("average_attendance") or first_row.get("total_marks")
                metric_name = "CGPA" if "cgpa" in first_row else ("attendance" if "attendance" in str(columns) else "score")
                return f"Retrieved top {row_count} records. The highest-ranked student is {lead_name.strip()} with a {metric_name} of {lead_metric}."
            elif "faculty_name" in first_row:
                return f"Displaying top {row_count} faculty members, led by {first_row['faculty_name']} ({first_row.get('department_code', '')}) teaching {first_row.get('student_count', 0)} students."

        # Case: Comparison (Between 2 departments)
        if intent == "COMPARISON" and len(rows) >= 2:
            r1, r2 = rows[0], rows[1]
            code1 = r1.get("department_code", "Dept 1")
            code2 = r2.get("department_code", "Dept 2")
            m1 = r1.get("average_cgpa") or r1.get("average_marks")
            m2 = r2.get("average_cgpa") or r2.get("average_marks")
            metric_label = "average CGPA" if "average_cgpa" in r1 else "average marks"
            return f"Comparison shows {code1} has an {metric_label} of {m1}, compared to {code2} with an {metric_label} of {m2}."

        # Case: Group by breakdown (Departments, Semesters, Subjects)
        if "department_code" in columns and ("student_count" in columns or "average_cgpa" in columns or "average_marks" in columns):
            metric_col = "student_count" if "student_count" in columns else ("average_cgpa" if "average_cgpa" in columns else "average_marks")
            top_dept = rows[0].get("department_code")
            top_val = rows[0].get(metric_col)
            return f"Found breakdown across {row_count} departments. {top_dept} leads with {top_val} {metric_col.replace('_', ' ')}."

        # Case: General list filter
        if "attendance_percentage" in columns:
            return f"Found {row_count} student attendance records matching the attendance filter criteria."

        if "total_marks" in columns or "grade" in columns:
            return f"Retrieved {row_count} student examination marks matching the score criteria."

        return f"Successfully retrieved {row_count} records matching your query criteria in {execution_time_ms}ms."


explanation_service = ExplanationService()
