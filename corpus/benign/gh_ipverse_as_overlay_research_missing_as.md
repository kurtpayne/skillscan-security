---
name: research-missing-as
description: Research a missing AS entry for overlay.json. Investigates BGP announcements, prefix ownership, and AS paths to identify organization and country. Invoke with /research-missing-as {ASN}
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: ipverse/as-overlay
# corpus-url: https://github.com/ipverse/as-overlay/blob/d4ee3827102bb176279a7647787a74857d024135/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Research Missing AS

## Background

An AS (Autonomous System) is a network or collection of networks under a single administrative entity, identified by a unique ASN (Autonomous System Number). ASes exchange routing information via BGP (Border Gateway Protocol) to enable internet traffic to flow between networks. Each AS announces IP prefixes (address blocks) it controls to its BGP peers.

AS metadata (organization name, country, handle) is typically published in RIR (Regional Internet Registry) databases. However, some ASes actively announce prefixes via BGP without publishing proper WHOIS metadata - these are the entries we need to research.

## Your Role

You are a community contributor researching an AS entry to add to `overlay.json`. Your goal is to find the organization name and country for an AS that has actively announced BGP prefixes but no published metadata.

**Important**: Research only ONE AS at a time. Each PR should contain data for a single AS only. Do not submit another PR until the previous one has been merged.

## Instructions

### Step 1: Parse and Validate

Extract the ASN from the user's argument (e.g., `/research-missing-as 11636` means ASN 11636).

If the user provides a prefix, note it for Step 3 (e.g., `/research-missing-as 11636 38.99.129.0/24`).

If `missing.json` is available, verify:
- The ASN exists in the file
- The entry has `"missing": "all"`

If the file is unavailable or the ASN isn't in it, proceed anyway - the research is still valuable.

### Step 2: Initial Discovery

Start with these sources (suggested order, but adapt as needed):

1. **BGP.HE.NET** - `https://bgp.he.net/AS{ASN}`
   - Look for: announced prefixes, upstream ASes, peer ASes, any descriptive text
   - **Important**: Note the list of IPv4/IPv6 prefixes being announced - these are critical for Step 3
   - If the user provided a prefix, you can skip this step

2. **RDAP on prefix** - Query the announced prefix (see Step 3 for endpoints)
   - Often more reliable than ASN lookup for missing entries

3. **RDAP on ASN** - `https://rdap.arin.net/registry/autnum/{ASN}` (or appropriate RIR)
   - Query the ASN directly for any registered metadata

4. **PeeringDB** - `https://www.peeringdb.com/asn/{ASN}`
   - Look for: organization name, country, network type

5. **RADb/IRR** - `whois -h whois.radb.net AS{ASN}`
   - Check for route objects with organization info

6. **Reverse DNS** - `dig -x {first-ip-in-prefix} +short`
   - PTR records may reveal organization

Record all findings. If any source has complete data, you may have enough already.

**Be creative.** If standard sources fail, try:
- Web search for the IP address with prefix (e.g., "38.99.129.0/24")
- Web search for the IP address without prefix (e.g., "38.99.129.0")
- Web search for the ASN with common terms (e.g., "AS11636 network")
- Geofeed files from upstream providers (often linked in WHOIS comments)
- Looking up domains hosted on IPs in the prefix

The goal is identification - use whatever legitimate sources help achieve it.

### Step 3: Prefix Ownership Investigation

**This step is critical when ASN metadata is missing.** The announced prefixes often reveal the organization.

For each announced prefix found in Step 2 (or provided by user):

1. **Query the prefix via RDAP** (not the ASN):
   - **ARIN**: `https://rdap.arin.net/registry/ip/{prefix}`
   - **RIPE**: `https://rdap.db.ripe.net/ip/{prefix}`
   - **APNIC**: `https://rdap.apnic.net/ip/{prefix}`
   - **LACNIC**: `https://rdap.lacnic.net/rdap/ip/{prefix}`
   - **AFRINIC**: `https://rdap.afrinic.net/rdap/ip/{prefix}`

2. **Check for sub-allocations**: If the RDAP response shows a parent block (e.g., a /8 owned by a large provider like Cogent), the prefix may be a customer reassignment. Look for:
   - `parentHandle` or parent network references
   - rwhois referral servers mentioned in comments (e.g., `rwhois.cogentco.com:4321`)
   - Geofeed URLs in comments (e.g., `https://geofeed.cogentco.com/geofeed.csv`)

3. Record:
   - Organization name from allocation/reassignment record
   - Country code from allocation record
   - Any handle/identifier

If RDAP only returns the parent block with no reassignment info, note this as a dead end for that source.

### Step 4: AS Path Analysis

If the country is still unclear after Steps 2-3, analyze BGP relationships:

1. From BGP.HE.NET, identify the upstream providers
2. Research where those upstreams operate:
   - If all upstreams are regional ISPs in one country, the AS is likely there
   - Example: All upstreams are South African ISPs = AS is likely in ZA
3. Check peer relationships for additional geographic clues

### Step 5: Synthesize Findings

Based on all gathered evidence:

