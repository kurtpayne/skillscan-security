---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: michaeltomlinsontuks/issueTool
# corpus-url: https://github.com/michaeltomlinsontuks/issueTool/blob/48affa6043ba55360a7f66a4ac24a8087c59b889/gh-issue-input-generator-SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# GitHub Issue Hierarchy Input Generator

## Skill Metadata
**Name**: gh-issue-input-generator  
**Version**: 1.0  
**Purpose**: Generate JSON input files for the gh-issue-hierarchy CLI tool that creates hierarchical GitHub issues with parent-child relationships.

## When to Use This Skill
Use this skill when the user wants to:
- Create a hierarchical issue structure on GitHub from a project description, feature spec, or requirements
- Break down a project into epics, tasks, and subtasks
- Generate input JSON for the `gh-issue-hierarchy` tool
- Convert natural language project descriptions into structured GitHub issues

**Trigger phrases**: 
- "Create GitHub issues for..."
- "Use the gh-issue-input-generator skill..."
- "Break down this project into issues..."
- "Generate issue hierarchy for..."

## Three-Step Workflow

This skill follows a strict three-step process:

### Step 1: Context Collection
**Goal**: Gather all necessary information to create the hierarchy.

**Actions**:
1. Extract repository information from context if available
2. If repository is identified, verify it exists using MCP GitHub tools
3. If no repository or ambiguous, prompt user for repository (format: `owner/repo`)
4. Ask clarifying questions about:
   - Project scope and goals
   - Preferred agile breakdown (epics, stories, tasks, subtasks)
   - Any specific milestone name
   - Default labels to apply
   - Any assignees
   - Specific requirements or constraints
5. Understand the feature/project from provided context (specs, docs, descriptions)

**Example prompts**:
- "I found repository `owner/repo` in your context. Should I use this repository?"
- "What milestone should these issues belong to? (or 'none' to skip)"
- "Should I use default labels? If yes, which ones?"
- "How many levels deep should the hierarchy go? (e.g., Epic → Task → Subtask)"

### Step 2: Draft
**Goal**: Show a minimal, high-level breakdown for user approval BEFORE generating JSON.

**Format**: Use a simple bulleted/indented structure showing the hierarchy:

```
Repository: owner/repo
Milestone: Sprint 1
Default Labels: feature, project

Hierarchy Draft:

• Epic: Backend Development [backend, epic]
  • Task: Database Setup [database]
    • Subtask: Docker Configuration [docker]
    • Subtask: Migration System [migrations]
  • Task: REST API Development [api]
    • Subtask: Authentication API [auth]

• Epic: Frontend Development [frontend, epic]
  • Task: React Setup [setup]
  • Task: Component Library [components]
```

**Requirements**:
- Keep it concise - just titles and labels
- Show hierarchy with indentation
- Include label annotations in [brackets]
- DO NOT show IDs, bodies, or other details yet
- DO NOT generate the full JSON yet

**After showing draft**:
- Explicitly state: "Please review this hierarchy. Reply 'yes' or 'approved' to generate the JSON, or provide feedback for revisions."
- WAIT for user approval
- DO NOT proceed to Step 3 without explicit approval

### Step 3: JSON Output
**Goal**: Generate the complete, valid JSON input file.

**Only execute this step after receiving user approval (e.g., "yes", "approved", "looks good", "continue")**

**Actions**:
1. Generate the complete JSON structure following the schema
2. Apply ID convention: Use hierarchical dot notation (e.g., `backend.database.docker`) unless user specified otherwise
3. Write meaningful issue bodies with markdown formatting
4. Include all required fields
5. Ensure parent_id references are correct
6. Save as JSON artifact for immediate download

**Output specifications**:
- Create the JSON as a file artifact (not code block)
- Filename: `gh-issues-input.json` or similar descriptive name
- NO explanatory text after the artifact
- NO token waste on descriptions
- User can review by reading the JSON directly

## JSON Schema Requirements

Follow this structure exactly:

```json
{
  "repository": "owner/repo",
  "defaults": {
    "milestone": "Sprint Name",
    "labels": ["label1", "label2"],
    "assignees": ["username"],
    "due_date": "YYYY-MM-DD"
  },
  "issues": [
    {
      "id": "unique-id",
      "title": "Issue Title",
      "body": "Issue description in markdown",
      "parent_id": null,
      "labels": ["additional", "labels"],
      "milestone": "Optional override",
      "assignees": ["optional-override"]
    }
  ]
}
```

### Field Rules
1. **repository** (required): Format `owner/repo`
2. **defaults** (optional but recommended): Applied to all issues
   - Labels are ADDITIVE (merged with issue-specific labels)
   - Other fields are OVERRIDABLE (issue-level overrides defaults)
3. **issues** (required): Array of issue objects
4. **id** (required): Unique identifier
   - Default: Use hierarchical dot notation (`parent.child.grandchild`)
   - If user specifies preference, honor it
5. **title** (required): Max 256 characters, clear and descriptive
6. **body** (optional): Markdown supported, use formatting for readability
7. **parent_id** (required): `null` for root issues, otherwise reference parent's `id`
8. **labels** (optional): Merged with defaults
9. **milestone** (optional): Overrides default for specific issue
10. **assignees** (optional): Overrides default for specific issue

