---
name: colyseus_skill
description: Colyseus is a powerful, open-source multiplayer game framework for Node.js
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: BatuhanK/skills-colyseus
# corpus-url: https://github.com/BatuhanK/skills-colyseus/blob/65539d22b7e6192657d4466f2857bc6e67e3f519/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Colyseus Multiplayer Framework - AI Agent Skills Guide

> **Version:** 0.17 | **Last Updated:** 2024

## What is Colyseus?

Colyseus is a powerful, open-source multiplayer game framework for Node.js. It provides:

- **Real-time state synchronization** with efficient binary patching
- **Room-based architecture** for matchmaking and game sessions
- **Schema-based state management** with automatic client-server sync
- **WebSocket communication** with fallback support
- **Horizontal scaling** with Redis presence
- **Multiple client SDKs** (TypeScript, Unity, Defold, Haxe, C++, Construct 3)

---

## Quick Navigation

| Document                                              | Description                             | When to Use                                  |
| ----------------------------------------------------- | --------------------------------------- | -------------------------------------------- |
| [Core Concepts](./colyseus/core.md)                   | Room lifecycle, state sync, matchmaking | Learning fundamentals or building first room |
| [Architecture & Patterns](./colyseus/architecture.md) | Design patterns, scalability, auth      | Building production games                    |
| [Client Integration](./colyseus/client.md)            | Client SDK, callbacks, reconnection     | Implementing client-side code                |
| [Best Practices](./colyseus/bestpractices.md)         | Performance, security, testing          | Optimizing and deploying                     |
| [Command Pattern](./colyseus/command-pattern.md)      | @colyseus/command usage                 | Structuring complex game logic               |

---

## Table of Contents

