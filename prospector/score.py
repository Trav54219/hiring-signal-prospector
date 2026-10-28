"""Roll postings up to companies and score how good a prospect each one is."""
import re
from collections import defaultdict

from .extract import extract_pay, extract_tools, extract_years

GTM_ENGINEER = re.compile(r"gtm engineer|go-to-market engineer|growth engineer", re.I)

WEIGHTS = {"intensity": 35, "gtm_engineer": 25, "stack_fit": 30, "ai_signal": 10}


def enrich_posting(p: dict) -> dict:
    text = p.get("description", "")
    return {**p, "tools": extract_tools(text), "years": extract_years(text), "pay": extract_pay(text)}


def score_company(postings: list[dict], target_tools: list[str]) -> tuple[int, list[str]]:
    """0-100 score and the reasons behind it."""
    reasons, score = [], 0.0
    n = len(postings)
    pts = WEIGHTS["intensity"] * min(n, 4) / 4
    score += pts
    reasons.append(f"{n} open GTM role(s): +{pts:.0f}")

    if any(GTM_ENGINEER.search(p["title"] or "") for p in postings):
        score += WEIGHTS["gtm_engineer"]
        reasons.append(f"hiring a GTM engineer: +{WEIGHTS['gtm_engineer']}")

    tools = {t for p in postings for t in p["tools"]}
    wanted = {t.lower() for t in target_tools}
    hit = sorted(t for t in tools if t.lower() in wanted)
    if wanted:
        pts = WEIGHTS["stack_fit"] * len(hit) / len(wanted)
        score += pts
        reasons.append(f"stack match {len(hit)}/{len(wanted)} ({', '.join(hit) or 'none'}): +{pts:.0f}")

    if "LLM/AI" in tools:
        score += WEIGHTS["ai_signal"]
        reasons.append(f"AI workflow signal: +{WEIGHTS['ai_signal']}")
    return round(score), reasons


def rank_companies(postings: list[dict], target_tools: list[str]) -> list[dict]:
    by_co = defaultdict(list)
    for p in map(enrich_posting, postings):
        if p.get("company"):
            by_co[p["company"]].append(p)
    rows = []
    for company, ps in by_co.items():
        score, reasons = score_company(ps, target_tools)
        rows.append({
            "company": company,
            "score": score,
            "open_roles": len(ps),
            "titles": " | ".join(sorted({p["title"] for p in ps})),
            "tools": ", ".join(sorted({t for p in ps for t in p["tools"]})),
            "why": "; ".join(reasons),
            "example_url": ps[0].get("url", ""),
        })
    return sorted(rows, key=lambda r: (-r["score"], r["company"]))
