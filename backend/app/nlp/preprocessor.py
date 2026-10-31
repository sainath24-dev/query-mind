import re
from typing import Dict, List, Any

# Map colloquial abbreviations to standard domain terms
ACADEMIC_SYNONYMS = {
    r"\baiml\b": "AIML",
    r"\bcse\b": "CSE",
    r"\bise\b": "ISE",
    r"\bece\b": "ECE",
    r"\beee\b": "EEE",
    r"\bmech\b": "ME",
    r"\bmechanical\b": "ME",
    r"\bcivil\b": "CIVIL",
    r"\bds\b": "DS",
    r"\bdata science\b": "Data Science",
    r"\bcyber security\b": "Cyber Security",
    r"\bcybersecurity\b": "Cyber Security",
    r"\bit\b": "IT",
    r"\binformation technology\b": "Information Technology",
    r"\bml\b": "Machine Learning",
    r"\bdbms\b": "Database Management Systems",
    r"\bos\b": "Operating Systems",
    r"\bcn\b": "Computer Networks",
    r"\bdsa\b": "Data Structures",
    r"\bdata structures\b": "Data Structures",
    r"\bai\b": "Artificial Intelligence",
    r"\bdl\b": "Deep Learning",
    r"\bnlp\b": "Natural Language Processing",
    r"\biot\b": "Internet of Things",
    r"\bcv\b": "Computer Vision",
    r"\bpointer\b": "cgpa",
    r"\bgpa\b": "cgpa",
    r"\bscore\b": "marks",
    r"\bscores\b": "marks",
    r"\bflunked\b": "failed",
    r"\bprof\b": "faculty",
    r"\bprofessor\b": "faculty",
    r"\bteacher\b": "faculty",
    r"\blecturer\b": "faculty"
}

NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "1st": 1, "2nd": 2, "3rd": 3, "4th": 4, "5th": 5, "6th": 6, "7th": 7, "8th": 8,
    "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8
}


class TextPreprocessor:
    def __init__(self):
        pass

    def clean_text(self, text: str) -> str:
        """Strips special characters, reduces whitespace, preserves meaningful tokens."""
        text = text.strip()
        # Remove trailing question marks or punctuation
        text = re.sub(r"[?!.,;]+$", "", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def normalize(self, text: str) -> str:
        """
        Normalizes natural language questions for reliable entity extraction and intent matching.
        """
        cleaned = self.clean_text(text)
        lowered = cleaned.lower()

        # Word numbers to digits where relevant (e.g. "top five" -> "top 5")
        for word, val in NUMBER_WORDS.items():
            lowered = re.sub(rf"\b(top|limit|first|highest|lowest|scored|failed)\s+{word}\b", rf"\1 {val}", lowered)
            lowered = re.sub(rf"\b{word}\s+(year|semester|subject|subjects|students)\b", rf"{val} \1", lowered)

        # Standardize domain keywords
        result = lowered
        for pattern, replacement in ACADEMIC_SYNONYMS.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

        return result

    def tokenize(self, text: str) -> List[str]:
        """Simple linguistic tokenization splitting on word boundaries."""
        clean = self.normalize(text)
        return re.findall(r"\b[\w%.-]+\b", clean)


preprocessor = TextPreprocessor()
