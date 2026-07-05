# Review Pull Request

Argument: $ARGUMENTS — the PR number or branch name to review.

Steps:
1. Fetch the diff: `git diff main...$ARGUMENTS`
2. Check for new or changed files in `src/api/` — apply `.claude/rules/api.md` conventions
3. Run the code-review skill rubric from `.claude/skills/CODE-REVIEW.md`
4. Report findings grouped by: bugs, convention violations, missing tests
