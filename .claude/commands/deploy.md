# Deploy to Staging

Argument: $ARGUMENTS (optional: "prod" to deploy to production instead)

Run the following steps in order. Stop and report on any failure.

1. Confirm there are no uncommitted changes: `git status`
2. Run the test suite: `uv run python -m pytest -q`
3. Lint: `uv run ruff check .`
4. If $ARGUMENTS is "prod", ask the user to confirm before continuing.
5. Run the deploy script: `./scripts/deploy-staging.sh`
6. Verify the health endpoint responds 200: `curl -sf http://localhost:8000/health`
7. Report: tests passed, linted clean, deploy successful (or which step failed).
