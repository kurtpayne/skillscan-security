---
name: pgis
description: Performance Glycemic Intelligence System (PGIS) - integrates CGM, HRV, heart rate, sleep, and training data to provide daily readiness assessments, training prescriptions, post-workout analysis, fueling strategies, and clinical performance audits. Use for analyzing training data, generating readiness reports, creating performance audit presentations, and producing audio summaries for endurance athletes with Type 2 diabetes.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: chukwumaonyeije/pgis-manus-skill
# corpus-url: https://github.com/chukwumaonyeije/pgis-manus-skill/blob/cb8b592d743c7d835c6bd1f0a0744ea524122355/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# PGIS (Performance Glycemic Intelligence System)

The Performance Glycemic Intelligence System (PGIS) is an integrated decision-support framework for optimizing endurance training while managing Type 2 diabetes. This skill provides daily readiness assessments, training prescriptions, post-workout analysis, and clinical performance audits tailored to the user's physiological profile.

## Overview

PGIS combines multiple data streams to make intelligent training decisions:
- **Metabolic data**: CGM readings, fasting glucose, glucose trends
- **Cardiac data**: Heart rate, HRV, resting heart rate
- **Recovery data**: Sleep duration/quality, Body Battery, DOMS
- **Training load**: Recent workout history, strength sessions

The system uses a traffic light model (GREEN/YELLOW/RED) to gate daily training decisions, preventing overtraining, hypoglycemia, and injury while optimizing metabolic adaptation.

## Core Use Cases

### 1. Daily Readiness Assessment
Generate morning readiness report with training recommendations.

**Inputs needed:**
- HRV (baseline: user-specific, see profile)
- Resting HR (baseline: user-specific, see profile)
- Sleep hours
- Fasting glucose and CGM trend
- DOMS score (0-10)
- Body Battery
- Recent strength session (Y/N)
- Training load past 48 hours

**Process:**
1. Read `references/user_profile.md` for baselines
2. Read `references/readiness_algorithm.md` for decision logic
3. Use `scripts/readiness_calculator.py` to compute readiness status
4. Generate visual report (slides or infographic) using style guide
5. Generate audio summary using `scripts/audio_summary_generator.py`

**Outputs:**
- Readiness status (GREEN/YELLOW/RED)
- Current metrics vs baselines
- Flags (red or yellow)
- Specific training recommendations
- Fasted run safety assessment
- Audio podcast (MP3) with conversational briefing

### 2. Training Prescription
Generate HR-based training plan for specific workout.

**Inputs needed:**
- Readiness status (from daily assessment)
- Workout type (aerobic, strength, mixed)
- Target duration
- Fasted or fueled

**Process:**
1. Verify readiness status allows training
2. Set HR zones based on readiness (GREEN: 118-128 bpm, YELLOW: 110-120 bpm, RED: rest)
3. Determine fueling strategy based on glucose and readiness
4. Set safety protocols (glucose monitoring frequency, abort criteria)
5. Generate structured prescription with warmup/cooldown requirements

**Outputs:**
- HR zone prescription
- Duration and structure
- Fueling strategy (pre/during/post/bedtime)
- Safety protocols
- Slide or document format

### 3. Post-Workout Analysis
Analyze completed workout and provide optimization recommendations.

**Inputs needed:**
- Workout data (duration, HR average/peak, volume)
- Pre/during/post glucose readings
- Body Battery change
- Subjective assessment
- Screenshots from Garmin/Dexcom (optional)

**Process:**
1. Assess HR zone compliance (did HR stay within prescribed zones?)
2. Evaluate metabolic response (glucose stability = optimal/suboptimal/poor)
3. Check recovery markers (Body Battery, predicted recovery time)
4. Identify optimization opportunities
5. Generate clinical performance audit presentation
6. Generate audio summary of analysis

**Outputs:**
- Performance summary with HR compliance
- Metabolic response assessment
- Recovery predictions
- Optimization recommendations
- Clinical performance audit slides/infographic
- Audio podcast with analysis

