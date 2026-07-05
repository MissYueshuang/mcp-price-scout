# priceScout — Claude Context

## Project purpose
priceScout is an MCP-powered tool that scrapes competitor AI pricing pages,
stores results in SQLite, and answers comparison queries via a multi-agent workflow.

## Architecture
- `server.py`   — MCP server exposing `scrape_websites` and `extract_scraped_info` tools
- `client.py`   — AI-powered MCP client (ChatSession, DataExtractor)
- `main.py`     — entry point; wires client → server and starts the chat loop
- `server_config.json` — lists all MCP servers the client connects to

## Key conventions
- All pricing data goes into `test.db` (SQLite); never use raw files as the source of truth
- Scraped files land in `scraped_content/` as `{provider}_{format}.txt`
- Metadata is tracked in `scraped_metadata.json` next to `scraped_content/`
- Use Pydantic models for all API request/response shapes (see `.claude/rules/api.md`)

## Running the project
```bash
uv run python client.py          # start interactive chat
uv run python -m pytest        # run tests
```

## What NOT to do
- Never hardcode API keys; always read from `.env`
- Never `DROP TABLE` or `DELETE FROM` without a WHERE clause
- Never commit `test.db` or `scraped_content/` (they are gitignored)