- [How to Use This Guide](#how-to-use-this-guide)
- [Quick Start](#quick-start)
- [Document Reference](#document-reference)
- [Common Patterns Cheat Sheet](#common-patterns-cheat-sheet)
- [Troubleshooting](#troubleshooting)

---

## How to Use This Guide

### For AI Agents

This guide is split into focused documents to help you quickly find relevant information:

1. **Quick Start** (below) - Get a room running in 5 minutes
2. **[Core Concepts](./colyseus/core.md)** - Fundamental patterns every developer needs
3. **[Architecture & Patterns](./colyseus/architecture.md)** - Production-ready design patterns
4. **[Client Integration](./colyseus/client.md)** - Client SDK implementation details
5. **[Best Practices](./colyseus/bestpractices.md)** - Performance, security, deployment
6. **[Command Pattern](./colyseus/command-pattern.md)** - Advanced pattern for complex games

### Decision Framework

```
┌─────────────────────────────────────────────────────────────────┐
│              WHAT DO YOU NEED TO IMPLEMENT?                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ Basic Room  │  │ State Sync  │  │Matchmaking  │             │
│  │  Setup      │  │             │  │             │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         │                │                │                     │
│         ▼                ▼                ▼                     │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  Quick Start → Core Concepts                         │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ Production  │  │  Client     │  │  Complex    │             │
│  │  Scaling    │  │   SDK       │  │  Game Logic │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         │                │                │                     │
│         ▼                ▼                ▼                     │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  Architecture → Client Integration → Command Pattern │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐                              │
│  │ Performance │  │  Security   │                              │
│  │  Optimize   │  │   Harden    │                              │
│  └──────┬──────┘  └──────┬──────┘                              │
│         │                │                                     │
│         ▼                ▼                                     │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  Best Practices                                      │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Installation

```bash
# Create a new Colyseus project
npm create colyseus-app@latest ./my-server
cd my-server

# Or add to existing project
npm install colyseus @colyseus/schema
```

### Minimal Server (Modern Pattern)

```typescript
// src/rooms/MyRoom.ts
import { Room, Client, CloseCode } from "colyseus";
import { Schema, type, MapSchema } from "@colyseus/schema";

// Define state
class Player extends Schema {
  @type("string") sessionId: string = "";
  @type("string") name: string = "";
  @type("number") x: number = 0;
  @type("number") y: number = 0;
}

class GameState extends Schema {
  @type({ map: Player }) players = new MapSchema<Player>();
}

// Define room
export class MyRoom extends Room<GameState> {
  maxClients = 4;
  state = new GameState();

  // Modern message handling pattern
  messages = {
    move: (client: Client, data: { x: number; y: number }) => {
      const player = this.state.players.get(client.sessionId);
      if (player) {
        player.x = data.x;
        player.y = data.y;
      }
    },

    chat: (client: Client, message: string) => {
      this.broadcast(
        "chatMessage",
        {
          sender: client.sessionId,
          text: message,
        },
        { except: client },
      );
    },
  };

  onCreate(options: any) {
    console.log("Room created:", this.roomId);
  }

  onJoin(client: Client, options: any) {
    console.log(client.sessionId, "joined!");

    const player = new Player();
    player.sessionId = client.sessionId;
    player.name = options.name || "Player";
    player.x = Math.random() * 100;
    player.y = Math.random() * 100;
    this.state.players.set(client.sessionId, player);
  }

  onLeave(client: Client, code: CloseCode) {
    console.log(client.sessionId, "left!");
    this.state.players.delete(client.sessionId);
  }

  onDispose() {
    console.log("Room disposed:", this.roomId);
  }
}
```

### Server Configuration

```typescript
// src/app.config.ts
import { defineServer, defineRoom } from "colyseus";
import { MyRoom } from "./rooms/MyRoom";

export default defineServer({
  rooms: {
    my_room: defineRoom(MyRoom, {
      // Room options
      maxClients: 8,
    }),
  },

  // Optional: HTTP routes
  express: (app) => {
    app.get("/health", (req, res) => {
      res.json({ status: "ok" });
    });
  },
});
```

### Minimal Client

```typescript
import { Client } from "colyseus.js";

const client = new Client("ws://localhost:2567");

async function main() {
  try {
    // Join or create a room
    const room = await client.joinOrCreate("my_room", {
      name: "Player1",
    });

    console.log("Joined room:", room.roomId);

    // Listen to state changes
    room.state.players.onAdd((player, sessionId) => {
      console.log("Player joined:", sessionId, player.name);
    });

    room.state.players.onRemove((player, sessionId) => {
      console.log("Player left:", sessionId);
    });

    room.state.players.onChange((player, sessionId) => {
      console.log("Player moved:", sessionId, player.x, player.y);
    });

    // Send messages
    room.send("move", { x: 50, y: 50 });
    room.send("chat", "Hello everyone!");

    // Handle messages from server
    room.onMessage("chatMessage", (data) => {
      console.log(`${data.sender}: ${data.text}`);
    });
  } catch (e) {
    console.error("Join error:", e);
  }
}

main();
```

### Run the Server

```bash
npm start
# Server listening on ws://localhost:2567
```

---

## Document Reference

### [Core Concepts](./colyseus/core.md)

Essential knowledge for every Colyseus developer:

- **Room Lifecycle** - onCreate, onJoin, onLeave, onDrop, onReconnect, onDispose
- **State Synchronization** - @colyseus/schema, decorators, MapSchema, ArraySchema
- **State vs Messages** - When to use each communication method
- **Matchmaking** - joinOrCreate, join, create, joinById with filtering
- **Modern Message Handling** - The `messages` object pattern (recommended)

**Use this when:** Building your first room or need to understand fundamentals.

---

### [Architecture & Design Patterns](./colyseus/architecture.md)

Production-ready patterns for scalable games:

- **Room Design Patterns** - Game Room, Lobby, Spectator, Persistent World
- **State Management** - Keeping schemas lean, logic delegation
- **Message Handling** - Validation with Zod, broadcasting strategies
- **Authentication** - Token validation, client.auth patterns
- **Scalability** - RedisPresence, RedisDriver, multi-process

**Use this when:** Building production games or designing complex systems.

---

### [Client Integration & SDK Usage](./colyseus/client.md)

Everything about client-side implementation:

- **Client SDK Basics** - Creating connections, joining rooms
- **State Sync Callbacks** - onAdd, onRemove, onChange
- **Message Handling** - Sending and receiving messages
- **Reconnection Strategies** - Manual and automatic reconnection
- **Integration Patterns** - HTTP routes, database, external APIs
- **Client-Side Considerations** - Interpolation, prediction

**Use this when:** Implementing client-side code or integrating with game engines.

---

### [Best Practices & Performance](./colyseus/bestpractices.md)

Optimize and secure your game:

- **Performance Optimization** - Patch rate tuning, StateView, bandwidth
- **Memory Management** - Clock timers, cleanup, preventing leaks
- **Security Best Practices** - Rate limiting, validation, auth
- **Error Handling** - Exceptions, reconnection, graceful shutdown
- **Testing & Debugging** - Unit tests, load testing, monitoring
- **Production Checklist** - Deployment, monitoring, common pitfalls

**Use this when:** Optimizing performance or preparing for production.

---

### [Command Pattern](./colyseus/command-pattern.md)

Advanced pattern for complex game logic:

- **Why Use Commands** - Decoupling, queues, undo/redo, testability
- **Installation** - @colyseus/command setup
- **Basic Usage** - Dispatcher, command classes, execution
- **Advanced Patterns** - Delayed commands, undo support, batching
- **Best Practices** - When to use, common pitfalls

**Use this when:** Building complex games with many actions, need undo/redo, or want clean architecture.

---

## Common Patterns Cheat Sheet

### Room Lifecycle Methods

```typescript
class MyRoom extends Room {
  // Called once when room is created
  onCreate(options) {}

  // Called when each client joins
  onJoin(client, options) {}

  // Called when client disconnects unexpectedly
  onDrop(client, code) {}

  // Called when client successfully reconnects
  onReconnect(client) {}

  // Called when client leaves (consented or after onDrop)
  onLeave(client, code) {}

  // Called when room is destroyed
  onDispose() {}
}
```

### Modern Message Handling (Recommended)

```typescript
class MyRoom extends Room {
  messages = {
    // Specific handlers
    move: (client, data) => {
      /* ... */
    },
    attack: (client, data) => {
      /* ... */
    },

    // Fallback for unhandled types
    "*": (client, type, data) => {
      /* ... */
    },
  };
}
```

### State Decorators

```typescript
class Player extends Schema {
  @type("string") name: string;
  @type("number") x: number;
  @type("boolean") isReady: boolean;
  @type(["string"]) tags: string[];
  @type({ map: Item }) inventory: MapSchema<Item>;
}
```

### Matchmaking Methods

```typescript
// Client-side
const room = await client.joinOrCreate("room_name", options);
const room = await client.join("room_name", options);
const room = await client.create("room_name", options);
const room = await client.joinById("room_id", options);

// Server-side (matchMaker API)
import { matchMaker } from "colyseus";
const room = await matchMaker.createRoom("room_name", options);
const reservation = await matchMaker.joinOrCreate("room_name", options);
```

### Client State Callbacks

```typescript
// Listen to state changes
room.state.players.onAdd((player, sessionId) => {});
room.state.players.onRemove((player, sessionId) => {});
room.state.players.onChange((player, sessionId) => {});

// Listen to specific property changes
player.listen("x", (newX, prevX) => {});
```

### Authentication Pattern

```typescript
class MyRoom extends Room {
  async onAuth(client, options, context) {
    // Validate token
    const user = await validateToken(options.token);
    if (!user) throw new Error("Invalid token");
    return user; // Available as client.auth
  }

  onJoin(client, options) {
    console.log(client.auth.userId); // Access auth data
  }
}
```

### Rate Limiting Pattern

```typescript
class MyRoom extends Room {
  maxMessagesPerSecond = 30; // Built-in rate limiting

  messages = {
    spam: (client, data) => {
      // This room allows 30 messages/second per client
      // Excess messages auto-disconnect the client
    },
  };
}
```

---

## Troubleshooting

### Common Errors

| Error                                                    | Cause                                     | Solution                                                    |
| -------------------------------------------------------- | ----------------------------------------- | ----------------------------------------------------------- |
| `seat reservation expired`                               | Server overload or mixed package versions | Increase `seatReservationTimeout` or check package versions |
| `Class constructor Room cannot be invoked without 'new'` | Wrong tsconfig target                     | Set `"target": "es2015"` or higher                          |
| State not synchronizing                                  | Missing type decorators                   | Add `@type()` decorators to all sync properties             |
| `Cannot read property of undefined`                      | Accessing state before onCreate           | Initialize state in `onCreate()` or as class property       |

### Debug Logging

```typescript
onCreate() {
  // Enable verbose logging
  this.onMessage("*", (client, type, message) => {
    console.log(`[${client.sessionId}] ${type}:`, message);
  });
}
```

### Performance Checklist

- [ ] State size under 100KB per room
- [ ] Patch rate at 20-50ms (20-50fps)
- [ ] Using StateView for per-client filtering
- [ ] Validating all client inputs
- [ ] Rate limiting enabled
- [ ] Proper cleanup in onDispose

---

## Quick Links

- **Official Documentation**: https://docs.colyseus.io/
- **GitHub**: https://github.com/colyseus/colyseus
- **npm**: https://www.npmjs.com/package/colyseus
- **Discord**: http://chat.colyseus.io/

---

_This guide is maintained for AI agents working with Colyseus. For the latest updates, refer to the official documentation._