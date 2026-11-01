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

## 2. Company search
- Plan one search per ICP segment (or just the segment given). Each `apollo_mixed_companies_search` request costs **1 credit** and returns up to 100 companies with full details. Use `per_page` 25–50.
- **Before running**, give the plan and total cost, using Apollo's required wording: "N searches (one per segment), 1 credit each, N credits total. This will consume N credits. Do you want to proceed?". Wait for "yes", then run the batch without asking again.
- If James says no to credits: use the free `apollo_organizations_lookup` with the same filters (it returns only name/domain/website), then score from a quick web check of each site.
- Filters:
  - `organization_locations`: event city/country (and the region for HQ-elsewhere companies with a local office)
  - `organization_num_employees_ranges`: `201,500`, `501,1000`, `1001,5000`, `5001,10000`, `10001,1000000` (the 200+ rule)
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
- **Expect saved accounts to dominate.** In the first test run, all 100 results were James's team's existing Apollo `accounts`, and there were 0 net-new `organizations`. For each one, report the **owner** (map `owner_id` with `apollo_users_search`), the **sequence history** (`contact_campaign_status_tally`) and the **lists** (`label_ids` → `apollo_labels_index`). **Include accounts owned by colleagues (e.g. Kirsty Darlington, Evelyn Wilson) with a flag.** Mark them `⚑ Owner: <name>` in the shortlist table and fill `apollo_owner` in the lead sheet. They aren't excluded. By default, leave out accounts with live sequence activity (`not_sent`/`paused`/activity in the last 30 days) and accounts on another event's sponsor-prospect list (e.g. "SPEX"), and list them separately so James can add them back.
- Apollo responses are big (60–500k characters) and get saved to a file. Parse them with `python3`; never read them raw.
- Results come in two buckets. For `organizations`, `id` is the org ID. For `accounts` (already saved by James's team), use `organization_id`, and note "already in Apollo accounts".
- Pull about 2× the requested count, dedupe by domain, and remove the exclusion list.

## 3. Score and shortlist (no credits)
- Score each company 1–5 with the CLAUDE.md rubric. Give a **one-line reason** using only data from Apollo (industry, keywords, headcount, locations, description) or a quick web check. Don't guess.
- Add: segment, suggested tier (indicative: larger, multi-region companies lean Gold/Gold Plus/Platinum; regional or mid-size lean Bronze/Silver/Gold) and a one-line angle.
- Drop 1s. Sort by score, then size. Keep the requested count.
- Save `output/YYYY-MM-DD/shortlist-<city>-<year>.json` (the company rows).

⛔ **Gate 1: shortlist.** Show a table: #, company, website, HQ/region, size, segment, score, reason, suggested tier. Ask James which to keep (e.g. "all", "1-12", "drop 4, 9").

## 4. Find people (no email reveal yet)
For each approved company:
- People search returns surnames masked (e.g. "Le***t") until enrichment. That's expected.
- First run `apollo_contacts_search` (James's own Apollo CRM) to find people already saved there. Reuse them and don't pay twice.
- Then run `apollo_mixed_people_api_search` with `q_organization_domains_list` set to the company domain, `person_seniorities` set to `c_suite, vp, head, director`, and titles in two passes:
  - **Marketing:** `CMO`, `Chief Marketing Officer`, `VP Marketing`, `Head of Marketing`, `Marketing Director`, `Field Marketing`, `Event Marketing`, `Brand`, `Partnerships`
  - **BD/Sales:** `CRO`, `Chief Revenue Officer`, `VP Sales`, `Head of Sales`, `Head of Business Development`, `Strategic Partnerships`, `Sales Director`
  - Prefer people located in the event region, and regional titles ("North America", "Americas", "East", "UK&I", "DACH", "APAC").
- Note each person's Apollo contact owner if they're already a saved contact. If it's a colleague, flag it (`⚑ Owner: <name>`) even when the account itself is unowned.
- Keep **1–3 BD and 1–3 Marketing** per company. Every company must have at least one of each, or be flagged as "no BD found" / "no marketing found".

⛔ **Gate 2: contacts to enrich.** Show the contacts per company (name, title, function, location, LinkedIn, and whether they're already in Apollo CRM with an email). Give the **credit estimate** (see step 5: about 1 per person on a standard match, variable with waterfall; no phones). Ask James to approve all of them or a subset.

## 5. Enrich approved contacts only
- Once per conversation, call `apollo_users_api_profile` with `include_waterfall_capability=true` and `include_credit_usage=true`. **Note the balance before you spend.**
  - **Waterfall email enabled** (it is for James's team): credits are **variable** per person. In the first test it was 36 credits for 10 people.
  - **Not enabled:** a standard match, about 1 credit per person matched.
- **Use `apollo_people_bulk_match` in batches of ≤10**, with the Apollo person `id`s, `reveal_personal_emails: false`, no phone reveal, and `run_waterfall_email: true` when waterfall is on.
  - Waterfall is **async**. The response carries a `request_id` and no emails. Poll `apollo_webhook_result_show` with it until `status: success`, and read `credits_consumed`.
  - **Don't use `apollo_agent_bulk_enrich`.** Apollo suggests it for more than 10 people, but it **saves everyone as Apollo contacts**, and that's a write James must approve separately.
  - Waterfall can return **personal emails** (gmail etc., `email_source_cd: rampedup`). Use only the work-domain email.
  - Run batches **one at a time**, not in parallel, so an interruption leaves a clean state. If a batch is interrupted, compare the balance before and after; it may have run without returning results.
- Report credits used per batch, and the balance after.
- Record the email and email status. If an email is missing, leave it blank. Never guess an email pattern.

## 6. Build the lead sheet
- Write the rows (one row per contact, with company fields repeated) to `output/YYYY-MM-DD/leads-<city>-<year>.json` using the keys from `scripts/xlsx_tools.py` `LEAD_COLUMNS`. Set `source`, e.g. `Apollo search 2026-11-01`, and `status: enriched` (or `shortlisted` for not-enriched rows).
- Run `python3 scripts/xlsx_tools.py lead-sheet --in <json> --out output/YYYY-MM-DD/lead-sheet-<city>-<year>.xlsx`.
- Summarise: companies, contacts (BD / Marketing), emails found, credits used, and gaps. Suggest next steps: `/research-account <company>` for the top ones, or `/batch-outreach <lead sheet>`.

Never write to Apollo (contacts, accounts, lists, sequences) in this skill unless James explicitly asks and says yes to a preview.
