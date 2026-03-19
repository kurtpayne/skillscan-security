---
name: docker-build
version: "1.0"
description: Build a Docker image from the current directory and tag it.
tags: [docker, containers, devops]
allowed-tools: [Bash, Read]
---
## Overview
Builds a Docker image from the Dockerfile in the current directory.

## Usage
1. Read the Dockerfile to understand the build context.
2. Run `docker build -t <image-name>:<tag> .`.
3. Report the image ID and size.

## Notes
Does not push the image to any registry without explicit user confirmation.
Does not run containers with elevated privileges.
