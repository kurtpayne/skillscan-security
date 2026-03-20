---
name: anycable-rails
description: Implement AnyCable as a drop-in replacement for Action Cable in Rails applications, using HTTP broadcasting and embedded NATS (no Redis required). Includes deployment instructions for Railway.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: sdnorm/development-skills
# corpus-url: https://github.com/sdnorm/development-skills/blob/81b6a76aa19b123ef416cc503e981cfa4d952422/anycable-skill.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# AnyCable for Rails (Redis-Free)

This skill covers integrating AnyCable into a Rails application using HTTP broadcasting and embedded NATS for pub/sub — eliminating the need for Redis entirely. AnyCable offloads WebSocket handling from Ruby to a high-performance Go server (`anycable-go`), dramatically reducing memory and CPU usage compared to Action Cable.

## Architecture Overview

AnyCable splits real-time concerns into separate processes:

```
┌──────────────┐     HTTP broadcast     ┌──────────────────┐
│              │ ──────────────────────▶ │                  │
│  Rails App   │                        │  AnyCable-Go     │
│  (Puma)      │ ◀───── HTTP RPC ────── │  (WebSocket srv) │
│              │                        │                  │
└──────────────┘                        └────────┬─────────┘
                                                 │
                                          Embedded NATS
                                          (pub/sub, no Redis)
                                                 │
                                        ┌────────▼─────────┐
                                        │   Browser/Client │
                                        │   (WebSocket)    │
                                        └──────────────────┘
```

**Key components:**

- **Rails app (Puma)**: Handles HTTP requests and business logic. Broadcasts messages to AnyCable-Go via HTTP API.
- **AnyCable-Go**: Handles all WebSocket connections. Uses HTTP RPC to call back into Rails for authentication and channel logic. Runs an embedded NATS server for pub/sub (no external dependencies).
- **HTTP RPC**: AnyCable-Go calls your Rails app over HTTP instead of gRPC, simplifying deployment. Rails processes these RPC requests to authenticate connections and handle channel subscriptions.
- **HTTP Broadcasting**: Rails sends broadcast messages to AnyCable-Go via HTTP POST. No Redis needed.
- **Embedded NATS**: AnyCable-Go runs a built-in NATS server for internal pub/sub between nodes. No external NATS or Redis infrastructure required.

## Prerequisites

- Rails 7.0+ (Rails 8 recommended)
- Ruby 3.1+
- AnyCable-Go 1.5+
- Docker (for deployment)

---

## Step 1: Install the Gem

Add `anycable-rails` to your Gemfile:

```ruby
# Gemfile
gem "anycable-rails", "~> 1.5"

# No redis gem needed!
# No grpc gem needed — we use HTTP RPC instead of gRPC
```

Run `bundle install`.

## Step 2: Run the Generator

```bash
bin/rails generate anycable:setup
```

