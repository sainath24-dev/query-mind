import re
import math
from collections import Counter
from typing import List, Dict, Any, Tuple
from backend.app.services.schema_service import TABLE_DESCRIPTIONS, COLUMN_DESCRIPTIONS

# Domain Semantic Concepts mapping natural language query concepts to target relational tables and columns
SEMANTIC_CONCEPTS = [
    # Attendance concepts
    ("poor attendance low attendance attendance shortage bunked detained warning condoned classes attended", "attendance", "attendance_percentage"),
    ("high attendance regular students eligible for exam class attendance highest attendance", "attendance", "attendance_percentage"),
    ("classes conducted total lectures sessions held", "attendance", "classes_conducted"),

    # Performance / Marks concepts
    ("high grades toppers high cgpa best students rankers academic performance honors highest cgpa top cgpa", "students", "cgpa"),
    ("low cgpa poor marks struggling students academic probation", "students", "cgpa"),
    ("failed subjects backlogs arrears flunked backlog count uncleared courses failed more than", "students", "backlogs"),
    ("internal marks continuous evaluation cia test marks", "marks", "internal_marks"),
    ("external marks semester end exam sem exam written score", "marks", "external_marks"),
    ("total marks overall score subject marks exam result average marks lowest marks", "marks", "total_marks"),
    ("letter grade grade point O A+ A B+ B C P F grade distribution", "marks", "grade"),
    ("passed failed pass percentage pass status result status failed subject", "marks", "result_status"),

    # Department concepts
    ("department branch engineering stream hod head building block department code", "departments", "department_code"),

    # Subject / Course concepts
    ("subjects courses credits core elective lab syllabus subject code machine learning data structures", "subjects", "subject_name"),

    # Faculty concepts
    ("faculty teachers professors lecturers designation experience teaching staff instructor teaches", "faculty", "designation"),

    # Enrollment concepts
    ("enrolled enrollments registered course registration active dropped enrollment count", "enrollments", "status"),

    # Student demographic concepts
    ("student usn roll number registration number admission year current semester section city bangalore mysore", "students", "usn")
]


class SemanticSchemaMatcher:
    """
    Pure Python TF-IDF Vector Space Model for Natural Language to Schema Matching.
    Calculates Cosine Similarity between user query terms and relational concept vectors.
    """
    def __init__(self):
        self.concepts = SEMANTIC_CONCEPTS
        self.docs = [self._tokenize(c[0]) for c in self.concepts]
        self.N = len(self.docs)
        
        # Calculate Document Frequencies (DF)
        self.dfs = Counter()
        for doc in self.docs:
            for term in set(doc):
                self.dfs[term] += 1
                
        # Calculate Inverse Document Frequencies (IDF) with smoothing
        self.idfs = {
            term: math.log((self.N + 1.0) / (df + 1.0)) + 1.0
            for term, df in self.dfs.items()
        }
        
        # Precompute L2-normalized TF-IDF vectors for concept profiles
        self.concept_vectors = [self._vectorize(doc) for doc in self.docs]

    def _tokenize(self, text: str) -> List[str]:
        return [w for w in re.findall(r'[a-z0-9_]+', text.lower()) if len(w) > 1]

    def _vectorize(self, tokens: List[str]) -> Dict[str, float]:
        tfs = Counter(tokens)
        vec = {term: count * self.idfs.get(term, 1.0) for term, count in tfs.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        return {term: v / norm for term, v in vec.items()}

    def _cosine_similarity(self, vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
        dot = 0.0
        # Iterate over smaller dict
        if len(vec_a) > len(vec_b):
            vec_a, vec_b = vec_b, vec_a
        for term, val in vec_a.items():
            if term in vec_b:
                dot += val * vec_b[term]
        return dot

    def match(self, question: str, entities: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
        Returns:
            relevant_tables: list of table names needed for query
            relevant_columns: list of "table.column" strings identified as relevant
        """
        lower = question.lower()
        matched_tables = set()
        matched_columns = set()

        # 1. Base table on primary entity
        primary = entities.get("primary_entity", "students")
        matched_tables.add(primary)

        # 2. Add tables implied by extracted entities
        if entities.get("departments"):
            matched_tables.add("departments")
            matched_columns.add("departments.department_code")
            matched_columns.add("departments.department_name")

        if entities.get("subjects"):
            matched_tables.add("subjects")
            matched_columns.add("subjects.subject_name")
            matched_tables.add("marks") # Subject questions usually involve marks

        # Add tables from condition entities
        for cond in entities.get("conditions", []):
            tbl = cond.get("table")
            col = cond.get("column")
            if tbl:
                matched_tables.add(tbl)
            if tbl and col:
                matched_columns.add(f"{tbl}.{col}")

        # 3. Vector Space Cosine Similarity Schema Matching
        q_tokens = self._tokenize(lower)
        q_vec = self._vectorize(q_tokens)

        scored_concepts = []
        for idx, c_vec in enumerate(self.concept_vectors):
            score = self._cosine_similarity(q_vec, c_vec)
            scored_concepts.append((score, idx))

        scored_concepts.sort(key=lambda x: x[0], reverse=True)

        # Top matching semantic concepts with relevance threshold
        for score, idx in scored_concepts[:3]:
            if score > 0.08:
                _, tbl, col = self.concepts[idx]
                matched_tables.add(tbl)
                matched_columns.add(f"{tbl}.{col}")

        # 4. Relational Bridge Rules (ensure join integrity)
        if "subjects" in matched_tables and "students" in matched_tables and "marks" not in matched_tables:
            matched_tables.add("marks")

        if "faculty" in matched_tables and "students" in matched_tables:
            matched_tables.add("enrollments")

        return sorted(list(matched_tables)), sorted(list(matched_columns))


schema_matcher = SemanticSchemaMatcher()

