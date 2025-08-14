# A simple database of banned keywords and their categories
# Inspired by the research paper's approach 
BANNED_KEYWORDS = {
    "fraud": ["get rich quick", "guaranteed profit", "investment scheme"],
    "gamble": ["betting", "casino", "poker", "win real cash"],
    "eroticism": ["adult", "erotic", "sexy"],
    "superstition": ["lucky charm", "astrology", "fortune teller"],
    "prohibited_substances": ["tobacco", "alcohol", "vape"]
}

def check_text_for_violations(text: str) -> list[str]:
    """
    Checks the input text against the banned keywords database.
    Returns a list of violation categories found.
    """
    violations_found = []
    text_lower = text.lower()
    for category, keywords in BANNED_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                violations_found.append(category)
                break # Move to the next category once a keyword is found
    return violations_found