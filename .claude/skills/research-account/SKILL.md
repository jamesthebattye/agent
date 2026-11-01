---
name: research-account
description: Research one prospect company for a WORKTECH event - what they sell, recent news, funding, product launches, office openings, hiring in the event's region, workplace-event footprint, and 2-3 sourced "why this event, why now" hooks. Use when James says "research [company]", "/research-account Acme New York 2027", "what's the angle for [company]", "brief me on [company] for [event]", or before drafting an email to a contact at that company.
argument-hint: <company or domain> [event city + year]   add "docx" for a Word document
---

# research-account

Arguments: `$ARGUMENTS` = company (name or domain), optional event (default: the event on the current lead sheet, or ask), and optional `docx`.

## How
1. Delegate the research to the **`lead-researcher`** subagent so raw search results stay out of the main conversation. Pass it:
   - the company name and domain, and Apollo org ID if known
   - the event: city, date, host, audience and themes (copied from `knowledge/events-2027.md`)
   - any history rows for this company from `knowledge/past-sponsors` (read with `python3 scripts/xlsx_tools.py read`)
   - the brief format: `templates/account-brief.md`
   - today's date (for "last 12 months")
   For several companies, launch one `lead-researcher` per company **in parallel** (one message, several Agent calls).
2. Check what comes back:
   - every fact has a source link, or is marked as Apollo data / `knowledge/`
   - hooks are specific, recent (ideally <12 months) and tied to the event's city, audience, host or theme
   - nothing about WORKTECH history is claimed unless it's in `knowledge/past-sponsors`
   Anything unsourced: remove it, or mark it `[PLACEHOLDER: verify]`.
3. Save it to `output/YYYY-MM-DD/research-<company-slug>.md`.
4. Output:
   - **Default:** show the brief in chat (compact) and give the file path.
   - **If James asked for `docx`:** run `python3 scripts/md_to_docx.py output/YYYY-MM-DD/research-<slug>.md`. That writes the .docx and one .xlsx per table.

## What the brief must cover
What they sell · HQ, size, presence in the event region · funding/ownership · recent news, launches, office openings/expansions (last 12 months) · hiring in the event's region · WORKTECH appearances (only from `knowledge/`) and similar workplace events (CoreNet Global, IFMA World Workplace, NeoCon, Orgatec, Workplace Futures, etc., sourced) · **2–3 "why this event, why now" hooks, each with a source link** · suggested tier and BD/Marketing angle · gaps.

Credits: research uses web search plus Apollo **search** (`apollo_mixed_companies_search`, `apollo_organizations_job_postings`, `apollo_mixed_people_api_search`). No email reveals. If `apollo_organizations_enrich` would help, say it uses credits and ask first.
