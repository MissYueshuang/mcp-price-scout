
import os
import json
import logging
from typing import List, Dict, Optional
from firecrawl import FirecrawlApp
from urllib.parse import urlparse
from datetime import datetime
from mcp.server.fastmcp import FastMCP

from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

SCRAPE_DIR = "scraped_content"

mcp = FastMCP("llm_inference")

@mcp.tool()
def scrape_websites(
    websites: Dict[str, str],
    formats: List[str] = ['markdown', 'html'],
    api_key: Optional[str] = None
) -> List[str]:
    """
    Scrape multiple websites using Firecrawl and store their content.
    
    Args:
        websites: Dictionary of provider_name -> URL mappings
        formats: List of formats to scrape ['markdown', 'html'] (default: both)
        api_key: Firecrawl API key (if None, expects environment variable)
        
    Returns:
        List of provider names for successfully scraped websites
    """
    
    if api_key is None:
        api_key = os.getenv('FIRECRAWL_API_KEY')
        if not api_key:
            raise ValueError("API key must be provided or set as FIRECRAWL_API_KEY environment variable")
    
    app = FirecrawlApp(api_key=api_key)
    
    path = os.path.join(SCRAPE_DIR)
    os.makedirs(path, exist_ok=True)
    
    # save the scraped content to files and then create scraped_metadata.json as a summary file
    # check if the provider has already been scraped and decide if you want to overwrite
    # {
    #     "cloudrift_ai": {
    #         "provider_name": "cloudrift_ai",
    #         "url": "https://www.cloudrift.ai/inference",
    #         "domain": "www.cloudrift.ai",
    #         "scraped_at": "2025-10-23T00:44:59.902569",
    #         "formats": [
    #             "markdown",
    #             "html"
    #         ],
    #         "success": "true",
    #         "content_files": {
    #             "markdown": "cloudrift_ai_markdown.txt",
    #             "html": "cloudrift_ai_html.txt"
    #         },
    #         "title": "AI Inference",
    #         "description": "Scraped content goes here"
    #     }
    # }
    metadata_file = os.path.join(path, "scraped_metadata.json")

    # Load existing metadata
    if os.path.exists(metadata_file):
        with open(metadata_file, "r") as f:
            metadata = json.load(f)
    else:
        metadata = {}

    successfully_scraped = []

    for provider_name, url in websites.items():
        if provider_name in metadata:
            logger.info(f"Skipping {provider_name} — already scraped at {metadata[provider_name]['scraped_at']}")
            successfully_scraped.append(provider_name)
            continue

        logger.info(f"Scraping {provider_name}: {url}")
        try:
            result = app.scrape_url(url, formats=formats)
            domain = urlparse(url).netloc
            content_files = {}

            for fmt in formats:
                content = getattr(result, fmt, None)
                if content:
                    filename = f"{provider_name}_{fmt}.txt"
                    filepath = os.path.join(path, filename)
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                    content_files[fmt] = filename

            page_metadata = getattr(result, "metadata", {}) or {}
            title = page_metadata.get("title", "") if isinstance(page_metadata, dict) else getattr(page_metadata, "title", "")
            description = page_metadata.get("description", "") if isinstance(page_metadata, dict) else getattr(page_metadata, "description", "")

            metadata[provider_name] = {
                "provider_name": provider_name,
                "url": url,
                "domain": domain,
                "scraped_at": datetime.now().isoformat(),
                "formats": formats,
                "success": "true",
                "content_files": content_files,
                "title": title,
                "description": description,
            }
            successfully_scraped.append(provider_name)
            logger.info(f"Successfully scraped {provider_name}")

        except Exception as e:
            logger.error(f"Failed to scrape {provider_name} ({url}): {e}")
            metadata[provider_name] = {
                "provider_name": provider_name,
                "url": url,
                "domain": urlparse(url).netloc,
                "scraped_at": datetime.now().isoformat(),
                "formats": formats,
                "success": "false",
                "content_files": {},
                "title": "",
                "description": str(e),
            }

    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)

    return successfully_scraped

@mcp.tool()
def extract_scraped_info(identifier: str) -> str:
    """
    Extract information about a scraped website.
    
    Args:
        identifier: The provider name, full URL, or domain to look for
        
    Returns:
        Formatted JSON string with the scraped information
    """
    
    logger.info(f"Extracting information for identifier: {identifier}")
    if os.path.exists(SCRAPE_DIR):
        logger.info(f"Files in {SCRAPE_DIR}: {os.listdir(SCRAPE_DIR)}")

    metadata_file = os.path.join(SCRAPE_DIR, "scraped_metadata.json")
    logger.info(f"Checking metadata file: {metadata_file}")

    if not os.path.exists(metadata_file):
        return "No information in the database."

    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    # Match by provider name, full URL, or domain
    identifier_lower = identifier.lower()
    for provider_name, entry in metadata.items():
        if (
            identifier_lower == provider_name.lower()
            or identifier_lower == entry.get("url", "").lower()
            or identifier_lower == entry.get("domain", "").lower()
        ):
            # Attach content inline for each format
            result = dict(entry)
            result["content"] = {}
            for fmt, filename in entry.get("content_files", {}).items():
                filepath = os.path.join(SCRAPE_DIR, filename)
                if os.path.exists(filepath):
                    with open(filepath, "r", encoding="utf-8") as f:
                        result["content"][fmt] = f.read()
            logger.info(f"Found match for '{identifier}': {provider_name}")
            return json.dumps(result, indent=4)

    return f"No scraped information found for identifier: '{identifier}'"

if __name__ == "__main__":
    mcp.run(transport="stdio")