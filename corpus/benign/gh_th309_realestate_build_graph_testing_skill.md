---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: th309/Realestate
# corpus-url: https://github.com/th309/Realestate/blob/f3031034f425b5803ea8c0c350a5985d3ba9cca9/BUILD_GRAPH_TESTING_SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Instructions: Build Graph Page Testing Skill

## Objective
Build a comprehensive Cursor skill that tests the PropertyIQ graphs page at https://propertyiq.vercel.app/graphs to ensure data loads correctly, graphs render properly, and all interactive features work as expected.

## Step 1: Analyze the Codebase

First, locate and read these files in the repository:

### Find the Graphs Page Component
Search for the graphs page in these likely locations:
- `PropertyIQ/src/app/graphs/page.tsx`
- `packages/frontend/src/app/graphs/page.tsx`
- `packages/frontend/src/pages/graphs.tsx`
- Or search for files containing "graph" in the name

**What to extract:**
1. What chart library is being used? (Recharts, Chart.js, Plotly, D3, etc.)
2. What are the component names?
3. What props/state does the graph component accept?
4. What data structure does it expect?

### Find the Data Layer
Look for how the graph fetches data:
- Search for hooks like `useGraphData`, `useChartData`, `useQuery`
- Look for Supabase queries in the graph component
- Find API routes if any (`/api/graph-data` or similar)
- Check for data transformation utilities

**What to extract:**
1. Database tables queried
2. Query parameters (geography type, geography ID, time period, score type)
3. Expected data format/schema
4. Any caching or data transformation logic

### Find the Search/Filter Component
Locate the search functionality:
- Search for "search" components in the graphs directory
- Look for filter components or dropdowns
- Check the maps page sidebar (mentioned as reference)

**What to extract:**
1. What can users search for? (geographies, metrics, etc.)
2. What filters are available? (state, metro, county, score type, time period)
3. How is search implemented? (autocomplete, dropdown, text input)
4. What data format does search return?

### Find Data Validation/Schema
Look for:
- TypeScript interfaces/types for graph data
- Validation schemas (Zod, Yup, etc.)
- Constants defining valid ranges (e.g., scores 0-100)

**What to extract:**
1. Valid data ranges for each metric type
2. Required vs optional fields
3. Data type constraints

## Step 2: Document Findings

Create a document called `GRAPH_PAGE_ANALYSIS.md` with:

```markdown
# Graph Page Analysis

## Chart Implementation
- **Library**: [Recharts/Chart.js/etc.]
- **Component Path**: [path/to/component]
- **Chart Types**: [LineChart, BarChart, etc.]

## Data Flow
1. **Data Source**: 
   - Database: [Supabase table names]
   - API Endpoint: [if any]
   
2. **Query Parameters**:
   - Geography Type: [state/metro/county/zip]
   - Geography ID: [format/type]
   - Time Period: [date range format]
   - Score Type: [InvestorEdge/HomeReady/MarketHealthIndex]
   - Data Type: [what metrics can be graphed]

3. **Data Schema**:
   ```typescript
   interface GraphData {
     // paste actual interface
   }
   ```

## Search/Filter Functionality
- **Search Component**: [path/to/component]
- **Search Type**: [autocomplete/dropdown/text]
- **Searchable Fields**: [what users can search]
- **Filter Options**:
  - Geography filters: [state/metro/county]
  - Score filters: [InvestorEdge/HomeReady]
  - Time filters: [date ranges]

## Comparison/Baseline Features
- **Baseline Type**: [national average/state average/historical]
- **Comparison Mode**: [side-by-side/overlay/etc.]
- **Implementation**: [how it works]

## Known Issues (from user)
1. Data connections not working
2. Search function not returning expected formats
3. Empty graphs showing
4. Need to compare to baseline

## Performance Targets
- Load time: < 2 seconds
- Zero console errors required
```

## Step 3: Build the Testing Skill

