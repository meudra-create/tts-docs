---
description: Comprehensive feature development workflow — guides you through discovery, codebase exploration, architecture design, implementation, and quality review in 7 structured phases
---

Implement a new feature using a systematic 7-phase approach that prioritizes deep understanding, clear architecture, and quality code.

**Core principles**: Ask clarifying questions early. Understand before acting. Keep solutions simple and elegant. Wait for explicit user approval before major phase transitions.

## Phase 1 — Discovery

Clarify what needs to be built:
- Restate the feature request in your own words
- Ask targeted questions about the problem, intended functionality, and constraints
- Confirm your understanding with the user before proceeding

## Phase 2 — Codebase Exploration

Launch parallel `code-explorer` agents targeting different aspects:
- Similar features already implemented
- Overall architecture and layer structure
- UI patterns and component conventions
- Data flow and state management patterns

Read the key files identified by the agents to build comprehensive context.

## Phase 3 — Clarifying Questions

*This is one of the most important phases.*

Before designing anything, identify every underspecified aspect:
- Edge cases and error conditions
- Integration points with existing systems
- Scope boundaries (what's in, what's out)
- Performance and accessibility requirements
- Backwards compatibility concerns

Present all questions at once and wait for answers before proceeding.

## Phase 4 — Architecture Design

Launch a `code-architect` agent to design the implementation. Present the agent's output to the user:
- Multiple implementation approaches with trade-offs
- A recommended approach with clear rationale
- Component breakdown with file paths

**Wait for the user to select an approach before proceeding.**

## Phase 5 — Implementation

Only begin after explicit user approval of the architecture.

- Follow existing codebase conventions strictly
- Implement in the order specified by the blueprint
- Update progress using TodoWrite as tasks complete
- Flag any unexpected complexity or deviations immediately

## Phase 6 — Quality Review

Launch parallel `code-reviewer` agents examining:
- Code simplicity and elegance
- Correctness and edge case handling
- Adherence to project conventions

Present findings to the user and address issues per their direction.

## Phase 7 — Summary

Document the completed work:
- What was built and key decisions made
- All files created or modified
- Known limitations or follow-up work
- Suggested next steps
