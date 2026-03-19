---
name: kubernetes-status
version: "1.0"
description: Check the status of Kubernetes pods, deployments, and services.
tags: [kubernetes, devops, monitoring]
allowed-tools: [Bash]
---
## Overview
Reports the current status of Kubernetes resources in the specified namespace.

## Usage
1. Run `kubectl get pods -n <namespace>` to list pod statuses.
2. Run `kubectl get deployments -n <namespace>` for deployment status.
3. Run `kubectl get services -n <namespace>` for service endpoints.
4. Flag any pods in CrashLoopBackOff, Error, or Pending state.

## Notes
Read-only. Does not modify, restart, or delete any resources.
