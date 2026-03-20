---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Labmat2090/my-ministry-organizer
# corpus-url: https://github.com/Labmat2090/my-ministry-organizer/blob/2e6aeae0defe975d1ddd25e5bba3f2ce2f4c1f23/PROJECT_SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# My Ministry Organizer App - Project Skill

## Project Overview
**Name:** My Ministry Organizer App  
**Purpose:** Field service organizer for Jehovah's Witness pioneers to track monthly hours, bible studies, and return visits  
**Tech Stack:** Next.js + Dexie.js (IndexedDB) + Vercel  
**Privacy:** All data stored locally on user's device - no cloud storage  

## Key Decisions Made

### Architecture
- **Frontend:** Next.js 14 (App Router)
- **Database:** Dexie.js for IndexedDB management
- **Styling:** Tailwind CSS
- **Deployment:** Vercel (static export)
- **No Authentication:** Privacy-first, local-only storage

### Why Dexie.js over Supabase?
Privacy is paramount for religious activity tracking. Users wanted:
- Data that never leaves their device
- No account creation required
- Complete user control over their data
- Works 100% offline

### Database Schema (IndexedDB via Dexie)
```javascript
// Main tables:
- profiles (user settings)
- timeEntries (daily hours, bible studies, return visits)
- bibleStudies (detailed student tracking - optional)
- returnVisits (detailed RV tracking - optional)
- monthlyGoals (custom monthly targets)
```

## Project Structure
```
my-ministry-organizer/
├── src/
│   ├── app/              # Next.js app router
│   ├── components/       # React components
│   ├── lib/
│   │   ├── db.js        # Dexie database setup
│   │   └── utils.js     # Helper functions
│   └── styles/
├── public/
├── docs/
│   ├── SETUP.md
│   ├── DATABASE.md
│   └── FEATURES.md
├── PROJECT_STATUS.md
└── DECISIONS.md
```

## Current Phase: **Phase 1 - Initial Setup**

### Completed:
- ✅ Project planning and architecture decisions
- ✅ Database schema design
- ✅ Technology stack selected

### In Progress:
- 🔄 Creating initial project files
- 🔄 Setting up Dexie database schema
- 🔄 GitHub repository structure

### Next Steps:
1. Complete initial file structure
2. Set up Dexie database
3. Create basic Next.js app
4. Build calendar UI component
5. Implement time entry form
6. Add export/import functionality

## Development Phases

### Phase 1: Foundation (Current)
- Project setup
- Database schema
- Basic Next.js structure
- Documentation

### Phase 2: Core Features
- Calendar view
- Time entry form
- Monthly summary calculations
- Profile settings

### Phase 3: Enhanced Tracking
- Bible studies detailed tracking
- Return visits management
- Notes and experiences

### Phase 4: Reports & Export
- Monthly reports
- Annual progress tracking
- Export to JSON/CSV
- Import functionality

### Phase 5: Polish & Deploy
- UI/UX refinement
- Testing
- Deployment to Vercel
- User documentation

## Key Features

### MVP (Minimum Viable Product):
1. Monthly calendar view
2. Daily time entry (hours, bible studies, return visits)
3. Automatic totals and progress tracking
4. 600-hour annual goal tracking
5. Export/import data (JSON)

### Future Enhancements:
- Detailed bible study student tracking
- Return visit database with reminders
- Multiple pioneer profiles (family members)
- Print-friendly reports
- Dark mode
- PWA (installable web app)

## Technical Notes

### IndexedDB Structure
- Database name: `ministryOrganizerDB`
- Version: 1
- Uses Dexie.js for clean API
- Automatic schema upgrades

### Data Export Format
```json
{
  "version": "1.0",
  "exportDate": "2026-02-01",
  "profile": {...},
  "timeEntries": [...],
  "bibleStudies": [...],
  "returnVisits": [...]
}
```

### Browser Compatibility
- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support (iOS 12.2+)
- IndexedDB has ~98% global browser support

## User Scenarios

### Primary User: Regular Pioneer
- Commits to 600 hours annually
- Needs to track daily/weekly to stay on pace
- Conducts bible studies and makes return visits
- Wants simple, fast entry
- Values privacy

### Usage Pattern:
1. Open app on phone/computer
2. Click today's date
3. Enter hours worked
4. Update bible study and RV counts
5. View progress toward monthly/annual goal
6. Export data monthly for backup

## Privacy & Security
- **No telemetry** - zero tracking
- **No external requests** - works completely offline
- **User owns data** - can export anytime
- **Browser storage only** - nothing sent to servers
- **Optional:** Users can sync via their browser's native sync

## Session Continuity Instructions

When resuming this project in a new session:
1. Read this PROJECT_SKILL.md file
2. Check PROJECT_STATUS.md for current phase
3. Review DECISIONS.md for context
4. Continue from last checkpoint in status file

## Contact & Feedback
User is on Claude free tier - sessions may be interrupted.
Progress is tracked via these markdown files for easy continuation.