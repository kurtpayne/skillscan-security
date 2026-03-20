---
name: truston-checklist-migration
description: Migrate TrustOn inspection checklist items to a new version in the database
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: ncherevatenko/truston-checklist-migration-skill
# corpus-url: https://github.com/ncherevatenko/truston-checklist-migration-skill/blob/b489ec10076243eea3e66eeb0e4b61fab657bcac/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# TrustOn Checklist Migration Skill

Automates upgrading CheckItem.itemSpec and creating WorkOrderRouting in the TrustOn database when checklist versions are released (e.g., v4.8 → v4.9.2).

## When to use

- New checklist version released (v4.9.2, Centromash v4.9.2, v4.10, etc.)
- CheckItem specs need updating across all inspection orders
- Post ordering, items, or metadata has changed
- Need to add new check items or remove deprecated ones
- User requests to apply new checklist to specific vehicle/order

## Problem

When checklist versions are released:
1. The database contains thousands of CheckItem records with old specs
2. Orders may be missing WorkOrderRouting records (causing 404 errors on `/orders/{orderId}/routing` endpoint)
3. Manual updates are error-prone and time-consuming

## Solution

This skill provides:

**CheckItem Migration:**
- **TypeScript Script**: `scripts/migrate_single_order_checklist.ts` for single order migration (RECOMMENDED)
- **HTTP Endpoint**: `POST /migrate/checkitems-v{VERSION}` for batch/single order migration
- **Query params**: `?orderId=<id>` (single), `?dryRun=true` (test), `?confirm=true` (production)
- **Safe operations**: Preserves deleted items, adds new items, updates order fields
- **Migration scripts**: TypeScript (primary), Python, SQL alternatives

**Routing Creation (REQUIRED):**
- **TypeScript Script**: `scripts/create_routing_for_order.ts` for automatic routing creation
- **SQL Script**: `scripts/create_routing_for_order.sql` for manual routing creation
- **Automatic grouping**: CheckItems grouped by post prefix (P3, P4, P5, P6)
- **RouteStep generation**: Creates steps with sequence, status, assignedCheckItemIds

## Key Concepts

**CheckItem Structure:**
```json
{
  "itemSpec": {
    "itemId": "P4.801",
    "title": "Охлаждающая жидкость: уровень/состояние",
    "order": 16,
    "block": "Подкапотное пространство",
    "priority": "P4",
    "fields": [...],
    "methodology": "..."
  }
}
```

**Available Checklists:**
- **General Checklist**: `TrustOn Bundle v4.9.2.json` - standard inspection checklist
- **Centromash Checklist (current default)**: `TrustOn Checklist v4.9.2 CM - centromash.v4.9.7.full-from-xlsx.json`
  - Version: `4.0.9.7-final-centromash+full-xlsx`
  - Items: 20 specialized checks
  - Focus: XLSX-aligned CM flow for body panels, glass, interior, underhood, underbody, and split suspension checks
  - Optimized for: Posts P1, P2, P3
- **Legacy Centromash Bundles**: `TrustOn Checklist v4.9.2 CM - centromash.json`, `TrustOn Checklist v4.9.2 CM - centromash.v4.9.5.strict.json`
  - Keep only for historical migrations or compatibility checks; do not use as the current default.

**Migration Logic:**
1. Load new bundle (`v4.9.7.full-from-xlsx` for current CM migrations)
2. Extract itemId → itemSpec mapping
3. For each order: iterate CheckItems, update itemSpec where code matches
4. Add new items (for example `P4.CM.BODY.PANELS`, `P6.CM.SUSP.RL`, `P6.CM.SUSP.RR`) if missing
5. Preserve deleted items (P3.000, P4.700-702, P4.809-810)
6. When replacing historical structures, explicitly handle `P6.CM.SUSP.REAR -> P6.CM.SUSP.RL + P6.CM.SUSP.RR`
7. Update `checkItemToPostMap` expectations and routing after the split

## Instructions

### Step 1: Prepare Bundle

**Choose checklist type:**
- **Centromash**: For Centromash diagnostic center orders → `TrustOn Checklist v4.9.2 CM - centromash.v4.9.7.full-from-xlsx.json`
- **General**: For standard inspections → `TrustOn Bundle v4.9.2.json`

**Update script CHECKLIST_PATH** (if using TypeScript script):
```typescript
const CHECKLIST_PATH = path.join(
  __dirname,
  '../docs/checklist/checklist4/TrustOn Checklist v4.9.2 CM - centromash.v4.9.7.full-from-xlsx.json'
);
```

**Bundle format:**
```json
{
  "schema": "TrustOn.ChecklistBundle.v2",
  "version": "4.0.9.7-final-centromash+full-xlsx",
  "items": [
    { "itemId": "P1.010", "title": "...", "order": 1, ... }
  ],
  "optionsRegistries": { ... },
  "checkItemToPostMap": { "P4.THK.001": "P4", ... }
}
```

