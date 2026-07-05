# Review Pull Request

Argument: $ARGUMENTS — the PR number or branch name to review.

Steps:
1. Fetch the diff: `git diff main...$ARGUMENTS`
2. Run the code-review skill rubric from `.claude/skills/CODE-REVIEW.md`
3. Report findings grouped by: bugs, convention violations, missing tests
