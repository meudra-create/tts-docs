# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Public API documentation site for the TTS OpenAI (Text-to-Speech) API, at `docs-dev.ttsopenai.com` (dev) / production equivalent. Built with **Nuxt 3** + **Nuxt Content v2** + **`@nuxt/ui-pro`** (the Nuxt UI Pro docs template). The actual product/API lives in other repos — this repo is docs only.

## Commands

Package manager is **pnpm** (`packageManager: pnpm@9.12.2`, `.npmrc` has `shamefully-hoist=true`).

```bash
pnpm install       # install deps (also runs `nuxt prepare` via postinstall)
pnpm dev           # start dev server
pnpm build         # production build (SSR)
pnpm generate      # static site generation — this is what CI/deploy uses
pnpm preview       # preview a generated/built output locally
pnpm lint          # eslint .
pnpm typecheck     # nuxt typecheck (vue-tsc)
```

There is no test suite in this repo (no `test` script, no test framework installed) — don't invent one. Verify changes with `pnpm lint`, `pnpm typecheck`, and `pnpm dev`/`pnpm generate`.

## Architecture

This is a **content-driven** site: nearly all "content" work is editing Markdown files under `content/`, not Vue/TS code. The Vue layer under `app/` is thin and mostly fixed.

### Content structure (`content/`)

- Files/folders are numeric-prefixed (`1.getting-started/`, `2.index.md`, ...) — the prefix controls sidebar/nav ordering via Nuxt Content and is stripped from the URL (e.g. `content/1.getting-started/2.authentication.md` → `/getting-started/authentication`).
- Each directory has a `_dir.yml` with a `title:` used for the nav group label.
- `content/index.yml` drives the homepage hero/features (not Markdown — a YAML "page" consumed by `pages/index.vue`).
- Every doc page needs `title` and `description` frontmatter (used for `<title>`, OG/SEO meta, and nav/TOC).
- Docs use Nuxt Content's MDC component syntax for rich elements, e.g. `::callout`, `::code-group`, `::u-button` (see existing pages for patterns). Multi-language request examples typically use `::code-group` with one fenced block per language.
- Field-style attribute docs use the recurring inline-style pattern: `` `field_name` [type]{style="color: rgb(var(--color-gray-400) / var(--tw-text-opacity, 1)); font-weight: 300;"} `` followed by a description paragraph — copy this pattern for new request/response attribute docs rather than inventing a new format.
- Setting `navigation: false` in frontmatter (as `content/index.yml` does) excludes a page from the sidebar/search/surround-links.

### App shell (`app/`)

- `app/app.vue` — root: header/footer, injects `navigation` (from `fetchContentNavigation()`) and `files` (from `/api/search.json`) for the command palette search (`UContentSearch`).
- `app/layouts/docs.vue` — the docs layout: left `UAside` nav tree (built from injected `navigation` via `mapContentNavigation`) + page slot.
- `app/pages/[...slug].vue` — catch-all page that resolves a content doc by route via `queryContent(route.path).findOne()`, 404s if missing, and renders it with `ContentRenderer`, plus prev/next (`findSurround`) and right-side TOC.
- `app/pages/index.vue` — renders the homepage from `content/index.yml`.
- `app/app.config.ts` — non-content-editable site config: theme colors, header/footer links, TOC "Community" links, GitHub edit-link base (`toc.bottom.edit`) used to build each page's "Edit this page" link from `page._file`.
- `server/api/search.json.get.ts` — serves all markdown content (minus `navigation: false` pages) for client-side search indexing.

### Global component registration

`nuxt.config.ts` has a `components:extend` hook that makes `UButton` and `UIcon` global so they can be used directly inside `.md` content without explicit imports. If a new `.md` file needs another Nuxt UI component available unqualified in Markdown, register it there rather than importing per-page.

## Deployment

- CI/CD is Jenkins (`Jenkinsfile`), triggered on `develop` (→ dev env) and `main` (→ prod env) branches. Pipeline builds via Docker (`Dockerfile`, target `build`, runs `pnpm run generate`) then ships the static `.output` artifact; Ansible playbooks under `deployment/` handle the actual deploy step per environment (`deployment/group_vars/{dev,prod}.yml`).
- `Dockerfile` generates a static build with `pnpm run generate` — this is a statically generated site (`nitro.prerender` in `nuxt.config.ts` prerenders `/` and crawls links; `/api/search.json` is also prerendered).
