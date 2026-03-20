---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: migkapa/chatkit-skill
# corpus-url: https://github.com/migkapa/chatkit-skill/blob/557a90d2f584ea7931d2e396e12b0eaca43ced5a/skill.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# ChatKit Skill

Build AI-powered chat experiences using OpenAI's ChatKit framework.

## When to Use This Skill

Use this skill when the user asks to:
- Set up ChatKit in a project
- Create ChatKit widgets (cards, forms, lists, buttons)
- Customize ChatKit themes
- Implement ChatKit actions
- Build a self-hosted ChatKit server
- Connect ChatKit to Agent Builder workflows

## Overview

ChatKit is OpenAI's framework-agnostic, drop-in chat solution for building agentic chat experiences. It provides:
- **UI Components**: Pre-built widgets for rich chat interfaces
- **Theming**: Customizable colors, typography, density, and styling
- **Actions**: Trigger backend logic from UI interactions
- **Streaming**: Built-in response streaming support
- **File Attachments**: Upload handling with multiple strategies
- **Entity Tags**: @mentions with custom search and previews

### Integration Methods
- **React**: `@openai/chatkit-react` package with `useChatKit` hook
- **Vanilla JS**: `<openai-chatkit>` web component via CDN

### Backend Options
- **OpenAI-hosted**: Uses Agent Builder workflows (recommended for quick setup)
- **Self-hosted**: ChatKit Python SDK on your own infrastructure

### Key Resources
- JS SDK: https://github.com/openai/chatkit-js
- Python SDK: https://github.com/openai/chatkit-python
- Widget Builder: https://widgets.chatkit.studio
- Playground: https://chatkit.studio/playground
- Demo: https://chatkit.world

---

## Quick Start

### React Setup

```bash
npm install @openai/chatkit-react
```

```tsx
import { ChatKit, useChatKit } from '@openai/chatkit-react';

export function MyChat() {
  const { control } = useChatKit({
    api: {
      async getClientSecret(existing) {
        if (existing) {
          // Implement session refresh if needed
        }
        const res = await fetch('/api/chatkit/session', { method: 'POST' });
        const { client_secret } = await res.json();
        return client_secret;
      },
    },
  });

  return <ChatKit control={control} className="h-[600px] w-[320px]" />;
}
```

### Vanilla JS Setup

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js" async></script>
</head>
<body>
  <openai-chatkit id="my-chat" style="height: 600px; width: 320px;"></openai-chatkit>

  <script>
    const chatkit = document.getElementById('my-chat');
    chatkit.setOptions({
      api: {
        async getClientSecret(currentClientSecret) {
          if (!currentClientSecret) {
            const res = await fetch('/api/chatkit/session', { method: 'POST' });
            const { client_secret } = await res.json();
            return client_secret;
          }
          // Handle refresh
          const res = await fetch('/api/chatkit/refresh', {
            method: 'POST',
            body: JSON.stringify({ currentClientSecret }),
            headers: { 'Content-Type': 'application/json' },
          });
          const { client_secret } = await res.json();
          return client_secret;
        }
      }
    });
  </script>
</body>
</html>
```

### Session Endpoint (FastAPI)

```python
from fastapi import FastAPI
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

@app.post("/api/chatkit/session")
def create_chatkit_session():
    session = client.chatkit.sessions.create(
        workflow={"id": "wf_YOUR_WORKFLOW_ID"},
        user="user_123"  # Optional user identifier
    )
    return {"client_secret": session.client_secret}
```

### Session Endpoint (Express)

```typescript
import express from 'express';
import OpenAI from 'openai';

const app = express();
const openai = new OpenAI();

