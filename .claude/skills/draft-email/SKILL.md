---
name: draft-email
description: Write a bespoke WORKTECH sponsorship first-touch email plus 2 follow-ups for one contact, using the account research, knowledge/ files and James's voice samples, then have the email-critic score it and revise once. Saves to the dated outbox (.md per contact + outbox.xlsx). Never sends. Use when James says "draft an email to [person]", "/draft-email Jane Doe at Acme", "write outreach for [contact]", or "re-engagement email for [past sponsor]".
argument-hint: <contact name> [at <company>] [event]   or a row number from the latest lead sheet
---

# draft-email

Arguments: `$ARGUMENTS` = a contact (name plus company, an email, or a row in the most recent `output/*/lead-sheet-*.xlsx`) and an optional event.

## 1. Gather inputs (don't invent anything)
- **Contact row:** get it from the latest lead sheet (`python3 scripts/xlsx_tools.py read --in <lead sheet>`), or look it up with Apollo `apollo_mixed_people_api_search` (no enrichment). If the email is blank, the draft can still be written. Flag that enrichment is needed before sending.
- **Research:** use today's `output/YYYY-MM-DD/research-<company>.md` if it exists. Otherwise run the `research-account` steps first (via `lead-researcher`).
- **Event facts:** from `knowledge/events-2027.md`. **Proof points:** only from `knowledge/proof-points.md`. **History:** from `knowledge/past-sponsors` (re-engagement).
- **Voice:** the files in `knowledge/voice/`. If there are none, note "not voice-matched".
- Fill in `templates/email-brief.md` and save it as `output/YYYY-MM-DD/outbox/briefs/<contact-slug>.md`.

## 2. Draft (subagent `email-drafter`)
Call `email-drafter` with the brief path, and the voice and proof-point paths. It writes `output/YYYY-MM-DD/outbox/<firstname-lastname>-<company>.md` in the `templates/email-draft.md` format:
- Email 1 (first touch, 60–120 words), Follow-up 1 (day 4, <80), Follow-up 2 (day 10, <80)
- the **angle depends on function**: BD = pipeline and meetings with senior buyers; Marketing = brand presence, speaking slot, content
- re-engagement: name the event and year they sponsored, honestly
- a `## Claims check` mapping every factual claim to a source

## 3. Critique (subagent `email-critic`)
Call `email-critic` with the draft path and brief path. It runs `scripts/check_email.py`, scores the draft 1–10 against the email rules, and returns specific edits.

## 4. Revise once
Apply the critic's edits yourself (or send them back to `email-drafter`). Do **one** revision. Re-run `python3 scripts/check_email.py <draft>` to confirm the mechanical checks pass. Update the front matter `critic_score` (the critic's score, plus your estimate after revision) and add the `## Critic notes`. Leave `status: draft`.

## 5. Outbox
- `python3 scripts/xlsx_tools.py outbox --dir output/YYYY-MM-DD/outbox` rebuilds `outbox.xlsx` (contact, subject, body, follow-ups, critic score, status = draft).
- Show James the final Email 1 + follow-ups in chat, the critic score, and any [PLACEHOLDER]s still to fill.

**Never send, never create Apollo messages or sequences here.** To load drafts into Apollo, use `batch-outreach`, which asks first.
