# CI Check (non-interactive)

This command is designed to run headlessly in CI pipelines.
Usage: claude --print "/ci" (no TTY required)

Steps — exit non-zero if any fail:
1. `uv run python -m pytest --tb=short -q`
2. `uv run ruff check .`
3. `uv run mypy server.py client.py`
4. Print a one-paragraph summary of what passed and what (if anything) failed.
   Format: "CI PASS" or "CI FAIL: <reason>" as the very first line so scripts can grep it.
