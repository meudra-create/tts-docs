# Self-improvement loop

This repo has [`self-improving-agent`](https://github.com/BerriAI/self-improving-agent)
(BerriAI, MIT) wired in as a devDependency. It gives an AI agent two tools —
`write_improvement_proposal` and `apply_proposal` — so it can suggest a
minimal diff against this repo and, only after a human explicitly approves,
open a draft PR with that diff. It does not touch this project's own
build/content and isn't loaded by the Nuxt app; it's a standalone script you
run on demand.

## Setup

1. Copy `.env.example` to `.env` and fill in:
   - `SELF_IMPROVING_AGENT_REPO` — `owner/name` of the repo the agent may PR against (defaults to this repo).
   - `SELF_IMPROVING_AGENT_GITHUB_TOKEN` — a [fine-grained PAT](https://github.com/settings/tokens?type=beta)
     scoped to that one repo, with **Contents: Read & write** and
     **Pull requests: Read & write** only. Never commit this token.
2. `pnpm self-improve "<feedback about this docs site>"`

The vendored package lives at `vendor/self-improving-agent-0.5.0.tgz`,
built from the upstream repo at commit `0da0a209` and referenced via a
`file:` dependency in `package.json` — it isn't published to npm yet.

## Safety model

`apply_proposal` pushes a branch and opens a PR, so four layers guard it:

1. **Tool description** — the model is only told to call `apply_proposal` after explicit approval in the user's most recent message.
2. **Schema gate** — the tool requires `userConfirmedInThisMessage: true`; it throws if that's false.
3. **`onBeforeApply` hook** — available if you need custom rejection logic (rate limits, allowlists); not used here by default.
4. **Token scope** — the PAT is pinned to one repo with only `contents:write` + `pull_requests:write`, capping the blast radius.

`apply_proposal` also refuses to run if the target file is missing or if
`originalSnippet` doesn't match exactly once in the current file.
