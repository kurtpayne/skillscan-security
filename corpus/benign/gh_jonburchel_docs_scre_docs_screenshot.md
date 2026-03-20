---
name: docs-screenshot
description: Capture, process, and redact screenshots for Microsoft Learn documentation. Use when the user needs screenshots of Azure, M365, SharePoint, Entra, or any Microsoft web portal. Also use when updating existing docs, validating screenshots, or creating screenshots for new documentation.
allowed-tools: Bash(playwright-cli:*), Bash(python:*), Bash(az:*), Bash(pwsh:*), Bash(powershell:*)
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: jonburchel/docs-screenshot
# corpus-url: https://github.com/jonburchel/docs-screenshot/blob/3b292ab5f823a6c94ee0377069a29a016e51ec1f/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Microsoft Documentation Screenshot Skill

Automates the full pipeline for creating documentation screenshots across all Microsoft web portals (Azure, M365, SharePoint, Entra ID, Power Platform, etc.) that comply with Microsoft Learn contributor guidelines: browser automation, resource provisioning, PII redaction with approved fictitious values, callout boxes, smart cropping, and GIMP handoff.

## Two Primary Usage Scenarios

### Scenario 1: New Documentation Authoring

The user is writing a new article and needs screenshots. They describe what the screenshot should show, including:
- Which portal/service (Azure, M365 Admin, SharePoint, etc.)
- What the user should see (e.g., "the VM creation blade with size B2s selected")
- What resources must exist (e.g., "a resource group named contoso-rg with a VM")
- What elements to highlight with callout boxes
- How to crop the image

**Workflow:**
1. Parse the user's description to determine required resources and portal page
2. Provision any resources needed (using `az`, `m365`, Graph API, PowerShell, etc.)
3. Open the correct portal and navigate to the target page
4. Configure the view (expand panes, select items, scroll to correct position)
5. Scrub all PII from the DOM across all frames
6. Capture screenshot at 1200x800
7. Post-process: callouts, crop, border, optimize
8. Open in GIMP for final review
9. Ask user whether to clean up provisioned resources

### Scenario 2: Existing Documentation Maintenance

The user has an existing markdown article with screenshots that need to be validated or refreshed. They provide the article file path or URL.

**Workflow:**
1. Read the markdown article and parse all image references
2. For each image, read its alt text and surrounding context to understand what it should show
3. Determine the portal URL, required resources, and page state for each screenshot
4. For each screenshot:
   a. Provision resources if needed
   b. Navigate to the correct page
   c. Scrub PII, capture, process
   d. Compare with the original image (dimensions, rough visual similarity)
   e. Save to the correct media/ path with the correct filename
5. Generate a report: which screenshots were updated, which matched, which differed
6. Open all new screenshots in GIMP for final review

**Example prompt:** *"Update the screenshots in /docs/azure-sql/create-database.md. The article shows creating an Azure SQL database through the portal."*

## Limitations

- **Credential-scoped provisioning**: The skill can only create resources the user's credentials allow. If you lack permissions for a specific Azure service, M365 feature, or SharePoint site, the skill cannot provision those resources for you.
- **MFA/Conditional Access**: Some portals may trigger MFA prompts that require manual interaction. The skill will pause and ask for help.
- **Portal-specific quirks**: Each Microsoft portal has unique popup patterns, loading behaviors, and DOM structures. Azure portal is the most thoroughly tested. Other portals may need additional popup dismissal patterns added.
- **Closed Shadow DOM**: Some portal components use closed Shadow DOM that cannot be accessed even via Playwright. In rare cases, post-screenshot pixel-level redaction is needed as a fallback.
- **Dynamic content**: Portals with real-time data (metrics, logs, dashboards) may show different values between captures. The skill scrubs PII but cannot guarantee identical content across runs.
- **Canvas/SVG content**: Charts, graphs, and other canvas/SVG-rendered content cannot be scrubbed via DOM manipulation. These require the pixel-level image editing fallback.

## Quick Start

> **Note:** This skill uses `playwright-cli` commands (from the Copilot CLI playwright-cli skill), which run headless by default. If you're using VS Code with the [Playwright MCP server](https://github.com/microsoft/playwright-mcp), configure it with `--headless --browser=msedge` to avoid browser popups. See [Phase 1](#phase-1-authentication--setup) for details.

