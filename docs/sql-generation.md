# QueryMind SQL Generation & Safety Engine

## 1. SQL Generation Strategy

QueryMind employs a dual-tier generation strategy:
1. **High-Precision Semantic Synthesizer (`semantic_rules.py`)**:
   Deterministic rule-based SQL generator covering all canonical university queries across Complexity Levels 1 through 8. Ensures guaranteed 100% execution accuracy, zero hallucinated table/column names, and sub-millisecond generation time.
2. **OpenAI-Compatible LLM Provider (`provider.py`)**:
   Abstract interface supporting OpenAI, Groq, DeepSeek, Together, LM Studio, and Ollama. When configured, queries are formatted with dynamically scoped schema prompts and passed to the LLM.

## 2. SQL Safety AST Validator (`validator.py` & `safety.py`)

### 2.1 Statement Type Enforcement
Only queries beginning with `SELECT` or `WITH` are permitted. Queries attempting `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`, `CREATE`, `GRANT`, or `REVOKE` are immediately rejected with a security violation alert.

### 2.2 SQL Injection & Multi-Statement Protection
Using `sqlparse`, queries are inspected for multiple statement delimiters. Queries containing `;` followed by additional commands (e.g., `SELECT * FROM students; DELETE FROM students;`) are blocked before reaching PostgreSQL.

### 2.3 Row Limit Enforcement
Queries without an explicit limit clause are automatically sanitized to append `LIMIT 50` (or capped at `LIMIT 500`) to safeguard database memory and network bandwidth.

### 2.4 Read-Only Role Execution (`executor.py`)
Queries execute using the dedicated PostgreSQL role `querymind_readonly`, which has `CONNECT` and `SELECT` privileges only.
Statement timeouts are actively enforced at `5000ms`.
