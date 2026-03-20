---
name: feathersjs-expert
description: Expert guidance on FeathersJS (v6 Six). You MUST use this skill for ANY request related to FeathersJS, including services, around/before/after hooks, TypeBox schemas, resolvers, authentication strategies (JWT, OAuth, Local), and transports like @feathersjs/koa or @feathersjs/socketio. Use it for architecture design, debugging service methods, migrations from v4 (Crow), and client-side integration. Trigger this skill even if the user just mentions 'Feathers', '@feathersjs', or wants to build a 'real-time, event-driven API' with Node.js, Deno, or Bun.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: nazifishrak/feathersjs-expert-skill
# corpus-url: https://github.com/nazifishrak/feathersjs-expert-skill/blob/10c8fa7069d3bec5b5fc4f9c8b2f0b47144a63cb/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# FeathersJS Expert

This skill provides expert knowledge on FeathersJS, specifically the latest version (v6 Six). Feathers is a framework for building real-time applications and REST APIs using JavaScript or TypeScript.

## Core Concepts

### Services
Services are the heart of every Feathers application. A service is an object or instance of a class that implements a certain interface. Standard methods include:
- `find(params)` - Find multiple resources.
- `get(id, params)` - Get a single resource.
- `create(data, params)` - Create a new resource.
- `update(id, data, params)` - Update a resource (replaces the whole resource).
- `patch(id, data, params)` - Patch a resource (merges changes).
- `remove(id, params)` - Remove a resource.

### Hooks
Hooks are pluggable middleware functions that can be registered **around**, **before**, **after** or on **error**(s) of a service method.
- `around` hooks (new in v6) or v5 wrap the entire call, including before/after/error logic.
- `before` hooks run before the service method.
- `after` hooks run after the service method.
- `error` hooks run if an error occurs.

### Schemas & Resolvers
Feathers 5 uses **TypeBox** for schema definition and **Resolvers** for data transformation and validation.
- `userSchema`: Defines the data model.
- `userValidator`: Validates incoming data.
- `userResolver`: Resolves properties (e.g., population, hashing passwords).
- `userExternalResolver`: Safely hides sensitive data for external clients.

### Authentication
Feathers provides a built-in authentication service with strategies for JWT, Local (username/password), and OAuth.

### Transports
Common transports are:
- `@feathersjs/koa` for REST.
- `@feathersjs/socketio` for real-time.

## References
Detailed documentation is available in the `references/` directory. Use the following guides for specific tasks:

### API Reference
- `api/application.md`: The `app` object.
- `api/services.md`: Working with services.
- `api/hooks.md`: Registering and using hooks.
- `api/authentication.md`: Authentication service.
- `api/channels.md`: Real-time events and channels.

### Guides
- `guides/basics/starting.md`: Quick start.
- `guides/basics/generator.md`: Creating an app with the CLI.
- `guides/basics/schemas.md`: Using schemas and resolvers.
- `guides/basics/authentication.md`: Setting up authentication.

### Cookbook (Recipes)
- `cookbook/authentication/`: Various authentication recipes (Auth0, Google, etc.).
- `cookbook/express/`: File uploads and SSR.
- `cookbook/general/scaling.md`: Scaling Feathers apps.

## Usage Guidelines
- **Always use TypeScript**: Feathers 5 is designed with TypeScript in mind. Provide typed examples.
- **Prefer Around Hooks**: For Feathers 5, use `around` hooks for better control and type safety.
- **Use Schemas for Validation**: Do not use manual validation in hooks; prefer TypeBox schemas and resolvers.
- **Real-time**: Explain how `app.publish` and channels work for real-time updates.
- **Transports**: Mention that Feathers is transport-agnostic; code works the same for REST and WebSockets.