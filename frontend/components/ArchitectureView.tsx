"use client";

import React, { useState } from "react";
import {
  Search,
  Filter,
  Brain,
  Layers,
  Code2,
  ShieldCheck,
  Database,
  CheckCircle2,
  ArrowRight,
  Terminal,
  Cpu,
  Lock,
  GitBranch
} from "lucide-react";

interface PipelineStep {
  id: string;
  stepNumber: string;
  title: string;
  subtitle: string;
  category: "NLP" | "Semantic" | "SQL" | "Security" | "Database";
  nlpConcept: string;
  componentFile: string;
  summary: string;
  howItWorks: string[];
  exampleInput: string;
  exampleOutput: string;
  guarantees: string;
}

const PIPELINE_STEPS: PipelineStep[] = [
  {
    id: "step-1",
    stepNumber: "01",
    title: "NLP Preprocessing & Cleaning",
    subtitle: "Tokenization, case normalization, and conversational noise reduction",
    category: "NLP",
    nlpConcept: "Text Normalization & Tokenization",
    componentFile: "backend/app/nlp/preprocessor.py",
    summary:
      "Cleans the raw user query, strips conversational fillers ('give me', 'show me', 'can you list'), and normalizes domain abbreviations while preserving critical numbers, operators, and USN patterns.",
    howItWorks: [
      "Trims leading conversational filler phrases ('give me the data of', 'please find', 'list all').",
      "Standardizes academic acronyms (e.g., 'aiml' -> 'AIML', 'cse' -> 'CSE', 'gpa' -> 'CGPA').",
      "Preserves comparison operators ('more than', 'below', '>=', '<=') and numeric thresholds."
    ],
    exampleInput: '"give me the data of student of all the aiml student"',
    exampleOutput: '"students from AIML"',
    guarantees: "Eliminates parsing ambiguity and prevents filler words from distorting entity extraction."
  },
  {
    id: "step-2",
    stepNumber: "02",
    title: "Named Entity & Attribute Extraction",
    subtitle: "Domain recognition of departments, course subjects, metrics, and out-of-scope detection",
    category: "NLP",
    nlpConcept: "Information Extraction & Named Entity Recognition (NER)",
    componentFile: "backend/app/nlp/entity_extractor.py",
    summary:
      "Scans tokens against academic ontology: maps 10 engineering departments, fuzzy-matches across 438 university course titles, extracts numerical filters, and detects queries outside database scope.",
    howItWorks: [
      "Matches department codes and colloquial aliases across 10 official academic disciplines.",
      "Uses sequence matcher algorithm to fuzzy-match course titles with typo-tolerance.",
      "Extracts numeric constraints (e.g., 'above 8.5 CGPA', 'attendance below 75%').",
      "Rejects out-of-scope requests (e.g., 'placement packages', 'hostel fees') with educational feedback."
    ],
    exampleInput: '"students from AIML with attendance below 75%"',
    exampleOutput: JSON.stringify(
      {
        departments: ["AIML"],
        primary_entity: "students",
        condition: { field: "attendance_percentage", operator: "<", value: 75.0 },
        is_out_of_scope: false
      },
      null,
      2
    ),
    guarantees: "Guarantees domain grounding; prevents hallucinated or unrepresented attributes from reaching SQL compilation."
  },
  {
    id: "step-3",
    stepNumber: "03",
    title: "Intent Classification",
    subtitle: "Categorizing query into one of 8 canonical analytical query objectives",
    category: "NLP",
    nlpConcept: "Semantic Intent Classification & Clause Mapping",
    componentFile: "backend/app/nlp/intent_classifier.py",
    summary:
      "Determines the structural purpose of the question—identifying whether the query requires counting, averaging, ranking top N, grouping, or record-level filtering.",
    howItWorks: [
      "Classifies input into canonical intents: COUNT, AVERAGE, TOP_N, COMPARISON, GROUP_BY, FILTER, or DETAIL_LOOKUP.",
      "Identifies required SQL aggregate functions (AVG, COUNT, MAX, MIN) and ordering clauses.",
      "Recognizes multi-department comparative queries ('Compare average marks of CSE vs AIML')."
    ],
    exampleInput: '"give me the data of student of all the aiml student"',
    exampleOutput: JSON.stringify(
      {
        intent: "FILTER",
        confidence: 0.96,
        target_clause: "SELECT * ... WHERE department_code = 'AIML'",
        requires_aggregation: false
      },
      null,
      2
    ),
    guarantees: "Enforces deterministic SQL structural templates tailored to the user's specific analytical goal."
  },
  {
    id: "step-4",
    stepNumber: "04",
    title: "Semantic Schema Matching",
    subtitle: "TF-IDF Vector Space Model & Cosine Similarity over database concept profiles",
    category: "Semantic",
    nlpConcept: "TF-IDF Vector Space Model & Cosine Similarity",
    componentFile: "backend/app/nlp/schema_matcher.py",
    summary:
      "Projects natural language terms into a high-dimensional vector space indexed over verified PostgreSQL table and column profiles, calculating cosine similarity to select the exact relational entities.",
    howItWorks: [
      "Maintains domain concept profiles constructed from table descriptions, column names, and semantic synonyms.",
      "Calculates Cosine Similarity between the normalized user query vector and database entity vectors.",
      "Resolves foreign key relational bridge paths when queries span multiple tables (e.g. students -> enrollments -> subjects)."
    ],
    exampleInput: 'Terms: ["student", "aiml"]',
    exampleOutput: JSON.stringify(
      {
        matched_tables: ["students", "departments"],
        bridge_tables: [],
        join_path: "students.department_id = departments.department_id",
        similarity_score: 0.94
      },
      null,
      2
    ),
    guarantees: "Eliminates column hallucination by strictly constraining SQL to verified PostgreSQL schema definitions."
  },
  {
    id: "step-5",
    stepNumber: "05",
    title: "SQL Synthesis & Generation",
    subtitle: "Deterministic semantic rule engine combined with dynamic LLM compilation",
    category: "SQL",
    nlpConcept: "Natural Language to Code Generation (NL2SQL)",
    componentFile: "backend/app/sql/generator.py",
    summary:
      "Synthesizes ANSI PostgreSQL query strings by combining the extracted intent, filtered entities, and resolved schema join paths into high-performance SQL with defensive LIMIT guards.",
    howItWorks: [
      "Constructs explicit ANSI SQL JOIN clauses matching primary/foreign keys.",
      "Applies clean table aliasing (s for students, d for departments, a for attendance).",
      "Applies case-insensitive ILIKE patterns for textual filtering and exact matching for codes.",
      "Injects defensive LIMIT clauses (default 50/100) to protect database memory and bandwidth."
    ],
    exampleInput: "Intent: FILTER, Entity: students, Dept: AIML",
    exampleOutput: `SELECT s.student_id, s.usn, s.first_name, s.last_name, 
       s.email, s.cgpa, s.semester, d.department_code, d.department_name
FROM students s
JOIN departments d ON s.department_id = d.department_id
WHERE d.department_code = 'AIML'
ORDER BY s.usn ASC
LIMIT 100;`,
    guarantees: "Produces deterministic, ANSI-compliant SQL queries optimized for PostgreSQL index usage."
  },
  {
    id: "step-6",
    stepNumber: "06",
    title: "AST Validation & Security Sandbox",
    subtitle: "Abstract Syntax Tree parsing and multi-layer destructive statement rejection",
    category: "Security",
    nlpConcept: "SQL AST Parsing & Security Policy Verification",
    componentFile: "backend/app/sql/safety.py",
    summary:
      "Parses generated SQL into an Abstract Syntax Tree (AST) using sqlparse. Verifies that only read-only statements exist and unconditionally blocks injection attempts or destructive commands.",
    howItWorks: [
      "Strict statement verification: Only SELECT and WITH (CTE) queries are permitted.",
      "Unconditionally rejects destructive statements: DROP, DELETE, UPDATE, INSERT, ALTER, TRUNCATE, GRANT, REVOKE.",
      "Blocks SQL injection tricks: Rejects multiple semicoloned queries (query chaining) and sleep/benchmark injections.",
      "Enforces a strict 5.0-second query timeout limit."
    ],
    exampleInput: `SELECT ... FROM students; DROP TABLE students;`,
    exampleOutput: `[REJECTED] Security Violation: Multiple statement execution detected. Semicolon chaining prohibited.`,
    guarantees: "Zero data modification risk. Protects the PostgreSQL database against accidental or malicious tampering."
  },
  {
    id: "step-7",
    stepNumber: "07",
    title: "PostgreSQL Execution & Isolation",
    subtitle: "Execution via dedicated restricted read-only role with statement timeout",
    category: "Database",
    nlpConcept: "Relational Execution & Read-Only Role Isolation",
    componentFile: "backend/app/sql/executor.py",
    summary:
      "Dispatches the validated SQL query to the local PostgreSQL 16 database using an isolated, read-only database user (querymind_readonly) and formats the raw tabular records into typed JSON.",
    howItWorks: [
      "Connects using dedicated restricted role: querymind_readonly with strictly SELECT permissions.",
      "Sets connection-level timeout: SET statement_timeout = 5000 (5 seconds maximum).",
      "Extracts column headers, row records, data types, and execution duration in milliseconds.",
      "Serializes date, decimal, and boolean values cleanly for frontend consumption."
    ],
    exampleInput: `SELECT s.usn, s.first_name, s.last_name FROM students s ... LIMIT 100;`,
    exampleOutput: `100 rows returned in 4.82ms (Total matching in DB: 520 AIML students)`,
    guarantees: "Database-level privilege enforcement guarantees that even if a query bypassed AST checks, PostgreSQL would reject writes."
  },
  {
    id: "step-8",
    stepNumber: "08",
    title: "Grounded Explanation & Visualization",
    subtitle: "Data-to-text natural language summary and automatic visual chart heuristics",
    category: "NLP",
    nlpConcept: "Data-to-Text Natural Language Generation (NLG)",
    componentFile: "backend/app/services/explanation_service.py",
    summary:
      "Synthesizes a friendly, humanized explanation grounded strictly in the returned PostgreSQL rows, and automatically determines whether the dataset can be visualized as a bar chart.",
    howItWorks: [
      "Generates clear, contextual conversational response referencing exact numbers and insights.",
      "Zero hallucination guarantee: The explanation engine only references fields and values present in the returned SQL result.",
      "Heuristic visual detection: If dataset contains numeric comparisons across categories, automatically generates chart configurations."
    ],
    exampleInput: "Execution: 520 AIML student rows retrieved successfully",
    exampleOutput: '"Retrieved 520 students enrolled in the Artificial Intelligence and Machine Learning (AIML) department."',
    guarantees: "Provides full transparency: user gets plain-English summary, raw SQL code block, and interactive data table."
  }
];

