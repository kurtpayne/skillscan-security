---
name: job-application-agent-suite
description: Build and run a multi-agent workflow for Korean job applications, especially self-introduction essays and cover letters. Use when users ask to analyze a target company/role, extract and map personal experiences, draft application answers, rewrite tone for a specific company, detect AI-like writing patterns, and run final submission checks.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: HyunWoo9930/job-application-agent-suite
# corpus-url: https://github.com/HyunWoo9930/job-application-agent-suite/blob/e183fd87c6118b86673f34fc550c24e3646954a0/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Job Application Agent Suite

## Overview

Use this skill to execute a full writing pipeline for job applications.
Run eleven specialized agents in order so each output becomes the next agent's input.

You can also run any agent independently when the user requests partial work.

## Invocation UX

If user says only "agent를 불러줘" (or equivalent), use progressive intake in this order:

1. Ask only company/role (+ posting link/text if possible) and run company-role analysis first.
2. Ask application question(s) and character limits.
3. Ask candidate experience details last.

Do not ask for candidate experience in step 1.

Use these staged templates:

1) Stage-1 (company/role first)

```json
{
  "company_name": "네이버",
  "role_title": "백엔드 개발자",
  "job_posting_text_or_link": "https://careers.example.com/naver/backend"
}
```

2) Stage-2 (questions after baseline analysis)

```json
{
  "application_questions": [
    {
      "question_id": "Q1",
      "question_text": "지원 동기와 입사 후 기여 방안을 작성해 주세요.",
      "char_limit": 800
    }
  ]
}
```

3) Stage-3 (candidate evidence last)

```json
{
  "candidate_profile": "백엔드 3년차, Java/Spring, 대용량 트래픽 서비스 운영 경험",
  "experience_notes": "결제 API 병목 개선(응답속도 35% 단축), 장애 대응 자동화 경험",
  "forbidden_claims_or_constraints": ["확인되지 않은 수치 사용 금지", "기밀 정보 노출 금지"]
}
```

Optional shortcut when user already has a draft:

4) Existing draft path (`agent-06 -> agent-07`)

```json
{
  "question_text": "지원 동기와 입사 후 기여 방안을 작성해 주세요.",
  "char_limit": 800,
  "final_draft": "저는 사용자 문제를 기술로 해결하는 과정에서 동기를 얻습니다. 이전 회사에서 결제 API 병목을 분석해 응답 시간을 35% 단축한 경험이 있습니다..."
}
```

## Workflow

1. Run the intake-validator agent.
2. Run the analysis baseline in this order:
   - `agent-01a` industry analyst
   - `agent-01b` company analyst
   - `agent-01c` role analyst
   - `agent-01` synthesis analyst
3. Run the corpus-experience recommender agent.
   - must report "what was scanned" and "what will be used" to user
4. Run the experience miner agent.
5. Run the question-experience matcher agent.
6. Run the experience-refiner agent (tail-question/refinement gate).
7. Run the metric-evidence tracker agent.
8. Run the drafting assistant agent.
9. Run the tone-customizer agent.
10. Run the AI-style reviewer and final QA checker.
11. Collect external AI feedback and write it to `external_feedback_notes`.
12. Run the final-packager agent.

## Default Persistence

Persist analysis outputs by default.

Unless the user explicitly says not to save files, save analysis artifacts automatically.

Default save rules:

- company-only analysis:
  - `~/job_runs/<company_slug>/company_analysis.md`
- company + role analysis:
  - `~/job_runs/<company_slug>/<role_slug>/01_company_role_analysis.md`
- industry-only analysis:
  - `~/job_runs/<company_slug>/<role_slug>/01a_industry_analysis.md`
- company-only step inside a multi-step run:
  - `~/job_runs/<company_slug>/<role_slug>/01b_company_analysis.md`
- role-only step inside a multi-step run:
  - `~/job_runs/<company_slug>/<role_slug>/01c_role_analysis.md`

Persistence rules:

- If no run directory exists, create it automatically.
- Save the human-readable markdown result first.
- If the response contains structured lists/tables worth reusing, preserve them in the markdown file rather than dropping them.
- Tell the user where the file was saved.
- Only skip saving if the user explicitly asks for chat-only output.

