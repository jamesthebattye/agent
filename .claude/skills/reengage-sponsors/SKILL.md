---
name: reengage-sponsors
description: Build the WORKTECH 2027 re-engagement list from past and 2026 sponsors - checks each company in Apollo for current BD and marketing contacts, flags past contacts who have left, matches each company to a relevant 2027 event, and outputs a lead sheet with sponsorship history columns. Use when James says "re-engage past sponsors", "/reengage-sponsors", "who sponsored before that we should go back to", "2027 renewal list", or "check if my old sponsor contacts are still there".
argument-hint: [filter]   e.g. "2026" | "London" | "Gold+" | "top 20" (blank = all)
---

# reengage-sponsors

Arguments: `$ARGUMENTS` is an optional filter (year, event, tier, or "top N"). Follow CLAUDE.md. Use a task list and **stop at each ⛔ gate**.

## 1. Load history (no credits)
- Find `knowledge/past-sponsors.xlsx` or `.csv`. If neither exists, stop and tell James to fill in `knowledge/past-sponsors.template.xlsx` and save it as `past-sponsors.xlsx`.
- Read it: `python3 scripts/xlsx_tools.py read --in knowledge/past-sponsors.xlsx`.
- Group rows by company: events sponsored, years, tiers, contacts, outcomes, notes. Apply the filter. Note any rows where the outcome says not to approach (e.g. "Declined 2027", "do not contact"). Exclude those and list them.
- Read `knowledge/events-2027.md` for the 2027 events, with dates and tiers available.

## 2. Check each company in Apollo (search only, no enrichment)
For each company (in parallel where possible):
- **Company:** run `apollo_organizations_lookup` (free) with the domain or name to confirm the Apollo org and domain. For headcount, locations and office countries, batch the domains into **one** `apollo_mixed_companies_search` per 100 companies (1 credit each). Ask first: "This will consume N credits. Do you want to proceed?". Note any acquisition or rename.
- **Past contact still there?** Search `apollo_mixed_people_api_search` for the past contact's name at that domain, and check `apollo_contacts_search`.
  - Found with a current title at the company → `Yes`.
  - Found at another company, or not found at this domain → `Left`. If they moved to another ICP company, note "now at X". That's a warm lead too, and goes in the notes.
  - Can't tell → `Unknown`.
- **Owner:** record the Apollo owner of the account and of each contact. If it's a colleague, include it with a flag (`⚑ Owner: <name>`, `apollo_owner` column). Don't drop it.
- **Current contacts:** pull 1–3 **BD** and 1–3 **Marketing** people (the same title lists as `find-leads`). Prefer the regions of the events they sponsored before or will most likely sponsor.

## 3. Match a 2027 event per company
Pick a primary event (and an optional second one) using, in order:
1. The same city they sponsored before (a renewal).
2. A city where they've opened offices or are hiring, or a region they've expanded into since (from Apollo locations; check job postings with `apollo_organizations_job_postings` if useful).
3. A sister event in the same region (e.g. London → Amsterdam or Frankfurt; New York → Toronto or San Francisco).

Give a one-line reason. Suggested tier: start from their last tier (an "upgrade from Silver" angle only if there's a reason, e.g. growth).

⛔ **Gate 1: re-engagement shortlist.** Show a table: company, history (events/years/tier/outcome), past contact status, proposed 2027 event + reason, number of BD/Marketing contacts found, suggested tier. Show the people who'd need enriching and the **credit estimate** (≈1 credit per new email reveal; people already in James's Apollo CRM with an email are free). Ask for approval.

## 4. Enrich approved contacts
Follow `find-leads` step 5: check waterfall capability once; `apollo_people_bulk_match` for ≤10 people, or `apollo_agent_bulk_enrich` for more; emails only, no phones. Report credits used and the balance.

## 5. Output
- Rows go to `output/YYYY-MM-DD/reengage-2027.json`, using the `LEAD_COLUMNS` and `HISTORY_COLUMNS` keys (`past_events`, `past_years`, `past_tier`, `past_contact`, `past_contact_status`, `past_outcome`, `history_notes`) from `scripts/xlsx_tools.py`.
- `python3 scripts/xlsx_tools.py lead-sheet --history --in <json> --out output/YYYY-MM-DD/lead-sheet-reengage-2027.xlsx`
- Summarise: companies, contacts by function, how many past contacts have left, "moved to another ICP company" leads, and excluded accounts. Then suggest `/batch-outreach output/YYYY-MM-DD/lead-sheet-reengage-2027.xlsx`.

Re-engagement emails must name the event and year they sponsored, honestly, from the history file. No exaggeration about how it went.