```bash
# 1. Open Azure portal in Edge with persistent profile (inherits your SSO)
playwright-cli open --browser=msedge --persistent "https://portal.azure.com/?feature.customportal=false"

# 2. Navigate to the target page
playwright-cli goto "https://portal.azure.com/#view/HubsExtension/BrowseResource/resourceType/Microsoft.Compute%2FVirtualMachines"

# 3. Wait for page to load, dismiss any popups
playwright-cli run-code "async page => { await page.waitForTimeout(3000); }"

# 4. Take screenshot + extract DOM info simultaneously
playwright-cli screenshot --filename=raw-screenshot.png
# Then run the DOM extraction (see "Extract DOM Info" section below)

# 5. Process the image (PII redaction, callouts, crop, optimize)
python <skill-install-path>/lib/screenshot_processor.py \
  --dom-json dom_data.json --image raw-screenshot.png \
  --output processed-screenshot.png \
  --description "Virtual machines list in Azure portal"
```

## Full Workflow

### Phase 0: Determine the Target Portal

This skill works with ANY Microsoft web portal that uses Microsoft SSO. Choose the correct base URL:

| Portal | Base URL | Customer View Flag |
|--------|----------|-------------------|
| **Azure** | `https://portal.azure.com/` | `?feature.customportal=false` |
| **M365 Admin** | `https://admin.microsoft.com/` | none |
| **SharePoint Admin** | `https://admin.microsoft.com/sharepoint` | none |
| **SharePoint Site** | `https://<tenant>.sharepoint.com/` | none |
| **Microsoft Entra** | `https://entra.microsoft.com/` | none |
| **Power Platform** | `https://make.powerapps.com/` | none |
| **Teams Admin** | `https://admin.teams.microsoft.com/` | none |
| **Exchange Admin** | `https://admin.exchange.microsoft.com/` | none |
| **Intune** | `https://intune.microsoft.com/` | none |
| **Defender** | `https://security.microsoft.com/` | none |
| **Purview** | `https://compliance.microsoft.com/` | none |
| **Fabric** | `https://app.fabric.microsoft.com/` | none |
| **DevOps** | `https://dev.azure.com/` | none |

**Resource provisioning tools by portal:**

| Portal | Provisioning Tool | Example |
|--------|------------------|---------|
| Azure | `az` CLI | `az group create --name contoso-rg --location eastus` |
| M365 / Entra | Microsoft Graph PowerShell | `New-MgUser`, `New-MgGroup` |
| SharePoint | PnP PowerShell | `New-PnPSite`, `Add-PnPListItem` |
| Power Platform | Power Apps CLI (`pac`) | `pac solution create` |
| Exchange | Exchange Online PowerShell | `New-Mailbox`, `New-DistributionGroup` |
| DevOps | `az devops` CLI | `az devops project create` |

### Phase 1: Authentication & Setup

