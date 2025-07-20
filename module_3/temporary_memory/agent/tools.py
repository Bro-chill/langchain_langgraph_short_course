import os
import logging
from dotenv import load_dotenv

from pymongo import MongoClient

from langchain.agents import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import ArxivAPIWrapper


logger = logging.getLogger(__name__)

load_dotenv()
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

@tool
def tavily_search(query: str) -> str:
    """Search using Tavily information about a topic"""
    try:
        tavily_search = TavilySearchResults(
            max_results=3,
            tavily_api_key=TAVILY_API_KEY
        )
        result = tavily_search.invoke(query)
        return str(result)
    except Exception as e:
        return f"Error searching using Tavily: {str(e)}"
    
@tool
def research_paper_search(query: str) -> str:
    """Search Research Paper about a topic"""
    try:
        arxiv = ArxivAPIWrapper()
        result = arxiv.run(query)
        return result
    except Exception as e:
        return f"Error searching For Research Paper: {str(e)}"
    
tools = [tavily_search, research_paper_search]