"use client";

import React, { useState } from "react";
import {
  Brain,
  Database,
  ShieldCheck,
  Code2,
  Workflow,
  Search,
  Filter,
  CheckCircle,
  Cpu,
  Layers,
  ArrowRight,
  Terminal,
  Activity
} from "lucide-react";

interface PipelineStep {
  id: string;
  number: string;
  title: string;
  icon: React.ReactNode;
  subtitle: string;
  nlpConcept: string;
  exampleInput: string;
  exampleOutput: string;
  technicalDetails: string[];
}

const PIPELINE_STEPS: PipelineStep[] = [
  {
    id: "step-1",
    number: "01",
    title: "NLP Preprocessing & Cleaning",
    icon: <Search className="w-5 h-5 text-blue-400" />,
    subtitle: "Tokenization, case normalization, and punctuation cleanup",
    nlpConcept: "Text Normalization & Tokenization",
    exampleInput: `"show me students from aiml who scored more than 80 in machine learning"`,
    exampleOutput: `"Show students from AIML who scored more than 80 in Machine Learning."`,
    technicalDetails: [
      "Standardizes capitalization for domain entities (AIML, CSE, CGPA).",
      "Strips trailing conversational noise and punctuation.",
      "Preserves numerical criteria (80, 75%) and mathematical comparison operators."
    ]
  },
  {
    id: "step-2",
    number: "02",
    title: "Named Entity & Attribute Extraction",
    icon: <Filter className="w-5 h-5 text-emerald-400" />,
    subtitle: "Domain recognition of departments, subjects, grades, and metrics",
    nlpConcept: "Information Extraction & Named Entity Recognition (NER)",
    exampleInput: `"Which AIML students have attendance below 75%?"`,
    exampleOutput: `{"departments": ["AIML"], "attribute": "attendance_percentage", "operator": "<", "value": 75.0}`,
    technicalDetails: [
      "Matches 10 academic department codes (CSE, AIML, ISE, ECE, EEE, ME, CIVIL, DS, CS, IT).",
      "Fuzzy matches university course titles across 438 subjects.",
      "Detects comparative operators (above, below, greater than, at least, top N).",
      "Flags out-of-scope attributes (salary, placement, fees) for graceful rejection."
    ]
  },
  {
    id: "step-3",
    number: "03",
    title: "Intent Classification",
    icon: <Brain className="w-5 h-5 text-purple-400" />,
    subtitle: "Determining structural query objective (COUNT, TOP_N, COMPARISON, etc.)",
    nlpConcept: "Rule-Based + Semantic Intent Classification",
    exampleInput: `"Compare average CGPA between AIML and CSE."`,
    exampleOutput: `Intent: COMPARISON (Confidence: 0.95)`,
    technicalDetails: [
      "Categorizes query into canonical intents: COUNT, AVERAGE, TOP_N, COMPARISON, GROUP_BY, FILTER, DETAIL_LOOKUP.",
      "Identifies whether query requires aggregation (AVG, COUNT) or ordering (ORDER BY DESC LIMIT N).",
      "Recognizes cross-department comparative inquiries."
    ]
  },
  {
    id: "step-4",
    number: "04",
    title: "Semantic Schema Matching",
    icon: <Layers className="w-5 h-5 text-amber-400" />,
    subtitle: "Vector space cosine similarity matching natural terms to database tables",
    nlpConcept: "TF-IDF Vector Space Model & Cosine Similarity",
    exampleInput: `"students with poor attendance"`,
    exampleOutput: `Matched Tables: ["students", "attendance"], Relevant Column: "attendance.attendance_percentage"`,
    technicalDetails: [
      "Builds TF-IDF vector space over relational domain concept profiles.",
      "Computes Cosine Similarity between user query terms and table/column semantics.",
      "Eliminates hallucinated database columns by grounding in verified schema definitions.",
      "Applies relational bridge rules to ensure foreign key join path integrity."
    ]
  },
  {
    id: "step-5",
    number: "05",
    title: "SQL Synthesis & Generation",
    icon: <Code2 className="w-5 h-5 text-cyan-400" />,
    subtitle: "Translating structured intent and entities into ANSI PostgreSQL SQL",
    nlpConcept: "Natural Language to Code Generation (NL2SQL)",
    exampleInput: `Intent: TOP_N, Dept: AIML, Limit: 5, Metric: CGPA`,
    exampleOutput: `SELECT s.usn, s.first_name, s.last_name, d.department_code, s.cgpa FROM students s JOIN departments d ON s.department_id = d.department_id WHERE d.department_code = 'AIML' ORDER BY s.cgpa DESC LIMIT 5;`,
    technicalDetails: [
      "Employs high-precision semantic SQL synthesizer with dynamic LLM provider interface.",
      "Enforces explicit ANSI JOIN clauses linking foreign keys.",
      "Applies table aliasing (s, d, m, sub) for disambiguation.",
      "Automatically applies defensive LIMIT constraints to avoid unbounded queries."
    ]
  },
  {
    id: "step-6",
    number: "06",
    title: "AST Validation & Security Sandbox",
    icon: <ShieldCheck className="w-5 h-5 text-rose-400" />,
    subtitle: "Syntactic parsing and destructive statement rejection",
    nlpConcept: "SQL AST Parsing & Security Policy Verification",
    exampleInput: `"Delete all students." or "DROP TABLE students;"`,
    exampleOutput: `REJECTED: Security Violation: Destructive statement or function 'DELETE' is prohibited.`,
    technicalDetails: [
      "Uses sqlparse AST parser to enforce strictly SELECT or WITH query statements.",
      "Blocks prohibited keywords (DROP, DELETE, UPDATE, INSERT, ALTER, TRUNCATE, GRANT, REVOKE).",
      "Rejects multiple statements separated by semicolons to prevent SQL injection.",
      "Enforces 5.0s query timeout."
    ]
  },
  {
    id: "step-7",
    number: "07",
    title: "PostgreSQL Execution & Result Processing",
    icon: <Database className="w-5 h-5 text-emerald-400" />,
    subtitle: "Executing query safely against university cluster using read-only user",
    nlpConcept: "Relational Execution & Read-Only Role Isolation",
    exampleInput: `Validated SQL Statement`,
    exampleOutput: `5 rows returned in 8.03ms with column metadata`,
    technicalDetails: [
      "Executed using dedicated restricted PostgreSQL role: querymind_readonly.",
      "Runs with statement_timeout = 5000ms to safeguard cluster resources.",
      "Formats rows and decimal fields into JSON-serializable structures."
    ]
  },
  {
    id: "step-8",
    number: "08",
    title: "Natural Language Explanation & Visualization",
    icon: <Brain className="w-5 h-5 text-blue-400" />,
    subtitle: "Grounded natural language answer generation and dynamic charting",
    nlpConcept: "Data-to-Text Natural Language Generation (NLG)",
    exampleInput: `Rows: Top 5 AIML students with Harish Kulkarni CGPA 9.67`,
    exampleOutput: `"Retrieved top 5 records. The highest-ranked student is Harish Kulkarni with a CGPA of 9.67."`,
    technicalDetails: [
      "Grounded explanation synthesizes insights strictly from actual PostgreSQL return data.",
      "Never hallucinates figures or conclusions absent from query results.",
      "Auto-detects visualization heuristics: Bar chart for rankings/counts, Line chart for trends, Pie for grade distributions."
    ]
  }
];