### 4. Screenshot Analysis
Extract data from Garmin and Dexcom screenshots and integrate into reports.

**Process:**
1. View screenshots using multimodal understanding
2. Extract key metrics (HR, duration, glucose readings, trends)
3. Integrate into readiness assessment or post-workout analysis
4. Include screenshots in visual reports with annotations

### 5. Weekly Trend Analysis
Summarize weekly patterns and recommend adjustments.

**Inputs needed:**
- Daily readiness statuses for the week
- All workout data for the week
- Average metrics (HRV, RHR, sleep, glucose)
- Hypoglycemia events

**Process:**
1. Aggregate training load (sessions, duration, types)
2. Calculate readiness distribution (GREEN/YELLOW/RED days)
3. Analyze metabolic stability (glucose variability, hypo events)
4. Identify recovery trends
5. Recommend adjustments for next week

**Outputs:**
- Weekly summary presentation
- Trend visualizations
- Pattern identification
- Adjustment recommendations

## Data Input Methods

### Manual Entry
When user provides metrics directly in text:
```
HRV: 29
RHR: 59 bpm
Sleep: 7.5 hours
Fasting glucose: 93 mg/dL, trend stable
DOMS: 2/10
Body Battery: 77
Recent strength: No
```

Parse these values and use in readiness calculator.

### Screenshot Upload
When user uploads Garmin or Dexcom screenshots:
1. View images using multimodal understanding
2. Extract visible metrics
3. Confirm extracted values with user if critical
4. Save screenshots to working directory for inclusion in reports
5. Annotate screenshots in final presentations

### Combination
User may provide some metrics manually and supplement with screenshots. Prioritize manual entries for critical values (glucose, HRV) and use screenshots for context and visual documentation.

## Output Generation

### Visual Reports (Slides and Infographics)

