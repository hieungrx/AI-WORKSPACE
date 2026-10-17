# Prompt: BUILD & VERIFY

Read project context plus canonical code repository instructions. Feature: `[FEATURE]`.

1. Do read-only discovery first. Identify requirements, risks, acceptance criteria, baseline, test commands.
2. Propose a scoped plan and get human approval for schema, security, new dependencies or architecture decisions.
3. Work on a separate branch. Implement small reversible changes.
4. Run actual lint/typecheck/tests/build; benchmark only on comparable conditions.
5. Report actual command outputs, changed files, remaining failures, risks and KEEP/REVERT/HUMAN_REVIEW.
6. Update approved decision records and knowledge references only after acceptance. Do not auto-merge, auto-deploy or modify production.
