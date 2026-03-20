---
name: commonpaper
description: Query and manage contracts via the Common Paper REST API. Use when the user asks about their contracts, agreements, signers, NDAs, CSAs, renewals, deal values, or wants to create/void/reassign agreements. Also use when user mentions "Common Paper", "commonpaper", or asks contract-related questions like "how many signed contracts do I have?" or "do I have an NDA with X?".
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: CommonPaper/claude-skill
# corpus-url: https://github.com/CommonPaper/claude-skill/blob/c6f3094be06c9c72acd9a8fce891c7f8ca1ab788/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Common Paper API Skill

## Security Rules

**CRITICAL — follow these rules at all times:**

1. **NEVER display, echo, or include the API token in chat output.** Do not print credentials in responses, code blocks, or explanations unless the user explicitly asks to see them.
2. **NEVER pass the API token as a literal string in command-line arguments.** Always read it from the credentials file via command substitution (see Making Requests below) so the token value is not visible in the command text shown to the user.
3. **When showing the user a curl command** (e.g., if they ask "what query did you use?"), replace the auth header with a placeholder like `-H "Authorization: Bearer $CP_TOKEN"`. Never substitute in the real value. Always URL-encode brackets as `%5B` and `%5D` in the shown command so it can be copy-pasted into zsh without errors.
4. **Sanitize user inputs** before inserting into URLs. Strip or URL-encode any characters that could break the URL or be used for injection (e.g., `&`, `=`, `#`, `?`, newlines, backticks, `$()`, semicolons). Only allow alphanumeric characters, spaces, dots, commas, hyphens, and common punctuation in filter values.
5. **Validate credential format** before saving. The API token should match the pattern `zpka_*` and contain only alphanumeric characters and underscores.

## Authentication

The API uses Bearer token authentication. Only an API token is required — the organization is inferred from the token. No Organization ID header is needed.

### Credential Loading

Before making any API call, check if a saved token exists:

```bash
cat ~/.claude/skills/commonpaper/cp-api-token 2>/dev/null
```

If the file exists and is non-empty, use its contents as the token. **Do not echo or display the value to the user.**

If the file does not exist or is empty, ask the user:

- **API Token**: "What is your Common Paper API token? (You can generate one from your account's Integrations tab)"

### Credential Validation

Before saving or using the token, validate it:

- Must contain only alphanumeric characters and underscores

After receiving and validating the token, test it with a lightweight API call:

```bash
curl -s -H "Authorization: Bearer $(cat ~/.claude/skills/commonpaper/cp-api-token)" "https://api.commonpaper.com/v1/agreements?page%5Bsize%5D=1" -o /dev/null -w "%{http_code}"
```

If the response is not `200`, inform the user that their token appears invalid and ask them to double-check.

### Saving Credentials

After successful validation, ask: "Would you like me to save this token for future sessions?"

If yes:

```bash
echo -n "THE_TOKEN" > ~/.claude/skills/commonpaper/cp-api-token && chmod 600 ~/.claude/skills/commonpaper/cp-api-token
```

### Making Requests

**All API requests MUST read the token from the credentials file via command substitution to avoid exposing it as a literal in the command.**

```bash
curl -s -H "Authorization: Bearer $(cat ~/.claude/skills/commonpaper/cp-api-token)" \
  "https://api.commonpaper.com/v1/agreements"
```

For POST/PATCH requests, add:
```bash
-H "Content-Type: application/json"
```

**Base URL**: `https://api.commonpaper.com/v1`

**IMPORTANT — URL encoding**: Always URL-encode square brackets in query parameters. Use `%5B` for `[` and `%5D` for `]`. Unencoded brackets will cause `zsh: no such file or directory` errors.

**Note**: While `$(cat ~/.claude/skills/commonpaper/cp-api-token)` is expanded by the shell before execution (so the token briefly appears in the process list), this is significantly better than having the literal token in the command text shown in chat. The token file is also chmod 600 so only the user can read it.

## Endpoints

### List Agreements (Primary endpoint for queries)

