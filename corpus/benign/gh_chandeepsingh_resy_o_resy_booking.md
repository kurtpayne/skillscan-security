---
name: resy-booking
description: Complete Resy restaurant reservation management - search restaurants, check availability, book, cancel, modify reservations, and manage waitlists.
homepage: https://resy.com/
metadata: {"clawdbot":{"emoji":"🍽️","requires":{"env":["RESY_API_KEY","RESY_AUTH_TOKEN"],"bins":["python3"]}}}
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: chandeepsingh/resy-openclaw-skill
# corpus-url: https://github.com/chandeepsingh/resy-openclaw-skill/blob/830b1db969895142460a7f6b1f56fe87893ffbab/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Resy Booking

Manage restaurant reservations through Resy. Search restaurants, check availability, book tables, modify existing reservations, join waitlists, and manage your dining plans.

## Setup

### Option 1: Environment Variables

```bash
export RESY_API_KEY="your_api_key"
export RESY_AUTH_TOKEN="your_auth_token"
```

### Option 2: Secure File Storage (Recommended)

```bash
# Create credential files
echo "your_api_key" > ~/.resy_key
echo "your_auth_token" > ~/.resy_token
chmod 600 ~/.resy_key ~/.resy_token

# Set file paths
export RESY_API_KEY_FILE="~/.resy_key"
export RESY_AUTH_TOKEN_FILE="~/.resy_token"
```

### Option 3: Configuration File

```bash
# Run interactive setup wizard
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/config.py --setup
```

To get your credentials:
1. Log into Resy in your browser
2. Open Developer Tools (F12) → Network tab
3. Visit any restaurant page
4. Look for API calls to `api.resy.com`
5. Find `Authorization` header for API key and `x-resy-auth-token` for auth token

## Usage

### Search Restaurants

Find restaurants by name or location:

```bash
# Search by name
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/search.py --query "Nobu"

# Search by location
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/search.py --location "New York" --query "Italian"
```

### Check Availability

See available time slots for a restaurant:

```bash
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/availability.py \
  --venue-id 12345 \
  --date 2024-12-25 \
  --party-size 2
```

### Book a Reservation

Make a reservation at your chosen restaurant:

```bash
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/book.py \
  --venue-id 12345 \
  --date 2024-12-25 \
  --time 19:00 \
  --party-size 2
```

### List Your Reservations

View all upcoming reservations:

```bash
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/list_reservations.py
```

### Cancel a Reservation

Cancel an existing reservation:

```bash
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/cancel.py \
  --reservation-id abc123
```

### Modify a Reservation

Change time, date, party size, or special requests:

```bash
# Change time
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/modify.py \
  --reservation-id abc123 \
  --time 20:00

# Change party size
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/modify.py \
  --reservation-id abc123 \
  --party-size 4

# Change date and add special requests
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/modify.py \
  --reservation-id abc123 \
  --date 2024-12-26 \
  --notes "Window table please"
```

### Waitlist Management

Join waitlists when restaurants are fully booked:

```bash
# Check if waitlist is available
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/waitlist.py check \
  --venue-id 12345 \
  --date 2024-12-25 \
  --party-size 2

# Join a waitlist
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/waitlist.py join \
  --venue-id 12345 \
  --date 2024-12-25 \
  --time 19:00 \
  --party-size 2 \
  --notes "Anniversary dinner"

# Check waitlist status
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/waitlist.py status \
  --waitlist-id wl_abc123

# Cancel waitlist entry
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/waitlist.py cancel \
  --waitlist-id wl_abc123
```

## API Reference

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `RESY_API_KEY` | Yes* | Your Resy API key from browser headers |
| `RESY_AUTH_TOKEN` | Yes* | Your Resy auth token from browser headers |
| `RESY_API_KEY_FILE` | Alternative | Path to file containing API key |
| `RESY_AUTH_TOKEN_FILE` | Alternative | Path to file containing auth token |
| `RESY_TIMEZONE` | No | Your local timezone (default: America/New_York) |

*Either the direct value or the file path must be set.

### Date and Time Formats

- **Date**: `YYYY-MM-DD` (e.g., `2024-12-25`)
- **Time**: `HH:MM` 24-hour format (e.g., `19:00` for 7 PM)

### Party Sizes

Valid party sizes range from 1 to 20 guests.

## Examples

### Complete booking workflow

```bash
# 1. Search for the restaurant
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/search.py --query "Don Angie"
# Note the venue_id from the output (e.g., 1505)

# 2. Check availability
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/availability.py \
  --venue-id 1505 \
  --date 2024-12-25 \
  --party-size 4

# 3. Book the reservation with special requests
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/book.py \
  --venue-id 1505 \
  --date 2024-12-25 \
  --time 19:00 \
  --party-size 4 \
  --notes "Anniversary dinner, gluten-free options please"

# 4. View your reservations
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/list_reservations.py

# 5. Modify if needed (change time)
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/modify.py \
  --reservation-id resy_abc123 \
  --time 20:00

# 6. Or cancel if plans change
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/cancel.py \
  --reservation-id resy_abc123
```

### Quick availability check

```bash
python3 ~/.openclaw/workspace/skills/resy-booking/scripts/availability.py \
  --venue-id 1505 \
  --date $(date -d "+1 day" +%Y-%m-%d) \
  --party-size 2
```

## Error Handling

All scripts provide clear error messages:

- **Missing credentials**: Will prompt to set environment variables
- **Invalid venue ID**: Suggests using search to find correct ID
- **No availability**: Lists alternative times if available
- **Booking conflicts**: Explains the conflict clearly

## Security Notes

- Credentials are never written to disk
- Only connects to official Resy API (`api.resy.com`)
- All API calls are logged to stderr for debugging
- No sensitive data in error messages

## Troubleshooting

**"Authentication failed"**
- Verify your `RESY_API_KEY` and `RESY_AUTH_TOKEN` are correct
- Tokens may expire - re-extract from browser if needed

**"No availability found"**
- Try different dates or times
- Some restaurants release reservations at specific times
- Check if restaurant accepts walk-ins

**"Booking failed"**
- Ensure you have a credit card on file for the restaurant
- Some high-demand restaurants have stricter booking policies

## Documentation

- Full API docs: `~/.openclaw/workspace/skills/resy-booking/references/api-docs.md`
- Setup guide: `~/.openclaw/workspace/skills/resy-booking/references/setup-guide.md`
- Error codes: `~/.openclaw/workspace/skills/resy-booking/references/error-codes.md`

Resy website: https://resy.com/