interface ArchitectureViewProps {
  onSelectQuery?: (query: string) => void;
}

export const ArchitectureView: React.FC<ArchitectureViewProps> = ({ onSelectQuery }) => {
  const [activeStepId, setActiveStepId] = useState<string>("step-1");
  const currentStep = PIPELINE_STEPS.find((s) => s.id === activeStepId) || PIPELINE_STEPS[0];

  return (
    <div className="max-w-[1020px] mx-auto w-full py-8 px-4 sm:px-6 space-y-10">
      {/* 1. Header Hero */}
      <div className="space-y-3">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-[#0066cc]/10 text-[#0066cc] text-[12px] font-medium">
          <Cpu className="w-3.5 h-3.5" />
          <span>Under the Hood</span>
        </div>
        <h2 className="text-[34px] sm:text-[40px] font-semibold tracking-[-0.025em] text-[#1d1d1f] leading-tight">
          How QueryMind Works
        </h2>
        <p className="text-[17px] text-[#7a7a7a] tracking-[-0.022em] max-w-2xl leading-relaxed">
          QueryMind is an 8-stage Natural Language to SQL pipeline. It transforms free-form human language into safe, deterministic PostgreSQL queries with zero hallucination.
        </p>
      </div>

      {/* 2. Linear Pipeline Flow Ribbon (Apple Minimalist) */}
      <div className="bg-[#ffffff] border border-[#e0e0e0] rounded-[18px] p-5 shadow-[0_1px_3px_rgba(0,0,0,0.02)] space-y-3">
        <div className="flex items-center justify-between text-[12px] text-[#7a7a7a] px-1 font-medium uppercase tracking-wider">
          <span>End-to-End Pipeline Stages</span>
          <span>Click a stage to inspect</span>
        </div>

        {/* 8 Step Buttons */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2">
          {PIPELINE_STEPS.map((step) => {
            const isActive = step.id === activeStepId;
            return (
              <button
                key={step.id}
                onClick={() => setActiveStepId(step.id)}
                className={`p-3 rounded-[14px] text-left transition-all duration-150 flex flex-col justify-between h-[84px] border ${
                  isActive
                    ? "bg-[#0066cc] text-[#ffffff] border-[#0066cc] shadow-sm"
                    : "bg-[#f5f5f7] hover:bg-[#e8e8ed] text-[#1d1d1f] border-transparent"
                }`}
              >
                <div className="flex items-center justify-between w-full">
                  <span
                    className={`font-mono text-[11px] font-bold ${
                      isActive ? "text-[#ffffff]/80" : "text-[#7a7a7a]"
                    }`}
                  >
                    {step.stepNumber}
                  </span>
                  <span
                    className={`text-[9px] uppercase tracking-wider font-semibold px-1.5 py-0.5 rounded-full ${
                      isActive
                        ? "bg-[#ffffff]/20 text-[#ffffff]"
                        : "bg-[#ffffff] text-[#7a7a7a] border border-[#e0e0e0]"
                    }`}
                  >
                    {step.category}
                  </span>
                </div>
                <div className="line-clamp-2 text-[12px] font-medium leading-snug">
                  {step.title.split("&")[0].split("(")[0]}
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* 3. Deep Dive Stage Detail Card */}
      <div className="bg-[#ffffff] border border-[#e0e0e0] rounded-[18px] p-6 sm:p-8 space-y-8 shadow-[0_1px_3px_rgba(0,0,0,0.02)]">
        {/* Stage Header */}
        <div className="flex flex-wrap items-start justify-between gap-4 pb-6 border-b border-[#f0f0f0]">
          <div className="space-y-1 max-w-xl">
            <div className="flex items-center space-x-2 text-[13px] font-mono font-semibold text-[#0066cc]">
              <span>Stage {currentStep.stepNumber} of 08</span>
              <span>·</span>
              <span className="text-[#7a7a7a]">{currentStep.nlpConcept}</span>
            </div>
            <h3 className="text-[26px] sm:text-[30px] font-semibold text-[#1d1d1f] tracking-tight">
              {currentStep.title}
            </h3>
            <p className="text-[15px] text-[#7a7a7a] leading-relaxed">
              {currentStep.subtitle}
            </p>
          </div>

          <div className="text-right">
            <span className="text-[11px] font-mono text-[#7a7a7a] bg-[#f5f5f7] px-3 py-1.5 rounded-full border border-[#e0e0e0] inline-block">
              {currentStep.componentFile}
            </span>
          </div>
        </div>

        {/* 2-Column Content: How It Works & Input/Output */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left: How It Works */}
          <div className="space-y-5">
            <div>
              <h4 className="text-[13px] font-semibold uppercase tracking-wider text-[#7a7a7a] mb-2">
                Process Breakdown
              </h4>
              <p className="text-[15px] text-[#1d1d1f] leading-relaxed">
                {currentStep.summary}
              </p>
            </div>

            <div className="space-y-2.5">
              <h5 className="text-[12px] font-semibold uppercase tracking-wider text-[#7a7a7a]">
                Core Operations
              </h5>
              <ul className="space-y-2">
                {currentStep.howItWorks.map((item, idx) => (
                  <li key={idx} className="flex items-start space-x-2.5 text-[14px] text-[#1d1d1f]">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#0066cc] shrink-0 mt-2" />
                    <span className="leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Safety Guarantee */}
            <div className="p-4 rounded-[14px] bg-[#fafafc] border border-[#e0e0e0] space-y-1">
              <div className="flex items-center space-x-2 text-[12px] font-semibold text-[#0066cc] uppercase tracking-wider">
                <ShieldCheck className="w-4 h-4" />
                <span>Architecture Guarantee</span>
              </div>
              <p className="text-[13px] text-[#7a7a7a] leading-relaxed">
                {currentStep.guarantees}
              </p>
            </div>
          </div>

          {/* Right: Concrete Example (Apple Dark Tile Code Box) */}
          <div className="space-y-4">
            <h4 className="text-[13px] font-semibold uppercase tracking-wider text-[#7a7a7a]">
              Live Transformation Example
            </h4>

            {/* Input Tile */}
            <div className="space-y-1.5">
              <div className="flex items-center justify-between text-[11px] font-medium text-[#7a7a7a]">
                <span>STAGE INPUT</span>
              </div>
              <div className="bg-[#272729] text-[#f5f5f7] p-4 rounded-[12px] font-mono text-[13px] leading-relaxed overflow-x-auto border border-[#333333]">
                <pre className="whitespace-pre-wrap">{currentStep.exampleInput}</pre>
              </div>
            </div>

            {/* Arrow Divider */}
            <div className="flex justify-center py-0.5">
              <ArrowRight className="w-4 h-4 text-[#7a7a7a] rotate-90" />
            </div>

            {/* Output Tile */}
            <div className="space-y-1.5">
              <div className="flex items-center justify-between text-[11px] font-medium text-[#0066cc]">
                <span>STAGE OUTPUT</span>
              </div>
              <div className="bg-[#252527] text-[#2997ff] p-4 rounded-[12px] font-mono text-[13px] leading-relaxed overflow-x-auto border border-[#333333]">
                <pre className="whitespace-pre-wrap">{currentStep.exampleOutput}</pre>
              </div>
            </div>
          </div>
        </div>

        {/* Footer Navigation between steps */}
        <div className="pt-6 border-t border-[#f0f0f0] flex items-center justify-between">
          <button
            onClick={() => {
              const currentIndex = PIPELINE_STEPS.findIndex((s) => s.id === activeStepId);
              if (currentIndex > 0) setActiveStepId(PIPELINE_STEPS[currentIndex - 1].id);
            }}
            disabled={PIPELINE_STEPS.findIndex((s) => s.id === activeStepId) === 0}
            className="px-4 py-2 rounded-full border border-[#e0e0e0] text-[13px] text-[#1d1d1f] hover:bg-[#f5f5f7] disabled:opacity-40 disabled:cursor-not-allowed transition-all"
          >
            ← Previous Stage
          </button>

          <span className="text-[13px] text-[#7a7a7a]">
            Stage {PIPELINE_STEPS.findIndex((s) => s.id === activeStepId) + 1} of {PIPELINE_STEPS.length}
          </span>

          <button
            onClick={() => {
              const currentIndex = PIPELINE_STEPS.findIndex((s) => s.id === activeStepId);
              if (currentIndex < PIPELINE_STEPS.length - 1) setActiveStepId(PIPELINE_STEPS[currentIndex + 1].id);
            }}
            disabled={PIPELINE_STEPS.findIndex((s) => s.id === activeStepId) === PIPELINE_STEPS.length - 1}
            className="px-4 py-2 rounded-full bg-[#0066cc] text-white hover:bg-[#0071e3] text-[13px] disabled:opacity-40 disabled:cursor-not-allowed transition-all"
          >
            Next Stage →
          </button>
        </div>
      </div>

      {/* 4. Complete System Diagram Card */}
      <div className="bg-[#ffffff] border border-[#e0e0e0] rounded-[18px] p-6 sm:p-8 space-y-6 shadow-[0_1px_3px_rgba(0,0,0,0.02)]">
        <div className="space-y-1">
          <h3 className="text-[21px] font-semibold text-[#1d1d1f] tracking-tight">
            System Data Flow & Security Boundaries
          </h3>
          <p className="text-[14px] text-[#7a7a7a]">
            How data moves safely between frontend, NLP services, and PostgreSQL.
          </p>
        </div>

        {/* Visual Pipeline Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-4 rounded-[14px] bg-[#f5f5f7] border border-[#e0e0e0] space-y-2">
            <span className="text-[11px] font-semibold text-[#0066cc] uppercase tracking-wider block">Layer 1</span>
            <h4 className="text-[15px] font-semibold text-[#1d1d1f]">Client Interface</h4>
            <p className="text-[12px] text-[#7a7a7a]">
              Apple-styled conversational UI with instant query submission and state management.
            </p>
          </div>

          <div className="p-4 rounded-[14px] bg-[#f5f5f7] border border-[#e0e0e0] space-y-2">
            <span className="text-[11px] font-semibold text-[#0066cc] uppercase tracking-wider block">Layer 2</span>
            <h4 className="text-[15px] font-semibold text-[#1d1d1f]">NLP & Vector Space</h4>
            <p className="text-[12px] text-[#7a7a7a]">
              Preprocessing, 8-class Intent Classification, and TF-IDF Schema Matching.
            </p>
          </div>

          <div className="p-4 rounded-[14px] bg-[#f5f5f7] border border-[#e0e0e0] space-y-2">
            <span className="text-[11px] font-semibold text-[#0066cc] uppercase tracking-wider block">Layer 3</span>
            <h4 className="text-[15px] font-semibold text-[#1d1d1f]">AST Security Shield</h4>
            <p className="text-[12px] text-[#7a7a7a]">
              sqlparse abstract syntax validation blocking destructive commands and injection.
            </p>
          </div>

          <div className="p-4 rounded-[14px] bg-[#f5f5f7] border border-[#e0e0e0] space-y-2">
            <span className="text-[11px] font-semibold text-[#0066cc] uppercase tracking-wider block">Layer 4</span>
            <h4 className="text-[15px] font-semibold text-[#1d1d1f]">PostgreSQL Cluster</h4>
            <p className="text-[12px] text-[#7a7a7a]">
              PostgreSQL 16 executing read-only queries with 5s timeout across 135,188 rows.
            </p>
          </div>
        </div>

        {/* Try an Example In Chat Button */}
        {onSelectQuery && (
          <div className="pt-2 flex items-center justify-between border-t border-[#f0f0f0]">
            <span className="text-[13px] text-[#7a7a7a]">
              Want to see this pipeline in action?
            </span>
            <button
              onClick={() => onSelectQuery("give me the data of student of all the aiml student")}
              className="inline-flex items-center space-x-1.5 text-[13px] font-medium text-[#0066cc] hover:underline"
            >
              <span>Test AIML Query in Chat</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
