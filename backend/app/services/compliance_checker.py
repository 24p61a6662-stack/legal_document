def check_compliance(text):
    result = {
        "Compliance Status": "Partial",
        "Missing Elements": [],
        "Risk Areas": [],
        "Suggested Improvements": []
    }

    if "data protection" not in text.lower():
        result["Missing Elements"].append("GDPR Data Protection Clause")

    if "termination" not in text.lower():
        result["Risk Areas"].append("Termination terms unclear")

    return result