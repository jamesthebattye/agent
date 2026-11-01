---
name: proposal-brief
description: Produce the content outline for a WORKTECH sponsorship proposal for a warm lead - recommended tier with price from the event prospectus, benefits, why-them rationale and proof points - as a Word document ready to drop into James's WORKTECH PowerPoint template, or build the .pptx deck directly if the template is provided. Use when James says "/proposal-brief [company] [event]", "build a proposal for [company]", "they want a proposal", "put together a sponsorship deck", or "what tier should I pitch [company]".
argument-hint: <company> <event city + year> [tier] [path to template .pptx] [call notes]
---

# proposal-brief

Arguments: `$ARGUMENTS` = company, event, optional tier, optional template `.pptx` path, and optional notes from the call or reply (James can paste these too).

## 1. Inputs
- **Prospectus:** find the event's PDF in `knowledge/prospectus/` and read it (use the pdf skill or `pdftotext`). Pull out each tier's **price, currency, tax note and benefits**, and record the page number. If there's no prospectus, all prices become `[PLACEHOLDER: price from prospectus]`. **Never estimate a price.**
- **Event facts:** `knowledge/events-2027.md`. **Proof points:** `knowledge/proof-points.md` only.
- **Account:** the latest `output/*/research-<company>.md` (run `research-account` first if there isn't one) and any history in `knowledge/past-sponsors`.
- **What the lead said:** the call notes / reply James provides. Ask for them if there are none. They drive the "why them" slide.

## 2. Recommend a tier
Pick the tier whose benefits match what they said they want (e.g. speaking slot → a tier that includes one; meetings → a tier with hosted roundtable/delegate access), at a sensible budget for their size and history. Show the lower and higher options for contrast. Explain the recommendation in 2–3 lines, citing prospectus pages.

## 3. Write the brief
- Follow `templates/proposal-brief.md` (slide-by-slide). Save it to `output/YYYY-MM-DD/proposal-<company>-<city>-2027.md`.
- Convert it: `python3 scripts/md_to_docx.py output/YYYY-MM-DD/proposal-<company>-<city>-2027.md`. That produces the .docx plus one .xlsx per table (the package and options tables).

## 4. Deck (only if James gives the template .pptx)
- Use the **pptx skill**. Open James's WORKTECH template, reuse its layouts and master, and fill one slide per section of the brief. Keep the template fonts and colours. Don't invent imagery or logos; leave picture placeholders.
- Save to `output/YYYY-MM-DD/proposal-<company>-<city>-2027.pptx`. Render thumbnails to check that nothing overflows.

## 5. Hand-off
List the open items: placeholders, unconfirmed event facts, and anything to confirm with the lead. The proposal is never sent from here.
