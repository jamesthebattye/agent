# Morning brief settings

> These are James's standing instructions for the unattended `/morning-brief` run. Edit this file to change them. The scheduled task reads it every morning.
> Set by James on 2026-11-01: "run the searches and find the contacts, but don't enrich until I say otherwise."

## Credits (durable authorisation for unattended runs)
- **Company searches:** up to **5 credits per day** (`apollo_mixed_companies_search`, 1 credit per request). This is pre-approved for the morning brief only.
- **Contact searches:** free tools only (`apollo_mixed_people_api_search`, `apollo_contacts_search`, `apollo_organizations_lookup`).
- **Email reveals / enrichment:** **NOT allowed** in the morning brief. James picks contacts from the brief and says "enrich …" in a conversation, where the normal gate applies.
- **Apollo writes** (contacts, accounts, lists, sequences, tasks): never, from the brief.
- Never send any email.
- Stop and report if Apollo returns `apollo_plan_limit`, or if a run would go over the daily cap.

## Schedule
- Weekdays, about 07:30 UK time (Europe/London).

## Events to hunt for
- Rotate through all 2027 events. Until `knowledge/events-2027.md` has dates, use this rotation, one primary city per run, tracked in `state/brief-state.json`:
  London → New York → Frankfurt → San Francisco → Amsterdam → Toronto → Berlin → Seattle → Stockholm → Singapore → Madrid → Sydney
- Once event dates are filled in, weight the rotation towards the soonest events (an event within 6 months comes up twice as often).

## Volume
- **New companies per brief:** 8–12. Each one must not appear in `state/seen-companies.json`.
- **Contacts per company:** 1–2 BD and 1–2 Marketing.
- **Office moves:** 5–8 items. **Industry news:** 5–8 items.

## Delivery
- Files in `output/YYYY-MM-DD/`: `morning-brief.md`, `morning-brief.docx` (plus one .xlsx per table) and `leads-morning-YYYY-MM-DD.xlsx`.
- A private claude.ai page with the brief, refreshed each run (see the morning-brief skill), plus a push notification with a three-line summary.
