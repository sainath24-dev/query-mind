# QueryMind Natural Language Processing Pipeline

## 1. Pipeline Overview

QueryMind does not merely wrap an external API; it implements an explicit, multi-stage NLP pipeline designed for academic rigor, deterministic predictability, and transparent evaluation.

```
USER QUESTION
     ↓
[1] Preprocessor & Normalizer (tokenization, case-standardization)
     ↓
[2] Named Entity & Attribute Extractor (departments, subjects, operators)
     ↓
[3] Intent Classifier (COUNT, AVERAGE, TOP_N, COMPARISON, GROUP_BY, etc.)
     ↓
[4] Semantic Schema Matcher (TF-IDF Vector Space Model & Cosine Similarity)
     ↓
[5] Relational Bridge Builder (Foreign key join path resolution)
     ↓
[6] SQL Synthesizer & Generator (Deterministic semantic rules + LLM provider)
     ↓
[7] SQL AST Safety Validator (sqlparse token verification)
     ↓
[8] PostgreSQL Read-Only Execution (User: querymind_readonly)
     ↓
[9] Grounded Natural Language Explainer & Chart Heuristic Engine
```

## 2. Detailed NLP Components

### 2.1 Text Preprocessing & Normalization (`preprocessor.py`)
- **Cleaning**: Trims conversational filler phrases ("show me", "give me", "can you list", "please find").
- **Canonical Normalization**: Standardizes department codes (e.g., `ai & ml` -> `AIML`, `cs` -> `CSE`).
- **Tokenization**: Regex-based token extraction preserving numeric metrics, operators, and USN strings.

### 2.2 Named Entity Recognition & Scope Detection (`entity_extractor.py`)
- **Department Recognition**: Matches against 10 target departments and aliases.
- **Subject Fuzzy Matching**: Matches across 438 university course titles.
- **Comparison Operators**: Translates comparative phrases ("more than", "above", "higher than" -> `>`, "less than", "below", "under" -> `<`).
- **Out-of-Scope Detection**: Identifies attributes not present in the relational schema (salary, fees, hostel, placement packages) to trigger educational rejection.

### 2.3 Intent Classification (`intent_classifier.py`)
Categorizes user queries into canonical categories:
- `COUNT`: "How many students are enrolled in AIML?"
- `AVERAGE`: "What is the average CGPA of CSE students?"
- `TOP_N`: "Who are the top 10 students by CGPA?"
- `COMPARISON`: "Compare average marks between CSE and AIML."
- `GROUP_BY`: "How many students are enrolled in each department?"
- `MAXIMUM`: "Which department has the highest average CGPA?"
- `MINIMUM`: "Which subject has the lowest average marks?"
- `FILTER`: "Show all AIML students who scored above 80 in Machine Learning."
- `DETAIL_LOOKUP`: "Show marks of student with USN 1MS22AIML042."

### 2.4 Semantic Schema Matching (`schema_matcher.py`)
- **TF-IDF Vector Space Model**: Vectorizes user queries against pre-indexed domain concept profiles.
- **Cosine Similarity**: Calculates dot product between normalized TF-IDF query vectors and relational concepts.
- **Relational Bridge Rules**: Automatically links bridge tables (e.g., `enrollments` or `marks`) when cross-table joins between `students` and `subjects` are detected.

### 2.5 Conversational Follow-Up Resolution (`context_service.py`)
- Maintains per-session query context storing `previous_question`, `previous_sql`, `entities`, and `relevant_tables`.
- When a user asks a follow-up (e.g., "Only show the top 5" or "Only from 3rd year"), the context service re-interprets the query against previous constraints rather than blindly concatenating strings.