export const ArchitectureView: React.FC = () => {
  const [selectedStepId, setSelectedStepId] = useState<string>("step-1");
  const currentStep = PIPELINE_STEPS.find((s) => s.id === selectedStepId) || PIPELINE_STEPS[0];

  return (
    <div className="space-y-6">
      {/* 1. Architecture Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-blue-900/40 border border-blue-700/50 text-blue-300">
              System Specification
            </span>
            <h2 className="text-xl font-bold text-white tracking-tight">QueryMind End-to-End NLP Architecture</h2>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Complete pipeline converting natural language queries into safe, executable PostgreSQL queries with real data execution.
          </p>
        </div>
        <div className="flex items-center space-x-2 text-xs text-slate-400 bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">
          <Workflow className="w-4 h-4 text-blue-400" />
          <span>8 Modular Processing Stages</span>
        </div>
      </div>

      {/* 2. Interactive Step Pipeline Selector */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2">
        {PIPELINE_STEPS.map((step) => {
          const isSelected = step.id === selectedStepId;
          return (
            <button
              key={step.id}
              onClick={() => setSelectedStepId(step.id)}
              className={`p-3 rounded-lg border text-left transition-all ${
                isSelected
                  ? "bg-blue-600/10 border-blue-500/50 text-blue-300 shadow-md"
                  : "bg-slate-900 hover:bg-slate-800 border-slate-800 text-slate-400 hover:text-slate-200"
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className="font-mono text-[11px] font-bold text-slate-500">{step.number}</span>
                {step.icon}
              </div>
              <p className="font-semibold text-xs truncate text-white">{step.title.split(" ")[0]}</p>
              <p className="text-[10px] text-slate-400 truncate">{step.nlpConcept.split(" ")[0]}</p>
            </button>
          );
        })}
      </div>

      {/* 3. Detailed Step Explorer Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
        <div className="flex items-start justify-between border-b border-slate-800 pb-4">
          <div className="flex items-start space-x-3">
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
              {currentStep.icon}
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-mono text-xs px-2 py-0.5 rounded bg-blue-950 text-blue-400 font-bold">
                  STAGE {currentStep.number}
                </span>
                <h3 className="text-lg font-bold text-white">{currentStep.title}</h3>
              </div>
              <p className="text-sm text-slate-300 mt-1">{currentStep.subtitle}</p>
              <div className="mt-2 inline-flex items-center space-x-1.5 text-xs text-purple-400 font-mono bg-purple-950/40 px-2 py-0.5 rounded border border-purple-800/40">
                <Cpu className="w-3.5 h-3.5" />
                <span>NLP Paradigm: {currentStep.nlpConcept}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Example Input / Output Demonstration */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 rounded-lg bg-slate-950 border border-slate-800">
            <span className="text-xs uppercase font-bold text-slate-400 tracking-wider">Example Stage Input</span>
            <div className="mt-2 p-3 rounded bg-slate-900 border border-slate-800/80 font-mono text-xs text-slate-300 overflow-x-auto whitespace-pre-wrap">
              {currentStep.exampleInput}
            </div>
          </div>

          <div className="p-4 rounded-lg bg-slate-950 border border-slate-800">
            <span className="text-xs uppercase font-bold text-slate-400 tracking-wider">Example Stage Output</span>
            <div className="mt-2 p-3 rounded bg-slate-900 border border-slate-800/80 font-mono text-xs text-blue-300 overflow-x-auto whitespace-pre-wrap">
              {currentStep.exampleOutput}
            </div>
          </div>
        </div>

        {/* Technical Implementation Details */}
        <div>
          <h4 className="text-xs uppercase font-bold text-slate-400 tracking-wider mb-2">Technical Implementation Notes</h4>
          <ul className="space-y-1.5 text-xs text-slate-300">
            {currentStep.technicalDetails.map((detail, idx) => (
              <li key={idx} className="flex items-start space-x-2">
                <CheckCircle className="w-3.5 h-3.5 text-emerald-400 mt-0.5 shrink-0" />
                <span>{detail}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* 4. Complete Architecture Flow Diagram Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
        <h3 className="text-sm font-semibold text-white mb-2">Pipeline Architecture Flowchart</h3>
        <p className="text-xs text-slate-400 mb-4">Visual representation of data and query transformation</p>
        <div className="p-5 rounded-lg bg-slate-950 border border-slate-800 font-mono text-xs text-slate-300 overflow-x-auto whitespace-pre leading-relaxed">
{`  USER QUESTION
        ↓
  [01] Text Preprocessing & Normalization
        ↓
  [02] Entity & Constraint Extraction (Departments, Subjects, Metrics)
        ↓
  [03] Intent Classification (TOP_N, COUNT, AVERAGE, COMPARISON)
        ↓
  [04] TF-IDF Cosine Similarity Schema Matching (Match tables & columns)
        ↓
  [05] SQL Synthesis & Generation (PostgreSQL ANSI JOIN statements)
        ↓
  [06] SQL Safety AST Checker (Reject DROP/DELETE/ALTER; Enforce SELECT/WITH)
        ↓
  [07] Query Execution on PostgreSQL (User: querymind_readonly, Timeout: 5s)
        ↓
  [08] Grounded Natural Language Explanation & Dynamic Chart Visualization`}
        </div>
      </div>
    </div>
  );
};