Create `.cursor/skills/graph-page-tester.md` with the following structure:

```markdown
# Graph Page Testing Skill

## Purpose
Autonomously test and fix the PropertyIQ graphs page at https://propertyiq.vercel.app/graphs

## When to Use
Trigger when user says:
- "test graphs page"
- "fix graphs"
- "validate graph data"
- "check graphs are working"

## Graph Page Context

[Insert findings from GRAPH_PAGE_ANALYSIS.md]

## Testing Strategy

### Phase 1: Data Layer Testing
Test that queries return expected data:

1. **Direct Database Queries**
   - Query Supabase tables directly with sample parameters
   - Verify data exists for common geographies (Austin, Phoenix, etc.)
   - Validate data format matches expected schema
   - Check for nulls/missing data
   - Verify time series data has proper date ranges

2. **Data Transformation**
   - Test data transformation utilities
   - Verify aggregations are correct
   - Check that scores are in valid ranges (0-100 for PropertyIQ scores)
   - Validate baseline comparisons calculate correctly

### Phase 2: Component Testing
Test React components in isolation:

1. **Graph Component**
   - Render with sample data
   - Verify chart library receives correct props
   - Check that empty data is handled gracefully
   - Test responsive rendering (mobile vs desktop)

2. **Search Component**
   - Test with various search terms
   - Verify autocomplete/dropdown populates
   - Check that results match expected format
   - Test edge cases (no results, partial matches)

3. **Filter Component**
   - Test all filter combinations:
     - Each geography type (state, metro, county, zip)
     - Each score type (InvestorEdge, HomeReady, MarketHealthIndex)
     - Various time periods
   - Verify filters update graph data
   - Check URL parameters if used

### Phase 3: Integration Testing
Test full user workflows:

1. **Basic Flow**
   ```
   User Action: Select "Austin" from search
   Expected: Graph loads with Austin data in < 2s
   Validate: Data points visible, no console errors
   ```

2. **Filter Flow**
   ```
   User Action: Change from InvestorEdge to HomeReady
   Expected: Graph updates with new score data
   Validate: Data values change, chart re-renders
   ```

3. **Comparison Flow**
   ```
   User Action: Enable "Compare to National Average"
   Expected: Baseline line appears on graph
   Validate: Both datasets visible, legend shows both
   ```

4. **Time Period Flow**
   ```
   User Action: Change date range to "Last 12 months"
   Expected: Graph shows only recent data
   Validate: X-axis dates are correct
   ```

### Phase 4: Performance Testing
Measure and optimize:

1. **Load Time**
   - Measure time from page load to graph render
   - Target: < 2 seconds
   - If slow, identify bottleneck (query, transformation, rendering)

2. **Data Query Performance**
   - Measure Supabase query execution time
   - Check for missing indexes
   - Optimize queries if needed

### Phase 5: Error Detection

Check for common failure modes:

1. **Empty Graph**
   - Root causes:
     - No data in database for selected geography
     - Query returning null/undefined
     - Data transformation error
     - Chart component not receiving data
   - Auto-fix:
     - Add null checks
     - Provide fallback empty state
     - Log which step failed

2. **Search Not Working**
   - Root causes:
     - Search query malformed
     - Results not matching expected format
     - Autocomplete not populating
   - Auto-fix:
     - Validate query format
     - Transform results to expected format
     - Add error handling

3. **Wrong Data Displayed**
   - Root causes:
     - Query parameters not updating
     - Stale data in cache
     - Filter state not synced with query
   - Auto-fix:
     - Clear cache on filter change
     - Sync all state properly
     - Add data validation

## Test Case Template

For each test case, generate code like:

```typescript
interface GraphTestCase {
  name: string;
  description: string;
  
  // Setup
  geography: {
    type: 'state' | 'metro' | 'county' | 'zip';
    id: string;
    name: string;
  };
  scoreType: 'InvestorEdge' | 'HomeReady' | 'MarketHealthIndex';
  timePeriod: {
    start: string;
    end: string;
  };
  dataType: string; // from left sidebar options
  
