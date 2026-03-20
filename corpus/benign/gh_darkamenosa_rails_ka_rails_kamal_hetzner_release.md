---
name: rails-kamal-hetzner-release
description: Use when deploying a Rails + Inertia.js app to production with Kamal on Hetzner, setting up Cloudflare DNS, registering Stripe webhooks, configuring production email, or troubleshooting deployment issues including SSL certificates, deploy locks, empty secrets, and SSH host key mismatches.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: darkamenosa/rails-kamal-hetzner-release
# corpus-url: https://github.com/darkamenosa/rails-kamal-hetzner-release/blob/2989d7f9e43d1049f059530fc11fd0ab38874e74/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Rails + Kamal Production Release (Hetzner + Cloudflare)

## Overview

Operational runbook for deploying a Rails 8 + Inertia.js + Kamal app to Hetzner Cloud with Cloudflare DNS. Covers first-time infrastructure setup through ongoing releases.

**Deployment guide:** This skill includes `references/deployment-guide.md` — a template with complete file examples for single-env and multi-env (Kamal destinations) setups. Copy it to `docs/deployment-guide.md` in the target project if it doesn't already exist, and add a reference in `CLAUDE.md`.

**Prerequisites:**
- `rails-solid-stack-kamal` skill already applied (deploy.yml, .kamal/secrets, bin/jobs, db/production.sql)
- `rails-inertia-stripe-billing` skill already applied (if using Stripe)
- Working local development environment with `config/master.key` present

## When to Use

- First production deployment to Hetzner
- Setting up Cloudflare DNS for a Kamal-deployed app
- Registering Stripe webhooks for production
- Configuring production email (SMTP)
- Troubleshooting Kamal deployment failures
- Subsequent releases after code changes

## Step 1: Gather Information

**CRITICAL:** Before proceeding, ask the user for:

```
1. App name          — e.g., myapp (service name, DB name, Docker image)
2. Domain            — e.g., myapp.example.com
3. Docker Hub user   — e.g., tuyenhx
4. Hetzner type      — e.g., cax21 (4 vCPU ARM, 8GB, cheapest ARM option)
5. Hetzner location  — e.g., nbg1, fsn1, hel1
6. SSH key name      — as configured in Hetzner Cloud Console
7. Environment       — single (one server) or multi (staging + production)?
```

**If multi-environment:** Use Kamal destinations. See `docs/deployment-guide.md` Section 3 for complete file templates. The key differences:
- `.env.staging` / `.env.production` instead of single `.env`
- `.kamal/secrets-common` + `.kamal/secrets.staging` / `.kamal/secrets.production`
- `config/deploy.yml` (base) + `config/deploy.staging.yml` / `config/deploy.production.yml`
- All commands use `-d staging` or `-d production` flag

## Step 2: Provision Hetzner Server

### Required CLI

```bash
hcloud version    # Must be installed and authenticated
```

### Create Server

```bash
hcloud server create \
  --name APP_NAME \
  --type cax21 \
  --image ubuntu-24.04 \
  --ssh-key SSH_KEY_NAME \
  --location nbg1
```

Note the server IP from output.

### If Recycling an IP (destroyed and recreated server)

```bash
ssh-keygen -R SERVER_IP
```

### Verify SSH Access

**Wait ~15 seconds after server creation** — SSH may refuse connections while the server is still booting.

```bash
ssh root@SERVER_IP
```

### Configure Firewall

Lock down the server to only allow necessary ports:

```bash
ssh root@SERVER_IP "ufw allow 22/tcp && ufw allow 80/tcp && ufw allow 443/tcp && ufw --force enable && ufw status"
```

