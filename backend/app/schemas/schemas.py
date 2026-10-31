from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class QueryRequest(BaseModel):
    question: str = Field(..., description="Natural language question to execute against the database")
    session_id: str = Field("default_session", description="Session identifier for conversational context")


class VisualizationConfig(BaseModel):
    can_visualize: bool = False
    recommended_chart: str = "table" # "bar", "line", "pie", "table"
    x_axis_key: Optional[str] = None
    y_axis_key: Optional[str] = None
    category_key: Optional[str] = None
    title: str = ""
    description: str = ""


class QueryResponse(BaseModel):
    query_id: Optional[int] = None
    question: str
    intent: str
    entities: Dict[str, Any]
    sql: str
    columns: List[str]
    rows: List[Dict[str, Any]]
    row_count: int
    execution_time_ms: float
    explanation: str
    visualization: VisualizationConfig
    tables_used: List[str]
    session_id: str
    is_answerable: bool = True
    error_message: Optional[str] = None
    status: str = "SUCCESS" # "SUCCESS", "UNANSWERABLE", "ERROR"


class ValidateQueryRequest(BaseModel):
    sql: str


class ValidateQueryResponse(BaseModel):
    is_valid: bool
    is_safe: bool
    statement_type: str
    tables_referenced: List[str]
    columns_referenced: List[str]
    error_message: Optional[str] = None


class ExplainQueryRequest(BaseModel):
    question: str
    sql: str
    columns: List[str]
    rows: List[Dict[str, Any]]


class ExplainQueryResponse(BaseModel):
    explanation: str


class SchemaColumnInfo(BaseModel):
    name: str
    data_type: str
    is_nullable: bool
    is_primary_key: bool
    is_foreign_key: bool
    foreign_key_target: Optional[str] = None
    description: str
    sample_values: List[Any] = []


class SchemaTableInfo(BaseModel):
    name: str
    description: str
    row_count: int
    columns: List[SchemaColumnInfo]
    foreign_keys: List[Dict[str, str]] = []


class SchemaResponse(BaseModel):
    tables: List[SchemaTableInfo]
    relationships: List[Dict[str, str]]


class DashboardStatsResponse(BaseModel):
    total_students: int
    total_departments: int
    total_subjects: int
    total_faculty: int
    total_enrollments: int
    average_cgpa: float
    average_attendance: float
    pass_percentage: float
    department_distribution: List[Dict[str, Any]]
    department_avg_cgpa: List[Dict[str, Any]]
    recent_queries: List[Dict[str, Any]]
    popular_query_types: List[Dict[str, Any]]


class QueryHistoryItem(BaseModel):
    query_id: int
    session_id: str
    natural_language_question: str
    intent: Optional[str] = None
    generated_sql: str
    execution_time_ms: float
    row_count: int
    status: str
    explanation: Optional[str] = None
    created_at: datetime


class QueryHistoryResponse(BaseModel):
    history: List[QueryHistoryItem]
    total_count: int
