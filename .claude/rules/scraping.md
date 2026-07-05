---
path: server.py
---

# Scraping conventions
- Always set a User-Agent header; never send bare requests
- Cap scrape concurrency at 5; use asyncio.Semaphore
- On HTTP error, log provider + status code; do NOT raise — return partial results
- scraped_metadata.json must be updated atomically (write to .tmp, then rename)