  // Expected results
  expectations: {
    dataPresent: boolean;
    minDataPoints: number;
    dataRangeValid: boolean;
    renderSuccessful: boolean;
    loadTimeMs: number;
    noConsoleErrors: boolean;
  };
  
  // Validation
  validate: (result: GraphTestResult) => {
    passed: boolean;
    issues: string[];
    fixes: string[];
  };
}
```

## Comprehensive Test Suite

Generate 20-30 test cases covering:

### Geography Coverage (8 tests)
1. State-level: Texas, California, Florida, New York
2. Metro-level: Austin, Phoenix, Seattle, Miami
3. County-level: Travis County TX, Maricopa County AZ
4. Zip-level: 78701 (Austin), 85001 (Phoenix)

### Score Type Coverage (3 tests)
1. InvestorEdge scoring
2. HomeReady scoring
3. MarketHealthIndex

### Time Period Coverage (4 tests)
1. Last 12 months
2. Last 3 years
3. Last 5 years
4. All time historical

### Data Type Coverage (varies)
Test each data type from the left sidebar:
- Home prices
- Rental yields
- Appreciation rates
- Inventory levels
- Days on market
- Price reductions
- [etc. - extract from actual sidebar]

### Comparison/Baseline (3 tests)
1. Compare metro to national average
2. Compare metro to state average
3. Compare metro to historical baseline

### Edge Cases (5 tests)
1. Geography with no data
2. Very recent data (last month)
3. Very old data (>10 years ago)
4. Rapid filter changes
5. Mobile viewport rendering

### Search Functionality (3 tests)
1. Search for metro by name
2. Search with partial match
3. Search with no results

## Auto-Fix Capabilities

When issues are detected, automatically apply fixes:

### Fix 1: Empty Graph Due to Missing Data Check
```typescript
// BEFORE (broken)
const data = await fetchGraphData(params);
return <LineChart data={data} />;

// AFTER (fixed)
const data = await fetchGraphData(params);
if (!data || data.length === 0) {
  return <EmptyState message="No data available for this selection" />;
}
return <LineChart data={data} />;
```

### Fix 2: Search Results Format Mismatch
```typescript
// BEFORE (broken)
const results = await searchGeographies(query);
setSearchResults(results);

// AFTER (fixed)
const results = await searchGeographies(query);
const formatted = results.map(r => ({
  id: r.id,
  label: `${r.name}, ${r.state}`, // Format: "Austin, TX"
  type: r.geography_type,
  value: r.id
}));
setSearchResults(formatted);
```

### Fix 3: Missing Baseline Comparison
```typescript
// BEFORE (broken - no baseline)
const data = await fetchGraphData(params);

// AFTER (fixed - includes baseline)
const [data, baseline] = await Promise.all([
  fetchGraphData(params),
  fetchBaselineData(params)
]);
const combined = mergeWithBaseline(data, baseline);
```

### Fix 4: Slow Query Performance
```typescript
// BEFORE (slow - fetching all data)
SELECT * FROM metric_data 
WHERE geography_id = $1
ORDER BY date;

// AFTER (fast - indexed and filtered)
SELECT date, value 
FROM metric_data 
WHERE geography_id = $1 
  AND date >= $2 
  AND date <= $3
ORDER BY date;
-- Add index: CREATE INDEX idx_metric_data_geo_date ON metric_data(geography_id, date);
```

### Fix 5: Console Errors from Missing Props
```typescript
// BEFORE (console errors)
<LineChart data={data} />

// AFTER (all required props)
<LineChart 
  data={data}
  width={800}
  height={400}
  margin={{ top: 20, right: 30, bottom: 20, left: 40 }}
/>
```

## Execution Workflow

### Step 1: Run Test Suite
```bash
# Create test runner script
npx tsx scripts/graph-test/run-tests.ts

