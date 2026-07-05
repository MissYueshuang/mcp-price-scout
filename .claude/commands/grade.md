# Code quality check
You must run your completed application and proof it's working

1. Run Your Client: In your terminal, run your client: `python starter_client.py`
2. Execute the 3 Test Prompts: 
    - Test 1 Query: `scrape these sites: {'cloudrift': 'https.www.cloudrift.ai/inference', 'deepinfra': 'https://deepinfra.com/pricing', 'fireworks': 'https://fireworks.ai/pricing#serverless-pricing', 'groq': 'https://groq.com/pricing'}`
    - Test 1 guardrils: it must return "Successfully scraped 4 out of 4 websites" (or similar) output.

    - Test 2 Query: `Query: Compare cloudrift ai and deepinfra's costs for deepseek v3`
    - Test 2 guardrils: show the query and the bot's full, natural-language answer.

    - Test 3 Query: `show data`
    - Test 3 guardrils: it must print formatted table of pricing plans.