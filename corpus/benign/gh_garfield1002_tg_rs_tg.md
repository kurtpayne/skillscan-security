---
name: tg
description: Use tg to send Telegram messages, attach files, and listen for replies from the command line. Trigger when the user wants to send notifications, share files, or receive messages via Telegram.
user-invocable: true
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Garfield1002/tg-rs
# corpus-url: https://github.com/Garfield1002/tg-rs/blob/f00618792bdbdeb88105945bdb565b58be17143c/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# tg - Telegram CLI

`tg` sends messages and files to a pre-configured Telegram chat.

## Setup

Ask the user to run `tg setup` once to configure the bot token and chat ID.
You cannot do the setup alone.

## Sending messages

```sh
# Positional arguments
tg "Hello, World!"
tg hello world

# From stdin
echo "build done" | tg
cat log.txt | tg

# Escape sequences
tg -e "line one\nline two"

# Parse modes
tg -m markdown "*bold* _italic_"
tg -m html "<b>bold</b>"

# Silent (no notification)
tg -s "low priority alert"
```

## Attaching files

```sh
# Single file
tg attach report.pdf

# Multiple files / glob
tg attach *.log
tg attach foo.txt bar.c

# Silent
tg attach -s backup.tar.gz
```

## Interactive mode

Stream stdin updates by editing a single message:

```sh
some-command | tg -i
some-command | tg -i -f 2   # update every 2s
```

## Listening for replies

```sh
tg listen          # prints incoming messages, stops on /eof
tg listen > out.txt
```

## Config management

```sh
tg config show     # print config path and contents
tg config reset    # delete config for re-setup
```

## Library usage

```rust
use tg_cli::telegram;

#[tokio::main]
async fn main() {
    telegram!("build {} complete", 42);
}
```

## Key flags

| Flag      | Description                         |
| --------- | ----------------------------------- |
| `-e`      | Interpret escape sequences          |
| `-n`      | Strip trailing newline              |
| `-m MODE` | Parse mode: `markdown` or `html`    |
| `-i`      | Interactive mode (edit one message) |
| `-f SECS` | Interactive update frequency        |
| `-s`      | Silent (no notification)            |
| `-q`      | Quiet (suppress non-error output)   |