Language rules for saved artifacts:

- Default saved analysis artifacts should be written in Korean.
- If the user explicitly requests English output, the saved artifact may be written in English.
- For Korean job-application workflows, prefer Korean headings, Korean summaries, and Korean writing hooks by default.

## Company Research Enforcement

When running `agent-01a`, `agent-01b`, `agent-01c`, or `agent-01`, treat the following company-research checks as mandatory, not optional.

Primary reference:

- `references/company-research-checklist.md`
- `references/company-research-checklist.json`

Always load and follow this file before or during company-analysis work.

Required company investigation scope:

- main business and core competitiveness
- industry position and strengths
- latest business focus, new business, and investment direction
- competitor comparison and differentiation
- company culture, work environment, and welfare/support systems

Verification rules (must enforce):

- Check the latest official homepage, careers page, newsroom, and IR/investor materials when available.
- If recent reporting is used, separate verified fact from interpretation.
- Do not state an ambiguous or weakly supported point as fact.
- If something is outdated, unclear, or cannot be confirmed, explicitly say it is not accurate enough to confirm.
- Prefer official and recent sources over generic summaries or stale blog content.
- If a user provides a custom company-research checklist later, merge it with this file instead of silently replacing this baseline.

Company-analysis output expectations:

- clearly distinguish official facts vs `[inference]`
- include evidence sources for current-company claims
- avoid guessed competitor comparisons
- avoid guessed culture/welfare claims
- surface missing verification gaps to the user instead of filling them with confident language

Gate rules (must enforce):

- User approval is required after each step (`manual_per_step`).
- If `agent-02a.ready_for_agent_02` is `false`, do not run `agent-02`.
- If `external_feedback_required=true` and `external_feedback_notes` is empty, do not run `agent-07`.

## Single-Question Flow (Recommended)

When the user writes one question at a time, use this order:

1. Run baseline analysis in this order:
   - `agent-01a` for industry understanding
   - `agent-01b` for company understanding
   - `agent-01c` for role understanding
   - `agent-01` once to synthesize reusable hooks
2. Run `agent-02a` to mine reusable experiences from local corpus first.
3. Run `agent-02` in question-first mode:
   - include `question_text`
   - ask clarifying questions first if evidence is missing
   - then output focused evidence cards
4. Run `agent-03` question-intent match.
5. Run `agent-03b` refinement gate:
   - if weak match or low detail, ask tail questions and refine cards
   - if strong match, pass through to drafting
6. Run `agent-03c` metric-evidence tracker:
   - verify numeric claims and block unsupported metrics
7. Run `agent-04` draft (ambition questions use SMART 1/3/5-year block).
8. Run `agent-05` tone adjust.
9. Run `agent-06` final QA + blind/compliance check.
10. Collect external AI feedback and update `external_feedback_notes`.
11. Run `agent-07` final packaging.

Execution control:

- Always move step-by-step with user confirmation.
- Do not auto-chain multiple agents in one go unless the user explicitly requests batch mode.
- During company analysis, do not skip the verification step even if the user asks for a quick summary; instead, keep the summary short but preserve the required checks.

## Length Guardrail

For every question with character limit `N`, target range is:

- Minimum: `N - 20`
- Maximum: `N`

If a draft is below `N - 20`, expand with evidence detail.
If a draft is above `N`, compress while preserving key evidence.

Recommended budget per question:

- `recommended_char_budget = max(N - 20, round(N * 0.9))`
- keep final hard validation in `N - 20 .. N`

## Run Individually

If the user asks for only one step, run only that agent and skip others.

- `agent-01a` or `industry analyst`: analyze industry only
- `agent-01b` or `company analyst`: analyze company only
- `agent-01c` or `role analyst`: analyze role only
- `agent-01` or `company-role analyst`: synthesize industry/company/role outputs into one baseline
- `agent-00` or `intake validator`: validate required inputs only
- `agent-02a` or `corpus experience recommender`: recommend experiences from local essay folder first
- `agent-02` or `experience miner`: extract evidence cards only
- `agent-03` or `question matcher`: map questions to experiences only
- `agent-03b` or `experience refiner`: refine weak matches and ask tail questions
- `agent-03c` or `metric evidence tracker`: validate metric claims and usage rules
- `agent-04` or `drafting assistant`: draft answers only
- `agent-05` or `tone customizer`: rewrite tone only
- `agent-06` or `ai-style reviewer`: feedback and AI-like pattern review only
- `agent-07` or `final packager`: package final submission output only

