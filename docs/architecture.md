# QueryMind System Architecture Specification

## 1. Architectural Overview

QueryMind is an end-to-end natural language database query system. It bridges the gap between natural language questions formulated by human users and structured relational data residing in a PostgreSQL database cluster.

```
                    ┌─────────────────────────┐
                    │      User Question      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    Next.js Frontend     │
                    │  (Port 3000 / Recharts) │
                    └────────────┬────────────┘
                                 │ HTTP POST /api/query
                                 ▼
                    ┌─────────────────────────┐
                    │     FastAPI Backend     │
                    │       (Port 8008)       │
                    └────────────┬────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
          ▼                      ▼                      ▼
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│  NLP Preprocessor│   │ Entity Extractor │   │ Intent Classifier│
│  & Tokenization  │   │  & Scope Checker │   │ (8 Canonical Cat)│
└─────────┬────────┘   └─────────┬────────┘   └─────────┬────────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   TF-IDF Vector Space   │
                    │     Schema Matcher      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    SQL Synthesizer      │
                    │ (Semantic Rules & LLM)  │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    SQL Safety Engine    │
                    │  (AST & Keyword Reject) │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ PostgreSQL Database     │
                    │ (querymind_readonly)    │
                    │ 5,200 Students, 135k Rec│
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Result Explanation    │
                    │ & Dynamic Visualization │
                    └─────────────────────────┘
```

## 2. Component Design

### 2.1 Frontend Architecture (Next.js 14 + TypeScript + Tailwind CSS)
- **Dashboard View**: Real-time university academic KPIs, department distribution charts, CGPA distribution charts, and popular query intents introspected live from PostgreSQL.
- **Query Assistant Interface**: Search input with autocomplete suggestion chips, conversational session breadcrumbs, multi-view data grid, Recharts visualizer (Bar, Line, Pie), collapsible raw SQL viewer, and grounded natural language explanations.
- **Schema Explorer**: Interactive relational table inspector showing row counts, column types, primary key flags, foreign key target relationships, and distinct sample values.
- **Query History**: Chronological audit trail logging natural language prompts, generated SQL, execution latency, row counts, and one-click query replay.
- **NLP Architecture Visualizer**: Interactive 8-stage pipeline demonstration explaining NLP paradigms for viva and presentation.

### 2.2 Backend Architecture (FastAPI + Python 3.13)
- **API Router Layer**: RESTful endpoints with Pydantic request/response validation.
- **NLP Processing Layer**: Pure Python text cleaner, domain entity extractor, canonical intent classifier, and TF-IDF cosine similarity schema matcher.
- **SQL Generation Layer**: Deterministic semantic rule engine with abstract OpenAI-compatible LLM interface for dynamic query synthesis.
- **SQL Safety & Validation Layer**: sqlparse AST syntax analyzer enforcing read-only SELECT/WITH queries and rejecting dangerous operations (DROP, DELETE, TRUNCATE, INSERT, ALTER).
- **Execution Layer**: Threaded PostgreSQL connection pool with dedicated read-only role `querymind_readonly`, 5-second statement timeout, and row limits.
- **Explanation & Visualization Engine**: Data-to-text grounded natural language synthesizer and heuristic chart recommender.

## 3. Security Architecture
1. **Database Role Segregation**: User queries are executed exclusively using `querymind_readonly`. Even if malicious SQL bypassed AST checks, PostgreSQL itself rejects writes at the kernel engine level.
2. **AST Static Analysis**: Every query is parsed via `sqlparse` to confirm only `SELECT` or `WITH` statement types exist and that multiple statements separated by semicolons are blocked.
3. **Keyword Blacklist**: Prohibits `DROP`, `DELETE`, `UPDATE`, `INSERT`, `TRUNCATE`, `ALTER`, `GRANT`, `REVOKE`, `COPY`, and `VACUUM`.
4. **Statement Timeout**: Guaranteed 5000ms query timeout via `SET statement_timeout = '5000ms'` prevents denial-of-service or long-running runaway joins.
5. **Row Ceiling**: Enforces defensive `LIMIT 50` or `LIMIT 500` to prevent memory exhaustion.