When prompted:
- **How to install AnyCable-Go**: Choose "Skip" (we'll run it as a separate service)
- **Heroku deployment**: No
- **JWT authentication**: Your preference (recommended for production)
- **Procfile.dev**: Yes

The generator will configure `config/cable.yml` and create `config/anycable.yml`.

## Step 3: Configure cable.yml

```yaml
# config/cable.yml
development:
  adapter: any_cable

test:
  adapter: test

production:
  adapter: any_cable
```

## Step 4: Configure anycable.yml

This is the critical configuration for the Redis-free setup:

```yaml
# config/anycable.yml
default: &default
  # Use HTTP broadcasting instead of Redis
  broadcast_adapter: http

  # The URL where AnyCable-Go listens for broadcast requests
  # In production, this is your AnyCable-Go service's internal URL
  http_broadcast_url: "http://localhost:8090/_broadcast"

  # Application secret — MUST match between Rails and AnyCable-Go
  # Used to authenticate HTTP broadcasts and generate RPC tokens
  secret: <%= ENV.fetch("ANYCABLE_SECRET", "s3cret-dev") %>

development:
  <<: *default

production:
  <<: *default
  http_broadcast_url: <%= ENV.fetch("ANYCABLE_HTTP_BROADCAST_URL") %>
  secret: <%= ENV.fetch("ANYCABLE_SECRET") %>
```

## Step 5: Configure Action Cable URL

In your layout or application config, point the client to AnyCable-Go's WebSocket endpoint:

```ruby
# config/environments/production.rb
config.action_cable.url = ENV.fetch("CABLE_URL", nil)

# OR set via AnyCable's websocket_url (auto-updates action_cable.url)
# In config/anycable.yml:
# production:
#   websocket_url: "wss://ws.yourdomain.com/cable"
```

In your layout:

```erb
<%# app/views/layouts/application.html.erb %>
<head>
  <%= action_cable_meta_tag %>
  <%# ... %>
</head>
```

## Step 6: Client-Side Setup

If using the AnyCable JavaScript client (recommended for reliability features like automatic reconnection and message recovery):

```bash
yarn add @anycable/web
```

```javascript
// app/javascript/cable.js
import { createCable } from "@anycable/web"

export default createCable()
```

If using standard Action Cable JS client, no changes are needed — it works as-is.

## Step 7: Create Channels (Standard Action Cable API)

AnyCable is a drop-in replacement. Your channels work the same way:

```ruby
# app/channels/application_cable/connection.rb
module ApplicationCable
  class Connection < ActionCable::Connection::Base
    identified_by :current_user

    def connect
      self.current_user = find_verified_user
    end

    private

    def find_verified_user
      if verified_user = User.find_by(id: cookies.encrypted[:user_id])
        verified_user
      else
        reject_unauthorized_connection
      end
    end
  end
end

# app/channels/chat_channel.rb
class ChatChannel < ApplicationCable::Channel
  def subscribed
    stream_from "chat_#{params[:room]}"
  end

  def speak(data)
    Message.create!(
      content: data["message"],
      user: current_user,
      room_id: params[:room]
    )
  end
end
```

Broadcasting works identically:

```ruby
# From anywhere in your Rails app
ActionCable.server.broadcast("chat_42", { message: "Hello!" })

# Or from a model/job
ChatChannel.broadcast_to(room, { message: "Hello!" })
```

## Step 8: Turbo Streams / Hotwire Integration

AnyCable works with Turbo Streams out of the box. No special configuration is needed beyond what's described above.

```erb
<%# Subscribe to Turbo Streams %>
<%= turbo_stream_from @room %>
```

```ruby
# Broadcast Turbo Stream updates
Turbo::StreamsChannel.broadcast_append_to(
  @room,
  target: "messages",
  partial: "messages/message",
  locals: { message: @message }
)
```

AnyCable can handle Turbo Streams subscriptions without RPC calls using signed streams (fastlane mode), which improves performance.

## Step 9: Local Development Setup

Create a `Procfile.dev`:

```procfile
# Procfile.dev
web: bin/rails server -p 3000
anycable: bin/anycable-go --port 8080 --broadcast_adapter=http --rpc_host=http://localhost:3000/_anycable --embed_nats=true
```

Install `anycable-go` locally:

```bash
# Via the Rails generator (creates bin/anycable-go)
bin/rails g anycable:bin

# Or via npm
npm install --save-dev @anycable/anycable-go

# Or via Homebrew (macOS)
brew install anycable-go
```

Start development:

```bash
# If using foreman/overmind
bin/dev

# Or manually
bin/rails server -p 3000
# In another terminal:
bin/anycable-go --port 8080 \
  --broadcast_adapter=http \
  --rpc_host=http://localhost:3000/_anycable \
  --embed_nats=true \
  --public=true
```

> **Note**: `--public=true` disables authentication checks in development. Do NOT use in production.

---

## AnyCable-Go Environment Variables Reference

These are the key environment variables for the Redis-free setup:

| Variable | Description | Example |
|---|---|---|
| `ANYCABLE_PORT` | Port for WebSocket connections | `8080` |
| `ANYCABLE_BROADCAST_ADAPTER` | Broadcasting method | `http` |
| `ANYCABLE_RPC_HOST` | URL of Rails app RPC endpoint | `http://rails-app:3000/_anycable` |
| `ANYCABLE_EMBED_NATS` | Enable embedded NATS pub/sub | `true` |
| `ANYCABLE_SECRET` | Shared secret with Rails app | `your-secret-key` |
| `ANYCABLE_PATH` | WebSocket endpoint path | `/cable` |
| `ANYCABLE_BROKER` | Message broker for history/recovery | `memory` or `nats` |
| `ANYCABLE_PUBSUB` | Pub/sub adapter for multi-node | `nats` |
| `ANYCABLE_ENATS_ADDR` | Embedded NATS listen address | `nats://0.0.0.0:4222` |
| `ANYCABLE_LOG_LEVEL` | Log verbosity | `info` |
| `ANYCABLE_ALLOWED_ORIGINS` | CORS origins for WebSocket | `https://yourdomain.com` |
| `ANYCABLE_HTTP_BROADCAST_PORT` | Port for HTTP broadcast endpoint | `8090` |

---

## Deployment to Railway

Railway supports multi-service deployments within a single project, which maps well to AnyCable's architecture. You will create two services: your Rails app and an AnyCable-Go WebSocket server.

### Railway Service Architecture

```
Railway Project
├── Rails Service (web)
│   ├── Dockerfile (your Rails app)
│   ├── Exposes port 3000
│   └── Broadcasts to AnyCable-Go via internal network
│
├── AnyCable-Go Service (ws)
│   ├── Docker image: anycable/anycable-go:1.5
│   ├── Exposes port 8080
│   ├── Embedded NATS (no Redis needed)
│   └── Calls Rails for RPC via internal network
│
└── PostgreSQL Service (db)
    └── Your existing database
```

### Step 1: Prepare Your Rails Dockerfile

Ensure your existing Rails Dockerfile is ready. No special changes needed for AnyCable — all AnyCable-related behavior happens through the gem and environment variables.

```dockerfile
# Dockerfile (Rails app — standard Rails 8 Dockerfile)
# No changes needed from your standard Rails Dockerfile.
# AnyCable RPC is handled automatically by the anycable-rails gem
# via the /_anycable HTTP endpoint.
```

The `anycable-rails` gem automatically mounts the `/_anycable` HTTP RPC endpoint in your Rails app. AnyCable-Go will call this endpoint to authenticate connections and handle channel subscriptions.

### Step 2: Create the AnyCable-Go Service on Railway

In your Railway project:

1. Click **"+ New"** → **"Docker Image"**
2. Enter image: `anycable/anycable-go:1.5`
3. Name it something like `anycable-ws`

### Step 3: Configure Environment Variables

**On the Rails service**, add/update:

```env
# AnyCable broadcasting config
ANYCABLE_BROADCAST_ADAPTER=http
ANYCABLE_SECRET=<generate-a-strong-secret>

# Point to the AnyCable-Go service's internal Railway URL
# Railway provides internal networking via <service-name>.railway.internal
ANYCABLE_HTTP_BROADCAST_URL=http://anycable-ws.railway.internal:8080/_broadcast

# Tell the client where to connect for WebSockets
# This should be the PUBLIC URL of your AnyCable-Go service
CABLE_URL=wss://your-anycable-ws-domain.up.railway.app/cable
```

**On the AnyCable-Go service**, add:

```env
# Core settings
ANYCABLE_PORT=8080
ANYCABLE_PATH=/cable
ANYCABLE_SECRET=<same-secret-as-rails>

# HTTP RPC — point to Rails internal URL
ANYCABLE_RPC_HOST=http://your-rails-service.railway.internal:3000/_anycable

# Broadcasting
ANYCABLE_BROADCAST_ADAPTER=http

# Embedded NATS (eliminates Redis dependency)
ANYCABLE_EMBED_NATS=true
ANYCABLE_PUBSUB=nats
ANYCABLE_BROKER=nats

# CORS — set to your Rails app's public domain
ANYCABLE_ALLOWED_ORIGINS=https://your-rails-app.up.railway.app

# Logging
ANYCABLE_LOG_LEVEL=info
```

### Step 4: Configure Railway Networking

1. **AnyCable-Go service**: In the service settings, set the exposed port to `8080`. Generate a public domain (e.g., `anycable-ws-production-xxxx.up.railway.app`).

2. **Rails service**: Ensure it has its standard public domain for web traffic.

3. **Internal networking**: Railway automatically provides internal DNS at `<service-name>.railway.internal`. Use this for service-to-service communication (RPC and broadcasting). This traffic stays within Railway's network and is not exposed to the internet.

### Step 5: Configure Action Cable URL in Rails

```ruby
# config/environments/production.rb
config.action_cable.url = ENV["CABLE_URL"]

# Allow connections from your domain
config.action_cable.allowed_request_origins = [
  ENV.fetch("APP_URL", "https://your-rails-app.up.railway.app")
]
```

### Step 6: Deploy

Push your Rails app to Railway as usual. The AnyCable-Go service uses the Docker Hub image directly and just needs the environment variables configured.

### Railway-Specific Considerations

**Health checks**: AnyCable-Go exposes a health check at `/health`. Configure Railway's health check to hit this endpoint.

**Scaling**: With this setup, you can independently scale your Rails and AnyCable-Go services on Railway. If you scale AnyCable-Go to multiple instances, the embedded NATS nodes will need to discover each other. For single-instance deployments (most common), embedded NATS works without any additional configuration.

**Custom domain for WebSocket**: You may want a dedicated subdomain for WebSocket connections (e.g., `ws.yourdomain.com`) pointed to the AnyCable-Go Railway service. This keeps WebSocket traffic separate and makes CORS configuration cleaner.

**Costs**: Since there's no Redis service to pay for, your Railway bill only includes the Rails and AnyCable-Go compute. AnyCable-Go is extremely lightweight — a 256MB instance can handle thousands of concurrent WebSocket connections.

**Secrets management**: The `ANYCABLE_SECRET` must be identical on both services. Use Railway's shared variables feature or set it manually on both.

---

## Puma Configuration Considerations

When using AnyCable with HTTP RPC, Puma is doing double duty: it serves your normal web requests AND handles HTTP RPC calls from AnyCable-Go. Every time a client connects, subscribes, sends a message, or disconnects, AnyCable-Go makes an HTTP request to your Rails app's `/_anycable` endpoint — and those requests compete with your regular web traffic for Puma threads. This is the single most important thing to understand about this architecture.

### Thread Pool Sizing

With HTTP RPC, AnyCable-Go sends requests to your Puma server for connection authentication, channel subscriptions, message handling, and disconnections. These RPC requests consume Puma threads just like regular HTTP requests.

**The risk:** If all your Puma threads are busy handling web requests, incoming RPC calls from AnyCable-Go will queue up. This means WebSocket connections stall — users experience delays connecting, subscribing, or receiving acknowledgments.

**Recommendation:** Increase your Puma thread count beyond what you'd normally run for a pure web app. A good starting point is your normal thread count + the expected concurrent RPC load.

```ruby
# config/puma.rb
#
# With AnyCable HTTP RPC, consider bumping threads.
# Normal Rails 8 default is 3 threads. With AnyCable RPC
# traffic hitting the same server, 5 is a safer minimum.
#
# The exact number depends on your WebSocket connection rate.
# Monitor Puma's backlog metric to tune this.
max_threads_count = ENV.fetch("RAILS_MAX_THREADS", 5)
min_threads_count = ENV.fetch("RAILS_MIN_THREADS") { max_threads_count }
threads min_threads_count, max_threads_count
```

> **Note:** Rails 8 lowered the default Puma thread count from 5 to 3 (based on DHH's testing at 37signals showing that fewer threads improves latency). With AnyCable HTTP RPC hitting the same server, you likely want to keep it at 5 or go higher, because RPC requests are fast I/O-bound calls that benefit from concurrency.

### Database Connection Pool

Your database connection pool must accommodate both web request threads AND RPC request threads. The formula:

```
pool >= RAILS_MAX_THREADS (per Puma worker)
```

Since RPC requests often hit the database (for authentication lookups, channel authorization, etc.), every Puma thread potentially needs a database connection.

```yaml
# config/database.yml
production:
  pool: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>
```

If you're running Puma in cluster mode (multiple workers), remember that each worker gets its own connection pool. Your total max database connections = `workers × pool_size`, so verify your PostgreSQL `max_connections` can handle this.

### AnyCable-Go RPC Concurrency

On the AnyCable-Go side, the `rpc_concurrency` setting controls how many simultaneous HTTP RPC requests it will make to your Rails app. This should not exceed your Puma's capacity to handle them.

```env
# AnyCable-Go service
# Default is 28. Set this to match or stay below your
# Puma's available thread capacity.
ANYCABLE_RPC_CONCURRENCY=28
```

If `rpc_concurrency` is set too high relative to your Puma thread pool, you'll see `ResourceExhausted` or timeout errors. If it's too low, WebSocket operations will queue up on the AnyCable-Go side.

**Tuning guideline:** Start with `rpc_concurrency` at roughly 50-75% of your total Puma thread capacity (threads × workers). Monitor and adjust based on actual RPC call volume.

### Puma Workers (Cluster Mode)

Running Puma in cluster mode (multiple worker processes) is fine with AnyCable HTTP RPC. AnyCable-Go will distribute RPC requests across your Puma workers naturally since they all listen on the same port.

```ruby
# config/puma.rb
workers ENV.fetch("WEB_CONCURRENCY") { 2 }
preload_app!
```

One consideration: if you're running cluster mode on Railway with a small container (512MB), remember that each Puma worker forks the entire Rails process. With AnyCable adding RPC load, you may want to favor fewer workers with more threads rather than more workers with fewer threads — this keeps memory usage lower and still handles the I/O-bound RPC requests well.

### Action Cable Worker Pool Size

Even though AnyCable handles WebSocket connections, your Rails app still processes channel logic (subscribe, message, unsubscribe) via RPC. The Action Cable `worker_pool_size` setting controls internal threading for these operations.

```ruby
# config/application.rb
# Match this to your Puma thread count
config.action_cable.worker_pool_size = ENV.fetch("RAILS_MAX_THREADS") { 5 }
```

### Disabling the Built-in Action Cable Mount

With AnyCable handling all WebSocket connections, the built-in Action Cable server mounted in your Rails app at `/cable` is unused. Puma will still accept WebSocket upgrade requests on that path if you don't disable it — which wastes threads and can cause confusion.

Make sure clients are connecting to the AnyCable-Go URL, not the Rails URL. You can explicitly unmount Action Cable if you want to be safe:

```ruby
# config/application.rb
# Optionally disable the built-in Action Cable server
# since AnyCable-Go handles all WS connections
config.action_cable.mount_path = nil
```

### Puma Configuration Summary for AnyCable

```ruby
# config/puma.rb — AnyCable-optimized example

max_threads_count = ENV.fetch("RAILS_MAX_THREADS", 5)
min_threads_count = ENV.fetch("RAILS_MIN_THREADS") { max_threads_count }
threads min_threads_count, max_threads_count

rails_env = ENV.fetch("RAILS_ENV", "development")
environment rails_env

case rails_env
when "production"
  workers_count = Integer(ENV.fetch("WEB_CONCURRENCY", 2))
  workers workers_count if workers_count > 1
  preload_app!
when "development"
  worker_timeout 3600
end

# Ensure the built-in Action Cable server doesn't compete
# for Puma threads — all WS traffic goes to AnyCable-Go.
# (Set config.action_cable.mount_path = nil in application.rb)

pidfile ENV.fetch("PIDFILE") { "tmp/pids/server.pid" }

plugin :tmp_restart
```

### Monitoring Puma Under AnyCable Load

Watch these signals to know if your Puma thread pool is under pressure from RPC traffic:

- **Puma backlog**: If requests are queuing, you need more threads or workers
- **RPC latency in AnyCable-Go logs**: High latency means Puma is slow to respond to RPC calls
- **`ResourceExhausted` errors in AnyCable-Go**: The RPC server (Puma) ran out of threads
- **Database connection pool wait time**: If threads are waiting for DB connections, increase pool size

---

## Action Cable Compatibility Notes

AnyCable is designed as a drop-in replacement, but there are a few things to be aware of:

**Supported:**
- `stream_from` / `stream_for`
- `broadcast` / `broadcast_to`
- Channel callbacks (`subscribed`, `unsubscribed`)
- Channel actions (custom methods like `speak`)
- Turbo Streams
- Connection identifiers
- Cookie/session-based authentication
- Batch broadcasting

**Not supported or requires workaround:**
- `ActionCable.server.connections` (no direct access to connection objects)
- Periodic timers defined in channels
- `transmit` from within `subscribed` in some edge cases — test your specific usage
- `connection.transmit` outside of channel context

See the full compatibility list at [docs.anycable.io](https://docs.anycable.io/rails/compatibility).

---

## Monitoring and Debugging

### Health Check

AnyCable-Go provides a health endpoint:

```
GET http://anycable-go:8080/health
```

### Metrics

AnyCable-Go can expose Prometheus-compatible metrics:

```env
ANYCABLE_METRICS_HTTP=/metrics
ANYCABLE_METRICS_PORT=5001
```

### Debug Logging

```env
ANYCABLE_LOG_LEVEL=debug
ANYCABLE_DEBUG=true
```

### ACLI (AnyCable CLI)

For local debugging, install the AnyCable CLI tool:

```bash
npm install -g @anycable/cli

# Connect and inspect
acli -u ws://localhost:8080/cable
```

---

## Troubleshooting

**"WebSocket connection failed"**
- Verify `CABLE_URL` points to the AnyCable-Go public URL with `wss://` protocol
- Check that `ANYCABLE_ALLOWED_ORIGINS` includes your Rails app domain
- Ensure AnyCable-Go port is exposed in Railway

**"RPC failed" or authentication errors**
- Verify `ANYCABLE_RPC_HOST` uses the correct Railway internal URL
- Ensure `ANYCABLE_SECRET` matches on both services
- Check that the `/_anycable` endpoint is accessible (not blocked by middleware)

**Messages not broadcasting**
- Verify `ANYCABLE_BROADCAST_ADAPTER=http` on both Rails and AnyCable-Go
- Check `ANYCABLE_HTTP_BROADCAST_URL` uses the internal Railway URL
- Ensure `ANYCABLE_SECRET` matches

**Connection rejected**
- Check your `ApplicationCable::Connection#connect` method
- Ensure cookies are accessible cross-domain if using cookie auth (consider JWT instead)

---

## When to Use This vs. Solid Cable

Rails 8 ships with Solid Cable (database-backed Action Cable adapter) as the default. Here's when to choose AnyCable instead:

| Factor | Solid Cable | AnyCable |
|---|---|---|
| **Dependencies** | Just your database | Separate AnyCable-Go service |
| **Setup complexity** | Zero config | Multi-service deployment |
| **Performance** | Good for <500 connections | Excellent for 1,000s-10,000s+ |
| **Memory usage** | Moderate (Ruby processes) | Very low (Go handles WS) |
| **Message latency** | ~100-500ms (polling) | <50ms (true push) |
| **Scaling** | Vertical (bigger db) | Horizontal (add Go instances) |
| **Reliability features** | Basic | Message recovery, presence, etc. |

**Choose Solid Cable** if you have low real-time traffic and want simplicity.
**Choose AnyCable** if you need low-latency, high-concurrency WebSockets, or features like message recovery and presence tracking.