---
name: gitcli
description: "Local git timeline CLI. Query commit history across 50+ repositories. Use when user asks about coding activity, what they worked on, commit history, project timeline, or 'what did I do on [date]'."
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: junghan0611/gitcli
# corpus-url: https://github.com/junghan0611/gitcli/blob/3304640660f18ea24cf39de582ac4d601df33a70/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# gitcli v0.2.0 — Local Git Timeline CLI

Query commit history across all local git repositories (~/repos/gh, ~/repos/work).

Binary is bundled in the skill directory. Invoke via `{baseDir}/gitcli`.

All output is JSON.

## When to Use

- "어제 뭐 코딩했지?" → `gitcli day --days-ago 1 --me --summary`
- "pi-mono 최근 커밋" → `gitcli log pi-mono --days 7`
- "이번 달 활동량" → `gitcli timeline --month 2026-02 --me`
- "리포 몇 개야?" → `gitcli repos`
- 특정 날짜 활동 → `gitcli day 2025-10-10 --me --summary`
- "회사 작업 정리" → `gitcli timeline --month 2026-02 --me --repos ~/repos/work`
- "연봉협상 자료" → `gitcli timeline --days 90 --me --repos ~/repos/work`

## Commands

### day — 특정 날짜의 모든 커밋

```bash
gitcli day                              # 오늘
gitcli day 2025-10-10 --me --summary    # 개요 (토큰 절약, 기본 추천)
gitcli day 2025-10-10 --me              # 상세 (커밋 메시지/diff 통계 포함)
gitcli day 20251010                     # Denote ID 호환
gitcli day --years-ago 1 --me           # 1년 전 오늘
gitcli day --days-ago 7 --me            # 7일 전
gitcli day --repos ~/repos/gh --me      # 특정 디렉토리만
gitcli day --me --tz +09:00             # UTC 서버에서 KST 기준 조회
gitcli day --me --max 10                # 상세 모드에서 최대 10커밋만
```

**`--summary` 출력** (~500B, 96% 절감):
```json
{"date":"2026-02-22","total_commits":45,"repos_summary":[{"name":"denotecli","commits":16},{"name":"pi-skills","commits":4}],"summary":{"active_repos":6,"first_commit":"16:39","last_commit":"20:18","active_hours":3.65}}
```

**기본 출력** (~13KB): 커밋별 hash, time, message, files_changed, insertions, deletions 포함.

### repos — 리포 목록과 통계

```bash
gitcli repos                        # 기본 (~/repos/gh + ~/repos/work)
gitcli repos --repos ~/repos/gh    # 개인만
```

### log — 특정 리포 커밋 로그

```bash
gitcli log pi-mono --days 7
gitcli log pi-mono --from 2025-10-01 --to 2025-10-31
gitcli log pi-mono --author junghan
```

### timeline — 기간별 활동 개요

```bash
gitcli timeline --days 30 --me
gitcli timeline --month 2025-10 --me
```

Output: period, total_commits, active_days, daily[].{date, commits, repos[], hours}

## Important Notes

- **`--me --summary` 기본 사용**: 토큰 절약 + 포크/AI 커밋 필터링
- **`--tz +09:00`**: UTC 서버에서 KST 날짜 경계 정확히 계산. 새벽 커밋 오분류 방지
- **기본 경로**: `~/repos/gh,~/repos/work` (둘 다 스캔)
- **경로 분리**: 개인(`--repos ~/repos/gh`), 회사(`--repos ~/repos/work`)
- **repos는 항상 `[]`**: 커밋 없는 날도 null 아닌 빈 배열 반환
- **authors 없으면 경고**: `~/.config/gitcli/authors` 미존재 시 stderr 경고 출력

## Author Config (~/.config/gitcli/authors)

```
# 한 줄에 하나, 대소문자 무관 부분 일치
junghan     # 개인: junghan, junghan0611, Jung Han, junghanacs
jhkim2      # 회사: Junghan Kim <jhkim2@goqual.com>
```

## Repo Groups

| 경로 | 성격 | 리포 수 | 기간 |
|------|------|---------|------|
| `~/repos/gh` | 개인 GitHub | ~30 | 2011~ |
| `~/repos/work` | 회사 GitHub | ~18 | 2025~ |