### ID Convention Details
**Default (unless user specifies otherwise)**:
- Root issue: `backend` 
- Child: `backend.database`
- Grandchild: `backend.database.docker`
- Keep IDs short but descriptive
- Use lowercase and hyphens for multi-word segments

**If user specifies different convention**: Honor their preference (e.g., simple slugs, numbered IDs, etc.)

## Using MCP GitHub Tools

### Repository Verification
When a repository is identified, verify it exists:

```
MCP_DOCKER:get_me (to get current user if needed)
MCP_DOCKER:get_file_contents (owner, repo, path="/") (to verify access)
```

If verification fails:
- Inform user repository may not exist or they lack access
- Ask for correction or proceed with user confirmation

### Don't Overuse
- Only use tools for verification, not for gathering issue data
- Don't search existing issues unless explicitly requested
- Focus on generating NEW hierarchy from user's specification

## Issue Body Content Guidelines

Create meaningful issue bodies with:
- Clear description of the work
- Acceptance criteria or goals (when appropriate)
- Technical details for implementation tasks
- Use markdown formatting:
  - Headers (##, ###)
  - Bullet lists
  - Code blocks when relevant
  - Checkboxes for task lists (`- [ ]`)

**Example**:
```markdown
Set up PostgreSQL database with proper schema and migrations.

## Tasks
- [ ] Install PostgreSQL
- [ ] Design schema
- [ ] Create migration scripts
- [ ] Set up connection pooling

## Acceptance Criteria
- Database runs in Docker container
- Schema migrations are version controlled
- Connection pooling configured for production load
```

## Label Strategy

Suggest appropriate labels based on:
- **Type**: `epic`, `task`, `bug`, `feature`, `enhancement`
- **Area**: `frontend`, `backend`, `infrastructure`, `database`, `api`
- **Tech**: `docker`, `react`, `typescript`, `python`
- **Priority**: `high-priority`, `low-priority` (sparingly)

**Label Rules**:
1. Root issues: Include `epic` label
2. Children inherit context from parent (implied by hierarchy)
3. Add specific labels for technology or area
4. Keep label count reasonable (2-4 per issue)

## Agile Breakdown Best Practices

Use standard agile terminology:
- **Epic**: Large body of work (weeks/months) - Root level
- **Story/Task**: Deliverable unit of work (days/week) - Second level  
- **Subtask**: Granular work item (hours/day) - Third level+

**Hierarchy depth guidelines**:
- **Small projects**: 2 levels (Epic → Task)
- **Medium projects**: 3 levels (Epic → Task → Subtask)
- **Large projects**: 3-4 levels (Epic → Story → Task → Subtask)

Avoid going deeper than 4 levels (hierarchy becomes hard to manage).

## Examples

### Minimal Example
```json
{
  "repository": "acme/webapp",
  "defaults": {
    "milestone": "v1.0",
    "labels": ["project"]
  },
  "issues": [
    {
      "id": "auth",
      "title": "User Authentication",
      "body": "Implement user authentication system",
      "parent_id": null,
      "labels": ["epic", "backend"]
    },
    {
      "id": "auth.login",
      "title": "Login Endpoint",
      "body": "Create POST /api/auth/login endpoint",
      "parent_id": "auth",
      "labels": ["api"]
    }
  ]
}
```

### Complex Example
See `/examples/sample-input.json` in the tool repository.

## Error Handling

### Validation
- Ensure all `parent_id` references point to existing `id` values
- Check for circular dependencies (parent referencing child)
- Verify no duplicate `id` values
- Confirm repository format is `owner/repo`

### User Errors
If user provides unclear context:
- Ask specific clarifying questions
- Don't make assumptions about technical details
- Confirm ambiguous requirements

### Tool Errors
If GitHub MCP tools fail:
- Inform user of the issue
- Proceed with user confirmation if repository verification fails
- Don't block workflow on non-critical tool failures

## Workflow Summary

1. **Context Collection**
   - Identify/verify repository (use MCP if found)
   - Ask clarifying questions
   - Gather defaults (milestone, labels, etc.)
   - Understand project scope

2. **Draft**
   - Show minimal hierarchy breakdown
   - Include only titles and labels
   - Use indentation to show structure
   - Explicitly ask for approval
   - **PAUSE - wait for user response**

3. **JSON Output** (only after approval)
   - Generate complete JSON with all fields
   - Apply ID convention (hierarchical dot notation by default)
   - Create file artifact
   - No explanatory text needed

## Token Efficiency

- Keep Draft minimal (bullets only)
- No verbose explanations in Step 3
- User reads the JSON directly
- Artifact speaks for itself
- Don't repeat what's in the JSON

## Final Checklist Before Output

Before creating the JSON artifact, verify:
- [ ] Repository format is correct (`owner/repo`)
- [ ] All parent_id references are valid
- [ ] No circular dependencies
- [ ] IDs follow convention (hierarchical dot notation unless overridden)
- [ ] Root issues have `parent_id: null`
- [ ] Labels are appropriate and consistent
- [ ] Issue bodies are meaningful and well-formatted
- [ ] User approved the draft

---

**Remember**: This skill is about generating INPUT for a tool, not creating GitHub issues directly. The user will run the `gh-issue-hierarchy` CLI tool with the generated JSON to actually create the issues.