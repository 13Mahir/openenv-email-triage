---
title: OpenEnv Email Triage
emoji: 📧
colorFrom: blue
colorTo: purple
sdk: docker
app_file: inference.py
pinned: false
---

# 📧 OpenEnv Email Triage Benchmark

## Overview
This project implements a high-difficulty OpenEnv benchmark for evaluating autonomous agents on real-world email triage tasks.

Agents must intelligently:
- classify email priority
- filter spam
- generate high-quality replies
- decide optimal action ordering

---

## 🚀 Why This Benchmark is Challenging

Unlike trivial environments, this benchmark requires:

- Semantic reasoning (no hardcoded IDs)
- Context understanding (sender + subject + content)
- Strategic prioritization (order matters)
- Language quality evaluation (reply tone affects score)
- Trade-off decision making (over-action penalties)

Weak agents fail. Strong agents plan.

---

## 🧠 Core Features

- Partial observability (truncated emails)
- Randomized inputs with fixed seed
- Multi-objective reward system
- Hidden scoring signals (priority & behavior)
- Non-trivial scoring distribution (no guaranteed 1.0)

---

## ⚙️ Action Space

- assign_label(email_id, label)
- archive(email_id)
- reply(email_id, reply_text)
- finish()

---

## 👁️ Observation Space

Each step returns:

- inbox → list of emails (truncated content)
- assigned_labels
- archived_emails
- replied_emails

---

## 🎯 Reward Design

Multi-factor reward shaping:

- Step penalty: -0.01
- Correct action: +0.1
- Early action bonus: +0.2
- Incorrect actions: -0.2 to -0.3
- Reply quality bonus: up to +0.3
- Over-processing penalty: up to -0.2
- Hidden prioritization bonus: +0.1

Final score is normalized in [0, 1].

---

## 🧪 Evaluation

The environment exposes:

POST /reset

Returns:

{
  "status": "ok",
  "score": 0.86,
  "steps": 6
}

---

## 🐳 Run Locally

docker build -t openenv-email .
docker run --rm openenv-email

---

## 📊 Benchmark Goal

This benchmark is designed to:

- Differentiate weak vs strong agents
- Reward reasoning over memorization
- Simulate realistic decision-making complexity

---

## 🏆 OpenEnv Compliance

- reset(), step(), state() implemented
- Multiple tasks (easy, medium, hard)
- Graders return normalized scores [0,1]
- Fully compatible with OpenEnv evaluation pipeline

---

## 🔐 Configuration

Required environment variables:

- HF_TOKEN
- API_BASE_URL
- MODEL_NAME

No secrets are stored in code.

---

## 🧠 Summary

This is not just an environment.

It is a reasoning benchmark for autonomous agents.
