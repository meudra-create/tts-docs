# Knowledge Base — Maintenance Guide

This directory is an LLM-maintained knowledge base about the TTS OpenAI API.
It lives in git alongside the docs site, so every change is versioned and reversible.

## Structure

```
knowledge-base/
├── CLAUDE.md          ← this file
├── index.md           ← master index; update on every change
├── api-overview.md    ← capabilities, models, rate limits
├── authentication.md  ← API keys, headers, security
├── endpoints.md       ← all endpoints with parameters + response shapes
├── webhooks.md        ← setup, signature verification, event types
├── errors.md          ← error codes, HTTP status codes, troubleshooting
└── voices.md          ← voice IDs, language support, emotion/vibe system
```

## Page format

Each page should start with a short summary block, then content, then a
cross-reference section at the bottom. Use this template:

```markdown
# <Title>

> **Summary**: one or two sentences.
> **Related**: [[other-page]], [[another-page]]

---

## <Section>
...
```

## Maintenance rules

1. **Always update `index.md`** when a page is added, renamed, or significantly changed.
2. **Cross-references**: when you add a fact that is mentioned in another page,
   add a link in both directions.
3. **Contradictions**: if new information contradicts an existing claim, update
   the claim, add a note in the index, and record the change date in a comment
   (`<!-- updated YYYY-MM-DD: reason -->`).
4. **Summaries**: every page's `> **Summary**` line should describe its current
   content accurately. Rewrite it whenever the page changes substantially.
5. **Completeness**: don't leave placeholder sections — only write sections you
   can fill in. An honest gap (`_Not yet documented_`) is better than wrong
   information.

## How to update

Point the LLM at the source (docs page, API response, changelog entry) and say:
"Update the knowledge base." It will read the relevant KB pages, apply changes,
update cross-references, and update the index. You review the diff and merge.