app.post('/api/chatkit/session', async (req, res) => {
  const session = await openai.chatkit.sessions.create({
    workflow: { id: 'wf_YOUR_WORKFLOW_ID' },
    user: 'user_123'
  });
  res.json({ client_secret: session.client_secret });
});
```

---

## Agent Builder Integration

Agent Builder is a visual canvas for designing multi-step agent workflows that power ChatKit backends.

### Steps to Connect
1. Create a workflow in Agent Builder at https://platform.openai.com/agent-builder
2. Copy your workflow ID (format: `wf_xxxx...`)
3. Pass the workflow ID when creating ChatKit sessions:

```python
session = client.chatkit.sessions.create(
    workflow={"id": "wf_68df4b13b3588190a09d19288d4610ec0df388c3983f58d1"}
)
```

---

## Theming Reference

Customize ChatKit appearance with the `theme` option.

### Complete Theme Options

```typescript
const options: Partial<ChatKitOptions> = {
  theme: {
    // Color scheme
    colorScheme: "light" | "dark",

    // Accent color
    color: {
      accent: {
        primary: "#2D8CFF",  // Hex color
        level: 2             // 1-5, intensity level
      }
    },

    // Border radius
    radius: "none" | "sm" | "md" | "lg" | "round",

    // Information density
    density: "compact" | "comfortable",

    // Typography
    typography: {
      fontFamily: "'Inter', sans-serif"
    }
  }
};
```

### Theme Presets

**Corporate Light**
```typescript
theme: {
  colorScheme: "light",
  color: { accent: { primary: "#0066CC", level: 2 } },
  radius: "md",
  density: "comfortable"
}
```

**Corporate Dark**
```typescript
theme: {
  colorScheme: "dark",
  color: { accent: { primary: "#4D9FFF", level: 2 } },
  radius: "md",
  density: "comfortable"
}
```

**Minimal**
```typescript
theme: {
  colorScheme: "light",
  radius: "sm",
  density: "compact"
}
```

**Playful**
```typescript
theme: {
  colorScheme: "light",
  color: { accent: { primary: "#FF6B6B", level: 3 } },
  radius: "round",
  density: "comfortable"
}
```

### Start Screen Customization

```typescript
const options = {
  composer: {
    placeholder: "Ask anything about your data..."
  },
  startScreen: {
    greeting: "Welcome to FeedbackBot!",
    prompts: [
      {
        name: "Check ticket status",
        prompt: "Can you help me check on the status of a ticket?",
        icon: "search"
      },
      {
        name: "Create Ticket",
        prompt: "Can you help me create a new support ticket?",
        icon: "write"
      }
    ]
  }
};
```

### Header Customization

```typescript
const options = {
  header: {
    enabled: true,  // Set false to hide
    customButtonLeft: {
      icon: "settings-cog",
      onClick: () => openProfileSettings()
    },
    customButtonRight: {
      icon: "home",
      onClick: () => openHomePage()
    }
  }
};
```

### File Attachments

```typescript
const options = {
  composer: {
    attachments: {
      uploadStrategy: { type: 'hosted' },
      maxSize: 20 * 1024 * 1024,  // 20MB per file
      maxCount: 3,
      accept: {
        "application/pdf": [".pdf"],
        "image/*": [".png", ".jpg"]
      }
    }
  }
};
```

### Entity Tags (@mentions)

```typescript
const options = {
  entities: {
    async onTagSearch(query) {
      return [
        {
          id: "user_123",
          title: "Jane Doe",
          group: "People",
          interactive: true
        },
        {
          id: "document_123",
          title: "Quarterly Plan",
          group: "Documents",
          interactive: true
        }
      ];
    },
    onClick: (entity) => {
      navigateToEntity(entity.id);
    },
    onRequestPreview: async (entity) => ({
      preview: {
        type: "Card",
        children: [
          { type: "Text", value: `Profile: ${entity.title}` },
          { type: "Text", value: "Role: Developer" }
        ]
      }
    })
  }
};
```

### Composer Tools

```typescript
const options = {
  composer: {
    tools: [
      {
        id: 'add-note',
        label: 'Add Note',
        icon: 'write',
        pinned: true
      }
    ]
  }
};
```

### Toggle UI Features

```typescript
const options = {
  history: { enabled: false },  // Hide thread history
  header: { enabled: false },   // Hide header
  locale: 'de-DE'               // Override locale
};
```

---

## Widget Reference

Widgets are rich UI components rendered in the chat. Use the Widget Builder at https://widgets.chatkit.studio to design visually.

### Containers

#### Card
Bounded container for widgets with optional status and actions.

```python
from chatkit.widgets import Card, Text, Button, ActionConfig

