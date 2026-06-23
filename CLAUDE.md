# CLAUDE.md

## Project Overview

This is the **TTSOpenAI API documentation site** — a static documentation website for the Text-to-Speech OpenAI API service at [ttsopenai.com](https://ttsopenai.com). It is built with Nuxt 3 + Nuxt UI Pro and deployed to Cloudflare Pages via Jenkins CI/CD.

The site documents the public REST API: endpoints, authentication, webhooks, error codes, and resource-specific guides (text, document, story, emotion, custom vibes).

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Nuxt 3 (`future.compatibilityVersion: 4`) |
| UI library | `@nuxt/ui-pro` (extends `@nuxt/ui`) |
| Content | `@nuxt/content` v2 (Markdown + YAML front matter) |
| Styling | Tailwind CSS (via `@nuxt/ui`), custom green palette |
| Font | DM Sans (via `@nuxt/fonts`) |
| Icons | Heroicons + Simple Icons (via `@iconify-json/*`) |
| OG images | `nuxt-og-image` |
| Search | Built-in `@nuxt/content` full-text search, pre-rendered at `/api/search.json` |
| Package manager | `pnpm@9.12.2` (required — do not use npm/yarn) |
| Node version | 20.16.0 |
| Deployment | Cloudflare Pages via `wrangler pages deploy` |
| CI/CD | Jenkins (`Jenkinsfile`) |
| CMS integration | `@nuxthq/studio` (Nuxt Studio visual editor) |

---

## Repository Structure

```
tts-docs/
├── app/                        # Nuxt app directory (compatibilityVersion: 4)
│   ├── app.vue                 # Root component: nav data fetch, SEO defaults, layout shell
│   ├── app.config.ts           # Runtime site config: theme, header/footer links, TOC
│   ├── error.vue               # Error boundary page
│   ├── layouts/
│   │   └── docs.vue            # Docs layout: left sidebar nav + main slot
│   ├── pages/
│   │   ├── index.vue           # Landing page (hero + features grid)
│   │   └── [...slug].vue       # Catch-all docs page (renders Markdown content)
│   └── components/
│       ├── AppHeader.vue       # Top navigation bar with animated logo
│       ├── AppFooter.vue       # Site footer with social links
│       ├── BaseSoundWave.vue   # Animated/static sound wave logo component
│       └── OgImage/
│           └── OgImageDocs.vue # OG image template for doc pages
├── content/                    # Markdown documentation source
│   ├── index.yml               # Landing page hero/features data
│   ├── 1.getting-started/      # Section 1: onboarding docs
│   │   ├── _dir.yml            # Section label: "Getting Started"
│   │   ├── 1.index.md          # Introduction
│   │   ├── 2.authentication.md # API key setup
│   │   ├── 3.webhooks.md       # Webhook setup and payload reference
│   │   ├── 4.marking-requests.md # First API request walkthrough
│   │   └── 5.errors.md         # Error codes and troubleshooting
│   └── 2.resources/            # Section 2: API resource docs
│       ├── _dir.yml            # Section label: "Resources"
│       ├── 1.tts-text.md       # Text-to-speech endpoint
│       ├── 2.tts-document.md   # Document conversion endpoint
│       ├── 3.tts-story.md      # Story/multi-voice endpoint
│       ├── 4.tts-emotion.md    # Emotion/tone endpoint
│       └── 5.custom-vibes.md   # Custom voice styles endpoint
├── public/                     # Static assets (favicon, OG image, PEM key)
│   └── assets/
│       └── uapi_public_key.pem # Webhook signature verification public key
├── server/
│   └── api/
│       └── search.json.get.ts  # Search index API route (pre-rendered)
├── nuxt.config.ts              # Nuxt configuration
├── nuxt.schema.ts              # Nuxt Studio schema (app config UI)
├── tailwind.config.ts          # Custom green color palette + DM Sans font
├── eslint.config.mjs           # ESLint config (Nuxt flat config + stylistic)
├── Dockerfile                  # Multi-stage Docker build → wrangler deploy
├── Jenkinsfile                 # CI/CD pipeline (develop → dev, main → prod)
└── deployment/                 # Ansible deployment playbooks (infra)
```

---

## Development Workflow

### Commands

```bash
pnpm install        # Install dependencies (required after clone)
pnpm dev            # Start dev server at http://localhost:3000
pnpm build          # SSR build
pnpm generate       # Static site generation (used in production)
pnpm preview        # Preview generated output
pnpm lint           # Run ESLint
pnpm typecheck      # Run vue-tsc type checking
```

### First-time setup

```bash
pnpm install        # Runs postinstall → nuxt prepare automatically
pnpm dev
```

The `.nuxt/` directory is generated on first run. Never commit it.

---

## Content Conventions

### File naming

Content files use numeric prefixes to control sidebar sort order:
- `1.getting-started/` sorts before `2.resources/`
- `1.index.md` sorts before `2.authentication.md`

The number prefix does not appear in the URL. `/getting-started/authentication` maps to `1.getting-started/2.authentication.md`.

### Front matter

Every Markdown content file must have:

```yaml
---
title: Page Title        # shown in <title> and page header
description: Short desc  # shown in page subheading and meta description
---
```

Optional front matter:
- `navigation: false` — excludes page from sidebar nav and search index
- `toc: false` — hides the right-hand table of contents panel
- `links: [...]` — adds action buttons in the page header

### Section labels

`_dir.yml` files set the display label for a content directory:

```yaml
title: Getting Started
```

### Landing page (`content/index.yml`)

The root `index.yml` is structured YAML (not Markdown). It drives the hero section and features grid on `app/pages/index.vue`. It follows the `@nuxt/ui-pro` `ULandingHero` / `ULandingCard` component prop shapes.

### MDC components in Markdown

`@nuxt/ui` components `UButton` and `UIcon` are registered globally and usable in Markdown files via MDC syntax:

```markdown
::u-button
---
icon: 'i-heroicons-arrow-right'
label: Click me
to: https://example.com
target: _blank
---
::
```

Use `::callout` (from UI Pro) for tips and notices:

```markdown
::callout
---
icon: i-heroicons-light-bulb
---
Your tip here.
::
```

Use `::code-group` for tabbed code examples:

````markdown
::code-group
```bash [terminal]
curl ...
```
```ts [py]
import requests
```
```ts [ts]
import axios
```
::
````

Note: Python code blocks use the `[py]` tab label but the `ts` language hint (for syntax highlighting purposes) — this is an existing pattern in the codebase.

### Inline type annotations

API attribute docs use inline HTML spans for type labels (not a component):

```markdown
`param_name` [string]{style="color: rgb(var(--color-gray-400) / var(--tw-text-opacity, 1)); font-weight: 300;"}
```

---

## App Configuration (`app/app.config.ts`)

Site-wide configuration lives in `app/app.config.ts`. Key sections:

- **`ui.primary`** — primary color (`"green"` — custom palette in `tailwind.config.ts`)
- **`ui.gray`** — neutral color (`"slate"`)
- **`seo.siteName`** — appended to all page `<title>` tags
- **`header.links`** — icon buttons in the top-right header
- **`footer.links`** — social/external links in the footer
- **`toc.bottom.edit`** — base URL for "Edit this page" links (points to GitHub `develop` branch)
- **`toc.bottom.links`** — community links shown at the bottom of the TOC panel

The `nuxt.schema.ts` file defines the Nuxt Studio UI schema for these config fields (visual editor metadata only — do not add runtime logic here).

---

## Styling Conventions

- **Primary color**: Custom green palette defined in `tailwind.config.ts` (teal-green, e.g. `#3a9284` = green-500)
- **Font**: DM Sans, configured in `tailwind.config.ts` as the default sans-serif
- **Dark mode**: Supported via Nuxt's `colorMode` (transitions disabled for performance)
- **Icons**: Use Iconify identifiers prefixed with the collection (`i-heroicons-*`, `i-simple-icons-*`, `i-mdi-*`, etc.)
- **No custom CSS** except in `BaseSoundWave.vue` (animation keyframes for the logo)

---

## Routing

| URL | Source |
|---|---|
| `/` | `app/pages/index.vue` + `content/index.yml` |
| `/getting-started` | `content/1.getting-started/1.index.md` |
| `/getting-started/authentication` | `content/1.getting-started/2.authentication.md` |
| `/resources/tts-text` | `content/2.resources/1.tts-text.md` |
| `/api/search.json` | `server/api/search.json.get.ts` (pre-rendered) |

All doc pages use the `docs` layout and are handled by `app/pages/[...slug].vue`.

---

## Deployment

### Environments

| Branch | Environment | Cloudflare Pages Project |
|---|---|---|
| `develop` | dev | `frontend-docs-tts-dev` |
| `main` | prod | `frontend-docs-tts-prod` |

### Build process

The Dockerfile runs `pnpm run generate` (static site generation) and then uses `wrangler pages deploy dist` to publish to Cloudflare Pages.

```
Docker build (multi-stage)
  → pnpm install
  → pnpm run generate  (outputs to dist/)
  → wrangler pages deploy dist --project-name=<project>
```

Environment variables (`CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN`) are injected by Jenkins from stored credentials — never hardcode these.

### Jenkins pipeline stages

1. **Pre Deployment** — Slack notification to `tts-cicd-notify`
2. **Checkout Source Code** — full clone with tags
3. **Update File Environment** — injects `.env` and `.cloudflare-pages.credentials` from Jenkins config file provider
4. **Build and Deploy** — Docker buildx build + wrangler deploy + image cleanup

Pipeline only runs on `develop` or `main` branches (or manual trigger via `BUILD_MANUAL=frontend-docs-tts`).

---

## Key Architectural Notes

- **`future.compatibilityVersion: 4`** is enabled — this moves app source files into the `app/` directory (non-default Nuxt 3 layout). Always place pages, components, layouts under `app/`.
- **Static generation** (`nuxt generate`) is the production build strategy. The site is entirely pre-rendered; there is no server-side runtime in production.
- **Search** is pre-rendered at `/api/search.json` and loaded client-side only (`server: false` in `useLazyFetch`). The search index includes all Markdown files where `navigation !== false`.
- **`UButton` and `UIcon` are global components** — registered in `nuxt.config.ts` hooks so they work inside `.md` MDC blocks without explicit imports.
- **OG images** are generated server-side via `nuxt-og-image` using the `OgImageDocs` component. The `defineOgImageComponent('Docs')` call in `[...slug].vue` activates this.
- **Navigation tree** is fetched once in `app.vue` and provided via Vue's `provide/inject` pattern (`'navigation'` key) to `AppHeader` and the `docs` layout.
- **Renovate** is configured to use `github>nuxt/renovate-config-nuxt` with lock file maintenance enabled.
