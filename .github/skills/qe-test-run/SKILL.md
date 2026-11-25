---
name: qe-test-run
description: Execute the approved test set for the current slice/phase and report evidence against acceptance criteria.
---

# QE Test Run

Run only the approved test set for the current slice/phase. First inspect package scripts, environment and test configuration. Do not install packages or alter CI settings without approval. Execute tests in an appropriate order, capture exact commands, exit codes, counts, durations and artifacts. Distinguish passed, failed, skipped, not-run and blocked. On failure, preserve logs and create defect candidates; do not weaken tests. Summarize evidence against AC IDs.