### Step 2: Create Migration Endpoint (NestJS)

Add controller in `apps/api/src/inspection/migrate.controller.ts`:

**Features:**
- Load ITEM_SPECS from bundle constant
- Support query params: `orderId`, `dryRun`, `confirm`
- Dry-run mode: returns count of changes without persisting
- Confirm mode: applies migration to all/single orders
- Returns: migration summary (updated count, new items added, etc.)

### Step 3: Execute Migration

**Option A: TypeScript Script (RECOMMENDED for single orders)**
```bash
# Migrate single order by orderId:
pnpm tsx scripts/migrate_single_order_checklist.ts <orderId>

# Example (Ford Explorer, Centromash v4.9.7.full-from-xlsx):
pnpm tsx scripts/migrate_single_order_checklist.ts bea653ec-d5d2-4c7f-a3e6-358c68284212
```

**Features:**
- Uses Prisma 7 with pg adapter
- Loads checklist from `docs/checklist/checklist4/TrustOn Checklist v4.9.2 CM - centromash.v4.9.7.full-from-xlsx.json`
- Updates existing CheckItems by matching `code` to `itemId`
- Adds new items not present in order
- Preserves unmatched items with warnings
- Shows detailed migration summary
- Current API default bundle already resolves to `v4.9.7.full-from-xlsx` via `apps/api/src/inspection/item-specs.constant.ts` and `apps/api/src/orders/template-catalog.service.ts`

**Option B: HTTP Endpoint (for batch migrations)**
```bash
# Single order test:
curl -X POST http://localhost:3000/migrate/checkitems-v492?orderId=<uuid>

# Dry-run on all orders:
curl -X POST http://localhost:3000/migrate/checkitems-v492?dryRun=true

# Production migration:
curl -X POST http://localhost:3000/migrate/checkitems-v492?confirm=true
```

**Option C: CLI Command**
```bash
pnpm --filter @truston/api migrate:checkitems-v492 --all --confirm
```

**Option D: Direct SQL**
```bash
jq -r '.items[] | @json' "$BUNDLE_PATH" | while read SPEC_JSON; do
  ITEM_ID=$(echo "$SPEC_JSON" | jq -r '.itemId')
  UPDATE "CheckItem" SET "itemSpec" = '$SPEC_JSON' WHERE code = '$ITEM_ID'
done
```

### Step 4: Create Routing for Order

**CRITICAL**: After migrating CheckItems, you MUST create routing (WorkOrderRouting) for the order to work with the API endpoint `/orders/{orderId}/routing`.

**Option A: TypeScript Script (RECOMMENDED)**
```bash
# Create routing automatically based on CheckItems:
pnpm tsx scripts/create_routing_for_order.ts <orderId>

# Example:
pnpm tsx scripts/create_routing_for_order.ts bea653ec-d5d2-4c7f-a3e6-358c68284212
```

**What it does:**
- Gets all posts from the order's service station
- Groups CheckItems by post prefix (P3, P4, P5, P6, etc.)
- Creates WorkOrderRouting record
- Creates RouteStep records for each post with assigned CheckItems
- Returns routing summary
- For current CM flow, expect rear suspension as two distinct items: `P6.CM.SUSP.RL` and `P6.CM.SUSP.RR`

**Option B: SQL Script**
```bash
# Use pre-generated SQL for specific order:
psql -h <host> -U <user> -d <database> -f scripts/create_routing_for_order.sql
```

**Important Notes:**
- RouteStep schema does NOT have `updatedAt` field (Prisma schema only has `createdAt`)
- Post assignment is automatic based on CheckItem code prefix
- Special handling: `PH.*` items go to `P3` (Фотозона)
- Each RouteStep gets `assignedCheckItemIds` array

**Routing Structure:**
```
WorkOrderRouting
├── orderId (unique)
└── route (RouteStep[])
    ├── postId
    ├── sequence (1, 2, 3, 4...)
    ├── status (pending, in_progress, completed)
    └── assignedCheckItemIds (CheckItem.id[])
```

### Step 5: Verify Results

**Check CheckItems migration:**
```sql
SELECT
  COUNT(*) as total_updated,
  COUNT(DISTINCT "order"::text) as unique_orders
FROM "CheckItem"
WHERE "itemSpec"->>'order' IS NOT NULL;

-- Check specific post (e.g., P4)
SELECT code, "itemSpec"->>'order' as "order", "itemSpec"->>'title' as title
FROM "CheckItem"
WHERE code LIKE 'P4.%'
GROUP BY code, "order"
ORDER BY ("itemSpec"->>'order')::int;
```