Card(
    children=[
        Text(value="Hello World"),
        Button(label="Click me", onClickAction=ActionConfig(type="click"))
    ],
    size="md",           # "sm" | "md" | "lg" | "full"
    padding=16,          # number or {"top": 8, "bottom": 8, "x": 16}
    background="#f5f5f5",
    radius="md",
    status={"text": "Processing...", "icon": "spinner"},
    confirm={"label": "Confirm", "action": ActionConfig(type="confirm")},
    cancel={"label": "Cancel", "action": ActionConfig(type="cancel")},
    collapsed=False,
    theme="light"        # "light" | "dark"
)
```

#### ListView
Displays a vertical list of items.

```python
from chatkit.widgets import ListView, ListViewItem, Text, Icon

ListView(
    children=[
        ListViewItem(
            children=[Icon(name="document"), Text(value="Report.pdf")],
            onClickAction=ActionConfig(type="open_file", payload={"id": "123"})
        ),
        ListViewItem(
            children=[Icon(name="image"), Text(value="Photo.jpg")]
        )
    ],
    limit=5,            # Max items to show, or "auto"
    status={"text": "3 items"}
)
```

### Layout Components

#### Box
Flexible container for layout with direction, spacing, and styling.

```python
Box(
    children=[...],
    direction="row",      # "row" | "column"
    align="center",       # "start" | "center" | "end" | "baseline" | "stretch"
    justify="between",    # "start" | "center" | "end" | "stretch" | "between" | "around" | "evenly"
    gap=8,
    padding=16,
    margin=8,
    border={"size": 1, "color": "#ccc", "style": "solid"},
    radius="md",
    background="#ffffff",
    flex=1,
    width="100%",
    height=200
)
```

#### Row
Horizontal arrangement (shorthand for Box with direction="row").

```python
Row(
    children=[Text(value="Left"), Spacer(), Text(value="Right")],
    gap=8,
    align="center"
)
```

#### Col
Vertical arrangement (shorthand for Box with direction="column").

```python
Col(
    children=[Title(value="Header"), Text(value="Content")],
    gap=16
)
```

#### Spacer
Flexible empty space for layouts.

```python
Spacer(minSize=16)
```

#### Divider
Horizontal or vertical separator.

```python
Divider(
    spacing=16,
    color="#e0e0e0",
    size=1
)
```

### Text Components

#### Text
Plain text with optional streaming and editing.

```python
Text(
    value="Hello World",
    color="#333333",
    size="md",           # "xs" | "sm" | "md" | "lg" | "xl"
    weight="normal",     # "normal" | "medium" | "semibold" | "bold"
    textAlign="start",   # "start" | "center" | "end"
    truncate=True,
    maxLines=2,
    streaming=False,
    editable={
        "name": "field_name",
        "required": True,
        "placeholder": "Enter text...",
        "pattern": "^[a-z]+$"
    }
)
```

#### Title
Prominent heading text.

```python
Title(
    value="Welcome",
    size="2xl",          # "xs" to "5xl"
    weight="bold",
    color="#000000"
)
```

#### Caption
Smaller supporting text.

```python
Caption(
    value="Last updated 5 minutes ago",
    size="sm",
    color="secondary"
)
```

#### Markdown
Renders markdown-formatted text with streaming support.

```python
Markdown(
    value="# Heading\n\nParagraph with **bold** text.",
    streaming=True
)
```

### Interactive Components

#### Button
Flexible action button.

```python
Button(
    label="Submit",
    onClickAction=ActionConfig(type="submit", payload={"form": "contact"}),
    style="primary",      # "primary" | "secondary"
    color="primary",      # "primary" | "secondary" | "info" | "success" | "warning" | "danger"
    variant="solid",      # "solid" | "soft" | "outline" | "ghost"
    size="md",
    iconStart="check",
    iconEnd="arrow-right",
    pill=False,
    block=False,          # Full width
    submit=False          # Form submit button
)
```

#### Select
Dropdown single-select input.

```python
Select(
    name="priority",
    options=[
        {"label": "Low", "value": "low"},
        {"label": "Medium", "value": "medium"},
        {"label": "High", "value": "high"}
    ],
    placeholder="Select priority",
    defaultValue="medium",
    onChangeAction=ActionConfig(type="priority_changed"),
    variant="outline",
    clearable=True,
    disabled=False
)
```

#### DatePicker
Date input with dropdown calendar.

```python
DatePicker(
    name="due_date",
    placeholder="Select date",
    min=datetime(2024, 1, 1),
    max=datetime(2025, 12, 31),
    defaultValue=datetime.now(),
    onChangeAction=ActionConfig(type="date_changed"),
    side="bottom",
    clearable=True
)
```

#### Form
Layout container with validation and submit action.

```python
Form(
    onSubmitAction=ActionConfig(type="submit_form"),
    children=[
        Text(value="Name", editable={"name": "name", "required": True}),
        Text(value="Email", editable={"name": "email", "required": True}),
        Select(name="role", options=[...]),
        Button(label="Submit", submit=True)
    ],
    gap=16,
    padding=16
)
```

### Media Components

#### Image
Displays an image with optional styling.

```python
Image(
    src="https://example.com/image.jpg",
    alt="Description",
    width=200,
    height=150,
    fit="cover",          # "none" | "cover" | "contain" | "fill" | "scale-down"
    position="center",    # "center" | "top" | "bottom" | "left" | "right"
    radius="md",
    frame=True
)
```

#### Icon
Displays an icon by name.

```python
Icon(
    name="check",         # Icon name from ChatKit icon set
    color="#00AA00",
    size="md"             # "xs" | "sm" | "md" | "lg" | "xl"
)
```

#### Badge
Small label for status or metadata.

```python
Badge(
    label="New",
    color="success",      # "secondary" | "success" | "danger" | "warning" | "info" | "discovery"
    variant="solid",      # "solid" | "soft" | "outline"
    pill=True,
    size="sm"
)
```

### Transition
Wraps content that may animate.

```python
Transition(
    children=Text(value="Animated content")
)
```

---

## Actions Reference

Actions trigger backend logic from UI interactions.

### Server-Side Action Handler (Python)

```python
from chatkit import ChatKitServer, Action, Event
from chatkit.widgets import Card, Text
from typing import AsyncIterator, Any

