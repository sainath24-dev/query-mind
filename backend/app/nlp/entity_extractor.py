import re
from typing import Dict, Any, List, Optional
from backend.app.nlp.preprocessor import preprocessor

DEPARTMENT_CODES = ["CSE", "AIML", "ISE", "ECE", "EEE", "ME", "CIVIL", "DS", "CS", "IT"]

DEPARTMENT_NAME_MAP = {
    "computer science and engineering": "CSE",
    "computer science": "CSE",
    "artificial intelligence and machine learning": "AIML",
    "artificial intelligence": "AIML",
    "information science and engineering": "ISE",
    "information science": "ISE",
    "electronics and communication engineering": "ECE",
    "electronics and communication": "ECE",
    "electrical and electronics engineering": "EEE",
    "electrical and electronics": "EEE",
    "mechanical engineering": "ME",
    "mechanical": "ME",
    "civil engineering": "CIVIL",
    "civil": "CIVIL",
    "data science": "DS",
    "cyber security": "CS",
    "cybersecurity": "CS",
    "information technology": "IT"
}

KNOWN_SUBJECTS = [
    "Machine Learning", "Data Structures", "Database Management Systems", "Operating Systems",
    "Computer Networks", "Artificial Intelligence", "Deep Learning", "Natural Language Processing",
    "Cloud Computing", "Computer Vision", "Software Engineering", "Web Technology",
    "Compiler Design", "Cyber Security", "Big Data Analytics", "Distributed Systems",
    "Internet of Things", "Mathematics", "Engineering Physics", "Engineering Chemistry",
    "Digital Image Processing", "C Programming", "Discrete Mathematical Structures"
]

CITIES = [
    "Bangalore", "Mysore", "Mangalore", "Hubli", "Belgaum", "Shimoga",
    "Udupi", "Tumkur", "Davangere", "Chennai", "Hyderabad", "Mumbai", "Pune", "Delhi"
]