**Check routing creation:**
```sql
-- Verify routing exists
SELECT * FROM "WorkOrderRouting" WHERE "orderId" = '<orderId>';

-- Check route steps
SELECT
  wr.id as routing_id,
  rs."postId",
  p.code as post_code,
  p.name as post_name,
  rs.sequence,
  rs.status,
  array_length(rs."assignedCheckItemIds", 1) as check_items_count
FROM "WorkOrderRouting" wr
JOIN "RouteStep" rs ON rs."workOrderRoutingId" = wr.id
JOIN "Post" p ON p.id = rs."postId"
WHERE wr."orderId" = '<orderId>'
ORDER BY rs.sequence;
```

**Test API endpoint:**
```bash
# Should return 200 with routing data (not 404):
curl https://api.thetasystem.com/orders/<orderId>/routing
```

## Migration Workflow

```
1. TypeSpec contracts updated
   ↓
2. pnpm gen (generates new bundle)
   ↓
3. Create migration endpoint/script
   ↓
4. Test on single order (dryRun or single orderId)
   ↓
5. Verify order field updates, especially any split mappings such as `P6.CM.SUSP.REAR -> P6.CM.SUSP.RL/RR`
   ↓
6. Create routing for order (CRITICAL STEP)
   ↓
7. Test API endpoint GET /orders/{orderId}/routing
   ↓
8. Execute on all orders (confirm=true)
   ↓
9. Verify counts match expectations
   ↓
10. Commit migration script to separate branch
```

## Data Preservation Rules

- **Deleted items**: Keep as-is (P3.000, P4.700-702, P4.809-810)
- **New items**: Add with full spec if missing
- **Updated items**: Replace entire itemSpec (order + metadata)
- **Unmatched items**: Log warnings, preserve unchanged
- **Split items**: When a historical item is replaced by multiple current items, preserve old records unless the migration explicitly deprecates them, and create the new split records with full specs.

## Files to Create

```
# CheckItem Migration
scripts/migrate_single_order_checklist.ts        # TypeScript migration script (PRIMARY)
apps/api/src/inspection/migrate.controller.ts    # HTTP endpoint (batch migrations)
apps/api/src/inspection/migrate-checkitems.command.ts  # CLI command
scripts/migrate_checkitem_v{VERSION}.py          # Python alternative
scripts/migrate-checkitems.sql                   # Direct SQL

# Routing Creation (REQUIRED after migration)
scripts/create_routing_for_order.ts              # TypeScript routing script (PRIMARY)
scripts/create_routing_for_order.sql             # SQL routing script
```

**TypeScript Migration Script Template:**
- Import `dotenv/config` to load DATABASE_URL
- Use `PrismaPg` adapter with `Pool` (Prisma 7 requirement)
- Read checklist bundle JSON from `docs/checklist/checklist4/`
- Build itemId → itemSpec mapping
- Update existing CheckItems by code
- Create new CheckItems with required fields (title, claimTemplate, required)
- Close pool connection after migration

**TypeScript Routing Script Template:**
- Import `dotenv/config` to load DATABASE_URL
- Use `PrismaPg` adapter with `Pool` (Prisma 7 requirement)
- Get order and service station posts
- Group CheckItems by post prefix (P3, P4, P5, P6)
- Create WorkOrderRouting record
- Create RouteStep records (WITHOUT updatedAt field)
- Each RouteStep includes: postId, sequence, status, assignedCheckItemIds
- Close pool connection after creation

## Testing Checklist

**CheckItem Migration:**
- [ ] Dry-run returns correct count of changes
- [ ] Order field updates for key items (P4.801, P6.010, etc.)
- [ ] New items added to all orders
- [ ] `P6.CM.SUSP.REAR` replacement logic creates `P6.CM.SUSP.RL` and `P6.CM.SUSP.RR` where required
- [ ] Deleted items preserved
- [ ] Post order sequence maintained (1-25 for P4)
- [ ] Run on single order first
- [ ] Verify on 2-3 random orders before batch
- [ ] Check database row counts match

**Routing Creation:**
- [ ] WorkOrderRouting record created for order
- [ ] RouteStep records created for all relevant posts
- [ ] CheckItems correctly grouped by post prefix
- [ ] Sequence numbers are sequential (1, 2, 3, 4...)
- [ ] assignedCheckItemIds arrays populated
- [ ] All RouteStep statuses set to 'pending'
- [ ] API endpoint `/orders/{orderId}/routing` returns 200 (not 404)
- [ ] No `updatedAt` field errors in RouteStep creation

## Common Issues

