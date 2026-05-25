import re


def clean_text(text: str) -> str:
    """
    Clean extracted text before chunking.
    """
    if not text:
        return ""

    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize multiple new lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove leading and trailing spaces from each line
    lines = [line.strip() for line in text.splitlines()]

    # Remove empty noise lines
    lines = [line for line in lines if line]

    cleaned_text = "\n".join(lines)

    return cleaned_text