---
name: foreign-news-collector
description: RSS 최적화 10개 매체에서 뉴스를 수집하고, RSS + 홈페이지 TOP + 랭킹 섹션 3중 신호 기반 Value Score로 중요 기사를 선별하는 스킬. 사용 시점 - 외신 브리핑 요청, 주요 뉴스 수집 요청, AI/기술/경제/국제정세 뉴스 요청 시
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: hong4137/briefing
# corpus-url: https://github.com/hong4137/briefing/blob/cf3d8a203a32f044c3d7aa0c85f7025ecde16660/foreign-news-collector-v5-SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Foreign News Collector v5 (외신 뉴스 수집기)

RSS 지원이 확실한 10개 매체에서 뉴스를 수집하고, **3중 신호 시스템**(RSS + 홈페이지 TOP + 랭킹 섹션)으로 중요 기사를 선별한다.

## v5 핵심 변경

- **매체 교체**: RSS 불안정 매체(WSJ, Economist, Nikkei, CNBC, MIT Tech Review) → RSS 안정 매체로 교체
- **3중 신호 시스템**: RSS 수집 + 홈페이지 TOP + 랭킹 섹션 크로스 체크
- **수집 안정성**: RSS 파싱 중심으로 웹 검색 의존도 최소화

---

## 대상 매체 (10개)

### AI/Tech 전문 (5개)

| 매체 | RSS URL | 랭킹 섹션 |
|------|---------|----------|
| TechCrunch | `https://techcrunch.com/feed/` | Most Popular ✅ |
| The Verge | `https://www.theverge.com/rss/index.xml` | Most Popular + Most Discussed ✅ |
| Ars Technica | `https://feeds.arstechnica.com/arstechnica/technology-lab` | Most Read ✅ |
| Wired | `https://www.wired.com/feed/rss` | Trending Stories ✅ |
| VentureBeat | `https://feeds.feedburner.com/venturebeat/SZYF` | ❌ |

### 경제/비즈니스 (3개)

| 매체 | RSS URL | 랭킹 섹션 |
|------|---------|----------|
| Reuters Tech | `https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best&best-sectors=tech` | ❌ |
| BBC Tech | `https://feeds.bbci.co.uk/news/technology/rss.xml` | ❌ |
| The Guardian Tech | `https://www.theguardian.com/uk/technology/rss` | Most Viewed ✅ |

### 아시아/글로벌 (2개)

| 매체 | RSS URL | 랭킹 섹션 |
|------|---------|----------|
| SCMP Tech | `https://www.scmp.com/rss/318208/feed` | ❌ |
| Rest of World | `https://restofworld.org/feed/` | ❌ |

---

## 핵심 개념: 3중 신호 Value Score

단순 최신순이 아닌, **3가지 신호를 교차 검증**하여 중요도 판단:

### 신호 1: RSS 수집 (기본)
- 모든 기사의 출발점
- 24~48시간 내 기사 필터링

### 신호 2: 홈페이지 TOP 배치
- Hero 영역 (첫 번째 대형 기사)
- Featured/Top Stories 섹션

### 신호 3: 랭킹 섹션 (6개 매체)
- Most Popular / Most Read / Most Viewed
- Trending Stories
- Most Discussed (댓글 기반)

### Value Score 계산

| 신호 | 점수 |
|------|------|
| 홈페이지 Hero (TOP) | +8 |
| Featured/Top Stories | +6 |
| Most Popular/Read/Viewed | +5 |
| Trending Stories | +5 |
| Most Discussed | +4 |
| RSS만 (일반) | +2 |
| 교차 보도 보너스 | +0.5 ~ +2.0 |
| 심층 매체 가중치 | ×1.2 |

```
Value Score = (배치점수 × 매체가중치) + 교차보도보너스
기준: Value Score ≥ 3.0 → 브리핑 포함
```

---

## 수집 프로세스

```
[Step 1] RSS 수집 (10개 매체)
    │
    ├─ feedparser로 각 매체 RSS 파싱
    ├─ 24~48시간 내 기사 필터링
    └─ 기사 URL, 제목, 발행시간 추출
    
[Step 2] 홈페이지 크롤링 (10개 매체)
    │
    ├─ firecrawl_scrape로 홈페이지 수집
    ├─ Hero 영역 기사 식별 → +8점
    └─ Featured 섹션 기사 식별 → +6점

[Step 3] 랭킹 섹션 크롤링 (6개 매체)
    │
    ├─ TechCrunch: Most Popular 섹션
    ├─ The Verge: Most Popular + Most Discussed
    ├─ Ars Technica: Most Read 섹션
    ├─ Wired: Trending Stories 섹션
    ├─ The Guardian: Most Viewed 섹션
    └─ 해당 기사 → +4~5점

[Step 4] 교차 검증 & 점수 계산
    │
    ├─ RSS 기사 ∩ 홈페이지 TOP = 높은 Value
    ├─ RSS 기사 ∩ 랭킹 섹션 = 중간 Value
    ├─ 동일 주제 다매체 보도 = 교차보도 보너스
    └─ Value Score 3.0 이상만 선별

[Step 5] Claude's Pick 선별
    │
    └─ 48시간 내, Signal 2개+, 관심사 1개+
```