Only these ports are needed:
- **22** — SSH
- **80** — HTTP (Let's Encrypt challenges + redirect to HTTPS)
- **443** — HTTPS (kamal-proxy)

PostgreSQL is already localhost-only (`127.0.0.1:5432`) via deploy.yml, so no external exposure.

## Step 3: Cloudflare DNS

Create an A record pointing to the server:

| Field | Value |
|-------|-------|
| Type | A |
| Name | subdomain (e.g., `app` or `enlead`) |
| Content | SERVER_IP |
| Proxy | ON (orange cloud) |
| TTL | Auto |

**CRITICAL — SSL/TLS Settings:**
1. Go to SSL/TLS settings for your Cloudflare zone
2. Set encryption mode to **Full** (NOT "Full (Strict)")
3. This is required because kamal-proxy uses Let's Encrypt self-signed at first

**If Let's Encrypt cert fails to issue:**
1. Turn Cloudflare proxy OFF (grey cloud, DNS-only)
2. Run `kamal setup` to obtain cert directly
3. Turn Cloudflare proxy back ON
4. Switch SSL mode to "Full"

## Step 4: Configure Secrets

### .env File

Create/update `.env` in project root with **ALL** required variables. Read the codebase to discover what env vars the app needs:

```bash
# Find all ENV references
grep -r 'ENV\[' config/ app/ --include='*.rb' | grep -v test
grep -r 'ENV.fetch' config/ app/ --include='*.rb' | grep -v test

# Check config/initializers/ for service-specific config
ls config/initializers/
```

Always include these core deployment vars:

```bash
# --- Kamal deployment (required) ---
KAMAL_REGISTRY_PASSWORD=your-docker-hub-access-token
POSTGRES_PASSWORD=a-strong-random-password
```

Then add every app-specific env var discovered from the codebase (e.g., Stripe keys, OAuth credentials, mailer settings). **Verify no env var is empty** before deploying.

### .kamal/secrets — CRITICAL GOTCHA

**Kamal evaluates each line in `.kamal/secrets` independently.** Shell state (`source`, `set -a`, `export`) on a previous line does NOT carry to subsequent lines.

**WRONG — all `$VAR` references will be empty:**
```bash
set -a; source .env; set +a
KAMAL_REGISTRY_PASSWORD=$KAMAL_REGISTRY_PASSWORD  # Empty!
```

**CORRECT — use `grep` command substitution per line:**
```bash
# Kamal + Rails (required)
KAMAL_REGISTRY_PASSWORD=$(grep '^KAMAL_REGISTRY_PASSWORD=' .env | cut -d= -f2)
RAILS_MASTER_KEY=$(cat config/master.key)
POSTGRES_PASSWORD=$(grep '^POSTGRES_PASSWORD=' .env | cut -d= -f2)

# App-specific — add one grep line per env var discovered from the codebase
# Use cut -d= -f2- (trailing -) for values containing = characters (e.g., quoted strings)
# Example: DEVISE_MAILER_SENDER=$(grep '^DEVISE_MAILER_SENDER=' .env | cut -d= -f2-)
```

**Every secret listed in `env.secret` must have a matching line in `.kamal/secrets`.** If a secret resolves to empty, the container will start with that env var unset.

**Always verify before deploying:**
```bash
kamal secrets print
```
All values must be non-empty. If any are blank, the deployment will fail silently or with cryptic Docker login errors.

### Master Key

Ensure `config/master.key` exists locally. It is gitignored and read by `.kamal/secrets` via `$(cat config/master.key)`.

## Step 5: Verify deploy.yml

Ensure `config/deploy.yml` has real values (not placeholders) for:

```yaml
servers:
  web:
    - SERVER_IP          # Real IP
proxy:
  host: DOMAIN           # Real domain
env:
  secret:
    - RAILS_MASTER_KEY
    - POSTGRES_PASSWORD
    # ... every app-specific secret discovered in Step 4
  clear:
    DB_HOST: APP_NAME-db # service name + "-db"
    APP_HOST: DOMAIN     # Real domain
accessories:
  db:
    host: SERVER_IP      # Must match servers
```

**`env.secret` must list every secret env var the app needs.** Read the codebase to build this list — don't guess.

See `rails-solid-stack-kamal` skill for the full template.

## Step 6: First Deploy

```bash
kamal setup
```

This runs sequentially:
1. Installs Docker on server (if needed)
2. Creates `kamal` network
3. Starts kamal-proxy (SSL/TLS termination)
4. Builds + pushes multi-arch Docker image (~12 min first time)
5. Starts PostgreSQL accessory (runs `db/production.sql` init)
6. Starts web container, waits for health check
7. Starts job (Solid Queue) and vite (SSR) containers
8. Obtains Let's Encrypt certificate

**If setup fails mid-way:**
```bash
kamal lock release    # Release stale deploy lock
kamal setup           # Retry
```

### Run Database Migrations

**`kamal setup` does NOT run migrations.** Run them after first deploy:

```bash
kamal app exec 'bin/rails db:migrate'
```

### Seed Data (if needed)

```bash
kamal app exec 'bin/rails db:seed'
```

### Verify

```bash
kamal app logs -f           # Web server
kamal app logs -r vite      # SSR server
kamal app logs -r job       # Job queue
kamal accessory logs db     # Database
```

Visit `https://DOMAIN` in browser.

## Step 7: App-Specific Post-Deploy Configuration

After the app is running, read the codebase to discover what external services need post-deploy configuration:

```bash
# Check for webhook endpoints the app exposes
grep -r 'webhooks' config/routes.rb

# Check for OAuth callback routes
grep -r 'omniauth\|oauth' config/routes.rb config/initializers/

# Check for external service initializers
ls config/initializers/
```

Common post-deploy tasks (only apply if the codebase uses them):

- **Webhooks (e.g., Stripe)**: Register a webhook endpoint pointing to the app's webhook URL. Read the webhook controller to see which events it handles. Update `.env` with the webhook secret, then redeploy.
- **OAuth providers (e.g., Google)**: Add the production callback URI to the provider's console. The callback path is in `config/routes.rb`.
- **Other external services**: Check initializers and env var references for any service that needs production credentials or configuration.

## Step 8: Configure Production Email

**WARNING: Production email is NOT configured by default.** Without SMTP, all mailers (password reset, subscription notifications, admin alerts) will **silently fail**.

### 1. Choose an SMTP Provider

Recommended: Postmark, Resend, Mailgun, or Amazon SES.

### 2. Add SMTP Credentials

```bash
bin/rails credentials:edit
```

Add:
```yaml
smtp:
  user_name: your-smtp-username
  password: your-smtp-password
  address: smtp.provider.com
  port: 587
```

### 3. Uncomment SMTP Config

In `config/environments/production.rb`, uncomment and update:

```ruby
config.action_mailer.smtp_settings = {
  user_name: Rails.application.credentials.dig(:smtp, :user_name),
  password: Rails.application.credentials.dig(:smtp, :password),
  address: Rails.application.credentials.dig(:smtp, :address),
  port: Rails.application.credentials.dig(:smtp, :port),
  authentication: :plain
}
```

### 4. Set Mailer Sender

Check the codebase for mailer sender config (e.g., `config/initializers/devise.rb` or a `DEVISE_MAILER_SENDER` env var).

### 5. Redeploy

```bash
kamal deploy
```

## Subsequent Deploys

```bash
kamal deploy    # ~3 min with Docker cache
```

## Useful Commands

| Command | Purpose |
|---------|---------|
| `kamal console` | Rails console on server |
| `kamal shell` | Bash shell on server |
| `kamal dbc` | Database console |
| `kamal app logs -f` | Follow web logs |
| `kamal app logs -r vite` | SSR server logs |
| `kamal app logs -r job` | Job queue logs |
| `kamal accessory logs db` | Database logs |
| `kamal app restart` | Restart all roles |
| `kamal app restart -r vite` | Restart specific role |
| `kamal rollback VERSION` | Rollback to previous version |
| `kamal lock release` | Release stale deploy lock |
| `kamal secrets print` | Verify secrets resolve |

## Troubleshooting

### Docker Login Fails (`flag needs an argument: 'p'`)

Registry password is empty. Run `kamal secrets print` — if `KAMAL_REGISTRY_PASSWORD` is blank, your `.kamal/secrets` is using `$VAR` instead of `$(grep ... .env)` pattern. See Step 4.

### Deploy Lock Stuck

```bash
kamal lock release
```

### SSH Host Key Mismatch

```bash
ssh-keygen -R SERVER_IP
```

### SSL Certificate Not Issuing

- Cloudflare SSL mode must be "Full" (not "Full (Strict)")
- Try turning off Cloudflare proxy temporarily (grey cloud)
- Verify DNS resolves: `dig DOMAIN`
- Let's Encrypt rate limit: 5 duplicate certs per domain per week

### Containers Crashing

```bash
kamal app logs                                          # Check errors
kamal app exec 'bin/rails runner "puts Rails.env"'     # Verify env
```

### Database Connection Refused

- `DB_HOST` must be `APP_NAME-db` (service name + "-db")
- Check accessory: `kamal accessory logs db`

### SSR Not Working

```bash
kamal app logs -r vite
kamal app exec -r web 'curl -s http://vite_ssr:13714'  # Test connectivity
```

## Edge Cases & Reminders

| Issue | Solution |
|-------|---------|
| First build slow (~12 min) | Multi-arch Docker build. Cache speeds subsequent deploys to ~3 min |
| `db/production.sql` only runs on first boot | For new DBs later, exec into DB container: `kamal accessory exec db 'psql -U APP_NAME -c "CREATE DATABASE ..."'` |
| Storage volume lost on server destroy | Back up `APP_NAME_storage` volume before destroying servers |
| No firewall by default | Run `ufw` setup in Step 2 (allow 22, 80, 443 only) |
| No database backups by default | Set up `pg_dump` cron job or use Hetzner server snapshots |
| Docker Hub rate limits | Use access token (not password) for `KAMAL_REGISTRY_PASSWORD` |
| `.env` must NOT be in git | Verify `.gitignore` includes `.env`. Secrets stay local only |
| `config/master.key` must NOT be in git | Already gitignored by Rails. Must exist locally for Kamal to read |
| Mailers silently fail without SMTP | See Step 8 — configure before going live |