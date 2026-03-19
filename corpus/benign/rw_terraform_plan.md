---
name: terraform-plan
version: "1.0"
description: Run terraform plan and summarize proposed infrastructure changes.
tags: [terraform, infrastructure, devops]
allowed-tools: [Bash, Read]
---
## Overview
Runs `terraform plan` and produces a human-readable summary of changes.

## Usage
1. Run `terraform init -input=false` if .terraform/ does not exist.
2. Run `terraform plan -out=tfplan.binary -input=false`.
3. Run `terraform show -json tfplan.binary` to get structured output.
4. Summarize: resources to add, change, and destroy.

## Notes
Does not run `terraform apply`. Only plans and reports.
