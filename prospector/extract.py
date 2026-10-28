"""Pull tools, experience and pay out of a job posting's text with plain regexes."""
import re

# "Outreach" is matched only as the product (outreach.io), not the everyday word.
TOOLS = {
    "Clay": r"\bclay\b",
    "HubSpot": r"hubspot",
    "Salesforce": r"salesforce",
    "Outreach.io": r"outreach\.io",
    "Salesloft": r"salesloft",
    "Apollo": r"\bapollo(?:\.io)?\b",
    "ZoomInfo": r"zoominfo",
    "n8n": r"\bn8n\b",
    "Zapier": r"zapier",
    "Python": r"\bpython\b",
    "SQL": r"\bsql\b",
    "Snowflake": r"snowflake",
    "dbt": r"\bdbt\b",
    "Gong": r"\bgong\b",
    "6sense": r"6sense",
    "Clearbit": r"clearbit",
    "Sales Navigator": r"sales navigator",
    "Smartlead": r"smartlead",
    "Instantly": r"\binstantly\b",
    "Lemlist": r"lemlist",
    "LLM/AI": r"\bllms?\b|large language|openai|claude|\bgpt|generative ai|ai agents?",
}

_YEARS = re.compile(r"(\d{1,2})\+?\s*(?:-\s*\d{1,2}\s*)?years", re.I)
_PAY = re.compile(r"\$\s?(\d{2,3}(?:,\d{3})?)(k)?\s*(?:-|–|to|and)\s*\$?\s?(\d{2,3}(?:,\d{3})?)(k)?", re.I)


def extract_tools(text: str) -> list[str]:
    text = text or ""
    return [name for name, pat in TOOLS.items() if re.search(pat, text, re.I)]


def extract_years(text: str):
    """First 'N years' ask in the text, or None."""
    m = _YEARS.search(text or "")
    return int(m.group(1)) if m else None


def _to_usd(num: str, k: str | None) -> int:
    n = int(num.replace(",", ""))
    return n * 1000 if (k or n < 1000) else n


def extract_pay(text: str):
    """First plausible annual pay range as (low, high), or None."""
    m = _PAY.search(text or "")
    if not m:
        return None
    lo, hi = _to_usd(m.group(1), m.group(2)), _to_usd(m.group(3), m.group(4))
    return (lo, hi) if 40_000 <= lo <= hi <= 600_000 else None