class MyChatKitServer(ChatKitServer):
    async def action(
        self,
        thread: ThreadMetadata,
        action: Action[str, Any],
        sender: WidgetItem | None,
        context: Any,
    ) -> AsyncIterator[Event]:
        if action.type == "submit_form":
            name = action.payload.get("name")
            email = action.payload.get("email")

            # Process the form...
            await save_contact(name, email)

            # Add hidden context for the model
            await self.store.add_thread_item(
                thread.id,
                HiddenContextItem(
                    id="item_123",
                    created_at=datetime.now(),
                    content=f"<USER_ACTION>User submitted contact form with name={name}</USER_ACTION>"
                ),
                context
            )

            # Stream a response
            async for e in self.generate(context, thread):
                yield e

        elif action.type == "delete_item":
            item_id = action.payload.get("id")
            await delete_item(item_id)

            # Update the widget
            yield WidgetUpdateEvent(
                item_id=sender.id,
                widget=Card(children=[Text(value="Item deleted")])
            )
```

### Client-Side Action Handler (JavaScript)

```typescript
// In widget definition, specify handler="client"
Button(
    label="Open Modal",
    onClickAction=ActionConfig(
        type="open_modal",
        payload={"id": 123},
        handler="client"  // Handle on client side
    )
)

// In ChatKit options
chatkit.setOptions({
  widgets: {
    async onAction(action, item) {
      if (action.type === "open_modal") {
        openModal(action.payload.id);

        // Optionally send follow-up action to server
        await chatkit.sendAction({
          type: "modal_opened",
          payload: { id: action.payload.id }
        });
      }
    }
  }
});
```

### Form Value Collection

When widgets with inputs are inside a `Form`, values are automatically included in action payloads:

```python
Form(
    onSubmitAction=ActionConfig(type="update_todo", payload={"id": todo.id}),
    children=[
        Text(value=todo.title, editable={"name": "title", "required": True}),
        Text(value=todo.description, editable={"name": "description"}),
        Select(name="priority", options=[...]),
        Button(label="Save", submit=True)
    ]
)