User utterances that should trigger single-agent mode:

- "agent-06만 돌려줘"
- "피드백만 해줘"
- "회사 분석만 해줘"
- "초안만 써줘"
- "문항 하나만 기준으로 경험 채굴해줘"
- "매칭 약한 경험 꼬리질문 해줘"

CLI examples for single-agent usage:

```bash
python3 scripts/use_agent.py --agent agent-01
python3 scripts/use_agent.py --agent agent-01a
python3 scripts/use_agent.py --agent agent-01b
python3 scripts/use_agent.py --agent agent-01c
python3 scripts/use_agent.py --agent agent-02a
python3 scripts/use_agent.py --agent agent-03b
python3 scripts/use_agent.py --agent agent-03c
python3 scripts/use_agent.py --agent agent-04
python3 scripts/use_agent.py --agent agent-06
python3 scripts/use_agent.py --agent agent-07
```

## Agent Prompts

Load only the prompt file needed for the current step:

- Intake validation: `references/agent-00-intake-validator.md`
- Company and role analysis: `references/agent-01-company-role-analyst.md`
- Industry analysis: `references/agent-01a-industry-analyst.md`
- Company analysis: `references/agent-01b-company-analyst.md`
- Role analysis: `references/agent-01c-role-analyst.md`
- Corpus experience recommendation: `references/agent-02a-corpus-experience-recommender.md`
- Experience mining: `references/agent-02-experience-miner.md`
- Question matching: `references/agent-03-question-experience-matcher.md`
- Experience refinement: `references/agent-03b-experience-refiner.md`
- Metric evidence tracking: `references/agent-03c-metric-evidence-tracker.md`
- Drafting: `references/agent-04-drafting-assistant.md`
- Tone customization: `references/agent-05-tone-customizer.md`
- AI-style and final QA: `references/agent-06-ai-style-and-qa-reviewer.md`
- Final packaging: `references/agent-07-final-packager.md`

For company-analysis steps, also consult:

- `references/company-research-checklist.md`
- `references/company-research-checklist.json`

For AI-like writing review, also consult:

- `references/ai-likeness-forensic-checklist.md`

## Required Inputs

Collect and normalize these inputs before drafting:

- Company name and role title
- Job posting text or link
- Application questions with character limits
- Candidate raw experience notes (projects, internship, activities, awards)
- Any forbidden claims or compliance constraints
- Local essay corpus path (default: `~/Desktop/취업/자기소개서`)

## Output Contract

Always return these artifacts:

1. Role keyword map (required competencies, preferred competencies, risk flags)
2. Talent profile mapping (official/inferred + evidence gap)
3. Question-to-experience mapping table
4. Draft answers with character counts
5. AI-style risk report with line-level rewrite suggestions
6. Final checklist (length, repetition, unsupported claims, tone consistency)

For company-analysis outputs specifically, also preserve:

1. what was verified from official/recent sources
2. what remains inferred
3. what could not be confirmed accurately

`agent-01` synthesis should also preserve:

1. `industry_analysis_summary`
2. `company_analysis_summary`
3. `role_analysis_summary`
4. `motivation_hooks`
5. `future_contribution_hooks`
6. `job_fit_hooks`

Structured chaining fields (recommended):

- For table/list rows, include stable `id`
- Include `confidence` where judgment is involved
- Include `evidence_source` for factual claims

Length checklist rule:

- Must satisfy `char_limit - 20 <= character_count <= char_limit`

## AI-Style Check Script

Run `scripts/ai_style_checker.py` on a draft when users ask for AI-like tone detection.

Example:

```bash
python3 scripts/ai_style_checker.py --file draft.txt
```

Or:

```bash
cat draft.txt | python3 scripts/ai_style_checker.py
```

