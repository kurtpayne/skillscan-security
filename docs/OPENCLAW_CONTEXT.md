# OpenClaw Incident Context (Design Input)

This repository includes safe fixtures inspired by reported OpenClaw/ClawHub attack patterns observed in early 2026.

Patterns reflected in fixtures and rules:

1. Download-and-execute bootstrap chains (`curl|bash`, `wget|sh`).
2. IOC reuse involving suspicious IP/domain infrastructure.
3. Coercive prerequisite instructions that ask users to weaken host defenses.
4. Obfuscated staged payload workflows.

SkillScan fixtures intentionally use non-live and sanitized examples where possible to avoid distributing active malware.

The built-in IOC database (`src/skillscan/data/intel/ioc_db.json`) includes seeds from public incident reporting, including IPs and URLs originally associated with OpenClaw campaigns. These are used for scanner behavior testing and can be extended via local intel sources or the automated intel-update workflow.