**Style Requirements:**
- Read `/home/ubuntu/skills/pgis/references/visual_style_guide.md` for complete specifications
- Dark backgrounds (#1a1a1a, #0d0d0d)
- Cyan primary accent (#00d9ff)
- Purple secondary accent (#9c27b0)
- Status colors: Green (#4caf50), Yellow (#ffc107), Red (#f44336)
- Clinical note boxes with cyan borders
- Icons for metrics (CGM, heart, sleep, etc.)
- Anatomical imagery in backgrounds (optional)

**Slide Structure:**
- Use `/home/ubuntu/skills/pgis/templates/slide_template.md` as structural guide
- Reference `/home/ubuntu/skills/pgis/templates/example_infographic.png` for visual style
- Generate using slides mode (HTML format preferred for editability)
- Include comparison tables (Actual vs Optimized)
- Integrate screenshots when provided

**File Naming:**
- `YYYYMMDD-PGIS_[type].pdf` (e.g., `20260219-PGIS_daily_readiness.pdf`)
- `infographic_YYYYMMDD.png`

### Audio Summaries (Podcasts)

**Voice and Style:**
- Voice: "nova" (professional, chatty, authoritative female)
- Model: "tts-1-hd" (high quality)
- Tone: Conversational yet clinical, like a sports medicine consultant
- Address user by their preferred name (customizable in profile)

**Script Generation:**
Use `scripts/audio_summary_generator.py`:

```python
from audio_summary_generator import AudioSummaryGenerator

generator = AudioSummaryGenerator(voice="nova", model="tts-1-hd")

# Daily readiness audio
audio_path = generator.generate_daily_readiness_audio(
    status="GREEN",
    metrics={
        'hrv': 29.0,
        'rhr': 59,
        'sleep_hours': 7.5,
        'fasting_glucose': 93,
        'cgm_trend': 'stable',
        'body_battery': 77,
        'doms': 2,
        'recent_strength': False
    },
    output_path="20260219-PGIS_daily_readiness.mp3",
    red_flags=[],
    yellow_flags=[],
    recommendations=[]
)
```

**Audio Types:**
- Daily readiness briefing (2-3 minutes)
- Post-workout analysis (2-4 minutes)
- Weekly trend summary (4-6 minutes)

**File Naming:**
- `YYYYMMDD-PGIS_audio_summary.mp3`

## Readiness Calculator Usage

The readiness calculator is the core decision engine. Use it for all readiness assessments:

```python
from readiness_calculator import ReadinessCalculator, Metrics, ReadinessStatus

# Create calculator with Dr. O's baselines (default)
calculator = ReadinessCalculator()

# Input metrics
metrics = Metrics(
    hrv=29.0,
    rhr=59.0,
    sleep_hours=7.5,
    fasting_glucose=93.0,
    doms=2,
    body_battery=77,
    cgm_trend="→",
    illness_signs=False,
    recent_strength=False,
    training_load_48h="low"
)

# Calculate readiness
status, red_flags, yellow_flags = calculator.calculate(metrics)

# Get recommendations
recommendations = calculator.get_recommendations(status, metrics)

# Check fasted run safety
is_safe, reason = calculator.check_fasted_run_safety(metrics, status)

# Generate formatted report
report = calculator.format_report(metrics)
print(report)
```

**CGM Trend Arrows:**
- `"↑↑"` - Rising rapidly
- `"↑"` - Rising
- `"→"` - Stable
- `"↓"` - Falling
- `"↓↓"` - Falling rapidly

## User Profile Summary

**Key Baselines (Example - Customize in user_profile.md):**
- Age: [User-specific]
- HRV baseline: [User-specific]
- RHR baseline: [User-specific]
- Primary aerobic HR: [User-specific, calculated from max HR]
- HR ceiling: [User-specific]
- Sleep minimum: 6 hours (7+ optimal)
- Fasting glucose target: <100 mg/dL

**Critical Considerations:**
- Type 2 diabetes management
- Increased nocturnal hypoglycemia risk after strength sessions
- Age-adjusted recovery profile
- Dietary preferences (user-specific)
- Training goals (user-specific)
- Philosophy: Durability and longevity over speed

**Training Constraints:**
- HR limits based on age and training phase
- Warmup ≥10 min and cooldown ≥5 min (non-negotiable)
- Carry glucose on all fasted runs
- Monitor CGM every 10-15 min during fasted runs
- Bedtime fueling after strength sessions

For complete profile, read `references/user_profile.md`.

## Workflow Examples

### Example 1: Morning Readiness Check

User provides:
> "HRV 28, RHR 62, slept 6.5 hours, fasting glucose 97 with stable trend, DOMS 3/10, Body Battery 65. Had strength training yesterday."

Process:
1. Parse metrics from message
2. Run readiness calculator
3. Determine status based on user's specific baselines
4. Generate readiness report with modified training recommendations if needed
5. Create slide presentation with current metrics vs baselines
6. Generate audio briefing explaining status and modifications
7. Deliver both visual and audio outputs

### Example 2: Post-Workout Analysis with Screenshots

User uploads Garmin screenshot and says:
> "Just finished my run. Felt good but want to see how my glucose responded."

Process:
1. View Garmin screenshot to extract workout data (duration, HR, etc.)
2. Ask for glucose data if not visible in screenshot
3. Assess HR zone compliance (was HR in 118-128 range?)
4. Evaluate metabolic response based on glucose stability
5. Generate clinical performance audit infographic
6. Include screenshot with annotations
7. Generate audio analysis explaining performance and any optimizations
8. Deliver visual and audio outputs

### Example 3: Training Prescription Request

User says:
> "What should my workout look like today? I'm planning a 45-minute run."

Process:
1. Check if readiness assessment has been done today
2. If not, request metrics and perform readiness assessment first
3. Based on readiness status, prescribe HR zones
4. Structure 45-minute run: 10 min warmup, 25 min main set, 10 min cooldown
5. Determine fueling strategy based on current glucose
6. Set safety protocols (CGM check frequency, abort criteria)
7. Generate training prescription slide
8. Optionally generate audio briefing of the workout plan

### Example 4: Weekly Review

User says:
> "Can you give me a weekly summary? I want to see how this week went."

Process:
1. Request daily data for the week (or use previously provided data)
2. Aggregate training load and readiness distribution
3. Calculate average metrics (HRV, RHR, sleep, glucose)
4. Identify patterns (e.g., "HRV declining mid-week", "glucose more stable on aerobic-only days")
5. Generate weekly trend presentation with visualizations
6. Provide specific recommendations for next week
7. Generate audio podcast summarizing the week

## Special Scenarios

### Nocturnal Hypoglycemia Risk (Post-Strength)
When recent_strength=True or user mentions strength session in last 24 hours:
- Flag increased insulin sensitivity
- Recommend bedtime fueling: 20-30g complex carbs + 10-15g protein
- Set CGM low alert to 75 mg/dL (instead of 70)
- Advise keeping fast-acting glucose at bedside
- Consider reduced intensity next day if overnight low occurred

Note: Specific glucose thresholds should be customized based on individual response patterns.

### Fasted Run Safety
Before clearing fasted run:
1. Verify GREEN readiness status
2. Check fasting glucose >85 mg/dL
3. Verify CGM trend stable or upward (→ or ↑)
4. Confirm no recent hypoglycemia (<12 hours)
5. Remind to carry glucose and check CGM every 10-15 min
6. Set abort criteria: glucose <70 mg/dL or rapid drop

### HR Ceiling Enforcement
Always enforce HR limits (customize based on age and training phase):
- Primary zone: [User-specific aerobic zone]
- Absolute ceiling: [User-specific ceiling]
- Brief spikes acceptable for <30 seconds
- If HR exceeds primary zone: slow pace immediately
- If HR exceeds ceiling: walk
- If unable to control HR: end workout

Rationale: Age-adjusted training prioritizes autonomic balance and long-term adaptation over pace.

### High Training Load Modifier
If training_load_48h="high" AND any yellow flags present:
- Elevate status from YELLOW to RED
- Mandate rest day
- Explain cumulative fatigue risk

High load = 2+ structured workouts, 1+ strength session, >3 hours total, or any workout with sustained HR >130 bpm in past 48 hours.

## Technical Notes

### Running Scripts
All Python scripts in `scripts/` are executable and tested. Install dependencies if needed:
```bash
pip install openai
```

Set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

### Generating Slides
Use Manus slides mode (HTML format) for creating presentations. Reference the visual style guide for colors and layout. The HTML format allows for custom CSS to match the dark theme and cyan/purple accents.

### File Organization
Create a working directory for each session:
```bash
mkdir -p pgis_reports/YYYYMMDD
cd pgis_reports/YYYYMMDD
```

Save all outputs (slides, audio, screenshots) in dated directories for easy tracking.

Note: Add `pgis_reports/` to .gitignore to prevent personal health data from being committed.

## Iteration and Improvement

After using this skill, note any:
- Metrics that are difficult to input or interpret
- Output formats that could be improved
- Additional analysis types needed
- Script errors or edge cases

This skill is designed for endurance athletes managing Type 2 diabetes and can be refined based on real-world usage patterns.

## Quick Reference

**Readiness Thresholds:**
- GREEN: All metrics within 10% of baseline, sleep ≥7 hrs, glucose stable
- YELLOW: Metrics 10-15% off baseline, sleep 6-7 hrs, mild glucose elevation
- RED: Metrics >15% off baseline, sleep <6 hrs, glucose unstable, DOMS >5, illness

**HR Zones (Example - customize based on max HR and training phase):**
- Primary aerobic: [User-specific]
- Absolute ceiling: [User-specific]
- YELLOW modification: Reduce by 8-10 bpm from normal

**Glucose Safety:**
- Fasted run minimum: >85 mg/dL
- During-workout abort: <70 mg/dL
- Post-strength bedtime fueling: If session in last 24 hrs

**Output Files:**
- Readiness report: `YYYYMMDD-PGIS_daily_readiness.pdf` + `.mp3`
- Post-workout: `YYYYMMDD-PGIS_performance_audit.pdf` + `.mp3`
- Infographic: `infographic_YYYYMMDD.png`
- Training prescription: `YYYYMMDD-PGIS_training_prescription.pdf`