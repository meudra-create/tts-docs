---
name: run-tts-docs
description: Run, start, build, screenshot, or test the tts-docs Nuxt documentation site. Use when asked to run the app, take a screenshot, verify a page, or check that docs render correctly.
---

# run-tts-docs

Nuxt 3 documentation site for the TTSOpenAI API. Driven headlessly via
`.claude/skills/run-tts-docs/driver.mjs` + a Playwright Chromium binary.

## Prerequisites

```bash
# Node 22+ and pnpm 9 are already in the dev container.
# Install pnpm deps (idempotent):
pnpm install

# Install Playwright Chromium into /tmp/pw-browsers (one-time, ~105 MB):
PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers npx playwright install chromium

# Install the Playwright npm package into /tmp (driver imports from there):
cd /tmp && npm install playwright && cd -
```

## Build / dev server

```bash
# Start the dev server in background (detached):
PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers \
  node .claude/skills/run-tts-docs/driver.mjs start

# Or manually — blocks the terminal:
PORT=3001 pnpm dev
```

The driver's `start` command spawns `pnpm dev`, detaches it, writes its PID to
`/tmp/tts-docs-server.pid`, then polls until the server answers on port 3001.

## Run (agent path)

The driver is the interface. All commands run from the repo root.

```bash
# Full smoke test — starts server if not running, screenshots 4 pages:
PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers \
  node .claude/skills/run-tts-docs/driver.mjs smoke

# Screenshot any URL → file:
PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers \
  node .claude/skills/run-tts-docs/driver.mjs screenshot /getting-started /tmp/out.png

# Dump visible text of a page to stdout:
PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers \
  node .claude/skills/run-tts-docs/driver.mjs text /getting-started/authentication

# Stop the dev server:
PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers \
  node .claude/skills/run-tts-docs/driver.mjs stop
```

Screenshots land in `/tmp/` by default unless you pass an explicit path.

## Run (human path)

```bash
pnpm dev
# → http://localhost:3000  (or 3001 if PORT=3001)
```

This opens a hot-reload dev server. `Ctrl-C` to stop. Useless headless.

## Routes

| Path | Content |
|------|---------|
| `/` | Landing page |
| `/getting-started` | Introduction |
| `/getting-started/authentication` | API key docs |
| `/getting-started/webhooks` | Webhooks |
| `/getting-started/making-requests` | Making requests |
| `/getting-started/errors` | Error reference |
| `/resources/tts-text` | Text TTS API |
| `/resources/tts-document` | Document TTS API |
| `/resources/tts-story` | Story maker |
| `/resources/tts-emotion` | Emotion TTS |
| `/resources/custom-vibes` | Custom vibes |

Content lives in `content/` as Markdown. Editing `.md` files hot-reloads instantly.

## Gotchas

- **Port 3000 vs 3001**: Nuxt defaults to 3000 but the `dev` script may already
  claim it. The driver always uses `PORT=3001`. Pass `PORT=3000` if needed.
- **`NUXT_UI_PRO_LICENSE` warning**: Dev mode emits a banner about a missing
  license key. The site renders fully without it — it is safe to ignore.
- **`/introduction` returns 404**: The route is `/getting-started`, not
  `/introduction`. The README's title is the doc page title, not the URL.
- **Playwright import path**: The driver imports from `/tmp/node_modules/playwright`.
  This is intentional — tts-docs has no Playwright dep of its own, so it lives in
  `/tmp` to avoid polluting `node_modules`. If `/tmp` is wiped, re-run
  `cd /tmp && npm install playwright`.
- **CommonJS named export**: `playwright/index.js` is CJS. Import as
  `import pkg from '…'; const { chromium } = pkg;` — not a named import.
- **`process.kill(-pid)` for group kill**: `pnpm dev` spawns `nuxt` as a child;
  sending SIGTERM to the pnpm pid alone leaves nuxt running. The driver kills the
  whole process group with `-pid`.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Cannot find package 'playwright'` | `cd /tmp && npm install playwright` |
| `Named export 'chromium' not found` | Already fixed in driver — use default import |
| `Server not ready after 60000ms` | Run `pnpm install` first; then retry |
| Screenshot is blank / shows loading spinner | Increase `waitUntil: 'networkidle'` timeout or add `await page.waitForTimeout(2000)` |
| `apt-get install chromium-browser` fails with 404 | Use `PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers npx playwright install chromium` instead |
