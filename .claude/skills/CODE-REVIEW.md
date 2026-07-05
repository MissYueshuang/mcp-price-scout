---
name: code review rubric
description: use the rubric to check the quality of code for submission
---

Use this project rubric to understand and assess the project criteria.

# Custom MCP Server
Criteria	Submission Requirements
Implement scrape_websites tool to scrape, persist, and track metadata
Running the tool creates scraped_content/ with one file per {provider}_{format}.txt for each successful provider and creates/updates scraped_metadata.json containing provider name, url, domain, scraped_at, content_files, title, description. Tool returns a list whose length equals number of successful scrapes.
Implement extract_scraped_info tool to load metadata and return file contents
Calling the tool with an identifier that matches provider name, URL, or domain returns a formatted JSON string whose content field includes loaded text for each available format; non-matching identifier returns a plain-text message indicating no saved information.

# AI-Powered MCP Client
Criteria	Submission Requirements
List available MCP tools
Server.list_tools checks session existence, calls list_tools(), and returns a list of dicts containing name, description, input_schema.
Execute tools with retries
Server.execute_tool contains a retry loop and within each attempt logs execution, calls session.call_tool(...) with a 60-second read timeout, and returns the result on success.
Persist structured pricing to SQLite via MCP
DataExtractor.extract_and_store_data iterates pricing_data["plans"] and executes the provided write_query insertion exactly as specified (including column order and json.dumps for features).
Drive tool use via LLM and complete tool-use loop
ChatSession.process_query sets a real model name (e.g., claude-3-5-sonnet-20240620), appends text chunks to full_response, appends assistant content, handles single-text completion exit, and for tool_use performs the full 1–7 loop (append tool request, locate server, execute tool, append tool result, call model again, and exit if next response is text only).
Display recently stored data from DB
| data from DB |

| ChatSession.show_stored_data executes the provided read_query, prints the header lines, iterates result rows, and prints the formatted bullet lines including company, plan, and token pricing, then a closing separator. |

# Orchestrate an Agentic Workflow
Criteria	Submission Requirements
Orchestrate a functional multi-agent MCP workflow
The running client connects to three MCP servers (custom scraper, SQLite, filesystem where applicable) and, from natural-language queries, delegates to the correct tools to scrape, analyze, and store competitor pricing, then answer follow-ups using stored data.
Demonstrate comparison Q&A
Screenshot showing the comparison query Compare cloudrift ai and deepinfra's costs for deepseek v3 and a full natural-language answer.
Demonstrate scraping success
**Screenshot **showing the scrape these sites: {...} query and output confirming success count (e.g., “Successfully scraped 4 out of 4 websites” or equivalent success log).