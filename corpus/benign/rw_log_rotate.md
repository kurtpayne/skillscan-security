---
name: configure-log-rotation
version: "1.0"
description: Generate a logrotate configuration for application logs.
tags: [sysadmin, logging, configuration]
allowed-tools: [Read, Write]
---
## Overview
Generates a logrotate configuration file for application log files.

## Usage
Provide: log file paths, rotation frequency (daily/weekly/monthly),
retention count, and compression preference.
The skill will generate a logrotate.d configuration file.

## Notes
Only writes the logrotate configuration file. Does not apply it.
