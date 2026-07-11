#!/usr/bin/env node
// Runs a one-off self-improvement session against this repo using
// self-improving-agent (https://github.com/BerriAI/self-improving-agent).
//
// The agent may call `write_improvement_proposal` to suggest a minimal diff.
// It only opens a draft PR (`apply_proposal`) after you explicitly approve
// in a follow-up reply — nothing is pushed without that approval. See
// SELF_IMPROVEMENT.md for setup and the safety model.
//
// Usage:
//   pnpm self-improve "the getting-started page is missing a curl example"
import { query } from "@anthropic-ai/claude-agent-sdk";
import { feedbackMcp } from "self-improving-agent/claude";

const feedback = process.argv.slice(2).join(" ");
if (!feedback) {
  console.error('Usage: pnpm self-improve "<feedback about this docs site>"');
  process.exit(1);
}

const fb = feedbackMcp();

for await (const message of query({
  prompt: feedback,
  options: {
    mcpServers: fb.mcpServers,
    allowedTools: fb.allowedTools,
  },
})) {
  if (message.type === "assistant") {
    for (const block of message.message.content) {
      if (block.type === "text") process.stdout.write(block.text);
    }
  }
}
process.stdout.write("\n");
