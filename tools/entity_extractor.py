import re


SERVICES = [
    "auth-service",
    "payments-service",
    "orders-service"
]

ERROR_KEYWORDS = [
    "timeout",
    "exhausted",
    "failed",
    "error",
    "unreachable",
    "latency"
]

OWNER_KEYWORDS = {
    "auth": "auth-team",
    "payments": "payments-team",
    "db": "database-team"
}


def extract_entities(text: str):
    """
    Extract services, error keywords, and owner hints from unstructured text.
    """
    text_lower = text.lower()

    services_found = set()
    errors_found = set()
    owners_found = set()

    for service in SERVICES:
        if service in text_lower:
            services_found.add(service)

    for keyword in ERROR_KEYWORDS:
        if keyword in text_lower:
            errors_found.add(keyword)

    for keyword, owner in OWNER_KEYWORDS.items():
        if keyword in text_lower:
            owners_found.add(owner)

    return {
        "services": list(services_found),
        "errors": list(errors_found),
        "owners": list(owners_found)
    }
