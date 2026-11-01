#!/usr/bin/env python3
"""Mechanical checks on an email draft file (used by the email-critic subagent).

Checks each email in a draft .md (sections '## Email 1 ...' and '## Follow-up ...'):
  - body word count (first touch 60-120, follow-ups < 80); the sign-off line 'James' is excluded
  - subject line 2-6 words
  - banned hype words / phrases
  - US spellings (UK English required)
  - first line opens about WORKTECH / the sender instead of the recipient
  - unresolved [PLACEHOLDER]s
  - exclamation marks
  - every hook in the front matter 'sources:' has a URL

Usage:  python3 scripts/check_email.py output/2026-11-01/outbox/jane-doe-acme.md
Prints a JSON report. Exit code 0 always (it informs the critic, it does not decide).
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from xlsx_tools import parse_draft  # noqa: E402

BANNED = [
    "revolutionary", "synergy", "synergies", "game-changer", "game changer", "game-changing",
    "hope this finds you well", "hope this email finds you", "cutting-edge", "cutting edge",
    "best-in-class", "world-class", "unparalleled", "unmissable", "don't miss", "leverage",
    "circle back", "touch base", "just checking in", "just following up", "quick question",
    "i wanted to reach out", "reaching out because", "exciting opportunity", "amazing",
    "incredible", "awesome", "thought leader in the space", "move the needle", "disrupt",
    "as per my last email", "bumping this", "i'd love to", "hop on a call", "pick your brain",
]
US_SPELLINGS = {
    "organize": "organise", "organization": "organisation", "organizations": "organisations",
    "prioritize": "prioritise", "optimize": "optimise", "color": "colour", "favorite": "favourite",
    "behavior": "behaviour", "analyze": "analyse", "realize": "realise", "recognize": "recognise",
    "program": "programme (unless software)", "catalog": "catalogue", "center": "centre (unless a proper noun)",
    "labor": "labour", "neighbor": "neighbour", "customize": "customise", "utilize": "use",
    "specialized": "specialised", "personalized": "personalised",
}
SELF_OPENERS = re.compile(r"^(i\b|i'm\b|i am\b|my name\b|we\b|we're\b|at worktech\b|worktech\b|hi\b.*,\s*$)", re.I)
GREETING = re.compile(r"^(hi|hello|dear|morning|afternoon)\b[^\n]*,?\s*$", re.I)


def words(s):
    return re.findall(r"[A-Za-z0-9£$€%'’\-\.]+", s)


def check_email(e, first_touch):
    issues = []
    body = e["body"].strip()
    lines = [l for l in body.splitlines() if l.strip()]
    # drop sign-off
    while lines and re.fullmatch(r"(james|james battye|best,?|thanks,?|cheers,?|regards,?|best regards,?|kind regards,?)\s*", lines[-1].strip(), re.I):
        lines.pop()
    # drop greeting for the first-line test (but count it)
    content_lines = lines[1:] if lines and GREETING.match(lines[0]) else lines
    text = "\n".join(lines)
    wc = len(words(text))
    if first_touch and not (60 <= wc <= 120):
        issues.append(f"Word count {wc} (first touch must be 60-120)")
    if not first_touch and wc >= 80:
        issues.append(f"Word count {wc} (follow-ups must be under 80)")
    swc = len(words(e.get("subject", "")))
    if e.get("subject") and not e["subject"].lower().startswith("re:") and not (2 <= swc <= 6):
        issues.append(f"Subject is {swc} words (must be 2-6)")
    if first_touch and not e.get("subject"):
        issues.append("Missing subject line")
    low = text.lower()
    for b in BANNED:
        if b in low:
            issues.append(f"Banned phrase: '{b}'")
    for us, uk in US_SPELLINGS.items():
        if re.search(rf"\b{us}\b", low):
            issues.append(f"US spelling '{us}' -> '{uk}'")
    if first_touch and content_lines and SELF_OPENERS.match(content_lines[0].strip()):
        issues.append("First line is about the sender/WORKTECH, not the recipient")
    if "[PLACEHOLDER" in text.upper():
        issues.append("Contains [PLACEHOLDER] - needs James to fill before sending")
    if "!" in text:
        issues.append("Contains an exclamation mark")
    q = text.count("?")
    if first_touch and q > 2:
        issues.append(f"{q} questions - keep to one soft ask")
    return {"section": e["title"], "subject": e.get("subject", ""), "word_count": wc, "issues": issues}


def main(path):
    text = Path(path).read_text(encoding="utf-8")
    meta, emails = parse_draft(text)
    report = {"file": str(path), "emails": [], "meta_issues": []}
    if not emails:
        report["meta_issues"].append("No '## Email 1' / '## Follow-up' sections found")
    for e in emails:
        report["emails"].append(check_email(e, e["title"].lower().startswith("email 1")))
    src = meta.get("sources", "")
    if not re.search(r"https?://", src):
        report["meta_issues"].append("Front matter 'sources:' has no URLs - hooks must be sourced")
    claims = re.search(r"^##\s+Claims check\s*\n(.*?)(?=^##\s|\Z)", text, re.S | re.M)
    if not claims or not claims.group(1).strip():
        report["meta_issues"].append("Missing '## Claims check' section mapping each claim to a source")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
