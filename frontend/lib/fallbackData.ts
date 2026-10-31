import { DashboardStats, SchemaResponse } from "../types";

export const FALLBACK_DASHBOARD: DashboardStats = {
  total_students: 5200,
  total_departments: 10,
  total_subjects: 438,
  total_faculty: 120,
  total_enrollments: 135188,
  average_cgpa: 7.18,
  average_attendance: 78.77,
  pass_percentage: 97.96,
  department_distribution: [
    { department_code: "AIML", department_name: "Artificial Intelligence and Machine Learning", student_count: 520 },
    { department_code: "CSE", department_name: "Computer Science and Engineering", student_count: 520 },
    { department_code: "DS", department_name: "Data Science", student_count: 520 },
    { department_code: "CS", department_name: "Cyber Security", student_count: 520 },
    { department_code: "IT", department_name: "Information Technology", student_count: 520 },
    { department_code: "ECE", department_name: "Electronics and Communication Engineering", student_count: 520 },
    { department_code: "EEE", department_name: "Electrical and Electronics Engineering", student_count: 520 },
    { department_code: "ME", department_name: "Mechanical Engineering", student_count: 520 },
    { department_code: "CIVIL", department_name: "Civil Engineering", student_count: 520 },
    { department_code: "ISE", department_name: "Information Science and Engineering", student_count: 520 }
  ],
  department_avg_cgpa: [
    { department_code: "CSE", department_name: "Computer Science and Engineering", average_cgpa: 7.24 },
    { department_code: "ECE", department_name: "Electronics and Communication Engineering", average_cgpa: 7.22 },
    { department_code: "ME", department_name: "Mechanical Engineering", average_cgpa: 7.21 },
    { department_code: "EEE", department_name: "Electrical and Electronics Engineering", average_cgpa: 7.21 },
    { department_code: "IT", department_name: "Information Technology", average_cgpa: 7.2 },
    { department_code: "DS", department_name: "Data Science", average_cgpa: 7.2 },
    { department_code: "ISE", department_name: "Information Science and Engineering", average_cgpa: 7.19 },
    { department_code: "AIML", department_name: "Artificial Intelligence and Machine Learning", average_cgpa: 7.18 },
    { department_code: "CS", department_name: "Cyber Security", average_cgpa: 7.17 },
    { department_code: "CIVIL", department_name: "Civil Engineering", average_cgpa: 7.04 }
  ],
  recent_queries: [
    {
      query_id: 1,
      question: "give me the data of student of all the aiml student",
      intent: "FILTER",
      sql: "SELECT s.usn, s.first_name, s.last_name, d.department_code, s.cgpa FROM students s JOIN departments d ON s.department_id = d.department_id WHERE d.department_code = 'AIML' LIMIT 50;",
      execution_time_ms: 3.67,
      row_count: 50,
      status: "SUCCESS",
      created_at: new Date().toISOString()
    },
    {
      query_id: 2,
      question: "Show total enrollment counts by department",
      intent: "GROUP_BY",
      sql: "SELECT d.department_code, d.department_name, COUNT(s.student_id) AS student_count FROM departments d LEFT JOIN students s ON d.department_id = s.department_id GROUP BY d.department_id, d.department_code, d.department_name ORDER BY student_count DESC LIMIT 50;",
      execution_time_ms: 8.19,
      row_count: 10,
      status: "SUCCESS",
      created_at: new Date().toISOString()
    }
  ],
  popular_query_types: [
    { intent: "FILTER", count: 92 },
    { intent: "GROUP_BY", count: 39 },
    { intent: "COUNT", count: 22 },
    { intent: "TOP_N", count: 17 },
    { intent: "MAXIMUM", count: 16 }
  ]
};

