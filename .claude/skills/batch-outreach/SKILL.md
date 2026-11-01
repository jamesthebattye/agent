---
name: batch-outreach
description: Run research-account and draft-email across an approved lead sheet in parallel using subagents, producing one dated outbox (one .md per contact + outbox.xlsx) for James's review, then - only after James approves each batch - offer to add approved contacts to an Apollo sequence. Use when James says "/batch-outreach [lead sheet]", "draft emails for the whole list", "do outreach for these leads", or "load these into a sequence".
argument-hint: <path to lead-sheet .xlsx>  [rows e.g. "1-20"] [function BD|Marketing|both]
---

# batch-outreach

Arguments: `$ARGUMENTS` = a lead sheet path (default: the most recent `output/*/lead-sheet-*.xlsx`), plus optional row range and function filter. Follow CLAUDE.md. Use a task list and **stop at each ⛔ gate**.

## 0. Load and confirm
- `python3 scripts/xlsx_tools.py read --in <lead sheet>`. Keep rows with status `approved` / `enriched` (or the rows James named).
- Group the rows by company. Show the count: N companies, M contacts (BD x / Marketing y), and how many have no email yet.
- ⛔ Confirm the batch before starting (batches of up to **10 companies** at a time keep review manageable).

## 1. Research in parallel
For each company in the batch with no research file from the last 14 days in `output/`, launch **one `lead-researcher` subagent per company in a single message** (parallel). Each one gets the company, domain, event facts and history rows, and returns a brief that gets saved to `output/YYYY-MM-DD/research-<company>.md`.

## 2. Draft in parallel
For each contact, build the email brief (`templates/email-brief.md`), then launch **one `email-drafter` per contact in parallel**. Contacts at the same company must get **different hooks or angles**: BD vs Marketing, and no copy-paste between colleagues.

## 3. Critique in parallel, then revise once
Launch **one `email-critic` per draft in parallel**. Apply each critic's edits (one revision per draft). Re-run `python3 scripts/check_email.py` on each draft.

## 4. Outbox
- `python3 scripts/xlsx_tools.py outbox --dir output/YYYY-MM-DD/outbox`
- ⛔ **Gate: drafts.** Show a review table: contact, company, function, subject, critic score, open flags/placeholders, file. Ask James to mark each one approve / edit / drop. Apply those edits. Set `status: approved` in the front matter of approved drafts and rebuild `outbox.xlsx`.

## 5. Optional: push approved drafts to Apollo (writes, so ask)
Offer this only when James has approved drafts. **Nothing gets written to Apollo without an explicit "yes" for this exact batch.**
1. List the sequences: `apollo_emailer_campaigns_search`. Ask which one to use, or whether to create one (`apollo_sequences_create` is a write, so preview it first). List the sending mailboxes: `apollo_email_accounts_index`.
2. People must exist as Apollo **contacts** to be sequenced. For anyone who isn't one yet, preview the `apollo_contacts_create` / `apollo_contacts_bulk_create` payload (name, title, company, email). ⛔ Wait for "yes".
3. Preview `apollo_emailer_campaigns_add_contact_ids`: sequence name, mailbox, contact list, and how the personalised copy will be used (e.g. put each contact's Email 1 into a custom field/step, or James pastes it in). Say plainly whether the sequence will **start sending automatically**. ⛔ Wait for "yes".
4. Only then make the calls. Report the result, and set `status: in sequence` in the outbox.

Never call `apollo_emailer_messages_send_now` or `apollo_emailer_campaigns_approve` unless James explicitly asks for that specific action and confirms the preview.
