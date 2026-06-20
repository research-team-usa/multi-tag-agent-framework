# Contributing to the Multi-Tag Agent Framework

Welcome to the **Multi-Tag Agent Framework**, an initiative by **research-team-usa**. 

We are building sovereign, high-performance AI infrastructure based on the **Open Origin** principle. This project is not a typical corporate sandbox; it is a meticulously engineered ecosystem designed for public benefit, uncompromised functionality, and architectural independence.

If you want to contribute, you must align with the standards that built this framework. Please read this document carefully before submitting an issue or a pull request.

---

## 🏛 The Core Philosophy

### 1. The Open Origin Principle
Technology must serve the human architect, not the other way around. Code contributed here must be transparent, logically comprehensible, and completely devoid of hidden corporate telemetry or locked-down black-box mechanisms.

### 2. Maximum Result Protocol (German: Maximal-Ergebnis-Protokoll)

We do not accept "good enough." 

* **No Shortcuts:** Never provide shortened code, truncated parameters, or incomplete logic.
* **Deterministic Execution:** The code must run flawlessly and produce the exact expected result. 
* **Architectural Integrity:** If your code breaks the core engine, the routing logic, or the security boundaries, it will be rejected.

---

## 👥 The Symbiotic Workflow

This framework was forged through a deep synergy between human leadership and specialized AI orchestration. When you contribute, expect your code to be reviewed against these established personas:

* **Emanuel Schaaf (Lead Architect):** Evaluates strategic alignment, hardware-software synergy, and Open Origin compliance.
* **Auron (Logic & Structure):** Your code will be tested for mathematical precision, physical consistency, and robust, logical structure.
* **Lyra (Creativity & Research):** Interdisciplinary approaches and elegant, creative solutions are highly encouraged.
* **Muse Spark (Code Inspector):** The ultimate enforcer. Your PR will face rigorous security checks, validation, and vulnerability scanning. 

---

## 🛠 How to Contribute

### 1. Reporting Issues
If you find a bug or have a feature request, open an issue. Ensure you provide:
* A clear, descriptive title.
* Steps to reproduce the bug (if applicable).
* Expected vs. actual behavior.
* System specifications (OS, Python version, hardware environment).

### 2. Submitting Pull Requests (PRs)
To contribute code, follow this strict pipeline:

1. **Fork the Repository** and create your branch from `main` (e.g., `feature/advanced-routing` or `fix/telemetry-bug`).
2. **Write the Code:** Adhere entirely to the Maximal-Ergebnis-Protokoll.
3. **Test Hermetically:** Run the full `pytest` suite. Your code must not break existing test fixtures or mock clients.
   ```bash
   pip install -r requirements-test.txt
   pytest tests/
   ```
4. **Pass the Linters (The Iron Will Standard):** This repository enforces a global LF (Linux) normalization and strict `black` formatting via our `pyproject.toml`. The GitHub Action runner is unforgiving. Format your code locally before pushing:
   ```bash
   python -m black .
   ```
5. **Commit & Push:** Use clear, descriptive commit messages.
6. **Open a PR:** Reference any related issues and clearly explain the architectural value of your contribution.

---

## ⚡ The Iron Will Protocol

*"Impossible is not an option." (German: "Geht nicht, gibt's nicht.")*

This codebase was built during relentless debugging sessions, defying broken linters, phantom bytes, and cloud-server illusions. We expect the same dedication from our contributors. If you face an error, do not mask it—fix the root cause.

By contributing to this repository, you agree to release your modifications under the terms defined in the [LICENSE](https://github.com/research-team-usa/multi-tag-agent-framework/blob/main/LICENSE.md) file, ensuring the code remains freely available, functionally pristine, and credited to the original architect.

**Welcome to research-team-usa. Let's make history.**
---