export const FALLBACK_SCHEMA: SchemaResponse = {
  tables: [
    {
      name: "students",
      description: "Undergraduate student profiles including USN, names, academic standing (CGPA), department, contact details, and admission quota.",
      row_count: 5200,
      columns: [
        { name: "student_id", data_type: "integer", is_nullable: false, is_primary_key: true, is_foreign_key: false, foreign_key_target: null, description: "Primary key identifier for students", sample_values: ["1", "2", "3", "4"] },
        { name: "usn", data_type: "character varying", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "University Seat Number", sample_values: ["1MS21AI001", "1MS21CS042"] },
        { name: "first_name", data_type: "character varying", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Student legal first name", sample_values: ["Aarav", "Ananya", "Rohan"] },
        { name: "last_name", data_type: "character varying", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Student legal surname", sample_values: ["Sharma", "Patel", "Reddy"] },
        { name: "department_id", data_type: "integer", is_nullable: false, is_primary_key: false, is_foreign_key: true, foreign_key_target: "departments.department_id", description: "Foreign key referencing departments", sample_values: ["1", "2", "3"] },
        { name: "current_semester", data_type: "integer", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Active semester of study (1 to 8)", sample_values: ["4", "6", "8"] },
        { name: "cgpa", data_type: "numeric", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Cumulative Grade Point Average (0.00 to 10.00)", sample_values: ["9.2", "8.7", "7.4"] },
        { name: "city", data_type: "character varying", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Residential origin city", sample_values: ["Bangalore", "Mumbai", "Delhi"] }
      ],
      foreign_keys: [
        { source_table: "students", source_column: "department_id", target_table: "departments", target_column: "department_id", display: "students.department_id -> departments.department_id" }
      ]
    },
    {
      name: "departments",
      description: "Academic departments offering degree programs, with department codes (CSE, AIML, etc.) and HOD details.",
      row_count: 10,
      columns: [
        { name: "department_id", data_type: "integer", is_nullable: false, is_primary_key: true, is_foreign_key: false, foreign_key_target: null, description: "Primary key identifier for a department", sample_values: ["1", "2", "3"] },
        { name: "department_code", data_type: "character varying", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Standard abbreviated code (CSE, AIML, etc.)", sample_values: ["AIML", "CSE", "ECE"] },
        { name: "department_name", data_type: "character varying", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Full department name", sample_values: ["Artificial Intelligence and Machine Learning"] },
        { name: "hod_name", data_type: "character varying", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Head of Department", sample_values: ["Dr. Sangeetha Rao"] }
      ],
      foreign_keys: []
    },
    {
      name: "attendance",
      description: "Class attendance records per student, subject, and semester, tracking classes conducted, attended, and eligibility status.",
      row_count: 135188,
      columns: [
        { name: "attendance_id", data_type: "integer", is_nullable: false, is_primary_key: true, is_foreign_key: false, foreign_key_target: null, description: "Primary key identifier", sample_values: ["1", "2", "3"] },
        { name: "student_id", data_type: "integer", is_nullable: false, is_primary_key: false, is_foreign_key: true, foreign_key_target: "students.student_id", description: "Foreign key to students", sample_values: ["1", "2"] },
        { name: "classes_conducted", data_type: "integer", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Sessions held", sample_values: ["60"] },
        { name: "classes_attended", data_type: "integer", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Sessions attended", sample_values: ["52"] },
        { name: "attendance_percentage", data_type: "numeric", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Percentage attended", sample_values: ["86.67"] },
        { name: "attendance_status", data_type: "character varying", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Eligibility: ELIGIBLE, WARNING, DETAINED", sample_values: ["ELIGIBLE"] }
      ],
      foreign_keys: [
        { source_table: "attendance", source_column: "student_id", target_table: "students", target_column: "student_id", display: "attendance.student_id -> students.student_id" }
      ]
    },
    {
      name: "subjects",
      description: "Course catalog across semesters and departments, specifying subject codes, credits, and subject types.",
      row_count: 438,
      columns: [
        { name: "subject_id", data_type: "integer", is_nullable: false, is_primary_key: true, is_foreign_key: false, foreign_key_target: null, description: "Primary key identifier", sample_values: ["1", "2"] },
        { name: "subject_code", data_type: "character varying", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Course code", sample_values: ["AIML501", "CS204"] },
        { name: "subject_name", data_type: "character varying", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Course name", sample_values: ["Machine Learning", "Operating Systems"] },
        { name: "credits", data_type: "integer", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Credits", sample_values: ["4", "3"] }
      ],
      foreign_keys: []
    },
    {
      name: "faculty",
      description: "Faculty teaching staff across departments, designations, and qualifications.",
      row_count: 120,
      columns: [
        { name: "faculty_id", data_type: "integer", is_nullable: false, is_primary_key: true, is_foreign_key: false, foreign_key_target: null, description: "Primary key identifier", sample_values: ["1", "2"] },
        { name: "faculty_name", data_type: "character varying", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Professor name", sample_values: ["Dr. Arvind Kulkarni"] },
        { name: "designation", data_type: "character varying", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Professor rank", sample_values: ["Professor", "Associate Professor"] }
      ],
      foreign_keys: []
    },
    {
      name: "enrollments",
      description: "Registration records linking students with specific subjects, faculty instructors, and semesters.",
      row_count: 135188,
      columns: [
        { name: "enrollment_id", data_type: "integer", is_nullable: false, is_primary_key: true, is_foreign_key: false, foreign_key_target: null, description: "Primary key identifier", sample_values: ["1", "2"] },
        { name: "student_id", data_type: "integer", is_nullable: false, is_primary_key: false, is_foreign_key: true, foreign_key_target: "students.student_id", description: "Student reference", sample_values: ["1", "2"] },
        { name: "subject_id", data_type: "integer", is_nullable: false, is_primary_key: false, is_foreign_key: true, foreign_key_target: "subjects.subject_id", description: "Subject reference", sample_values: ["1", "2"] }
      ],
      foreign_keys: []
    },
    {
      name: "marks",
      description: "Academic examination scores including internal assessments, semester exams, grade points, and result status.",
      row_count: 135188,
      columns: [
        { name: "mark_id", data_type: "integer", is_nullable: false, is_primary_key: true, is_foreign_key: false, foreign_key_target: null, description: "Primary key identifier", sample_values: ["1", "2"] },
        { name: "student_id", data_type: "integer", is_nullable: false, is_primary_key: false, is_foreign_key: true, foreign_key_target: "students.student_id", description: "Student reference", sample_values: ["1", "2"] },
        { name: "total_marks", data_type: "numeric", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Final mark out of 100", sample_values: ["88", "92"] },
        { name: "grade", data_type: "character varying", is_nullable: false, is_primary_key: false, is_foreign_key: false, foreign_key_target: null, description: "Letter grade ('S', 'A', 'B', 'C', 'D', 'E', 'F')", sample_values: ["S", "A"] }
      ],
      foreign_keys: []
    }
  ],
  relationships: [
    { source_table: "students", source_column: "department_id", target_table: "departments", target_column: "department_id", display: "students.department_id -> departments.department_id" },
    { source_table: "attendance", source_column: "student_id", target_table: "students", target_column: "student_id", display: "attendance.student_id -> students.student_id" },
    { source_table: "enrollments", source_column: "student_id", target_table: "students", target_column: "student_id", display: "enrollments.student_id -> students.student_id" },
    { source_table: "marks", source_column: "student_id", target_table: "students", target_column: "student_id", display: "marks.student_id -> students.student_id" }
  ]
};

