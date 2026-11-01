# WORKTECH Sponsorship Sales Agent

A Claude Code setup for James Battye: skills, subagents and templates for finding, researching and writing to WORKTECH sponsorship prospects. It's not an app. You run it by opening Claude Code in this folder.

## Setup (once)
1. **Clone:**
   ```bash
   git clone https://github.com/jamesthebattye/agent.git ~/worktech-sales-agent
   ```
2. **Python bits** (for the Excel/Word files). Needs Python 3.9+ and `pandoc`:
   ```bash
   pip3 install openpyxl python-docx
   ```
   ```bash
   brew install pandoc poppler
   ```
3. **Connect Apollo.** Name the server `apollo` so the permission rules in `.claude/settings.json` match:
   ```bash
   claude mcp add --transport http apollo https://mcp.apollo.io/mcp
   ```
   Then start `claude` in the folder, run `/mcp`, select **apollo** and sign in.
4. **Fill in `knowledge/`.** See `knowledge/README.md`: 2027 events, prospectus PDFs, past sponsors (`past-sponsors.template.xlsx` → save as `past-sponsors.xlsx`), proof points, and 5–10 of your emails in `voice/`.
5. Start Claude Code in the folder:
   ```bash
   cd ~/worktech-sales-agent && claude
   ```

## The 5 commands you'll use daily
| Command | What it does | Stops for your OK at |
|---|---|---|
| `/find-leads New York 2027 30` | Apollo company search → scored shortlist → BD and marketing contacts → lead sheet .xlsx | shortlist · contacts to enrich (with credit estimate) |
| `/reengage-sponsors 2026` | Past sponsors → who's still there / who's left → 2027 event per company → lead sheet with history | shortlist + credit estimate |
| `/research-account Acme New York 2027` | Sourced brief with 2–3 "why this event, why now" hooks (`docx` for Word) | – |
| `/draft-email Jane Doe at Acme` | First touch + 2 follow-ups, critic score, one revision → outbox | – (never sends) |
| `/batch-outreach output/2026-11-01/lead-sheet-new-york-2027.xlsx` | Research + drafts for a whole sheet, in parallel → outbox for review → optional Apollo sequence | batch · drafts · every Apollo write |

**Every weekday morning (automatic):** `/morning-brief` runs about 07:30 UK time. It covers new companies for the day's focus city, each company scored 1–5 for fit, BD and marketing contacts rated 1–5 (priority A/B/C, emails not revealed), outreach plays, office moves with the tech partners named in them, and industry news. It arrives as a private page plus a push notification. Reply "enrich <names>" in a session to reveal emails. Settings: `knowledge/brief-settings.md`. Covered companies are tracked in `state/seen-companies.json`. You can also run it by hand: `/morning-brief London`.

There's also `/proposal-brief Acme New York 2027`, a proposal outline (Word) with tier and price from the prospectus. Give it your WORKTECH template `.pptx` and it builds the deck.

## Example weekly routine
- **Monday (30 min):** `/reengage-sponsors` for one region, approve the list and the enrichment. Then `/batch-outreach` on it, review the drafts, and approve them into an Apollo sequence.
- **Tuesday:** `/find-leads <next event> 25` for new logos. Approve the shortlist and contacts.
- **Wednesday:** `/batch-outreach` on Tuesday's sheet. Review the drafts over coffee: approve, edit or drop.
- **Thursday:** replies. `/research-account` for anyone warm, then `/proposal-brief` for anyone who asked for a proposal (paste your call notes).
- **Friday (15 min):** add new wins, losses and notes to `knowledge/past-sponsors.xlsx`, add new testimonials or stats to `proof-points.md`, and drop any email that worked well into `voice/`.

## Where things go
```
CLAUDE.md                project memory: ICP, rules, guardrails, email style
knowledge/               your source of truth (you fill this in)
.claude/skills/          the 6 slash commands
.claude/agents/          lead-researcher, email-drafter, email-critic, industry-scout
.claude/settings.json    pre-approves read-only Apollo search; ALWAYS asks before credit spend or any Apollo write/send
templates/               lead-sheet.xlsx, email-brief.md, email-draft.md, account-brief.md, proposal-brief.md, morning-brief.md
state/                   morning-brief rotation + companies already covered (company names only, committed)
scripts/                 xlsx_tools.py (lead sheets, outbox, read xlsx), md_to_docx.py (Word + table→xlsx), check_email.py
output/YYYY-MM-DD/       everything produced that day (git-ignored: contains personal data)
```

## Guardrails built in
- Nothing is sent, sequenced, or written to Apollo without a preview and your explicit "yes". `.claude/settings.json` also forces a permission prompt on every Apollo write and email-reveal tool.
- Facts come only from `knowledge/` or cited sources. Gaps show as `[PLACEHOLDER]`.
- Search before enrich. Emails are revealed only for contacts you approve, and the credit estimate is shown first.

## Rebuilding templates
```bash
python3 scripts/build_templates.py
```
