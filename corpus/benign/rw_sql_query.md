---
name: run-sql-query
version: "1.0"
description: Execute a read-only SQL query against a local SQLite database.
tags: [sql, sqlite, data]
allowed-tools: [Read, Bash]
---
## Overview
Executes a SELECT query against a local SQLite database and returns
the results as a Markdown table.

## Usage
1. Validate the query is a SELECT statement (no INSERT/UPDATE/DELETE/DROP).
2. Run the query using `sqlite3 <database> "<query>"`.
3. Format the results as a Markdown table.

## Notes
Read-only queries only. Refuses to execute DDL or DML statements.