# In action handler:
async def action(self, thread, action, sender, context):
    if action.type == "update_todo":
        todo_id = action.payload["id"]
        title = action.payload["title"]       # From editable Text
        description = action.payload["description"]
        priority = action.payload["priority"]  # From Select
```

### Loading Behaviors

Control how actions show loading states:

```python
Button(
    label="Submit",
    onClickAction=ActionConfig(
        type="submit",
        loadingBehavior="container"  # "auto" | "self" | "container" | "none"
    )
)
```

| Value | Behavior |
|-------|----------|
| `auto` | Adapts based on widget type (default) |
| `self` | Loading state on the triggering widget only |
| `container` | Loading state on entire widget container |
| `none` | No loading state |

### Strongly-Typed Actions (Python)

```python
from pydantic import BaseModel
from typing import Literal, Annotated
from pydantic import Field, TypeAdapter

class SubmitFormPayload(BaseModel):
    name: str
    email: str

SubmitFormAction = Action[Literal["submit_form"], SubmitFormPayload]
DeleteItemAction = Action[Literal["delete_item"], dict]

AppAction = Annotated[
    SubmitFormAction | DeleteItemAction,
    Field(discriminator="type")
]

ActionAdapter = TypeAdapter(AppAction)

def parse_action(action: Action[str, Any]) -> AppAction:
    return ActionAdapter.validate_python(action)
```

---

## Self-Hosted Server Guide

For full control, run ChatKit on your own infrastructure.

### Installation

```bash
pip install openai-chatkit
```

### Basic Server Implementation

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, Response
from chatkit import ChatKitServer, Event, StreamingResult
from chatkit.store import SQLiteStore
from chatkit.files import DiskFileStore
from agents import Agent, Runner

app = FastAPI()

# Data persistence
data_store = SQLiteStore("chatkit.db")
file_store = DiskFileStore(data_store, "./uploads")

class MyChatKitServer(ChatKitServer):
    def __init__(self):
        super().__init__(data_store, file_store)

    # Define your agent
    assistant = Agent(
        model="gpt-4.1",
        name="Assistant",
        instructions="You are a helpful assistant."
    )

    async def respond(self, thread, input, context):
        """Handle user messages and tool outputs."""
        result = Runner.run_streamed(
            self.assistant,
            await to_input_item(input, self.to_message_content),
            context=context
        )
        async for event in stream_agent_response(context, result):
            yield event

    async def action(self, thread, action, sender, context):
        """Handle widget actions."""
        if action.type == "example":
            # Process action...
            pass

server = MyChatKitServer()

@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    result = await server.process(await request.body(), {})
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    return Response(content=result.json, media_type="application/json")
```

### Client Tools from Server

Trigger client-side tools from your agent:

```python
from chatkit import ClientToolCall
from agents import function_tool

@function_tool(description="Add an item to the user's todo list")
async def add_to_todo_list(ctx, item: str) -> None:
    ctx.context.client_tool_call = ClientToolCall(
        name="add_to_todo_list",
        arguments={"item": item}
    )

assistant = Agent(
    model="gpt-4.1",
    tools=[add_to_todo_list],
    tool_use_behavior=StopAtTools(stop_at_tool_names=["add_to_todo_list"])
)
```

Register on the client:

```typescript
chatkit.setOptions({
  clientTools: {
    add_to_todo_list: async ({ item }) => {
      await addTodoItem(item);
      return { success: true };
    }
  }
});
```

### Thread Metadata

Store server-side state in thread metadata:

```python
async def respond(self, thread, input, context):
    # Read metadata
    previous_run_id = thread.metadata.get("last_run_id")

    # Update metadata
    await self.store.update_thread_metadata(
        thread.id,
        {"last_run_id": new_run_id},
        context
    )
```

### Progress Updates

Stream progress for long-running operations:

```python
async def action(self, thread, action, sender, context):
    yield ProgressUpdateEvent(
        message="Processing step 1 of 3...",
        progress=0.33
    )
    await process_step_1()

    yield ProgressUpdateEvent(
        message="Processing step 2 of 3...",
        progress=0.66
    )
    await process_step_2()

    # Final response replaces progress
    yield AssistantMessageEvent(content="Done!")
```

---

## Widget Streaming

Stream widget updates for dynamic content:

```python
from chatkit import stream_widget

async def respond(self, thread, input, context):
    widget = Card(
        children=[
            Text(id="status", value="Loading...", streaming=True)
        ]
    )

    async for event in stream_widget(
        thread,
        widget,
        generate_id=lambda t: self.store.generate_item_id(t, thread, context)
    ):
        yield event

    # Update the text as content streams
    for chunk in generate_response():
        yield WidgetNodeUpdateEvent(
            node_id="status",
            value=chunk
        )
```

---

## Common Patterns

### Confirmation Dialog

```python
Card(
    children=[
        Title(value="Delete Item?"),
        Text(value="This action cannot be undone."),
    ],
    confirm={"label": "Delete", "action": ActionConfig(type="confirm_delete")},
    cancel={"label": "Cancel", "action": ActionConfig(type="cancel")}
)
```

### Data Table

```python
Card(
    children=[
        Row(children=[
            Text(value="Name", weight="bold", flex=2),
            Text(value="Status", weight="bold", flex=1),
            Text(value="Actions", weight="bold", flex=1)
        ]),
        Divider(),
        *[
            Row(children=[
                Text(value=item.name, flex=2),
                Badge(label=item.status, color="success" if item.active else "secondary", flex=1),
                Button(label="Edit", size="sm", onClickAction=ActionConfig(type="edit", payload={"id": item.id}))
            ])
            for item in items
        ]
    ]
)
```

### Profile Card

```python
Card(
    children=[
        Row(children=[
            Image(src=user.avatar, size=64, radius="full"),
            Col(children=[
                Title(value=user.name, size="lg"),
                Caption(value=user.role),
                Badge(label="Active", color="success")
            ], gap=4)
        ], gap=16, align="center")
    ],
    padding=24
)
```

### Multi-Step Form

```python
Card(
    children=[
        Title(value="Step 1: Basic Info"),
        Form(
            onSubmitAction=ActionConfig(type="next_step", payload={"step": 1}),
            children=[
                Col(children=[
                    Caption(value="Name"),
                    Text(value="", editable={"name": "name", "required": True, "placeholder": "Enter name"})
                ], gap=4),
                Col(children=[
                    Caption(value="Email"),
                    Text(value="", editable={"name": "email", "required": True, "placeholder": "Enter email"})
                ], gap=4),
                Row(children=[
                    Spacer(),
                    Button(label="Next", submit=True, iconEnd="arrow-right")
                ])
            ],
            gap=16
        )
    ]
)
```