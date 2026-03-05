def analyze_risk(text):
    risks = []

    if "unlimited liability" in text.lower():
        risks.append(("Unlimited Liability", "High"))

    if "auto-renewal" in text.lower():
        risks.append(("Auto Renewal Clause", "Medium"))

    if "indemnify" in text.lower():
        risks.append(("Indemnity Imbalance", "High"))

    return risks