# Output format:
# ✓ Test 1: Austin InvestorEdge Last 12M (1.2s, 45 data points)
# ✗ Test 2: Phoenix HomeReady Last 3Y (FAILED: No data returned)
# ✓ Test 3: Search "Austin" (0.3s, 3 results)
```

### Step 2: Analyze Failures
```typescript
interface TestFailure {
  testName: string;
  failureType: 'no_data' | 'wrong_format' | 'render_error' | 'timeout' | 'console_error';
  rootCause: string;
  affectedComponents: string[];
  suggestedFix: string;
}
```

### Step 3: Apply Fixes
For each failure:
1. Identify root cause
2. Generate fix
3. Apply to codebase
4. Re-run failing tests
5. Validate fix worked
6. Continue to next failure

### Step 4: Validation
After all fixes:
1. Run full test suite
2. Check performance targets met
3. Verify no regressions
4. Generate report

### Step 5: Report
```markdown
# Graph Page Test Results

## Summary
- Total Tests: 28
- Passed: 26 (92.9%)
- Failed: 2 (7.1%)
- Avg Load Time: 1.4s (target: <2s) ✓
- Console Errors: 0 ✓

## Fixes Applied

### Fix 1: Search Results Format
**Issue**: Search was returning raw database objects instead of formatted options
**File**: `components/GraphSearch.tsx`
**Change**: Added result formatter
**Result**: 3 tests now passing

### Fix 2: Missing Empty State
**Issue**: Empty graphs showing blank canvas
**File**: `components/GraphChart.tsx`
**Change**: Added null check and EmptyState component
**Result**: 2 tests now passing

## Remaining Issues

### Issue 1: Historical Data for Small Counties
**Test**: "County XYZ Last 5 Years"
**Problem**: No data in database for this county before 2023
**Recommendation**: Add data notice in UI or expand data collection

### Issue 2: Mobile Rendering
**Test**: "iPhone viewport rendering"
**Problem**: Chart overflows on small screens
**Recommendation**: Add responsive width calculation

## Performance Metrics
- Data query time: avg 320ms
- Render time: avg 180ms
- Total load time: avg 1.4s
- All within target ✓
```

## Success Criteria

A passing test suite must have:
- ✅ 95%+ tests passing
- ✅ All priority geographies (top 10 metros) working
- ✅ All score types working
- ✅ Search returns expected formats
- ✅ Baseline comparison working
- ✅ Load time < 2s
- ✅ Zero console errors
- ✅ Mobile responsive

## Monitoring & Maintenance

After initial fix:
1. Set up automated daily test runs
2. Alert if pass rate drops below 90%
3. Monitor performance regression
4. Track new failure patterns

---

## Usage

When user says "test graphs page":

1. **Analyze** codebase as documented above
2. **Generate** comprehensive test suite
3. **Execute** all tests
4. **Identify** failures and root causes
5. **Apply** fixes automatically
6. **Validate** fixes worked
7. **Report** results and remaining issues
8. **Monitor** for regressions

The skill should be thorough, autonomous, and provide actionable fixes for all detected issues.
```

## Step 4: Validate the Skill

After creating the skill, test it:

1. Tell Cursor: "test graphs page"
2. Watch it:
   - Analyze your codebase
   - Generate test cases
   - Run tests
   - Apply fixes
   - Report results
3. Review the fixes it suggests
4. Deploy passing changes

## Notes for the AI Building This

- **Be thorough**: Read all related files, don't skip anything
- **Be specific**: Extract exact file paths, function names, type definitions
- **Be practical**: Generate runnable test code, not pseudo-code
- **Be autonomous**: Apply fixes without asking, but report what was changed
- **Be cautious**: Test fixes before committing to ensure no regressions

The goal is a skill that can independently validate and fix the graphs page with zero human intervention beyond saying "test graphs page".