Use the script output as a signal only.
Confirm suspicious lines with semantic review before final feedback.

Checker output includes `line_no`-based flags for deterministic rewrites.

## Character Window Check Script

Validate the strict length window:

```bash
python3 scripts/char_window_check.py --file draft.txt --char-limit 800
```

Count-mode options for portal alignment:

```bash
python3 scripts/char_window_check.py --file draft.txt --char-limit 800 --count-mode no-newline
python3 scripts/char_window_check.py --file draft.txt --char-limit 800 --count-mode no-space
```

Modes:

- `raw`: 그대로 카운트
- `no-newline`: 줄바꿈 제외
- `no-space`: 공백/줄바꿈 제외

## Pipeline Orchestration Script

Validate chained inputs and identify the next runnable agent:

```bash
python3 scripts/orchestrate_pipeline.py --run-dir ~/job_runs/<company_role>/Q1
```

Write the next agent input payload:

```bash
python3 scripts/orchestrate_pipeline.py --run-dir ~/job_runs/<company_role>/Q1 --write-next-input next_input.json
```

Initialize per-question run directory with required artifacts:

```bash
python3 scripts/orchestrate_pipeline.py --run-dir ~/job_runs/<company_role>/Q1 --init-run-dir --input templates/pipeline-state.sample.json
```

Set custom corpus folder:

```bash
python3 scripts/orchestrate_pipeline.py --input state.json --essay-corpus-path ~/Desktop/취업/자기소개서 --write-next-input next_input.json
```

By default, orchestrator tries to load cached `agent-01` output from:

- `~/Desktop/회사 직무 분석/<company>__<role>/agent-01-latest.json`

If the combined file is missing but all sub-analysis files exist, orchestrator can synthesize `agent-01` from:

- `agent-01a-industry-latest.json`
- `agent-01b-company-latest.json`
- `agent-01c-role-latest.json`

Disable this behavior:

```bash
python3 scripts/orchestrate_pipeline.py --input state.json --no-cache-load
```

## Local Cache Script

Persist analysis outputs to local desktop folder and reuse them later.

Save current `agent_outputs`:

```bash
python3 scripts/persist_analysis_cache.py --input state.json --mode save
```

Load cached `agent-01` into state:

```bash
python3 scripts/persist_analysis_cache.py --input state.json --mode load-agent01 --write-output state.with_cache.json
```

Default cache path:

- `~/Desktop/회사 직무 분석/<company>__<role>/`

Saved analysis files:

- `agent-01a-industry-latest.json`
- `agent-01b-company-latest.json`
- `agent-01c-role-latest.json`
- `agent-01-latest.json`
- `industry-analysis-latest.md`
- `company-analysis-latest.md`
- `role-analysis-latest.md`
- `combined-analysis-latest.md`

Writing linkage defaults:

- 지원동기: `industry_analysis_summary` + `company_analysis_summary` + `motivation_hooks`
- 입사 후 포부: 산업 트렌드 + 회사 방향성 + `future_contribution_hooks`
- 직무 역량: `role_analysis_summary` + `job_fit_hooks` + candidate evidence

## Prompt Extraction Script

Run `scripts/use_agent.py` to print a single agent prompt template.

Examples:

```bash
python3 scripts/use_agent.py --agent agent-06
```

```bash
python3 scripts/use_agent.py --agent drafting
```

```bash
python3 scripts/use_agent.py --agent agent-04 --input vars.json
```

```bash
python3 scripts/use_agent.py --agent agent-02a --input vars.json
```

## Corpus Scan Script

Extract reusable experience candidates from local self-introduction files:

```bash
python3 scripts/scan_experience_corpus.py --path ~/Desktop/취업/자기소개서 --write-output corpus_candidates.json
```

Supported formats by default:

- `.docx`, `.txt`, `.md`, `.markdown`, `.rst`
- `.pdf`/`.hwp` are not parsed by this script.

Merge scanned candidates into pipeline state:

```bash
python3 scripts/scan_experience_corpus.py --path ~/Desktop/취업/자기소개서 --state-input state.json --write-state state.with_corpus.json
```