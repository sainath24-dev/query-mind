from backend.app.nlp.entity_extractor import entity_extractor
from backend.app.nlp.intent_classifier import intent_classifier
from backend.app.nlp.schema_matcher import schema_matcher


def test_top_students():
    q = "Who are the top 10 students by CGPA?"
    ents = entity_extractor.extract(q)
    intent, conf = intent_classifier.classify(q, ents)
    tables, cols = schema_matcher.match(q, ents)

    assert intent == "TOP_N"
    assert ents["limit"] == 10
    assert "students" in tables


def test_aiml_attendance():
    q = "Which AIML students have attendance below 75%?"
    ents = entity_extractor.extract(q)
    intent, conf = intent_classifier.classify(q, ents)
    tables, cols = schema_matcher.match(q, ents)

    assert "AIML" in ents["departments"]
    assert any(c["attribute"] == "attendance" and c["operator"] == "<" and c["value"] == 75.0 for c in ents["conditions"])
    assert "attendance" in tables
    assert "departments" in tables


def test_machine_learning_marks():
    q = "Show all AIML students who scored above 80 in Machine Learning."
    ents = entity_extractor.extract(q)
    tables, cols = schema_matcher.match(q, ents)

    assert "AIML" in ents["departments"]
    assert "Machine Learning" in ents["subjects"]
    assert "marks" in tables
    assert "subjects" in tables


def test_unsupported_query():
    q = "What is the average salary of AIML students?"
    ents = entity_extractor.extract(q)
    assert len(ents["unsupported_attributes"]) > 0
    assert "salary information" in ents["unsupported_attributes"]


if __name__ == "__main__":
    test_top_students()
    test_aiml_attendance()
    test_machine_learning_marks()
    test_unsupported_query()
    print("All NLP component tests passed!")
