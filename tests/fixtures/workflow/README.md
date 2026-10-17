# TEST_ONLY workflow benchmark

corpus.json defines invented English documents and wiki/decision metadata. queries.json independently defines 30 paired questions and expected retrieval/citation/scope/lifecycle/abstention results. Its relevance gold intentionally retains unlisted paraphrases as recall misses.

Do not copy these sources into the live sources/raw registry. tests/workflow_support.py builds disposable, hash-backed workspaces through actual admission and synthesis APIs. Simulated human decision approvals are test assertions, never production authorization.

Run python -B scripts/validate_workflows.py from the repository root. Read [measurement definitions and limits](../../../WORKFLOW_RELIABILITY.md). Gold is portable to future adapters; changing the retriever must not regenerate its own expected results.