```
GET /v1/agreements
```

Returns JSONAPI format with pagination metadata:
```json
{
  "data": [ { "id": "...", "type": "agreement", "attributes": { ... }, "links": { ... } } ],
  "meta": { "pagination": { "current": 1, "next": 2, "last": 5, "records": 127 } },
  "links": { "self": "...", "next": "...", "last": "..." }
}
```

**Key response fields:**
- `meta.pagination.records` — total number of matching agreements (use this for counts instead of paginating through all results)
- `data[].attributes` — agreement fields
- `data[].attributes.display_status` — human-friendly status (e.g., "Completed", "Waiting for counterparty") — prefer this over `status` when presenting to users
- `data[].links.agreement_url` — direct link to the agreement in the Common Paper app

### Get Single Agreement

```
GET /v1/agreements/{id}
```

### Create Agreement

```
POST /v1/agreements
```

**IMPORTANT**: The create endpoint does NOT use JSONAPI format. It uses a flat structure with these top-level keys:

```json
{
  "owner_email": "owner@company.com",
  "template_id": "uuid-of-template",
  "agreement": {
    "agreement_type": "NDA",
    "sender_signer_name": "Jane Smith",
    "sender_signer_title": "CEO",
    "sender_signer_email": "jane@company.com",
    "recipient_email": "recipient@example.com",
    "recipient_name": "John Doe"
  }
}
```

**Required fields:**
- `owner_email` — email of the user who will own this agreement (must be a user in the org)
- `template_id` — UUID of the template to use (get from `GET /v1/templates`)
- `agreement.recipient_email` — recipient's email address
- `agreement.recipient_name` — recipient's name (REQUIRED — will error without it)

**Optional but recommended fields:**
- `agreement.sender_signer_name`, `agreement.sender_signer_title`, `agreement.sender_signer_email`
- `agreement.recipient_organization`, `agreement.recipient_title`
- `agreement.agreement_type` — NDA, CSA, etc.
- `agreement.test_agreement` — set to `true` to send a test agreement

**Billing fields:**
- `agreement.include_billing_workflow` — set to `true` to enable a billing workflow after signing
- `agreement.billing_workflow_type` — `"link"` or `"stripe"`
- `agreement.payment_link_url` — payment URL shown after signing; requires `include_billing_workflow: true` and `billing_workflow_type: "link"`
- `agreement.include_automated_payment_reminders` — boolean; sends automatic payment reminders when true
- `agreement.include_billing_info` — boolean; enables billing contact fields
- `agreement.billing_name` — billing contact name; used when `include_billing_info` is true
- `agreement.billing_email` — billing contact email; used when `include_billing_info` is true

**Governing law fields:**
- `agreement.governing_law_country` — country whose laws govern the agreement (e.g., `"United States of America"`)
- `agreement.governing_law_region` — state or region whose laws govern the agreement (e.g., `"Delaware"`)
- `agreement.chosen_courts_country` — country where disputes will be resolved
- `agreement.chosen_courts_region` — state or region where disputes will be resolved
- `agreement.district_or_county` — district or county for dispute resolution

**Notice email fields:**
- `agreement.sender_notice_email_address` — email for legal notices to the sender
- `agreement.recipient_notice_email_address` — email for legal notices to the recipient

**Framework terms fields:**
- `agreement.framework_terms_type` — `"new"` (standard) or `"description"` (custom)
- `agreement.framework_terms_description` — custom framework terms; only used when `framework_terms_type` is `"description"`

**Other fields:**
- `agreement.manual_send` — set to `true` to mark the agreement as manually sent outside the platform

### Agreement Actions

```
PATCH /v1/agreements/{id}/void          — Void an agreement
PATCH /v1/agreements/{id}/reassign      — Reassign recipient
PATCH /v1/agreements/{id}/resend_email  — Resend signature email
GET   /v1/agreements/{id}/history       — Get agreement history
GET   /v1/agreements/{id}/download_pdf  — Download PDF
GET   /v1/agreements/{id}/shareable_link — Get shareable link
```

