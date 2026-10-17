# Experiments program (inspired by AutoResearch)

## Mission
Improve one measurable aspect of a task in a reproducible test environment.

## Permissions
- Only edit files approved in the task packet, in a throwaway branch/sandbox.
- Do not edit the metric implementation, protected test data, production secrets, or deployment configuration to game results.
- User approval is required to merge/deploy.

## Procedure
1. State hypothesis and metric (including lower/higher is better).
2. Record reproducible baseline, hardware, dataset and command.
3. Make one focused change and run fixed tests/benchmark.
4. Append real measurements and environment to `results.csv`.
5. Revert regression; propose KEEP only if functional guardrails pass and the metric improves reliably.
6. Stop at 3 failures or any safety, cost or resource boundary violation.

Never fabricate experiments. If a metric is not measured, record `NOT_RUN`.
