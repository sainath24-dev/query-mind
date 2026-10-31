import re
from typing import Dict, Any, Optional
import json
from backend.app.schemas.schemas import QueryResponse, VisualizationConfig
from backend.app.nlp.preprocessor import preprocessor
from backend.app.nlp.entity_extractor import entity_extractor
from backend.app.nlp.intent_classifier import intent_classifier
from backend.app.nlp.schema_matcher import schema_matcher
from backend.app.sql.generator import sql_generator
from backend.app.sql.validator import sql_validator
from backend.app.sql.executor import sql_executor
from backend.app.services.explanation_service import explanation_service
from backend.app.services.visualization_service import visualization_service
from backend.app.services.context_service import context_service
from backend.app.database.connection import execute_query_async


class QueryService:
    def __init__(self):
        pass

    async def process_query(self, question: str, session_id: str = "default_session") -> QueryResponse:
        """
        Executes the complete QueryMind Natural Language to SQL Pipeline.
        """
        clean_q = preprocessor.clean_text(question)

        # Check for Destructive / Malicious Operations in Natural Language
        lower_q = clean_q.lower()
        if re.search(r"\b(delete|drop|truncate|alter table|remove all students|clear database|update students|insert into)\b", lower_q):
            explanation = (
                "Security Policy Violation: Destructive database statements (such as DELETE, DROP, TRUNCATE, ALTER, INSERT, UPDATE) "
                "are prohibited. QueryMind operates exclusively in read-only analysis mode."
            )
            return QueryResponse(
                question=question,
                intent="DESTRUCTIVE_PROHIBITED",
                entities={},
                sql="-- Security Policy Violation: Destructive execution prohibited.",
                columns=[],
                rows=[],
                row_count=0,
                execution_time_ms=0.0,
                explanation=explanation,
                visualization=VisualizationConfig(can_visualize=False, recommended_chart="table"),
                tables_used=[],
                session_id=session_id,
                is_answerable=False,
                error_message="Destructive statement prohibited.",
                status="ERROR"
            )

        # 1. Fetch previous conversational context and resolve follow-ups
        prev_context = context_service.get_context(session_id)
        raw_entities = entity_extractor.extract(clean_q)
        effective_question, entities = context_service.resolve_followup(clean_q, raw_entities, prev_context)

        # 2. Check for Out-of-Scope / Unanswerable questions (e.g. salary, placement, fees)
        if entities.get("unsupported_attributes"):
            missing_attrs = ", ".join(entities["unsupported_attributes"])
            explanation = (
                f"I cannot answer this question because the university relational database "
                f"does not contain {missing_attrs}. The database tracks students, departments, "
                f"faculty, courses, marks, and attendance."
            )
            return QueryResponse(
                question=question,
                intent="UNSUPPORTED",
                entities=entities,
                sql="-- Query cannot be generated: requested attributes are not present in schema.",
                columns=[],
                rows=[],
                row_count=0,
                execution_time_ms=0.0,
                explanation=explanation,
                visualization=VisualizationConfig(can_visualize=False, recommended_chart="table"),
                tables_used=[],
                session_id=session_id,
                is_answerable=False,
                error_message=f"Missing schema attributes: {missing_attrs}",
                status="UNANSWERABLE"
            )

        # 3. Classify Intent
        intent, confidence = intent_classifier.classify(effective_question, entities)

        # 4. Semantic Schema Matching
        relevant_tables, relevant_cols = schema_matcher.match(effective_question, entities)

        # 5. SQL Generation
        generated_sql = await sql_generator.generate_sql(
            question=effective_question,
            intent=intent,
            entities=entities,
            relevant_tables=relevant_tables,
            context=prev_context
        )

        # 6. SQL Validation and Safety Checks
        is_valid, sanitized_sql, val_error = sql_validator.validate_and_sanitize(generated_sql, relevant_tables)
        if not is_valid:
            return QueryResponse(
                question=question,
                intent=intent,
                entities=entities,
                sql=generated_sql,
                columns=[],
                rows=[],
                row_count=0,
                execution_time_ms=0.0,
                explanation=f"Query rejected by security validator: {val_error}",
                visualization=VisualizationConfig(can_visualize=False, recommended_chart="table"),
                tables_used=relevant_tables,
                session_id=session_id,
                is_answerable=False,
                error_message=val_error,
                status="ERROR"
            )

        # 7. Execute SQL on Read-Only Connection
        exec_result = await sql_executor.execute_query(sanitized_sql)

        if not exec_result["success"]:
            err_msg = exec_result.get("error", "Database execution error.")
            return QueryResponse(
                question=question,
                intent=intent,
                entities=entities,
                sql=sanitized_sql,
                columns=[],
                rows=[],
                row_count=0,
                execution_time_ms=exec_result["execution_time_ms"],
                explanation=f"Execution Error: {err_msg}",
                visualization=VisualizationConfig(can_visualize=False, recommended_chart="table"),
                tables_used=relevant_tables,
                session_id=session_id,
                is_answerable=True,
                error_message=err_msg,
                status="ERROR"
            )

        columns = exec_result["columns"]
        rows = exec_result["rows"]
        row_count = exec_result["row_count"]
        exec_time = exec_result["execution_time_ms"]

        # 8. Determine Visualization
        vis_config = visualization_service.determine_visualization(columns, rows, intent)

        # 9. Generate Natural Language Explanation
        explanation = await explanation_service.explain_result(
            question=effective_question,
            intent=intent,
            columns=columns,
            rows=rows,
            execution_time_ms=exec_time
        )

        # 10. Update Conversational Context for follow-up turns
        context_service.update_context(
            session_id=session_id,
            question=effective_question,
            sql=sanitized_sql,
            intent=intent,
            entities=entities,
            tables=relevant_tables,
            result_metadata={"row_count": row_count, "columns": columns}
        )

        # 11. Log Audit Record to query_history table
        query_id = None
        try:
            insert_sql = """
                INSERT INTO query_history (
                    session_id, natural_language_question, intent,
                    detected_filters, generated_sql, execution_time_ms,
                    row_count, explanation, status
                ) VALUES (
                    %(session_id)s, %(question)s, %(intent)s,
                    %(filters)s, %(sql)s, %(exec_time)s,
                    %(row_count)s, %(explanation)s, 'SUCCESS'
                ) RETURNING query_id;
            """
            _, h_res = await execute_query_async(
                insert_sql,
                params={
                    "session_id": session_id,
                    "question": question,
                    "intent": intent,
                    "filters": json.dumps({}),
                    "sql": sanitized_sql,
                    "exec_time": exec_time,
                    "row_count": row_count,
                    "explanation": explanation
                },
                readonly=False
            )
            if h_res:
                query_id = h_res[0].get("query_id")
        except Exception:
            pass

        return QueryResponse(
            query_id=query_id,
            question=question,
            intent=intent,
            entities=entities,
            sql=sanitized_sql,
            columns=columns,
            rows=rows,
            row_count=row_count,
            execution_time_ms=exec_time,
            explanation=explanation,
            visualization=vis_config,
            tables_used=relevant_tables,
            session_id=session_id,
            is_answerable=True,
            error_message=None,
            status="SUCCESS"
        )


query_service = QueryService()