### Templates

```
GET /v1/templates          — List all templates
GET /v1/templates/{id}     — Get single template
```

Templates have a `type` field indicating the agreement type: `template_nda`, `template_csa`, `template_dpa`, `template_design`, `template_psa`, `template_partnership`, `template_baa`, `template_loi`, `template_software_license`, `template_pilot`.

When creating an agreement, look up the appropriate template by matching the `type` field. For example, to send an NDA, find the template where `type == "template_nda"`.

### Other Endpoints

```
GET /v1/users              — List organization users
GET /v1/users/{id}         — Get single user
GET /v1/agreement_types    — List all agreement types
GET /v1/agreement_statuses — List all agreement statuses
GET /v1/agreement_history  — List agreement histories (filterable)
POST /v1/attachments       — Upload attachment
```

### Users

The `/v1/users` endpoint returns user details including `name`, `email`, and `title`. Use this to look up sender information when creating agreements — the user may only provide an email, and you can fill in name/title from the user record.

## Filtering (Ransack)

The API supports filtering via query parameters using ransack predicates. The syntax is `filter[field_predicate]=value`.

### Predicates

| Predicate | Meaning | Example |
|-----------|---------|---------|
| `_eq` | Equals | `filter[status_eq]=signed` |
| `_not_eq` | Not equal | `filter[status_not_eq]=draft` |
| `_cont` | Contains (case-insensitive) | `filter[recipient_organization_cont]=microsoft` |
| `_i_cont` | Contains (case-insensitive, explicit) | `filter[recipient_organization_i_cont]=google` |
| `_gt` | Greater than | `filter[effective_date_gt]=2024-01-01` |
| `_lt` | Less than | `filter[end_date_lt]=2025-12-31` |
| `_gteq` | Greater than or equal | `filter[end_date_gteq]=2025-01-01` |
| `_lteq` | Less than or equal | `filter[end_date_lteq]=2025-12-31` |
| `_present` | Field is not null/empty | `filter[end_date_present]=true` |
| `_blank` | Field is null/empty | `filter[end_date_blank]=true` |
| `_in` | In a list | `filter[status_in][]=signed&filter[status_in][]=sent_to_recipient_for_signature` |
| `_null` | Is null | `filter[end_date_null]=true` |
| `_not_null` | Is not null | `filter[end_date_not_null]=true` |

### Combining Filters

Chain multiple filter params: `filter[status_eq]=signed&filter[agreement_type_eq]=NDA`

### Filterable Fields on Agreements

All agreement columns are filterable, including nested model fields prefixed with the model name. Key fields:

**Identity & Type:**
- `agreement_type` — NDA, CSA, DPA, PSA, Design, Partnership, BAA, LOI, Software License, Amendment, Pilot (or custom)
- `status` — see Agreement Statuses below
- `description`

**Parties:**
- `sender_signer_name`, `sender_signer_email`, `sender_signer_title`
- `sender_organization`
- `recipient_name`, `recipient_email`, `recipient_title`
- `recipient_organization`

**Dates:**
- `effective_date` — when the agreement takes effect
- `end_date` — expiration date
- `sent_date` — when it was sent
- `all_signed_date` — when fully executed
- `sender_signed_date`, `recipient_signed_date`

**Terms:**
- `term` — term length (integer, in units of term_period)
- `term_period_perpetual` — boolean
- `purpose`
- `governing_law_country`, `governing_law_region`

**Financial:**
- `ai_gmv` — gross contract value (available on all agreement types, useful for sorting by deal size)
- `ai_arr` — annual recurring revenue
- `csa_order_form_total_contract_value` — total contract value (CSA-specific)
- `csa_order_form_subscription_fee` — subscription fee amount
- `csa_order_form_payment_period` — payment frequency

**Roles (nested):**
- `agreement_roles_user_email` — filter by user email in any role

