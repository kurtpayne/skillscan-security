---
name: septa
description: Get real-time SEPTA Regional Rail train schedules, departures, arrival times, delays, and status between stations in the Philadelphia area
version: 1.2.0
user-invocable: true
slash-command: septa

metadata:
  openclaw:
    requires:
      bins: [node]
    emoji: "🚆"
    category: transportation
    tags: [septa, trains, philadelphia, transit, realtime, regional-rail]
    network: true

  parameters:
    type: object
    properties:
      command:
        type: string
        enum: [departures, to, trains, train]
        description: "Type of query: 'departures' for all trains from a station, 'to' for direct trains between stations, 'trains' for all active trains, 'train' for specific train schedule"
      station:
        type: string
        description: "Station name for departures (e.g., 'Suburban Station', 'Paoli')"
      origin:
        type: string
        description: "Starting station for 'to' command (e.g., '30th Street Station')"
      destination:
        type: string
        description: "Ending station for 'to' command (e.g., 'Airport Terminal A')"
      train_number:
        type: string
        description: "Train number for 'train' command (e.g., '2335')"
      results:
        type: integer
        description: "Number of results to return (default: 10 for departures, 5 for direct trains)"
        default: 10
    required: [command]

  examples:
    - prompt: "When is the next train from Suburban Station?"
      call: septa
      args:
        command: departures
        station: "Suburban Station"
        results: 5

    - prompt: "Next train from 30th Street to Malvern"
      call: septa
      args:
        command: to
        origin: "30th Street Station"
        destination: "Malvern"
        results: 3

    - prompt: "What trains are leaving from Paoli?"
      call: septa
      args:
        command: departures
        station: "Paoli"

    - prompt: "Show me all active trains right now"
      call: septa
      args:
        command: trains

    - prompt: "What's the schedule for train 2335?"
      call: septa
      args:
        command: train
        train_number: "2335"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: DeGrandis/septa-cli
# corpus-url: https://github.com/DeGrandis/septa-cli/blob/64f2a22822bd22e772e69250a0abe7e6d25e676d/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# SEPTA Regional Rail CLI Skill

Get real-time SEPTA Regional Rail train information including departures from any station, direct train schedules between stations, live status of all active trains, and detailed schedules for specific trains.

## When to use this skill

- User asks about SEPTA trains, schedules, or departures
- User wants to know when the next train is from a specific station
- User asks "When is the next train from X to Y?"
- User wants to know what platform/track a train departs from
- User asks about train status or delays
- User mentions traveling on Regional Rail in Philadelphia area
- User wants to see all active trains or track a specific train
- User asks about all stops for a particular train

## How to call it

**Execution:** This skill uses the `septacli` executable.

**Output Format:** Returns markdown tables by default for LLM-friendly parsing. Add `--json` flag for structured JSON output.

There are four main commands:

### 1. Get all departures from a station
**Command:** `~/.openclaw/skills/septa_cli/septacli departures "<station>" [results] [--json]`
- Returns northbound and southbound trains leaving that station
- Includes origin, destination, departure time, track, platform, service type, and status

### 2. Get direct trains from one station to another
**Command:** `~/.openclaw/skills/septa_cli/septacli to "<fromStation>" "<toStation>" [results] [--json]`
- Returns only trains that go directly from station A to station B
- Includes departure time from origin, arrival time at destination, and direct/transfer indicator

### 3. Get live status of all active trains
**Command:** `~/.openclaw/skills/septa_cli/septacli trains [--json]`
- Returns all currently running Regional Rail trains
- Includes train numbers, origins, destinations, current locations, GPS coordinates, heading, delays, consists, and tracks

### 4. Get detailed schedule for a specific train
**Command:** `~/.openclaw/skills/septa_cli/septacli train "<trainNumber>" [--json]`
- Returns complete schedule with all stops for a specific train
- Includes scheduled, estimated, and actual times for each stop

## Station Names

Station names MUST be exact (including spaces and capitalization).

**Common stations:**
- "Suburban Station"
- "30th Street Station"
- "Jefferson Station" (also known as "Market East")
- "Airport Terminal A"
- "Airport Terminal B"
- "Temple U"
- "Norristown TC"
- "Doylestown"
- "Wilmington"
- "Malvern"
- "Paoli"
- "Wayne Junction"

Full list available at: https://www3.septa.org/VIRegionalRail.html

## Examples

### Example 1: Get departures from Suburban Station
**User:** "When is the next train from Suburban Station?"
**Command:** `~/.openclaw/skills/septa_cli/septacli departures "Suburban Station" 5`
**Output:** Markdown table with northbound and southbound trains:
```markdown
# Departures from Suburban Station
*Suburban Station Departures: February 23, 2026, 10:47 am*

## Northbound
| Train | Origin | Destination | Line | Path | Depart | Track | Platform | Service | Status |
|-------|--------|-------------|------|------|--------|-------|----------|---------|--------|
| 4224 | Airport Terminal E-F | Norristown | Airport | R4/2N | 2026-02-23 11:05:00.000 | 1 | A | LOCAL | 9 min |
```

### Example 2: Get trains from 30th Street to Airport
**User:** "When does the next train to the airport leave from 30th Street?"
**Command:** `~/.openclaw/skills/septa_cli/septacli to "30th Street Station" "Airport Terminal A" 3`
**Output:** Markdown table with direct trains:
```markdown
# Trains from 30th Street Station to Airport Terminal A

| Train | Line | Depart | Arrive | Direct | Status |
|-------|------|--------|---------|--------|--------|
| 5432 | Airport | 3:55 PM | 4:12 PM | Yes | On time |
```

