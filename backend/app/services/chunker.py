import re

def clause_chunk(text: str):
    clauses = re.split(r'\n\d+\.\s', text)
    return [c.strip() for c in clauses if len(c.strip()) > 50]