**Issue**: PrismaClient initialization error (Prisma 7)
**Solution**:
```typescript
import 'dotenv/config';
import { PrismaPg } from '@prisma/adapter-pg';
import { Pool } from 'pg';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const adapter = new PrismaPg(pool);
const prisma = new PrismaClient({ adapter });
```

**Issue**: Missing required field `title` when creating CheckItem
**Solution**: Include all required fields in create:
```typescript
await prisma.checkItem.create({
  data: {
    orderId,
    code: item.itemId,
    title: item.title,
    claimTemplate: `Claim for ${item.itemId}`,
    required: item.required,
    itemSpec: item as any,
  },
});
```

**Issue**: Order field not updating
**Solution**: Ensure itemSpec is loaded as JSON object, not string

**Issue**: Unmatched items in logs
**Solution**: Check itemId format matches between bundle and database

**Issue**: 404 Not Found on `/orders/{orderId}/routing` endpoint
**Solution**: Routing not created for order. Run routing creation script:
```bash
pnpm tsx scripts/create_routing_for_order.ts <orderId>
```

**Issue**: RouteStep creation fails with "updatedAt does not exist"
**Solution**: RouteStep table does NOT have `updatedAt` field. Remove it from INSERT:
```typescript
// ❌ Wrong (has updatedAt)
await prisma.routeStep.create({
  data: { ...fields, createdAt: new Date(), updatedAt: new Date() }
});

// ✅ Correct (only createdAt)
await prisma.routeStep.create({
  data: { ...fields, createdAt: new Date() }
});
```

## Example Results

**Example 1: Single Order (Ford Explorer, Centromash v4.9.7.full-from-xlsx)**
```
Order ID: bea653ec-d5d2-4c7f-a3e6-358c68284212
VIN: 1FM5K8HC0LGA87502
Status: in_progress
Checklist version: 4.0.9.7-final-centromash+full-xlsx

Updated items: 0 (order had no existing items)
New items added: 20
- ✓ P1.CM.RECEPTION: Приемка на станции
- ✓ P1.CM.WASH: Мойка
- ✓ PH.PHOTO.STANDARD: Фотофиксация (стандартный набор)
- ✓ P4.THK.002: Проверка ультрафиолетовым сканером
- ✓ P4.THK.001: Проверка толщиномером
- ✓ P4.GLASS.INSPECT: Осмотр остекления
- ✓ P4.LIGHT.INSPECT: Осмотр световых приборов
- ✓ P4.MISC.BOOT: Багажное отделение
- ✓ P4.INT.INSPECT: Осмотр салона
- ✓ P4.600: OBD скан всех блоков
- ✓ P4.CM.BODY.PANELS: Осмотр кузовных панелей (Centromash)
- ✓ P4.CM.UNDERHOOD: Подкапотное пространство
- ✓ P5.CM.BRAKE_STAND: Тормозной стенд (Centromash)
- ✓ P6.CM.UNDERBODY: Подъемник: защиты и днище
- ✓ P6.CM.LIFT: Подъемник (Centromash)
- ✓ P6.CM.TESTDRIVE: Тест-драйв
- ✓ P6.CM.SUSP.FL: Подвеска переднего левого колеса
- ✓ P6.CM.SUSP.FR: Подвеска переднего правого колеса
- ✓ P6.CM.SUSP.RL: Подвеска заднего левого колеса
- ✓ P6.CM.SUSP.RR: Подвеска заднего правого колеса

Total items after migration: 20
```

**Routing creation:**
```
Routing ID: 41c3983c-b04b-463b-9066-bcf556a1ed2a
Order ID: bea653ec-d5d2-4c7f-a3e6-358c68284212

Route steps:
  1. P1 - Приемка / мойка
     Status: pending
     Items: 2 (P1.CM.RECEPTION, P1.CM.WASH)

  2. P2 - Кузовной осмотр
     Status: pending
     Items: 10 (PH.PHOTO.STANDARD, P4.THK.001, P4.THK.002, P4.CM.BODY.PANELS, etc.)

  3. P3 - Подъемник / тормозной стенд
     Status: pending
     Items: 8 (P5.CM.BRAKE_STAND, P6.CM.LIFT, P6.CM.UNDERBODY, P6.CM.SUSP.FL, P6.CM.SUSP.FR, P6.CM.SUSP.RL, P6.CM.SUSP.RR, P6.CM.TESTDRIVE)
```

**API endpoint test:**
```bash
curl https://api.thetasystem.com/orders/bea653ec-d5d2-4c7f-a3e6-358c68284212/routing
# Returns 200 OK with routing data ✅
```

**Example 2: Batch Migration (26 orders, general checklist)**
- 2763 CheckItems updated
- 52 new items added (P4.MISC.BOOT, P4.MISC.HOOD)
- 52 deleted items preserved
- Order range: 1-206
- Post 4 sequence: 25 items, orders 1-25