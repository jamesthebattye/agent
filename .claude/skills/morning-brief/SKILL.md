---
name: morning-brief
description: James's daily WORKTECH sales brief - finds NEW sponsor-prospect companies for the day's focus event, finds and rates BD and marketing contacts (no email reveals), drafts an outreach plan, and researches the latest office moves (and the technology, AV, furniture, design and FM partners named in them) plus industry news. Runs unattended each weekday morning from a scheduled task, or on demand. Use when James says "/morning-brief", "run my morning brief", "what are today's leads", or "morning leads for [city]".
argument-hint: "[city]   (default: the next city in the rotation in state/brief-state.json)"
---

# morning-brief

Arguments: `$ARGUMENTS` = an optional focus city. If none is given, use `rotation[next_index]` from `state/brief-state.json`.

**Read `knowledge/brief-settings.md` first.** It holds James's standing rules for this run: the credit cap, **no enrichment**, volume and delivery. Everything in CLAUDE.md also applies. The run may be unattended, so **never** wait for an answer. Where the normal skills would stop at a gate, the brief lists the options instead, and James acts on them later.

Today = `date +%F`. Output folder = `output/<today>/`. Keep a running count of credits spent and stop at the cap.

## 1. Load state (free)
- `state/brief-state.json` (rotation and next city), `state/seen-companies.json` (every company already briefed or reviewed), `knowledge/events-2027.md` (the focus event's facts), and `knowledge/past-sponsors.*` if it exists.
- Check Apollo is connected (`apollo_users_api_profile` with `include_credit_usage=true`) and record the balance at the start. If Apollo isn't available, still produce the research sections. Say "Apollo not connected" at the top and skip steps 3–4.

## 2. Research, in parallel (free)
Launch these subagents **in one message**:
- **`industry-scout` (office moves):** "Office moves, new HQs, relocations, major fit-outs and lease signings in <city> and its region in the last 14 days, plus the 3 largest elsewhere in WORKTECH cities. For each move, name the companies credited as partners: architect/designer, AV/collaboration integrator, workplace tech (booking, sensors, visitor management), furniture, smart building/BMS, FM provider, project manager/broker. Sources required."
- **`industry-scout` (industry news):** "Last 7 days of corporate real estate, facilities, workplace and HR-tech industry news relevant to WORKTECH sponsors: funding rounds, M&A, product launches, leadership moves, market reports (occupancy, leasing), and vendor events. Prioritise <city>/<region>. Sources required."

## 3. Find new companies (≤5 credits)
Candidates come from two places.
1. **Partners named in office moves** (from step 2). These are the strongest leads, because they have a live, sourced reason to talk now.
2. **Segment searches for the focus city:** `apollo_mixed_companies_search` with the city/country, 200+ employees, and one or two ICP segments a day. Rotate segments using the day of the year. Use `page` 2+ if page 1 is all companies from `seen-companies.json`.

To check candidates:
- Drop any domain already in `state/seen-companies.json`.
- Check the step-2 partner companies with **one** `apollo_mixed_companies_search` call using `q_organization_domains_list` (up to 100 domains, 1 credit). It returns headcount, industry and HQ, and shows which ones are already **saved Apollo accounts** (`accounts` bucket) and which are **net-new** (`organizations` bucket).
- For saved accounts, record the owner (`apollo_users_search` maps `owner_id` to a name), sequence history and lists. Apply the CLAUDE.md colleague rule: include them with a `⚑ Owner: <name>` flag. Accounts with live sequence activity (not_sent/paused, or activity in the last 30 days) go in "Already being worked", not in the main list.
- **Score company fit 1–5** with the CLAUDE.md rubric, adding **+1 (max 5)** for a sourced office-move or news trigger in the last 30 days. Keep 8–12, ranked. **Net-new companies rank above saved accounts when the score is tied.**

## 4. Find and rate contacts (free, no reveals)
For each kept company:
- First `apollo_contacts_search` (already in James's Apollo, with emails, free), then `apollo_mixed_people_api_search` for **1–2 BD and 1–2 Marketing** people (title lists as in `find-leads`). Prefer people located in the event region.
- **Never call `apollo_people_match`, `apollo_people_bulk_match` or `apollo_agent_bulk_enrich`.** Surnames stay masked (e.g. "Sarah P.") until James asks for an enrichment.

**Contact score (1–5).** Start at 1, then add:
- **+1 function match:** event, field or brand marketing, partnerships, or a BD/sales leader who owns the region.
- **+1 seniority sweet spot:** Director, Head, VP or SVP. C-suite only at companies under 1,000 staff.
- **+1 regional match:** based in the event's city or region, or a regional title (e.g. "North America", "UK&I", "DACH").
- **+1 reachable:** `has_email: true` in Apollo, or already a saved contact with a verified email.
- **−1** if the contact is owned by a colleague or is in a live sequence. The flag stays either way.
- Cap the score at 5.

**Priority** comes from company fit × contact score:
- **A = 16 or more:** work today.
- **B = 9–15:** this week.
- **C = 8 or less:** keep warm.

## 5. Outreach strategy (no emails sent, no Apollo writes)
For each **A** (and the best B if there are fewer than 3 A's), write a short play:
- **Why now:** the sourced trigger, e.g. "named AV partner on Deloitte's new London HQ fit-out (source)".
- **Who first:** BD or Marketing, and why.
- **Angle:** BD = pipeline and meetings with the occupiers in the room. Marketing = brand presence, a speaking slot, WORKTECH Academy content.
- **Suggested tier:** indicative only; prices only from the prospectus.
- **Opening line:** one sourced line. Not a full draft. James says "/draft-email <name>" to get one.

Also add up to 3 **"warm-up" plays from office moves**: companies that just moved or opened an HQ in an event city. They're possible **hosts, speakers or delegates**, not sponsors. Name the move and a suggested angle (e.g. "host a WORKTECH site tour").

## 6. Write the outputs
- Write `output/<today>/morning-brief.md` in the `templates/morning-brief.md` format. **Every fact gets a source link.** Unverified facts are marked or dropped.
- Leads to `output/<today>/leads-morning-<today>.json` using the `LEAD_COLUMNS` keys, including `contact_score`, `priority` and `apollo_owner`. Then run `python3 scripts/xlsx_tools.py lead-sheet --in <json> --out output/<today>/leads-morning-<today>.xlsx`.
- `python3 scripts/md_to_docx.py output/<today>/morning-brief.md`. That gives the .docx plus one .xlsx per table (house rule).
- Update `state/seen-companies.json` (add every company shown today, with its status) and `state/brief-state.json` (`next_index` +1, wrapping round; `last_run` = today). Commit **only the `state/` files** (they hold company names, not people data) with the message `morning-brief: <today> <city>`, then push to `origin main`. `output/` stays git-ignored.

## 7. Deliver
- **Private page:** publish `output/<today>/morning-brief.md`, turned into a simple, readable HTML page, to the artifact URL in `state/brief-state.json` `brief_artifact_url`. If it's empty, create one, store the URL and commit. Keep it private. Attach the .xlsx/.docx as page files if the tool allows. If publishing isn't possible in this session, say so in the summary.
- **Summary (the final message, shown in the push notification):** three lines.
  1. City; number of new companies; number of A-priority contacts.
  2. The top lead and its trigger.
  3. Credits spent today and the balance.
  Then: "Reply 'enrich <names>' to reveal emails, or '/draft-email <name>' to draft."

## Guardrails recap
No email reveals · no sending · no Apollo writes · ≤ the credit cap in `knowledge/brief-settings.md` · every claim sourced · people data only in `output/` and the private page.