**Other nested models:**
- `csa_*`, `csa_order_form_*`, `dpa_*`, `design_partner_*`, `psa_*`, `psa_statement_of_work_*`, `partnership_*`, `partnership_business_terms_*`, `baa_*`, `loi_*`

## Agreement Statuses

The `status` field contains the internal status. The `display_status` field contains a human-readable version. Prefer `display_status` when presenting results to users.

Internal statuses:
- `draft` — Not yet sent
- `sent_waiting_for_initial_review` — Sent, awaiting first review
- `sent_waiting_for_sender_review` — Waiting for sender to review
- `sent_waiting_for_recipient_review` — Waiting for recipient to review
- `in_progress` — Active negotiation
- `sent_to_recipient_for_signature` — Sent for recipient signature
- `sent_to_sender_signer_for_signature` — Sent for sender signature
- `waiting_for_sender_signature` — Awaiting sender signature
- `waiting_for_recipient_signature` — Awaiting recipient signature
- `signed` — Fully executed (display_status: "Completed")
- `signed_waiting_for_final_confirmation` — Signed, pending confirmation
- `declined_by_recipient` — Recipient declined
- `voided_by_sender` — Voided
- `sent_manually` — Sent outside the platform

**Signed/active** = `status_eq=signed`
**In-flight** = any status that is not `draft`, `signed`, `voided_by_sender`, or `declined_by_recipient`

## Pagination

Index endpoints return pagination metadata in `meta.pagination`:
- `records` — total number of matching results (use this for counts!)
- `current` — current page number
- `next` — next page number (null if on last page)
- `last` — last page number

Use `page[number]=N&page[size]=M` query params (URL-encoded: `page%5Bnumber%5D=N&page%5Bsize%5D=M`). Default page size is 25.

**For counting**: Use `page%5Bsize%5D=1` and read `meta.pagination.records` — no need to paginate through all results.

**For complete lists**: Paginate through all pages when the user wants a full list. Check for `meta.pagination.next` and keep fetching until it's null.

## Common Query Patterns

In all examples below, `$AUTH` refers to `-H "Authorization: Bearer $(cat ~/.claude/skills/commonpaper/cp-api-token)"`.

### "How many signed contracts do I have?"

```bash
curl -s $AUTH \
  "https://api.commonpaper.com/v1/agreements?filter%5Bstatus_eq%5D=signed&page%5Bsize%5D=1" | jq '.meta.pagination.records'
```

### "Do I have any contracts with {Company}?"

Use `_cont` for case-insensitive partial matching on `recipient_organization`. Also check `sender_organization` in case the user's org is the recipient.

### "Do I have an active NDA with {Company}?"

Combine agreement type, status, and company filters. An "active" NDA is signed and not expired:

```
filter[agreement_type_eq]=NDA&filter[status_eq]=signed&filter[recipient_organization_cont]={Company}&filter[expired_eq]=false
```

### "Who was the signer on the {Company} account?"

Find agreements with that company and extract signer info from attributes: `sender_signer_name`, `sender_signer_email`, `recipient_name`, `recipient_email`.

### "Largest CSA deal by total contract amount?"

Fetch all signed CSAs and sort client-side by `ai_gmv` with `jq`:

```bash
curl -s $AUTH \
  "https://api.commonpaper.com/v1/agreements?filter%5Bagreement_type_eq%5D=CSA&filter%5Bstatus_eq%5D=signed&page%5Bsize%5D=100" \
  | jq '[.data[] | {counterparty: .attributes.recipient_organization, gmv: (.attributes.ai_gmv // "0" | tonumber), summary: .attributes.summary}] | sort_by(-.gmv)'
```

Note: `ai_gmv` may be `"0"` or null for some agreements even if fees exist — check the `summary` field and nested fee data (`csa_order_form.fees`) for the full picture.

### "Upcoming renewal dates?"

```bash
curl -s $AUTH \
  "https://api.commonpaper.com/v1/agreements?filter%5Bstatus_eq%5D=signed&filter%5Bend_date_gteq%5D=$(date +%Y-%m-%d)&sort=end_date&page%5Bsize%5D=100"
```

