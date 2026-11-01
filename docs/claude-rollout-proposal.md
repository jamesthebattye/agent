---
title: "Claude at WORKTECH"
subtitle: "What our AI sales assistant does today, what it will do every day, and a plan to roll it out across the company"
author: "James Battye, Partnerships · WORKTECH Events (Unwired Ventures)"
date: "1 November 2026"
---

# Summary

On 1 November 2026 I used Claude (Anthropic's AI assistant, running as Claude Code) to build a working sales assistant for WORKTECH sponsorship. I then used it on live work the same day. In one session it:

- **Built the system:** 7 commands, 4 specialist AI helpers, templates and house rules, all saved in our own GitHub repository so the whole team can use and improve it.
- **Found and qualified prospects:** 25 companies across WORKTECH New York 2027 and London 2027, and **59 senior BD and marketing contacts**, each rated for fit. 30 now have verified work emails.
- **Researched and wrote:** sourced account briefs, and **6 personalised outreach drafts**. Each draft was scored by a separate AI "critic" and revised. Nothing was sent: every email waits for my approval.
- **Set up a daily brief:** every weekday at 07:09 it delivers new companies, rated contacts, outreach plays, recent office moves (with the partners named in them) and industry news.
- **Protected us from costly mistakes:** it flagged accounts already owned by colleagues, held back accounts with live sequences, caught a company record that was the wrong business, rejected an invalid email, and stopped an Apollo tool that would have silently created CRM records.
- **Cost:** 136 Apollo credits for the whole day, out of a balance of about 847,700.

**What I'm asking for:** a corporate Claude subscription so the sales team, and later conference production and marketing, can use the same system. The ask is a **6-week pilot with 3–5 people**, measured against the success measures in section 9.5, and then a decision on wider rollout.

# What we built

The system is a set of instructions, templates and small scripts that Claude follows. It is not a separate app to buy or maintain. It lives in a private GitHub repository (`jamesthebattye/agent`) and can be copied for any colleague.

| Part | What it is | Why it matters |
|---|---|---|
| Project memory (CLAUDE.md) | Our ideal customer profile, sponsorship tiers, writing style, guardrails and Apollo credit rules | Every run follows the same rules, for every user |
| Commands | `/find-leads`, `/reengage-sponsors`, `/research-account`, `/draft-email`, `/batch-outreach`, `/proposal-brief`, `/morning-brief` | Repeatable workflows anyone can run in plain English |
| Specialist helpers | lead-researcher, email-drafter, email-critic, industry-scout | Work runs in parallel, and an independent critic checks quality |
| Knowledge folder | Event details, prospectus PDFs, past sponsors, approved proof points, example emails | The only sources of truth for prices and claims. If something isn't there, it's marked as missing |
| Outputs | Excel lead sheets, Word documents (every table also saved as Excel), an outbox of drafts, a private daily web page | Fits how we already work |

# What it can do today

| Command | What it does | Where it stops for approval |
|---|---|---|
| `/find-leads <city> <year> <count>` | Searches Apollo by city and segment (workplace tech, AV, furniture, smart building, flex, design, CRE advisory, FM). Scores each company 1–5 for event fit with a one-line reason, finds BD and marketing contacts, and builds a lead sheet | The company shortlist, then which contacts to enrich (with a credit estimate) |
| `/reengage-sponsors` | Takes our past-sponsor list, checks who is still at each company and who has left, picks the most relevant 2027 event and adds the history columns | The shortlist and the credit estimate |
| `/research-account <company>` | A sourced brief covering what they sell, recent news, funding, office moves, regional hiring and event footprint, with 2–3 "why this event, why now" hooks, each with a link | None (research only) |
| `/draft-email <contact>` | A first email plus two follow-ups in our house style, with a different angle for BD and for marketing. An independent critic scores it 1–10 and it's revised once | Always. It never sends |
| `/batch-outreach <lead sheet>` | Research and drafts for a whole lead sheet in parallel, then optionally loads approved drafts into an Apollo sequence | Each batch of drafts, and every Apollo write |
| `/proposal-brief <company> <event>` | A proposal outline with the recommended tier and price, taken only from the prospectus. If given our PowerPoint template, it builds the deck | It doesn't send anything |
| `/morning-brief` | The daily brief (see section 4) | It never reveals emails or sends |

# What it does every day

Every weekday at **07:09 UK time** it runs on its own and refreshes a private web page for me, with a phone notification. It works through all 12 event cities in rotation (London, New York, Frankfurt, San Francisco, Amsterdam, Toronto, Berlin, Seattle, Stockholm, Singapore, Madrid, Sydney) and never repeats a company.

| Section | What's in it |
|---|---|
| Today's top 3 | The three best opportunities, each with its sourced reason to call now and who to call first |
| New companies | 8–12 companies we haven't covered before, scored 1–5 for fit, marked as new to Apollo or already saved, with the owning colleague flagged |
| Rated contacts | 1–2 BD and 1–2 marketing contacts per company, each scored 1–5 and given a priority (A = work today, B = this week, C = keep warm) |
| Outreach plays | Why now, who first, the BD or marketing angle, a suggested tier and an opening line |
| Office moves | New HQs, relocations and fit-outs, with the design, fit-out, AV, workplace-tech, furniture and FM partners named. Partners become leads, and the occupiers become possible hosts or speakers |
| Industry news | Funding, M&A, launches and market reports, each with why it matters for a sponsorship conversation |
| Already being worked | Accounts left out because a colleague or a live sequence is already on them |

**Standing rules for the unattended run:** at most 5 Apollo credits a day, contacts are found but emails aren't revealed until I approve them, nothing is sent, and nothing is written to Apollo.

# Results from day one

| Measure | Result (1 November 2026) |
|---|---|
| Time from empty folder to working system | One working session, about 4 hours, including two live test runs |
| Companies shortlisted and scored | 25 (15 for New York 2027, 10 for London 2027) |
| Senior BD and marketing contacts found and rated | 59 |
| Verified work emails | 30 (23 revealed with my approval, 7 already in our Apollo) |
| Account briefs written (sourced) | 2 in depth, plus trigger research on 8 more companies |
| Outreach drafts (first email + 2 follow-ups) | 6. Critic scores 4–7/10 before revision and an estimated 7–8/10 after. One was held back and retargeted |
| Office moves logged | 7, with named partners where the sources gave them |
| Industry news items | 8, each tied to a sales angle |
| Apollo credits used | 136 in total: 7 for company searches, 87 for 24 approved email reveals, and about 42 lost to an interrupted batch |
| Emails sent without approval | 0 |

**Examples of leads it surfaced:**

- **A fit-out contractor and a design firm** named on a new London office project (29 October), found through office-move research. These are leads we wouldn't have found from a database search.
- **A European furniture group** that had just exhibited at Orgatec (27–30 October). A timely reason to talk about London 2027.
- **A New York proptech company** whose own market report said New York had overtaken San Francisco as the strongest US office market. That became the opening line of its email.

# Guardrails, and what they caught on day one

| Guardrail | What happened |
|---|---|
| Never send, and never write to Apollo without my explicit yes | Every draft is saved in an outbox for review. The system spotted that one Apollo enrichment tool silently creates CRM contacts, and used a reveal-only tool instead |
| Respect colleagues' accounts | Accounts owned by teammates are kept but flagged with the owner's name. Accounts with live sequences (one had 80 contacts queued) are held back so we don't double-contact anyone |
| Never invent facts | Every claim in a brief or email links to a source. Prices come only from the prospectus. Anything missing appears as a placeholder for a human to fill |
| Credit discipline | It searches before enriching, quotes credits before spending, and stays within a daily cap. It corrected its own cost assumptions on day one, when one search type turned out to cost credits |
| Data quality checks | It dropped a company whose Apollo record was a different business (a payments firm with the same name), and rejected an email address that Apollo marked verified but a second validator marked invalid |
| Independent quality review | A separate critic scored every draft and flagged unsupported claims and generic lines. One draft was put on hold because the product didn't fit our audience, and a better-placed contact was found |
| Personal data | Contact data stays in an output folder that isn't uploaded to GitHub, and the daily page is private |

# Current limits

- **Knowledge still to fill in.** Event dates, hosts, audience numbers, proof points and prospectus PDFs aren't loaded yet, so drafts contain placeholders. This is a one-off task of a couple of hours, and most placeholders disappear once it's done.
- **Voice matching.** Drafts aren't yet tuned to my writing style. That needs 5–10 example emails added.
- **Some trade press is blocked.** The cloud environment can't reach a few sites (e.g. Property Week, CoStar, EG, Mix Interiors) where fit-out and technology partners are usually named. Allowing them is a settings change.
- **The scheduled run needs the Apollo connector added** in claude.ai settings. Until then, the daily brief covers research only.
- **A human stays in the loop by design.** It prepares and recommends. People decide, approve and send.
- **Data is only as good as its sources.** Apollo and web data can be out of date (one contact's title differed between Apollo's people data and our saved CRM record). The system flags conflicts rather than hiding them.

# What's next for my own workflow

| When | What |
|---|---|
| Week 1 | Load the knowledge folder (2027 event details, prospectuses, past sponsors, proof points, 5–10 of my emails). Turn on the Apollo connector for the daily brief. Allow the blocked trade-press sites |
| Weeks 1–2 | Run `/reengage-sponsors` across past and 2026 sponsors, our current campaign. Approve enrichment in batches and use `/batch-outreach` for drafts |
| Weeks 2–4 | Load approved drafts into Apollo sequences (each batch approved). Use `/proposal-brief` with our PowerPoint template for warm leads |
| Ongoing | Daily brief each morning. Weekly review of scoring and priority bands, then tune the rules based on what actually converts |

# Rolling it out company-wide

## Who else could use it

| Team | Example uses | What it would need |
|---|---|---|
| Sponsorship and partnerships sales | The same system: lead finding, re-engagement, research, drafts, proposals and a daily brief per territory | Their own territory or city settings and their Apollo login. It's already built |
| Conference production | Speaker and host research for each city: who has just moved into a notable HQ, who is publishing workplace research, plus agenda theme scans | A speaker-research command (variation on research-account) and the office-move scout already built |
| Delegate marketing | Target-company and job-title lists for each event, campaign copy drafts in house style, and a weekly market-news digest for social posts | A delegate-list command and approved messaging in the knowledge folder |
| WORKTECH Academy (content) | Weekly industry-news digests, research summaries and first drafts of articles from sourced material | The industry-scout already built, plus a content style guide |
| Event operations and support | Sponsor deliverable checklists from proposals, briefing packs for event days, and proof-reading | Templates per event |
| Leadership | Pipeline and market summaries for each city ahead of planning meetings | Read access to the shared outputs |

## Phased plan

| Phase | Who | Length | Goal |
|---|---|---|---|
| 1. Pilot | Me plus 2–4 sales colleagues | 6 weeks | Prove time saved and pipeline created, and tune the rules |
| 2. Sales team | The whole partnerships team | Month 2–3 | Shared repository, a territory per person, and a shared rule that no two people contact the same account |
| 3. Wider company | Production, marketing, Academy | Month 3–6 | Add team-specific commands built on the same guardrails |

## Governance

- **Approval gates stay on for everyone.** Nothing is sent and nothing is written to the CRM without the user's explicit approval.
- **One shared rulebook.** Changes to the project memory and guardrails go through a single owner, with version history in GitHub.
- **Credit budgets per person.** A daily cap for unattended runs, and estimates shown before larger spends.
- **Data protection.** Personal data stays in local or private outputs. We should confirm our position with whoever owns data protection, including how we handle contact data from Apollo under GDPR.
- **Colleague ownership is respected.** The system already flags colleague-owned accounts and live sequences.

## Costs to confirm

| Item | Status |
|---|---|
| Claude corporate subscription (seats, admin controls, data handling) | [PLACEHOLDER: quote from Anthropic] |
| Apollo credits | Measured: 136 credits on day one, including two full lead-and-draft runs. The daily brief is capped at 5 a day |
| Set-up time per extra user | Estimate: under an hour to copy the repository and connect Apollo. Measure in the pilot |
| Ongoing maintenance | A few hours a month for one owner to update rules and templates. Measure in the pilot |

## How we'll measure the pilot

| Measure | Baseline (now) | Target to judge the pilot |
|---|---|---|
| Hours a week spent on prospect research and list building | [PLACEHOLDER: each pilot user logs one normal week] | Measure, and agree a target after week 1 |
| Qualified contacts a week | [PLACEHOLDER] | Measure |
| First-touch reply rate | [PLACEHOLDER: current Apollo sequence stats] | Measure against our current sequences |
| Meetings booked from AI-assisted outreach | [PLACEHOLDER] | Measure |
| Pipeline value created (sponsorship proposals sent) | [PLACEHOLDER] | Measure |
| Apollo credits per qualified meeting | n/a | Measure |
| Accidental double-contacts of colleague accounts | [PLACEHOLDER] | Zero |

# Decision requested

1. Approve a **corporate Claude subscription for a 6-week pilot** with 3–5 users from the partnerships team.
2. Name **one owner** for the shared rules and templates (I'm happy to do this).
3. Confirm the **data-protection position** for using Apollo contact data with an AI assistant.
4. Review the pilot results in week 6 and decide on phase 2.

# Appendix: everyday commands

| Say this | What happens |
|---|---|
| `/find-leads London 2027 30` | 30 scored companies for London 2027, then contacts to approve |
| `/reengage-sponsors 2026` | Past sponsors checked: who's still there, who's left, and the best 2027 event |
| `/research-account <company> <event>` | A sourced brief with "why now" hooks |
| `/draft-email <name> at <company>` | First email plus 2 follow-ups, critic-checked, saved to the outbox |
| `/batch-outreach <lead sheet>` | Drafts for a whole list, then optional loading into Apollo sequences with approval |
| `/proposal-brief <company> <event>` | A proposal outline with tier and price from the prospectus, or a full deck from our template |
| `/morning-brief` | Today's brief on demand (it also runs automatically every weekday) |
| "enrich <names>" | Reveals emails for the people you choose, after a credit estimate |
