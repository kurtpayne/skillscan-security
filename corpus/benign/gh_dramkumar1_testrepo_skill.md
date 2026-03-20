---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: dramkumar1/testRepo
# corpus-url: https://github.com/dramkumar1/testRepo/blob/8698853e15fd5bf230ca27fac314f94cbbf277b0/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Skill: Structured Problem Decomposition

## Overview
This skill enables the model to take a complex, ambiguous, or multi-step problem and break it down into clear, logically ordered subproblems that are easier to solve. The focus is on clarity, correctness, and actionability rather than verbosity.

This skill is especially useful for:
- Technical troubleshooting
- Planning and strategy
- Complex user requests with multiple constraints
- Analytical or reasoning-heavy tasks

---

## Skill Goals
- Convert vague or high-level problems into concrete steps
- Identify dependencies between sub-tasks
- Surface assumptions and missing information
- Reduce cognitive load for the user

---

## When to Use
Use this skill when:
- A task cannot be solved in a single step
- The user’s request contains multiple goals or constraints
- The problem benefits from sequencing or prioritization
- Clarification or scoping is required before execution

Do **not** use this skill when:
- The task is trivial or purely factual
- The user explicitly asks for a short or direct answer only
- The problem is already well-structured

---

## Inputs
- A user query describing a problem, task, or goal
- Optional context, constraints, or preferences from the user

Example input:
> “I want to migrate our backend to the cloud without downtime and reduce costs.”

---

## Outputs
A structured breakdown of the problem, typically including:
1. Problem restatement (optional)
2. High-level phases or steps
3. Sub-tasks within each phase
4. Assumptions or open questions
5. Suggested next actions

Example output (excerpt):
- Phase 1: Assess current architecture  
- Phase 2: Identify cloud migration strategy  
- Phase 3: Plan zero-downtime rollout  
- Phase 4: Cost optimization and monitoring  

---

## Behavioral Guidelines
- Be concise but complete
- Prefer numbered or bulleted lists
- Avoid solving sub-tasks unless explicitly requested
- Clearly label assumptions
- Ask clarifying questions only when necessary

---

## Safety & Alignment Considerations
- Do not fabricate unknown constraints or requirements
- Avoid giving legal, medical, or financial advice unless explicitly allowed and properly scoped
- If the problem involves sensitive or high-risk domains, surface uncertainty clearly

---

## Quality Criteria
A good application of this skill:
- Produces a decomposition that is logically sound
- Makes the problem easier to act on
- Matches the user’s level of technical sophistication
- Does not introduce unnecessary complexity

A poor application of this skill:
- Over-explains obvious steps
- Misses key dependencies
- Solves the problem instead of structuring it
- Adds speculative or incorrect assumptions

---

## Evaluation Signals
- User proceeds step-by-step instead of asking for clarification
- User references specific sub-steps in follow-up questions
- Reduced back-and-forth due to clearer structure

---

## Related Skills
- Clarifying Questions
- Step-by-Step Reasoning
- Planning & Prioritization
- Constraint Identification

---

## Versioning
- Skill Version: 1.0
- Last Updated: 2026-02-03
- Owner: AI Platform Team