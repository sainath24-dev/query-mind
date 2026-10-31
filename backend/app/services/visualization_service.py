from typing import List, Dict, Any, Optional
from backend.app.schemas.schemas import VisualizationConfig


class VisualizationService:
    def __init__(self):
        pass

    def determine_visualization(
        self,
        columns: List[str],
        rows: List[Dict[str, Any]],
        intent: str
    ) -> VisualizationConfig:
        """
        Determines the most intuitive visualization format for a given SQL query result.
        """
        row_count = len(rows)

        # Non-visualizable if no rows or single scalar row without category
        if row_count <= 1 and not (row_count == 1 and len(columns) > 1):
            return VisualizationConfig(
                can_visualize=False,
                recommended_chart="table",
                title="Tabular Results"
            )

        # 1. PIE / DONUT CHART: Categorical distribution with <= 10 categories
        # E.g. Grade distribution, Result status, Scholarship status
        if "grade" in columns and "count" in columns and row_count <= 10:
            return VisualizationConfig(
                can_visualize=True,
                recommended_chart="pie",
                x_axis_key="grade",
                y_axis_key="count",
                category_key="grade",
                title="Grade Distribution",
                description="Distribution of grades among evaluated students"
            )

        if "result_status" in columns and "count" in columns:
            return VisualizationConfig(
                can_visualize=True,
                recommended_chart="pie",
                x_axis_key="result_status",
                y_axis_key="count",
                category_key="result_status",
                title="Pass / Fail Outcome Distribution",
                description="Proportion of students who passed vs failed"
            )

        # 2. LINE CHART: Sequential / Temporal Progression
        # E.g. Semester number + average marks, Year + student count
        if any(col in columns for col in ["semester_number", "current_semester", "admission_year"]):
            seq_col = next(col for col in columns if col in ["semester_number", "current_semester", "admission_year"])
            metric_cols = [c for c in columns if c in ["avg_marks", "average_marks", "average_cgpa", "student_count", "total_marks"]]
            if metric_cols:
                return VisualizationConfig(
                    can_visualize=True,
                    recommended_chart="line",
                    x_axis_key=seq_col,
                    y_axis_key=metric_cols[0],
                    title=f"{metric_cols[0].replace('_', ' ').title()} by {seq_col.replace('_', ' ').title()}",
                    description=f"Trend across sequential {seq_col.replace('_', ' ')}"
                )

        # 3. BAR CHART: Categorical Groups + Numerical Aggregates
        # Department + Student Count / Avg CGPA / Avg Marks
        if any(c in columns for c in ["department_code", "department_name"]):
            cat_col = "department_code" if "department_code" in columns else "department_name"
            metric_cols = [
                c for c in columns
                if c in ["student_count", "total_students", "average_cgpa", "average_marks", "avg_marks", "highest_average_cgpa", "lowest_average_cgpa"]
            ]
            if metric_cols:
                metric_name = metric_cols[0].replace("_", " ").title()
                return VisualizationConfig(
                    can_visualize=True,
                    recommended_chart="bar",
                    x_axis_key=cat_col,
                    y_axis_key=metric_cols[0],
                    title=f"{metric_name} by Department",
                    description=f"Comparative bar chart showing {metric_name.lower()} per department"
                )

        # Subject + Average Marks
        if any(c in columns for c in ["subject_code", "subject_name"]):
            cat_col = "subject_code" if "subject_code" in columns else "subject_name"
            metric_cols = [c for c in columns if c in ["average_marks", "avg_marks", "lowest_average_marks"]]
            if metric_cols:
                return VisualizationConfig(
                    can_visualize=True,
                    recommended_chart="bar",
                    x_axis_key=cat_col,
                    y_axis_key=metric_cols[0],
                    title="Average Marks by Subject",
                    description="Comparative subject performance"
                )

        # Top N Students ranking by CGPA
        if intent == "TOP_N" and "cgpa" in columns and row_count <= 15:
            label_col = "usn" if "usn" in columns else ("student_name" if "student_name" in columns else columns[0])
            return VisualizationConfig(
                can_visualize=True,
                recommended_chart="bar",
                x_axis_key=label_col,
                y_axis_key="cgpa",
                title="Top Ranked Students by CGPA",
                description="Comparative ranking bar chart"
            )

        # Default: Detailed records are best represented as interactive tables
        return VisualizationConfig(
            can_visualize=False,
            recommended_chart="table",
            title="Tabular Data Records"
        )


visualization_service = VisualizationService()
