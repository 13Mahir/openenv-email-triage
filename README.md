---
title: OpenEnv Email Triage
emoji: 📧
colorFrom: blue
colorTo: purple
sdk: docker
app_file: inference.py
pinned: false
---

# Email Triage System Benchmark

## Problem Description
This is a high-difficulty, realistic OpenEnv benchmark simulating an email inbox triage process. Autonomous agents must classify, respond, and manage emails intelligently.

## Realism
- Partial observability
- Randomized email content
- Semantic reasoning required
- Non-trivial reward shaping

## Action Space
- assign_label(email_id, label)
- archive(email_id)
- reply(email_id, reply_text)
- finish()

## Observation Space
- inbox (truncated email content)
- assigned_labels
- archived_emails
- replied_emails

## Reward Design
- Step penalty: -0.01
- Correct action: +0.1
- Early bonus: +0.2
- Wrong actions: -0.2 to -0.3
- Reply quality bonus: +0.1 to +0.3
- Perfect finish bonus: +0.5

## Run
```bash
docker build -t openenv-email .
docker run --rm openenv-email
```