class EntityExtractor:
    def __init__(self):
        pass

    def extract(self, text: str) -> Dict[str, Any]:
        """
        Extracts structured domain entities from natural language query.
        """
        norm_text = preprocessor.normalize(text)
        original_lower = text.lower()

        entities: Dict[str, Any] = {
            "departments": [],
            "subjects": [],
            "primary_entity": "students", # default primary entity
            "attributes": [],
            "conditions": [],
            "limit": None,
            "order": None,
            "city": None,
            "semester": None,
            "year": None,
            "grade": None,
            "unsupported_attributes": []
        }

        # 1. Detect Primary Entity (students, faculty, departments, subjects, marks, attendance)
        if re.search(r"\b(faculty|professor|professors|teacher|teachers|lecturer|lecturers|staff)\b", original_lower):
            entities["primary_entity"] = "faculty"
        elif re.search(r"\b(department|departments|branch|branches)\b", original_lower) and not re.search(r"\b(students?|faculty)\b", original_lower):
            entities["primary_entity"] = "departments"
        elif re.search(r"\b(subject|subjects|course|courses)\b", original_lower) and not re.search(r"\b(students?|marks)\b", original_lower):
            entities["primary_entity"] = "subjects"
        else:
            entities["primary_entity"] = "students"

        # 2. Extract Departments (by Code or by Name)
        found_depts = set()
        for code in DEPARTMENT_CODES:
            if re.search(rf"\b{code}\b", norm_text, flags=re.IGNORECASE):
                found_depts.add(code)

        for name, code in DEPARTMENT_NAME_MAP.items():
            if name in original_lower:
                found_depts.add(code)

        entities["departments"] = sorted(list(found_depts))

        # 3. Extract Subjects
        for subj in KNOWN_SUBJECTS:
            if subj.lower() in original_lower or subj.lower() in norm_text.lower():
                entities["subjects"].append(subj)

        # 4. Extract Limit / Top N (e.g. "top 10", "top 5", "first 3", "best 5")
        top_match = re.search(r"\b(top|first|highest|best|lowest)\s+(\d+)\b", norm_text, flags=re.IGNORECASE)
        if top_match:
            entities["limit"] = int(top_match.group(2))
            direction = "ASC" if top_match.group(1).lower() in ["lowest", "bottom"] else "DESC"
            entities["order"] = direction

        # 5. Extract Semester and Year
        sem_match = re.search(r"\b(semester|sem)\s*(\d+)\b", original_lower)
        if sem_match:
            entities["semester"] = int(sem_match.group(2))

        year_match = re.search(r"\b(\d+)(?:st|nd|rd|th)?\s*year\b", original_lower)
        if year_match:
            entities["year"] = int(year_match.group(1))

        # 6. Extract City
        for city in CITIES:
            if city.lower() in original_lower:
                entities["city"] = city
                break

        # 7. Extract Numerical Filter Conditions (Attribute, Operator, Value)
        # Check CGPA conditions
        cgpa_match = re.search(r"(?:cgpa|gpa|pointer)\s*(above|below|greater than|more than|less than|>=|<=|>|<|=)\s*(\d+(?:\.\d+)?)", original_lower)
        if not cgpa_match:
            cgpa_match = re.search(r"(above|below|greater than|more than|less than|>=|<=|>|<|=)\s*(\d+(?:\.\d+)?)\s*(?:cgpa|gpa|pointer)", original_lower)

        if cgpa_match:
            op_text, val_text = cgpa_match.group(1), cgpa_match.group(2)
            op = self._parse_operator(op_text)
            entities["conditions"].append({
                "attribute": "cgpa",
                "table": "students",
                "column": "cgpa",
                "operator": op,
                "value": float(val_text)
            })
            entities["attributes"].append("cgpa")

        # Check Attendance conditions (e.g. "attendance below 75%", "attendance above 85")
        att_match = re.search(r"attendance\s*(?:percentage)?\s*(above|below|greater than|more than|less than|>=|<=|>|<|=)\s*(\d+(?:\.\d+)?)\s*%?", original_lower)
        if not att_match:
            att_match = re.search(r"(above|below|greater than|more than|less than|>=|<=|>|<|=)\s*(\d+(?:\.\d+)?)\s*%\s*attendance", original_lower)

        if att_match:
            op_text, val_text = att_match.group(1), att_match.group(2)
            op = self._parse_operator(op_text)
            entities["conditions"].append({
                "attribute": "attendance",
                "table": "attendance",
                "column": "attendance_percentage",
                "operator": op,
                "value": float(val_text),
                "unit": "percentage"
            })
            entities["attributes"].append("attendance")

        # Check Marks conditions (e.g. "scored above 80 in Machine Learning", "marks greater than 75")
        marks_match = re.search(r"(?:scored|marks|score)\s*(above|below|greater than|more than|less than|>=|<=|>|<|=)\s*(\d+(?:\.\d+)?)", original_lower)
        if marks_match:
            op_text, val_text = marks_match.group(1), marks_match.group(2)
            op = self._parse_operator(op_text)
            entities["conditions"].append({
                "attribute": "marks",
                "table": "marks",
                "column": "total_marks",
                "operator": op,
                "value": float(val_text)
            })
            entities["attributes"].append("total_marks")

        # Check Backlogs conditions (e.g. "more than 2 backlogs", "failed more than two subjects")
        backlog_match = re.search(r"(?:more than|greater than|>)\s*(\d+)\s*(?:backlogs?|failed subjects?)", norm_text)
        if not backlog_match:
            backlog_match = re.search(r"failed\s*(?:more than|greater than|>)\s*(\d+)\s*subjects?", norm_text)

        if backlog_match:
            entities["conditions"].append({
                "attribute": "backlogs",
                "table": "students",
                "column": "backlogs",
                "operator": ">",
                "value": int(backlog_match.group(1))
            })
            entities["attributes"].append("backlogs")

        # Check Grade filter (e.g. "grade A+", "grade O", "grade F")
        grade_match = re.search(r"\bgrade\s*(?:of|=|is)?\s*([oO]|[aA]\+|[aA]|[bB]\+|[bB]|[cC]|[pP]|[fF])\b", original_lower)
        if grade_match:
            entities["grade"] = grade_match.group(1).upper()
            entities["conditions"].append({
                "attribute": "grade",
                "table": "marks",
                "column": "grade",
                "operator": "=",
                "value": grade_match.group(1).upper()
            })

        # 8. Check for Unanswerable Attributes (salary, placement, fee, bus, hostel, etc.)
        unsupported_keywords = [
            ("salary", "salary information"),
            ("package", "placement package / CTC information"),
            ("placement", "campus placement records"),
            ("fees", "tuition and fee payment details"),
            ("fee", "tuition fee details"),
            ("hostel", "hostel accommodation details"),
            ("bus", "transportation/bus routes"),
            ("canteen", "cafeteria/canteen data"),
            ("library fine", "library borrowing or fine records")
        ]
        for kw, desc in unsupported_keywords:
            if re.search(rf"\b{kw}\b", original_lower):
                entities["unsupported_attributes"].append(desc)

        return entities

    def _parse_operator(self, op_text: str) -> str:
        op_text = op_text.strip().lower()
        if op_text in ["above", "greater than", "more than", "higher than", ">"]:
            return ">"
        elif op_text in ["below", "less than", "fewer than", "under", "lower than", "<"]:
            return "<"
        elif op_text in [">=", "at least"]:
            return ">="
        elif op_text in ["<=", "at most"]:
            return "<="
        else:
            return "="


entity_extractor = EntityExtractor()
