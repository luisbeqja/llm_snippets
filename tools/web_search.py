import aiohttp
import json
import asyncio
from urllib.parse import quote_plus

# Define a tool that searches the web for information.
async def web_search(query: str) -> str:
    """Find information using Wikipedia's API"""
    encoded_query = quote_plus(query)
    
    try:
        async with aiohttp.ClientSession() as session:
            # First try a direct search since it's more reliable for finding relevant pages
            search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded_query}&format=json"
            async with session.get(search_url) as search_response:
                if search_response.status == 200:
                    search_data = await search_response.json()
                    search_results = search_data.get("query", {}).get("search", [])
                    
                    if not search_results:
                        return f"No information found about '{query}'."
                    
                    # Get full content for the top 2 most relevant results
                    full_results = []
                    for result in search_results[:2]:
                        result_title = result.get("title", "")
                        
                        # Get full page content using the "extracts" prop
                        extract_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=1&explaintext=1&titles={quote_plus(result_title)}&format=json"
                        async with session.get(extract_url) as extract_response:
                            if extract_response.status == 200:
                                extract_data = await extract_response.json()
                                pages = extract_data.get("query", {}).get("pages", {})
                                
                                # Extract the first page (there should only be one)
                                if pages:
                                    page_id = next(iter(pages))
                                    page = pages[page_id]
                                    title = page.get("title", "")
                                    extract = page.get("extract", "")
                                    
                                    if extract:
                                        wiki_url = f"https://en.wikipedia.org/wiki/{quote_plus(title)}"
                                        full_results.append(f"# {title}\n\n{extract}\n\nSource: {wiki_url}")
                    
                    if full_results:
                        return "\n\n---\n\n".join(full_results)
                    
                    # If we couldn't get full content, fall back to snippets
                    result_title = search_results[0].get("title", "")
                    snippet = search_results[0].get("snippet", "").replace("<span class=\"searchmatch\">", "").replace("</span>", "")
                    return f"# {result_title}\n\n{snippet}\n\nMore info: https://en.wikipedia.org/wiki/{quote_plus(result_title)}"
            
            # If search fails, try direct page lookup as a fallback
            wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_query}"
            async with session.get(wiki_url) as response:
                if response.status == 200:
                    wiki_data = await response.json()
                    extract = wiki_data.get("extract", "")
                    title = wiki_data.get("title", "")
                    if extract:
                        url = wiki_data.get("content_urls", {}).get("desktop", {}).get("page", "")
                        return f"# {title}\n\n{extract}\n\nSource: {url}"
                
            return f"No information found about '{query}'."
            
    except Exception as e:
        return f"Error during search: {str(e)}"

# Example usage
async def main():
    queries = [
        "What is AutoGen AI?",
        "Python programming language",
        "Machine learning",
        "Claude AI"
    ]
    
    for query in queries:
        print(f"\n\nSearching for: {query}")
        print("-" * 50)
        result = await web_search(query)
        print(result)
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())