---
name: access-review
version: "1.0"
description: Review IAM roles and permissions for least-privilege compliance.
tags: [security, iam, compliance]
allowed-tools: [Bash, Read]
---
## Overview
Reviews IAM roles and policies for overly permissive access.

## Usage
1. For AWS: run `aws iam list-roles` and `aws iam get-role-policy`.
2. Identify roles with wildcard actions (*) or overly broad resource scope.
3. Report violations with the principle of least privilege.

## Notes
Read-only. Does not modify IAM policies or roles.
