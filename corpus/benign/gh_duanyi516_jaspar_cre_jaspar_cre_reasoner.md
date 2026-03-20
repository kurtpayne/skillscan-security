---
name: jaspar-cre-reasoner
description: >
  Known-motif cis-regulatory element (CRE) reasoning skill. Activated when a
  user provides a DNA enhancer sequence (≤300 bp) or pre-computed JASPAR motif
  hits and asks about regulatory potential, predicted expression level, or
  mechanistic explanation in K562, HepG2, or SK-N-SH cells. Does NOT perform
  de novo motif discovery, whole-genome annotation, or clinical diagnosis.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: DuanYi516/jaspar-cre-reasoner
# corpus-url: https://github.com/DuanYi516/jaspar-cre-reasoner/blob/0e6d773850287feede2252de9bd5ebbd30eb8db1/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

## When to activate

- User supplies a short DNA sequence and asks about enhancer activity or
  expression level for a supported cell type.
- User supplies a motif-hit table (lite mode) and wants a structured
  regulatory analysis.
- User asks to compare two CRE sequences for relative activity.
- User asks *why* a CRE is active or inactive and wants an interpretable,
  evidence-grounded explanation.

## Non-goals

- De novo motif discovery or novel TF binding-site prediction.
- Chromosome-scale or whole-genome regulatory annotation.
- Promoter, silencer, or insulator analysis (enhancers only unless user
  explicitly adapts).
- Generating or fabricating motif evidence — all motif data comes from
  deterministic FIMO scanning against JASPAR PWMs.

## Mode selection

Determine the operating mode from the user's input:

**Full mode** — user provides raw DNA sequence(s).
Run scripts in order:

1. `scripts/fetch_jaspar.py --use-bundled` (skip if matrices already prepared).
2. `scripts/run_fimo_scan.py` with the user's sequence(s) and the prepared
   MEME file. Accepts CSV, FASTA, or a single `--sequence` string.
3. `scripts/build_rcc.py` on the FIMO output to produce the Regulatory
   Context Card (RCC).

**Lite mode** — user provides pre-computed motif hits (see
`references/input_examples.md` for the expected format).
Run only:

1. `scripts/build_rcc.py --lite` on the user-provided motif hits.

After either mode, use the `rcc_prompt` field from the RCC JSON as the
context for reasoning.

## Reference files to read

Before reasoning, load the relevant context from these files:

| File | Purpose | When to read |
|------|---------|--------------|
| `references/biology_priors.md` | Cell-type driver TFs, cooperative grammar rules, chromatin context, expression scale | Always — before producing any reasoning |
| `references/output_schema.md` | RCC field definitions, prompt format, reasoning output contract, validation checks | When formatting output or when user asks about schema |
| `references/input_examples.md` | Concrete input/output pairs for full and lite modes | When user needs format guidance or for self-reference |

## Evidence discipline

These rules are non-negotiable:

1. **Never invent motif hits.** Every motif cited in reasoning must come from
   the RCC's `motif_evidence` array, which was produced by deterministic
   FIMO scanning. Do not hallucinate TF names, scores, or positions.
2. **Never fabricate grammar tags.** Synergy candidates, clusters, composite
   elements, and driver coverage are computed by `scripts/build_rcc.py`.
   Cite them from the RCC's `grammar_tags`; do not infer new ones.
3. **Every reasoning claim must reference at least one RCC field** — a motif
   name, a score, a position, GC content, a grammar tag, or a family name.
   Unsupported speculation is not allowed.
4. **Deduplication is done in preprocessing.** If two same-family motifs
   overlap, only the highest-scoring hit survives into the RCC. Do not
   re-deduplicate or second-guess the motif table.

## Reasoning protocol

Using the `rcc_prompt` from the assembled RCC, produce a mechanistic analysis
that covers these aspects in a logical order:

1. **Chromatin accessibility** — interpret GC content and CpG O/E ratio.
2. **Driver motif identification** — name the top motifs, their scores,
   positions, and families.
3. **TF family coordination** — assess family co-occurrence and driver
   coverage for the target cell type.
4. **Motif grammar** — evaluate spacing, clustering, synergy candidates,
   and composite elements from the grammar tags.
5. **Evidence integration** — weigh positive and negative signals.
6. **Expression-level determination** — conclude with a level on the 0–3
   scale (defined in `references/biology_priors.md`).

The number of steps, their granularity, and the output format are flexible.
Use whatever structure best fits the user's question:

- For **training-data generation**, use `scripts/format_reasoning_output.py
  --mode convert` to produce the `<think>Step 1:…</think> ### Conclusion`
  format. This is the format expected by the R³LM training pipeline.
- For **interactive user-facing answers**, a clear numbered analysis with a
  final expression-level call is sufficient — `<think>` tags are not required.
- For **pairwise comparisons**, reason about each sequence separately, then
  compare.

## Output contract

Regardless of format, every reasoning output must include:

1. A discrete expression level: `0` (Inactive), `1` (Low), `2` (Moderate),
   or `3` (Highly Active).
2. A brief mechanistic summary tying the level to specific RCC evidence.
3. At least 50% of the RCC motif names cited somewhere in the reasoning
   (the `motif_coverage` check in `scripts/format_reasoning_output.py`
   enforces this for the training format).

## Script reference

| Script | Purpose | Key flags |
|--------|---------|-----------|
| `scripts/fetch_jaspar.py` | Prepare JASPAR MEME/TRANSFAC files | `--use-bundled`, `--meme-file`, `--transfac-file`, `--selfcheck` |
| `scripts/run_fimo_scan.py` | FIMO motif scanning + filtering + dedup | `--sequences-file`, `--sequence`, `--meme-file`, `--pvalue-threshold` |
| `scripts/build_rcc.py` | RCC assembly (stats + grammar + prompt) | `--motif-hits-file`, `--lite`, `--cell-type` |
| `scripts/format_reasoning_output.py` | Convert JSON→`<think>` or validate `<think>` text | `--mode convert\|validate`, `--reasoning-json`, `--reasoning-text` |

All scripts support `--help` and `--selfcheck`.