1. **Determine organization name**: Use the most authoritative source (RIR allocation > PeeringDB > BGP description)

2. **Determine country code**: Must be ISO 3166-1 alpha-2 (e.g., US, DE, BR, ZA)
   - Cross-reference multiple sources for confidence
   - RIR allocation country is usually definitive

3. **Generate handle** if none was found:
   - Based on organization name
   - UPPERCASE
   - No spaces (use hyphens)
   - Keep it short (e.g., "Acme Corporation" → "ACME-NET" or "ACME-CORP")

### Step 6: Prepare Output

Format the overlay.json entry with fields in this exact order:

```json
{ "asn": {asn}, "handle": "{HANDLE}", "description": "{Organization Name}", "countryCode": "{CC}", "reason": "missing" }
```

Format the PR description:

```markdown
Adding AS{ASN} - missing from WHOIS but actively announcing prefixes

**Sources:**
- BGP.HE.NET: https://bgp.he.net/AS{ASN} shows active announcements
- PeeringDB: https://www.peeringdb.com/asn/{ASN} [findings]
- {RIR} RDAP: {prefix} allocated to {org} in {country}
- [Additional sources used]

**Evidence summary:**
- Organization: {how determined}
- Country: {how determined}
```

Present both the overlay.json entry and PR description to the user for review. Do NOT modify any files until the user approves.

## Research Exhausted

Sometimes an AS cannot be identified despite thorough research. This is a valid outcome.

**Declare research exhausted when ALL of these return no useful data:**

| Source | Query | Expected Result |
|--------|-------|-----------------|
| ARIN RDAP (ASN) | `rdap.arin.net/registry/autnum/{ASN}` | null or no org name |
| ARIN RDAP (prefix) | `rdap.arin.net/registry/ip/{prefix}` | Parent block only, no reassignment |
| PeeringDB | `peeringdb.com/asn/{ASN}` | No entry |
| BGP.HE.NET | `bgp.he.net/AS{ASN}` | Empty description |
| RADb/IRR | `whois -h whois.radb.net AS{ASN}` | No entries |
| Reverse DNS | `dig -x {ip} +short` | No PTR or generic PTR |

**When research is exhausted, report to the user:**

```markdown
## Research Exhausted for AS{ASN}

Unable to identify the organization behind AS{ASN}. All primary sources returned no metadata:

| Source | Result |
|--------|--------|
| ARIN RDAP (ASN) | {result} |
| ARIN RDAP (prefix) | {result} |
| PeeringDB | {result} |
| BGP.HE.NET | {result} |
| RADb/IRR | {result} |
| Reverse DNS | {result} |

**Announced prefixes:** {list prefixes}
**Upstream providers:** {list upstreams if known}

**Recommendation:** Skip this AS for now. Options to revisit:
1. Monitor for future WHOIS updates
2. Contact upstream provider ({upstream}) for customer info
3. Check again in 3-6 months

This AS cannot be added to overlay.json without organization identification.
```

**Do NOT fabricate or guess organization names.** Only create overlay.json entries when there is documented evidence of the organization's identity.

**Do NOT include templates in research results.** When reporting findings (successful or exhausted), fill in all values with actual data. Never show placeholders like `{ASN}`, `{prefix}`, or `{result}` in output to the user.

## Data Freshness

Be mindful of stale data. AS metadata changes over time:
- Organizations get acquired or renamed
- Prefixes get reassigned to different entities
- Country registrations change when companies relocate

**Always prefer recent data:**
- Check dates on RIR records (look for "last modified" or "changed" fields)
- BGP.HE.NET shows when prefixes were first/last seen - prefer actively announced prefixes
- If PeeringDB data conflicts with recent RIR records, the RIR is likely more current
- Historical whois data may be outdated - cross-reference with current BGP state

**Red flags for stale data:**
- Prefix not currently announced (check BGP.HE.NET for "not announced" status)
- RIR record unchanged for many years while other sources show different info
- Organization name doesn't match current corporate records

When sources conflict, weight recent evidence more heavily than historical records.

## Data Sources

### Primary Sources (USE THESE)
- **PeeringDB**: https://www.peeringdb.com/asn/{ASN}
- **BGP.HE.NET**: https://bgp.he.net/AS{ASN}
- **RIR RDAP endpoints** (see Step 3)
- **RADb/IRR**: Query via whois if needed
- **Reverse DNS**: For PTR record hints

### DO NOT USE (Aggregators)
- ipinfo.io
- Team Cymru
- bgpview.io
- Other lookup aggregators

Per CONTRIBUTING.md, only primary sources should be cited in PRs.

## Entry Format Reference

Full metadata entry (for `missing: "all"`):
```json
{ "asn": 64512, "handle": "ACME-NET", "description": "Acme Corporation", "countryCode": "US", "reason": "missing" }
```

Field order is mandatory: `asn`, `handle`, `description`, `countryCode`, `reason`

## Validation

After preparing the entry, remind the user to run:
```bash
python scripts/validate.py
```

This validates the overlay.json format before committing.

## Submit PR

After validation passes, raise a pull request with sources documented in the description (use the format from Step 6).