Present results as a table with columns: Agreement Type, Counterparty, End Date, Term.

## Response Handling

### Presenting Results

- Format results as readable tables or summaries
- Use `display_status` (not `status`) when showing status to users
- For agreement lists, include: Agreement Type, Counterparty (recipient_organization), Status (display_status), Effective Date, End Date
- For signer queries, include: Name, Email, Title, Organization
- For financial queries, include currency amounts formatted properly
- When counting, give exact numbers from `meta.pagination.records`
- For date-based reports, sort chronologically and group logically
- Include `links.agreement_url` when the user might want to view the agreement in the app

### Error Handling

- **400 Bad Request**: Check the request body schema — the create endpoint uses a specific format (see Create Agreement above), not JSONAPI.
- **401 Unauthorized**: Token is invalid or expired. Ask the user to check their API token.
- **403 Forbidden**: Token may not have the required permissions.
- **404 Not Found**: The agreement or resource doesn't exist.
- **422 Unprocessable Entity**: Invalid filter or request body. Check the filter syntax.

## Write Operations

### Create Agreement

To create and send an agreement:

1. **Look up the sender** using `GET /v1/users` to get their name, title, and email
2. **Look up the template** using `GET /v1/templates` and find the one matching the desired type (e.g., `type == "template_nda"`)
3. **Confirm details** with the user before sending
4. **POST to `/v1/agreements`**:

```bash
curl -s -H "Authorization: Bearer $(cat ~/.claude/skills/commonpaper/cp-api-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "owner_email": "owner@company.com",
    "template_id": "uuid-of-template",
    "agreement": {
      "agreement_type": "NDA",
      "sender_signer_name": "Jane Smith",
      "sender_signer_title": "CEO",
      "sender_signer_email": "jane@company.com",
      "recipient_email": "recipient@example.com",
      "recipient_name": "John Doe"
    }
  }' \
  "https://api.commonpaper.com/v1/agreements"
```

The agreement will be created and sent immediately. The response includes the agreement URL in `data.links.agreement_url`.

### Void Agreement

Always confirm with the user before voiding.

### Reassign Recipient

Requires `recipient_email` and `recipient_name` in the request body.

### Resend Email

Simple PATCH to `/v1/agreements/{id}/resend_email`.

## Workflow

1. **Load or request credentials** (check saved token file first)
2. **Validate token** with a test API call if this is the first use
3. **Understand the user's question** — map it to the right endpoint and filters
4. **Sanitize any user-provided filter values** — URL-encode and strip dangerous characters
5. **Make API call(s)** — read token from file via `$(cat ...)`, use filtering to narrow results server-side when possible
6. **Paginate if needed** — for counts, just read `meta.pagination.records`; for full lists, paginate through all pages
7. **Present results clearly** — tables, summaries, or direct answers. **Never include credentials in output.**
8. **For write operations** — look up user/template info first, confirm details with user, then execute

## Notes

- **NEVER expose the API token in chat output or as a literal in commands**
- **Always URL-encode square brackets** in query parameters — use `%5B` for `[` and `%5D` for `]`. Unencoded brackets cause zsh errors.
- The `_cont` predicate is the best choice for company name searches since it handles partial and case-insensitive matching
- When a user asks about a company, search both `recipient_organization` and `sender_organization` fields since either party could be the counterparty
- For "active" or "current" agreements, filter on `status_eq=signed` combined with `expired_eq=false` or `end_date_gteq={today}`
- The API returns JSONAPI format for reads — data is in `response.data[].attributes`
- The API uses a **different format for creates** — NOT JSONAPI. Use `owner_email`, `template_id`, and `agreement` as top-level keys.
- Use `jq` for parsing JSON responses in curl commands
- When showing users the curl command you used, replace the auth header with `$CP_TOKEN` placeholder and ensure brackets are URL-encoded
- Use `display_status` instead of `status` when presenting results to users
- The `summary` field on agreements contains a human-readable summary of key terms — useful for quick overviews