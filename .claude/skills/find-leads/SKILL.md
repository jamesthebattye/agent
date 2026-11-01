---
name: find-leads
description: Find and score new sponsor prospects for a WORKTECH event using Apollo company and people search, then build an .xlsx lead sheet with BD and marketing contacts. Use when James says "find leads for [city/event]", "/find-leads London 2027 30", "who should sponsor WORKTECH [city]", "build a prospect list", or asks for companies in a segment (e.g. "AV companies for Frankfurt").
argument-hint: <city> [year] [count] [segment]   e.g. "New York 2027 30" or "Frankfurt 2027 20 office furniture"
---

# find-leads

Arguments: `$ARGUMENTS`. Parse them as: city (required), year (default 2027), count (default 25), and an optional segment or mode (`reengage` / `include-sponsors`). If no city was given, ask for one.

Follow CLAUDE.md (ICP, fit rubric, guardrails, credit discipline). Create a task list with the steps below. **Stop at each ⛔ gate** and wait for James.

## 1. Load context (no credits)
- From `knowledge/events-2027.md`, read the section for this event: date, host, audience mix, themes, tiers. Note anything TBC or [PLACEHOLDER].
- Read `knowledge/past-sponsors.xlsx|.csv` with `python3 scripts/xlsx_tools.py read --in <file>`. Build an **exclusion list** of existing/past sponsors (by company name and domain). Skip this exclusion only when the mode is `reengage` or `include-sponsors`. In that case, tag those rows instead.
- Work out the target geography: the event city plus its metro and country/region. For New York, use New York metro plus US Northeast and North America HQs with NY offices. For Frankfurt, use Germany/DACH. For Singapore, use Singapore/APAC.

## 2. Company search (Apollo `apollo_mixed_companies_search`)
- Run several focused searches rather than one broad one, one per ICP segment (or just the segment given). Use:
  - `organization_locations`: event city/country (and the region for HQ-elsewhere companies with a local office)
  - `organization_num_employees_ranges`: `200,500`, `501,1000`, `1001,5000`, `5001,10000`, `10001,` (the 200+ rule)
  - keyword tags per segment, e.g.
    - workplace tech: `workplace technology`, `occupancy sensors`, `space management`, `desk booking`, `workplace experience`, `visitor management`
    - AV & collaboration: `audio visual`, `video conferencing`, `collaboration technology`, `meeting room`
    - furniture: `office furniture`, `contract furniture`, `workplace furniture`, `acoustic pods`
    - lighting & building systems: `commercial lighting`, `building automation`, `HVAC`, `indoor air quality`, `access control`
    - smart building / proptech: `smart building`, `proptech`, `IWMS`, `CAFM`, `digital twin`, `building management system`
    - flex: `flexible workspace`, `coworking`, `serviced office`
    - A&D: `workplace design`, `interior architecture`, `fit-out`
    - CRE advisory: `commercial real estate advisory`, `occupier services`, `workplace strategy`
    - FM: `integrated facilities management`, `facility services`, `workplace services`
- Pull about 2× the requested count, dedupe by domain, and remove the exclusion list.
- If a response includes `mcp_credits`, report it.

## 3. Score and shortlist (no credits)
- Score each company 1–5 with the CLAUDE.md rubric. Give a **one-line reason** using only data from Apollo (industry, keywords, headcount, locations, description) or a quick web check. Don't guess.
- Add: segment, suggested tier (indicative: larger, multi-region companies lean Gold/Gold Plus/Platinum; regional or mid-size lean Bronze/Silver/Gold) and a one-line angle.
- Drop 1s. Sort by score, then size. Keep the requested count.
- Save `output/YYYY-MM-DD/shortlist-<city>-<year>.json` (the company rows).

⛔ **Gate 1: shortlist.** Show a table: #, company, website, HQ/region, size, segment, score, reason, suggested tier. Ask James which to keep (e.g. "all", "1-12", "drop 4, 9").

## 4. Find people (no email reveal yet)
For each approved company:
- First run `apollo_contacts_search` (James's own Apollo CRM) to find people already saved there. Reuse them and don't pay twice.
- Then run `apollo_mixed_people_api_search` with `q_organization_domains_list` set to the company domain, `person_seniorities` set to `c_suite, vp, head, director`, and titles in two passes:
  - **Marketing:** `CMO`, `Chief Marketing Officer`, `VP Marketing`, `Head of Marketing`, `Marketing Director`, `Field Marketing`, `Event Marketing`, `Brand`, `Partnerships`
  - **BD/Sales:** `CRO`, `Chief Revenue Officer`, `VP Sales`, `Head of Sales`, `Head of Business Development`, `Strategic Partnerships`, `Sales Director`
  - Prefer people located in the event region, and regional titles ("North America", "Americas", "East", "UK&I", "DACH", "APAC").
- Keep **1–3 BD and 1–3 Marketing** per company. Every company must have at least one of each, or be flagged as "no BD found" / "no marketing found".

⛔ **Gate 2: contacts to enrich.** Show the contacts per company (name, title, function, location, LinkedIn, and whether they're already in Apollo CRM with an email). Give the **credit estimate**: number of new people to enrich ≈ credits (about 1 per email reveal; no phones). Ask James to approve all of them or a subset.

## 5. Enrich approved contacts only
- Run `apollo_people_bulk_match` in batches of up to 10 (with `reveal_personal_emails: false`, no phone reveal), or `apollo_people_match` for one-offs. Use the Apollo person ID or name plus domain.
- Report the credits used and the balance after each batch (from `mcp_credits`, or `apollo_usage_stats_credit_usage_stats`).
- Record the email and email status. If an email is missing, leave it blank and don't guess a pattern.

## 6. Build the lead sheet
- Write the rows (one row per contact, with company fields repeated) to `output/YYYY-MM-DD/leads-<city>-<year>.json` using the keys from `scripts/xlsx_tools.py` `LEAD_COLUMNS`. Set `source`, e.g. `Apollo search 2026-11-01`, and `status: enriched` (or `shortlisted` for not-enriched rows).
- Run `python3 scripts/xlsx_tools.py lead-sheet --in <json> --out output/YYYY-MM-DD/lead-sheet-<city>-<year>.xlsx`.
- Summarise: companies, contacts (BD / Marketing), emails found, credits used, and gaps. Suggest next steps: `/research-account <company>` for the top ones, or `/batch-outreach <lead sheet>`.

Never write to Apollo (contacts, accounts, lists, sequences) in this skill unless James explicitly asks and says yes to a preview.
