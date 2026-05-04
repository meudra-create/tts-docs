# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A static documentation site for the TTSOpenAI API, built with Nuxt 3 + @nuxt/ui-pro + @nuxt/content. The site documents the Text-to-Speech REST API (hosted at `api.ttsopenai.com`). The output is a fully pre-rendered static site deployed via Docker/Ansible.

## Commands

```bash
pnpm install        # install deps (shamefully-hoist=true via .npmrc)
pnpm dev            # dev server with hot reload
pnpm generate       # static site generation (production build)
pnpm build          # SSR build (not used for deployment)
pnpm preview        # preview the generated output
pnpm lint           # ESLint
pnpm typecheck      # vue-tsc type checking
```

> The package manager is **pnpm** (v9.12.2). Do not use npm or yarn.

## Architecture

### Nuxt 4 Compatibility Mode

`nuxt.config.ts` sets `future.compatibilityVersion: 4`, which moves the app source into `app/` instead of the root. All Vue components, pages, and layouts live under `app/`.

### Content → Pages Mapping

`@nuxt/content` drives all documentation. Files under `content/` map directly to routes:

- `content/index.yml` — landing page data (hero, features grid), consumed by `app/pages/index.vue`
- `content/1.getting-started/*.md` → `/getting-started/*`
- `content/2.resources/*.md` → `/resources/*`

**Ordering**: Numeric prefixes on both directories and files (`1.getting-started/2.authentication.md`) control the sidebar navigation order. These prefixes are stripped from the URL.

**Directory titles**: Each section folder has a `_dir.yml` with a `title` field that becomes the sidebar section label.

### Search

`/api/search.json` is a pre-rendered Nitro server route (`server/api/search.json.get.ts`) that returns all markdown content for the client-side full-text search (`UContentSearch`).

### App Config vs Nuxt Config

- `nuxt.config.ts` — module registration, nitro prerender, ESLint stylistic rules, route rules
- `app/app.config.ts` — runtime UI config: site name, header links, footer links, TOC settings (including the "Edit this page" GitHub URL pointing to the `develop` branch)
- `nuxt.schema.ts` — Nuxt Studio schema for the app config fields (allows visual editing)

### Styling

Tailwind with a custom green palette (teal-green tones replacing the default green) and DM Sans as the primary font. Colors and font are configured in `tailwind.config.ts`. The UI primary color is `green` and gray scale is `slate`.

### OG Images

`nuxt-og-image` is used with a custom component at `app/components/OgImage/OgImageDocs.vue`. The `[...slug].vue` page calls `defineOgImageComponent('Docs')` to apply it per-page.

## Content Authoring Conventions

### Frontmatter

Every `.md` file needs at minimum:
```yaml
---
title: Page Title
description: Short description shown in metadata and page header.
---
```

### MDC Components in Markdown

`@nuxt/ui` components `UButton` and `UIcon` are registered globally (see `nuxt.config.ts` hooks) so they can be used directly in `.md` files:

```md
::u-button
---
icon: 'i-heroicons-arrow-right'
label: Click me
to: https://example.com
target: _blank
---
::
```

Callout boxes:
```md
::callout
---
icon: i-heroicons-light-bulb
---
Your callout text here.
::
```

Code groups (multiple tabs):
```md
::code-group
```bash [terminal]
...
```

```ts [py]
...
```
::
```

### Request Attribute Styling Pattern

API parameter docs use inline HTML for the type label (copy this pattern for consistency):

```md
`param_name` [string]{style="color: rgb(var(--color-gray-400) / var(--tw-text-opacity, 1)); font-weight: 300;"}

Description of the parameter.
```

## ESLint Rules

ESLint is configured via `@nuxt/eslint` with stylistic rules:
- **No trailing commas** (`commaDangle: 'never'`)
- **1tbs brace style** (`braceStyle: '1tbs'`)

Run `pnpm lint` before committing.

## Deployment

Production deploys use `pnpm run generate` (static export). The Dockerfile builds the static output and the Ansible playbook in `deployment/` handles server provisioning. The develop branch is the integration branch; `main` is production.
