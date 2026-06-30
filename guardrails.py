# guardrails.py

import re

MAX_INPUT_LENGTH = 25000

PROMPT_ATTACKS = [
    "ignore previous instructions",
    "forget previous instructions",
    "system prompt",
    "reveal your instructions",
    "jailbreak",
    "developer message",
    "act as chatgpt",
]

PII_PATTERNS = [
    r"\b\d{12}\b",                        # Aadhaar
    r"\b\d{3}-\d{2}-\d{4}\b",             # SSN
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+",  # Email
]


def validate_input(text):

    if not text:
        raise ValueError("Empty input.")

    if len(text) > MAX_INPUT_LENGTH:
        text = text[:MAX_INPUT_LENGTH]

    lower = text.lower()

    for attack in PROMPT_ATTACKS:
        if attack in lower:
            raise ValueError(
                f"Prompt injection attempt detected: {attack}"
            )

    return text


def remove_pii(text):

    for pattern in PII_PATTERNS:
        text = re.sub(pattern, "[REDACTED]", text)

    return text

MAX_OUTPUT = 7000

BAD_WORDS = [
    "password",
    "secret key",
    "api key",
]

HALLUCINATION_TERMS = [
    "100%",
    "guaranteed",
    "certified",
    "ISO 27001 certified",
    "SOC2 certified",
]


def validate_output(text):

    if len(text) > MAX_OUTPUT:
        text = text[:MAX_OUTPUT]

    for word in BAD_WORDS:

        if word.lower() in text.lower():
            text = text.replace(word, "[REDACTED]")

    return text


def detect_hallucination(text):

    flags = []

    for term in HALLUCINATION_TERMS:

        if term.lower() in text.lower():
            flags.append(term)

    return flags