**Browser automation tool:** This skill uses browser automation via one of these approaches (adapt commands to your environment):
- **Copilot CLI**: Uses the `playwright-cli` skill (install with `playwright-cli install --skills`)
- **VS Code / other editors**: Uses the [Playwright MCP server](https://github.com/microsoft/playwright-mcp) (`npx @playwright/mcp@latest --headless --browser=msedge`)

The commands in this skill use `playwright-cli` syntax. If you are using the Playwright MCP server instead, the equivalent MCP tool calls are similar (e.g., `browser_navigate` instead of `playwright-cli goto`). Adapt as needed for your environment.

**Open browser with persistent Edge profile (picks up existing Microsoft SSO):**
```bash
# For Azure (with customer view flag):
playwright-cli open --browser=msedge --persistent "https://portal.azure.com/?feature.customportal=false"

# For any other portal (no special flags needed):
playwright-cli open --browser=msedge --persistent "https://entra.microsoft.com/"
```

The persistent profile shares cookies with the user's regular Edge sessions, so Microsoft SSO typically works automatically.

**For Azure specifically:** always append `?feature.customportal=false` to hide internal/preview features.

**Check if authenticated:**
```bash
playwright-cli snapshot
# Look for user avatar/name in the snapshot. If you see a sign-in button, auth is needed.
```

**If login is needed, use the current user's credentials (DO NOT hardcode any specific email):**
```bash
playwright-cli snapshot
# Find the email input field ref
# Ask the user for their email, or detect it from:
#   az account show --query "user.name" -o tsv
#   $env:USERNAME + "@microsoft.com"  (as a guess, confirm with user)
playwright-cli fill <ref> "<user's email>"
playwright-cli click <submit-ref>
# MFA may be triggered - if so, pause and ask the user to complete it manually
# then wait for the redirect
playwright-cli run-code "async page => { await page.waitForLoadState('networkidle'); }"
```

**IMPORTANT: Never hardcode a specific user's credentials.** Always determine the current user's identity dynamically or ask them.

**Select the user's preferred subscription (if multiple exist):**
```bash
# Check what subscription is currently active
az account show --query "{name:name, id:id}" -o table

# If the user has a preferred subscription, switch to it:
# az account set --subscription "<subscription name or ID>"

# To list all available subscriptions:
# az account list --query "[].{name:name, id:id, isDefault:isDefault}" -o table
```

### Phase 2: Dismiss Popups & Banners

Azure portal frequently shows popups, preview banners, and welcome dialogs. Dismiss them all before taking screenshots.

```bash
# Common popup dismissal patterns
playwright-cli run-code "async page => {
  // Close 'Welcome' or 'What's new' dialogs
  const closeButtons = await page.locator('[aria-label=\"Close\"], [aria-label=\"Dismiss\"], button:has-text(\"Got it\"), button:has-text(\"Maybe later\"), button:has-text(\"Skip\"), button:has-text(\"No thanks\"), button:has-text(\"OK\"), .portal-banner-close, [data-telemetryname=\"DismissButton\"]').all();
  for (const btn of closeButtons) {
    try { await btn.click({ timeout: 1000 }); } catch(e) {}
  }
  // Close preview banners
  const previewBanners = await page.locator('[class*=\"preview-banner\"] button, [class*=\"fxs-banner\"] button').all();
  for (const btn of previewBanners) {
    try { await btn.click({ timeout: 1000 }); } catch(e) {}
  }
  // Wait for animations
  await page.waitForTimeout(500);
}"
```

**For persistent notification banners:**
```bash
playwright-cli run-code "async page => {
  // Hide notification panels via CSS
  await page.addStyleTag({ content: '.fxs-toast-container, .fxs-notification-panel { display: none !important; }' });
}"
```

### Phase 3: Azure Resource Provisioning

If the screenshot requires specific Azure resources to exist, create them using Azure CLI:

```bash
# Example: Create a resource group
az group create --name contoso-rg --location eastus

# Example: Create a VM
az vm create --resource-group contoso-rg --name contoso-vm \
  --image Ubuntu2204 --size Standard_B1s \
  --admin-username azureuser --generate-ssh-keys

# Example: Create a storage account
az storage account create --name contosostorageacct \
  --resource-group contoso-rg --location eastus --sku Standard_LRS
```

**IMPORTANT: Use fictitious-sounding names for resources** (contoso-*, fabrikam-*, etc.) so they appear correct in screenshots without needing redaction.

**After screenshots are complete, ASK the user whether to clean up:**
```bash
# List resources created
az group show --name contoso-rg --query "{name:name, location:location}"
# Ask user before deleting
az group delete --name contoso-rg --yes --no-wait
```

### Phase 4: Window Sizing & Screenshot Capture

**Set the browser to the standard documentation screenshot size (1200x800):**
```bash
playwright-cli resize 1200 800
```

**Wait for full page load:**
```bash
playwright-cli run-code "async page => {
  await page.waitForLoadState('networkidle');
  // Extra wait for Azure portal animations
  await page.waitForTimeout(2000);
}"
```

**Take the screenshot:**
```bash
playwright-cli screenshot --filename=raw-screenshot.png
```

### Phase 5: DOM Extraction for PII Detection

This is the key innovation. Instead of OCR, we extract text positions directly from the DOM, giving us pixel-perfect coordinates.

**Extract DOM info (save the output to a JSON file):**
```bash
playwright-cli run-code "async page => {
  return await page.evaluate(() => {
    const DPR = window.devicePixelRatio || 1;
    const results = [];
    function getEffectiveBgColor(el) {
      let current = el;
      while (current && current !== document.documentElement) {
        const bg = getComputedStyle(current).backgroundColor;
        if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') return bg;
        current = current.parentElement;
      }
      return 'rgb(255, 255, 255)';
    }
    function isVisible(el) {
      if (!el || !el.getBoundingClientRect) return false;
      const style = getComputedStyle(el);
      if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') return false;
      const rect = el.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return false;
      if (rect.bottom < 0 || rect.top > window.innerHeight) return false;
      if (rect.right < 0 || rect.left > window.innerWidth) return false;
      return true;
    }
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function(node) {
        const text = node.textContent.trim();
        if (!text) return NodeFilter.FILTER_REJECT;
        if (!isVisible(node.parentElement)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    let node;
    while (node = walker.nextNode()) {
      const el = node.parentElement;
      const range = document.createRange();
      range.selectNodeContents(node);
      const rects = range.getClientRects();
      for (const rect of rects) {
        if (rect.width === 0 || rect.height === 0) continue;
        const text = node.textContent.trim();
        if (!text) continue;
        const style = getComputedStyle(el);
        results.push({
          text: text,
          cssRect: { x: Math.round(rect.x*100)/100, y: Math.round(rect.y*100)/100, width: Math.round(rect.width*100)/100, height: Math.round(rect.height*100)/100 },
          pxRect: { x: Math.round(rect.x*DPR), y: Math.round(rect.y*DPR), width: Math.round(rect.width*DPR), height: Math.round(rect.height*DPR) },
          style: { fontFamily: style.fontFamily, fontSize: style.fontSize, fontWeight: style.fontWeight, color: style.color, backgroundColor: getEffectiveBgColor(el) },
          element: { tag: el.tagName.toLowerCase(), id: el.id || null, className: el.className || null },
          dpr: DPR,
        });
      }
    }
    return { url: window.location.href, title: document.title, viewport: { width: window.innerWidth, height: window.innerHeight }, dpr: DPR, timestamp: new Date().toISOString(), textNodes: results };
  });
}"
```

**Save the DOM extraction output** to a JSON file. The output from the run-code command contains the JSON under "### Result". Save it as `dom_data.json`.

### Phase 6: Image Processing

Use the screenshot processor to apply all transformations:

```bash
python F:\home\azure-screenshot\lib\screenshot_processor.py \
  --dom-json dom_data.json \
  --image raw-screenshot.png \
  --output my-final-screenshot.png \
  --description "Description of what this screenshot shows" \
  --callouts '[{"x": 100, "y": 200, "width": 300, "height": 50}]' \
  --crop-focus '[{"x": 50, "y": 150, "width": 400, "height": 300}]'
```

**Options:**
- `--skip-pii`: Skip PII detection/redaction
- `--skip-crop`: Skip smart cropping
- `--skip-border`: Skip gray border
- `--no-gimp`: Don't open in GIMP
- `--callouts`: JSON array of rectangles for red callout boxes
- `--crop-focus`: JSON array of rectangles defining area of interest

### Phase 7: Pre-Screenshot DOM Scrubbing (PREFERRED Method)

The most reliable approach is to replace PII directly in the DOM BEFORE taking the screenshot. This is the same approach as Microsoft's Screenshot Scrubber extension.

**CRITICAL: Azure portal uses cross-origin iframes** (`sandbox-*.reactblade.portal.azure.net`) for grid/table content. Standard `document.querySelectorAll` CANNOT reach them. You MUST use `page.frames()` to iterate all frames.

**Use the dom_scrubber.py module to generate the scrub script:**
```bash
python -c "
from F_home_azure_screenshot.lib.dom_scrubber import generate_scrub_js
js = generate_scrub_js(
    username='jburchel',
    subscription_name='jburchel BAMI subscription',
    tenant_display_name='Microsoft Customer Led',
    custom_replacements={
        'my-real-rg': 'contoso-rg',
        'DefaultResourceGroup-EUS': 'contoso-default-eus',
    },
)
with open('temp_scrub.js', 'w') as f:
    f.write(js)
"
playwright-cli run-code "$(cat temp_scrub.js)"
```

**Or inline, using the frame-aware pattern:**
```bash
playwright-cli run-code "async page => {
  const rules = [
    {isRegex: true, pattern: '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', flags: 'gi', replacement: 'aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e'},
    {isRegex: true, pattern: 'jburchel', flags: 'gi', replacement: 'john'},
    {isRegex: false, pattern: 'BAMI subscription', replacement: 'Contoso subscription'},
    // Add more rules as needed
  ];
  const frames = page.frames();
  let total = 0;
  for (const frame of frames) {
    try {
      const count = await frame.evaluate((r) => {
        let replaced = 0;
        function walk(root) {
          const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT, null);
          let n; const textNodes = [];
          while (n = w.nextNode()) {
            if (n.nodeType === 1) {
              if (n.shadowRoot) walk(n.shadowRoot);
              continue;
            }
            textNodes.push(n);
          }
          for (const tn of textNodes) {
            let t = tn.textContent; let changed = false;
            for (const rule of r) {
              let nt = rule.isRegex
                ? t.replace(new RegExp(rule.pattern, rule.flags), rule.replacement)
                : t.split(rule.pattern).join(rule.replacement);
              if (nt !== t) { t = nt; changed = true; }
            }
            if (changed) { tn.textContent = t; replaced++; }
          }
        }
        walk(document.body);
        document.querySelectorAll('*').forEach(el => { if (el.shadowRoot) walk(el.shadowRoot); });
        return replaced;
      }, rules);
      total += count;
    } catch(e) {}
  }
  return { framesProcessed: frames.length, totalReplaced: total };
}"
```

**Why this approach is preferred:**
1. The browser renders replacement text natively in Segoe UI at the correct size
2. No pixel-level font matching needed
3. Handles cross-origin iframes that pixel-level approaches cannot detect
4. The screenshot is "clean" from the start
5. Verified to produce 56+ replacements on a real Azure portal page

### Phase 8: Callout Boxes

For callout boxes, you need the pixel coordinates of the UI element to highlight. Get these from the DOM extraction:

```bash
# Find the element you want to highlight
playwright-cli snapshot
# Note the ref of the element (e.g., e15)

# Get its bounding box
playwright-cli run-code "async page => {
  const el = page.locator('[data-ref=\"e15\"]');
  const box = await el.boundingBox();
  return box;  // {x, y, width, height}
}"
```

Then pass those coordinates to the processor's `--callouts` argument, or draw them with the image_editor directly.

**Callout specifications (per Microsoft contributor guide):**
- Color: RGB **233, 28, 28** (hex #E91C1C)
- Border thickness: **3px**
- Rectangle should "hug" the element with 4px padding
- Maximum 3-4 callouts per screenshot
- Use numbered callouts for sequential steps if needed

### Phase 9: Final Review in GIMP

The processor automatically opens the result in GIMP. In GIMP, the user should:
1. Verify PII is fully redacted
2. Check callout placement
3. Adjust crop if needed
4. Verify the image looks natural and professional
5. Export as PNG (File > Export As > .png)

**GIMP location:** `C:\Program Files\GIMP 2\bin\gimp-2.10.exe`

If GIMP is already open, images open in the existing window.

### Phase 10: Summary Report

After processing, the skill outputs a summary:
- Image dimensions and file size
- Number of PII items detected and redacted
- Each PII item: original value, type, severity, replacement value, pixel location
- Number of callout boxes drawn
- Whether cropping was applied

---

## Scenario: Parsing an Existing Article for Screenshot Refresh

When given an existing markdown article, follow this process:

### Step 1: Read the article and extract image references

```bash
# Read the article
cat /path/to/article.md
```

Look for image references in either format:
- `:::image type="content" source="media/article-name/image-name.png" alt-text="Description.":::`
- `![Description](media/article-name/image-name.png)`

### Step 2: For each image, determine what it shows

Read the **alt text**, the **surrounding markdown** (especially numbered steps), and the **existing image** (if available) to understand:
- Which portal and page is shown
- What state the page should be in (resources created, settings configured, etc.)
- What elements have callout boxes
- How the image is cropped (full browser frame vs. focused view)

### Step 3: Plan resource provisioning

Examine all images together to build a single resource provisioning plan:
- What resources are needed across all screenshots
- Create them in dependency order
- Use fictitious names from the start (contoso-rg, etc.) so scrubbing is minimal

### Step 4: Capture each screenshot in order

Follow the full workflow (Phases 1-9) for each screenshot, saving to the correct `media/` path with the correct filename.

### Step 5: Generate comparison report

For each image, report:
- Original file: dimensions, size, exists?
- New file: dimensions, size
- What changed (new resources, updated UI, different crop)
- Any PII that was found and replaced

### Step 6: Offer cleanup

Ask the user whether to delete provisioned resources.

---

## PII Replacement Reference

### Approved GUIDs (from MS Sensitive Identifiers Reference)

| Type | Example Approved Value |
|------|----------------------|
| Application (client) ID | `00001111-aaaa-2222-bbbb-3333cccc4444` |
| Certificate ID (SEV 0) | `0a0a0a0a-1111-bbbb-2222-3c3c3c3c3c3c` |
| Correlation ID | `aaaa0000-bb11-2222-33cc-444444dddddd` |
| Directory (tenant) ID | `aaaabbbb-0000-cccc-1111-dddd2222eeee` |
| Object ID | `aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb` |
| Principal ID | `aaaaaaaa-bbbb-cccc-1111-222222222222` |
| Resource ID | `a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1` |
| Secret ID/Key ID (SEV 0) | `aaaaaaaa-0b0b-1c1c-2d2d-333333333333` |
| Subscription ID | `aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e` |
| Trace ID | `0000aaaa-11bb-cccc-dd22-eeeeee333333` |

### Approved Non-GUID Values

| Type | Example |
|------|---------|
| Client Secret | `Aa1Bb~2Cc3.-Dd4Ee5Ff6Gg7Hh8Ii9_Jj0Kk1Ll2` |
| Alphanumeric | `A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u` |
| Thumbprint | `AA11BB22CC33DD44EE55FF66AA77BB88CC99DD00` |
| Signature Hash | `aB1cD2eF-3gH4iJ5kL6-mN7oP8qR=` |

### Approved Fictitious Names (CELA-approved)

| Category | Approved Values |
|----------|----------------|
| Company domains | `contoso.com`, `fabrikam.com`, `northwindtraders.com`, `adventure-works.com` |
| Generic domains | `example.com`, `example.org`, `example.net` |
| Email format | First name only: `john@contoso.com` (NOT `john.smith@contoso.com`) |
| Resource groups | `contoso-rg`, `fabrikam-rg`, `myresourcegroup` |
| VMs | `contoso-vm`, `fabrikam-vm-01`, `myVM` |
| Storage accounts | `contosostorageacct`, `fabrikamstorage` |
| Key vaults | `contoso-kv`, `fabrikam-keyvault` |

### Safe IP Ranges for Documentation

- Private: `10.x.x.x`, `172.16-31.x.x`, `192.168.x.x`
- RFC 5737: `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`
- Azure wire server: `168.63.129.16`
- Loopback: `127.0.0.0/8`
- Link-local: `169.254.0.0/16`

---

## Image Requirements Checklist

- [ ] PNG format, lowercase `.png` extension
- [ ] Filename: lowercase, letters/numbers/hyphens only (no spaces)
- [ ] Max width: 1200px
- [ ] Target size: under 200 KB
- [ ] Gray border added (automatic with processor)
- [ ] First screenshot in article: full browser frame (URL bar + controls)
- [ ] Default Azure theme (dark blue sidebars, blue background)
- [ ] `?feature.customportal=false` in portal URL
- [ ] All PII replaced with approved fictitious values
- [ ] Callout boxes: RGB 233,28,28, 3px thickness
- [ ] Alt text prepared (descriptive, ends with period)
- [ ] Image naming follows: `service-technology-image-description.png`

---

## Common Azure Portal Popup Patterns

These are elements you'll frequently need to dismiss:

| Popup Type | Selector Pattern |
|-----------|-----------------|
| Welcome dialog | `button:has-text("Got it")`, `button:has-text("Maybe later")` |
| Preview banner | `[class*="preview-banner"] button`, `[class*="fxs-banner"] button` |
| Notification toast | `.fxs-toast-container button` |
| What's new | `button:has-text("What's new")` parent close button |
| Feature announcement | `[data-telemetryname="DismissButton"]` |
| Generic close | `[aria-label="Close"]`, `[aria-label="Dismiss"]` |
| Consent/cookie | `button:has-text("Accept")`, `button:has-text("OK")` |

---

## Lib Module Reference

All Python modules are at `F:\home\azure-screenshot\lib\`:

- **`screenshot_processor.py`**: Main orchestrator. CLI interface for full pipeline.
- **`pii_detector.py`**: Regex-based PII detection with context-aware GUID classification. All approved replacement values built in.
- **`image_editor.py`**: Pillow/OpenCV operations: crop, redact, callout, border, optimize.
- **`dom_scrubber.py`**: Frame-aware DOM PII replacement. Generates JS that uses `page.frames()` to scrub ALL frames including cross-origin Azure portal iframes. **This is the preferred pre-screenshot approach.**
- **`gimp_bridge.py`**: GIMP integration (detect running instance, open images).
- **`extract_dom_info.js`**: JavaScript payload for `playwright-cli run-code` DOM extraction (Shadow DOM aware).