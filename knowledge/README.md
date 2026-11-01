# knowledge/: your source of truth

The agent only states facts that are in this folder, or that it can cite with a link. Anything missing becomes `[PLACEHOLDER]`. The better this folder, the better the leads, emails and proposals.

| File / folder | What to put in it | How it's used |
|---|---|---|
| `events-2027.md` | One section per 2027 event: city, date, venue/host, audience size & mix, themes, tiers still available. A template is already in the file. | Matching companies to events, the "why this event" line in emails, proposal briefs |
| `prospectus/` | The sponsorship prospectus PDF for each event (or region). Name them like `new-york-2027.pdf`, `london-2027.pdf`, `global-2027.pdf`. | The **only** source of tier prices and benefits |
| `past-sponsors.xlsx` (or `.csv`) | One row per company × event × year: company, website, events sponsored, year, tier, contact name/title/email, notes, outcome. Start from `past-sponsors.template.xlsx`, then save it as `past-sponsors.xlsx`. | Re-engagement lists, excluding existing sponsors from new-lead searches, honest "you sponsored X in 2026" lines |
| `proof-points.md` | Testimonials (with name/company and permission), delegate stats, case studies, and attendee/host logos you're **allowed** to mention. Note which events each one applies to. | The single proof point in every email; proposal briefs |
| `voice/` | 5–10 of your best real emails (first touches, follow-ups, re-engagement), one `.md` or `.txt` per email. Strip anything confidential. | Drafts are written to sound like you |

## Tips
- **Dates and hosts change.** Mark anything unconfirmed as `TBC`. The agent will treat it as unconfirmed and won't put it in an email.
- **Audience numbers:** use the figures you'd defend in front of a sponsor (e.g. "~400 delegates, 60% CRE/FM/workplace leads"). Note the source/year.
- **Proof points:** if a quote is anonymous-only, say so ("anonymous: may not name the company").
- **Past sponsors:** keep one row per event sponsored, so the agent can see patterns (city, tier, upgrade/downgrade). Use the `Outcome` column (Renewed / Lapsed / Upgraded / Downgraded / Declined 2027).
- `past-sponsors.xlsx/.csv` and everything in `output/` are **git-ignored** because they hold personal data. Keep your own backup.
