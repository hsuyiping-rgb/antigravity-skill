# Subagent Batching

Use only when the user explicitly requests parallel generation and subagents are available.

1. Generate and approve one representative golden sample sequentially.
2. Save it in the project and write its path to `design_system.style_reference`.
3. Split non-overlapping page ranges across workers.
4. Give every worker the same `spec.yaml`, golden sample, prompt contract, output directory, and typography policy.
5. Require one image call per slide, local persistence, visual inspection, and a separate prompt log.
6. Do not let workers modify the same files.
7. The primary agent must inspect the final montage and regenerate drifted pages.

Parallel workers reduce waiting time; they do not increase image quota or guarantee style consistency.