### Example 3: See all active trains
**User:** "What trains are running right now?"
**Command:** `~/.openclaw/skills/septa_cli/septacli trains`
**Output:** Markdown table with all active trains:
```markdown
# Active Regional Rail Trains
| Train | Line | Origin | Destination | Current | Next Stop | Service | Track | GPS | Heading | Consist | Status |
|-------|------|--------|-------------|---------|-----------|---------|-------|-----|---------|---------|--------|
| 1711 | Trenton | Market East | Trenton | Jefferson Station | Market East | LOCAL | 3 | 39.9538889,-75.1677778 | 120.1deg | - | 20 min late |
```

### Example 4: Get schedule for specific train
**User:** "Show me all the stops for train 2335"
**Command:** `~/.openclaw/skills/septa_cli/septacli train "2335"`
**Output:** Markdown table with complete schedule:
```markdown
# Schedule for Train 2335

| Station | Scheduled | Estimated | Actual |
|---------|-----------|-----------|--------|
| Suburban Station | 10:59 pm | 10:56 pm | 10:56 pm |
| Gray 30th Street | 11:03 pm | 11:02 pm | 11:02 pm |
```

## Combining Commands (Advanced Workflow)

An LLM can chain commands together for comprehensive answers:

**Scenario:** User asks "I need to get from 30th Street to Suburban Station, which train should I take and when does it stop at each station?"

**Workflow:**
1. **Step 1:** Run `septacli to "30th Street Station" "Suburban Station"`
   - Gets available direct trains with train numbers
   - Example result: Train 435 departs 3:51 PM, arrives 3:56 PM

2. **Step 2:** Run `septacli train "435"`
   - Gets complete schedule showing all stops between origin and destination
   - Shows exact times at each intermediate station

3. **Step 3:** Present comprehensive answer to user:
   - "Take train 435 departing at 3:51 PM from 30th Street"
   - "It stops at: Penn Medicine Station (3:54 PM), Suburban Station (3:56 PM - arrival)"
   - "Total travel time: 5 minutes"

**Another Scenario:** User asks "Are there any delays on trains to the airport right now?"

**Workflow:**
1. Run `septacli trains` to get all active trains
2. Filter results for trains with destination containing "Airport"
3. Check delay status for each
4. Present summary: "Train 5432 to Airport Terminal A is on time, departing 4:12 PM"

## Output Format

**Default:** Markdown tables (shown in examples above)

**JSON Mode:** Add `--json` flag to any command for structured JSON output

### Departures command returns (JSON):
```json
{
  "station": "Suburban Station",
  "timestamp": "Suburban Station Departures: February 13, 2026, 3:45 pm",
  "northbound": [
    {
      "direction": "N",
      "train_id": "435",
      "destination": "Thorndale",
      "line": "Paoli/Thorndale",
      "depart_time": "3:51 PM",
      "track": "4",
      "status": "On Time"
    }
  ],
  "southbound": [...]
}
```

### To command returns:
```json
{
  "from": "30th Street Station",
  "to": "Airport Terminal A",
  "trains": [
    {
      "orig_train": "5432",
      "orig_line": "Airport",
      "orig_departure_time": "3:55 PM",
      "orig_arrival_time": "4:12 PM",
      "orig_delay": "On time"
    }
  ]
}
```

### Trains command returns:
```json
[
  {
    "lat": "40.0123",
    "lon": "-75.1234",
    "trainno": "2335",
    "service": "LOCAL",
    "dest": "Elwyn Station",
    "currentstop": "Suburban Station",
    "nextstop": "Gray 30th Street",
    "line": "Media/Elwyn",
    "consist": "4",
    "heading": "S",
    "late": 2,
    "SOURCE": "02/18/2026 10:56:00 PM",
    "TRACK": "4",
    "TRACK_CHANGE": ""
  }
]
```

### Train command returns:
```json
{
  "train_number": "2335",
  "schedule": [
    {
      "station": "Suburban Station",
      "sched_tm": "10:59 pm",
      "est_tm": "10:56 pm",
      "act_tm": "10:56 pm"
    },
    {
      "station": "Gray 30th Street",
      "sched_tm": "11:03 pm",
      "est_tm": "11:02 pm",
      "act_tm": "11:02 pm"
    }
  ]
}
```

## Important Notes

- **Zero Dependencies:** Uses only Node.js built-in `fetch` (requires Node 18+)
- **Real-Time Data:** Connects to official SEPTA API at `https://www3.septa.org/api`
- **Direct Trains Only:** The "to" command only shows direct trains (no transfers)
- **Station Names:** Must be exact - case sensitive and with correct spacing
- **Default Results:** 10 for departures, 5 for direct trains
- **No Authentication:** Public SEPTA API, no keys required
- **CLI Tool:** Uses `septacli` executable (made with Node.js shebang)
- **Command Chaining:** LLMs can combine `trains` + `train` commands for detailed journey planning

## Error Handling

- Invalid station names: API returns error or empty results
- Network errors: Script will output error message
- Invalid command: Shows usage instructions
- Non-existent route: Returns empty trains array
- Invalid train number: Returns empty schedule or error

## Technical Details

- **API Base URL:** `https://www3.septa.org/api`
- **Departures Endpoint:** `/Arrivals/index.php?station={station}&results={n}`
- **Direct Trains Endpoint:** `/NextToArrive/index.php?req1={from}&req2={to}&req3={n}`
- **Live Trains Endpoint:** `/TrainView/index.php`
- **Train Schedule Endpoint:** `/RRSchedules/index.php?req1={trainNumber}`
- **Response Format:** JSON
- **Update Frequency:** Real-time from SEPTA systems