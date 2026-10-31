export interface VisualizationConfig {
  can_visualize: boolean;
  recommended_chart: "bar" | "line" | "pie" | "table";
  x_axis_key?: string | null;
  y_axis_key?: string | null;
  category_key?: string | null;
  title: string;
  description: string;
}

export interface QueryEntities {
  departments: string[];
  subjects: string[];
  primary_entity: string;
  attributes: string[];
  conditions: Array<{
    attribute?: string;
    table?: string;
    column?: string;
    operator: string;
    value: any;
  }>;
  limit?: number | null;
  order?: "ASC" | "DESC" | null;
  city?: string | null;
  semester?: number | null;
  year?: number | null;
  grade?: string | null;
  unsupported_attributes?: string[];
}

export interface QueryResponse {
  query_id?: number | null;
  question: string;
  intent: string;
  entities: QueryEntities;
  sql: string;
  columns: string[];
  rows: Record<string, any>[];
  row_count: number;
  execution_time_ms: number;
  explanation: string;
  visualization: VisualizationConfig;
  tables_used: string[];
  session_id: string;
  is_answerable: boolean;
  error_message?: string | null;
  status: "SUCCESS" | "UNANSWERABLE" | "ERROR";
}

export interface SchemaColumnInfo {
  name: string;
  data_type: string;
  is_nullable: boolean;
  is_primary_key: boolean;
  is_foreign_key: boolean;
  foreign_key_target?: string | null;
  description: string;
  sample_values: any[];
}

export interface SchemaTableInfo {
  name: string;
  description: string;
  row_count: number;
  columns: SchemaColumnInfo[];
  foreign_keys: Array<{
    source_table: string;
    source_column: string;
    target_table: string;
    target_column: string;
    display: string;
  }>;
}

export interface SchemaResponse {
  tables: SchemaTableInfo[];
  relationships: Array<{
    source_table: string;
    source_column: string;
    target_table: string;
    target_column: string;
    display: string;
  }>;
}

export interface DashboardStats {
  total_students: number;
  total_departments: number;
  total_subjects: number;
  total_faculty: number;
  total_enrollments: number;
  average_cgpa: number;
  average_attendance: number;
  pass_percentage: number;
  department_distribution: Array<{
    department_code: string;
    department_name: string;
    student_count: number;
  }>;
  department_avg_cgpa: Array<{
    department_code: string;
    department_name: string;
    average_cgpa: number;
  }>;
  recent_queries: Array<{
    query_id: number;
    question: string;
    intent: string;
    sql: string;
    execution_time_ms: number;
    row_count: number;
    status: string;
    created_at: string;
  }>;
  popular_query_types: Array<{
    intent: string;
    count: number;
  }>;
}

export interface QueryHistoryItem {
  query_id: number;
  session_id: string;
  natural_language_question: string;
  intent?: string | null;
  generated_sql: string;
  execution_time_ms: number;
  row_count: number;
  status: string;
  explanation?: string | null;
  created_at: string;
}

export interface QueryHistoryResponse {
  history: QueryHistoryItem[];
  total_count: number;
}