---

## 홈페이지 URL

| 매체 | URL |
|------|-----|
| TechCrunch | `https://techcrunch.com` |
| The Verge | `https://www.theverge.com` |
| Ars Technica | `https://arstechnica.com` |
| Wired | `https://www.wired.com` |
| VentureBeat | `https://venturebeat.com` |
| Reuters Tech | `https://www.reuters.com/technology/` |
| BBC Tech | `https://www.bbc.com/news/technology` |
| The Guardian Tech | `https://www.theguardian.com/uk/technology` |
| SCMP Tech | `https://www.scmp.com/tech` |
| Rest of World | `https://restofworld.org` |

---

## 출력 형식

```markdown
# 외신 브리핑 (2025-12-25)

> Value Score 3.0 이상 기사만 선별 | 총 15건
> 3중 신호: RSS + 홈페이지 TOP + 랭킹 섹션

## AI/기술

### OpenAI Launches GPT-5.2 with Enhanced Coding
**OpenAI, 코딩 성능 강화된 GPT-5.2 출시**
> Codex 2.0 통합으로 보안 기능 대폭 강화

— [TechCrunch](https://...) | 📅 12/25 03:02 KST | 🔥 TOP 📈 인기 🔄 4개 매체 | Score: 10.5

---

## 경제/비즈니스

### ServiceNow to Acquire Armis for $7.75B
**서비스나우, 아르미스 $77.5억에 인수**
> AI 기반 사이버보안 역량 강화

— [Reuters](https://...) | 📅 12/24 22:00 KST | 🔥 TOP 🔄 3개 매체 | Score: 9.0

---

## 🎯 Claude's Pick

> 48시간 내 숨은 보석 | Signal 2개+ & 관심사 1개+

### Korean AI Startup Raises $50M Series B
**한국 AI 스타트업, 시리즈B $5천만 유치**
> 글로벌 확장 본격화

— [Rest of World](https://...) | 📅 12/24 15:00 KST

**선정 이유**: 신생 기업 첫 등장 + 투자 신호 | 한국 시장 연관성

---
```

### 배지 설명

| 배지 | 의미 | 점수 |
|------|------|------|
| 🔥 TOP | 홈페이지 Hero/Featured 배치 | +6~8 |
| 📈 인기 | Most Popular/Read/Viewed | +5 |
| 📊 트렌딩 | Trending Stories | +5 |
| 💬 댓글 | Most Discussed | +4 |
| 🔄 N개 매체 | 교차 보도 | +0.5~2.0 |

---

## v4에서 교체된 매체

| v4 매체 | 문제점 | v5 대체 매체 |
|---------|--------|-------------|
| WSJ | 유료벽, RSS 제한 | The Guardian |
| The Economist | 유료벽, RSS 제한 | Rest of World |
| Nikkei Asia | RSS 불안정 | SCMP |
| MIT Tech Review | RSS 일부 제한 | VentureBeat |
| CNBC | 크롤링 차단 | Reuters |

---

## 매체별 특성

| 매체 | 강점 | 가중치 |
|------|------|--------|
| TechCrunch | 스타트업, 투자, 제품 출시 | 1.0 |
| The Verge | 소비자 기술, 리뷰, 정책 | 1.0 |
| Ars Technica | 심층 기술 분석, 과학 | 1.1 |
| Wired | 트렌드, 문화, 장기 전망 | 1.1 |
| VentureBeat | 엔터프라이즈 AI, B2B | 1.0 |
| Reuters Tech | 속보, 기업 뉴스, 글로벌 | 1.0 |
| BBC Tech | 균형 잡힌 보도, 규제 | 1.0 |
| The Guardian Tech | 비판적 시각, 정책 | 1.0 |
| SCMP Tech | 중국/아시아 기술 동향 | 1.1 |
| Rest of World | 신흥국 기술, 글로벌 격차 | 1.2 |

---

## 버전 히스토리

| 버전 |