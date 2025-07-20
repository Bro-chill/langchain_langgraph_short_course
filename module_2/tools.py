import os
import logging
from dotenv import load_dotenv

from pymongo import MongoClient

from langchain.agents import tool
from langchain_community.tools.tavily_search import TavilySearchResults

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
def personal_data(query: str) -> str:
    """Retrieve personal data from mongodb to answer personal questions about identity, name, preferences, or FAQ."""

    client = None
    try:
        mongodb_uri = os.getenv("MONGODB_ATLAS_CLUSTER_URI")
        if not mongodb_uri:
            logger.warning("MONGODB_ATLAS_CLUSTER_URI not set, using fallback data")
            fallback_data = _get_fallback_data()
            return f"Personal Information: {fallback_data}"
        
        # Initialize timeout
        client = MongoClient(
            mongodb_uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=5000
        )

        # Database configuration
        DB_NAME = os.getenv("MONGODB_DB_NAME")
        COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME")

        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Test connection
        client.admin.command('ping')
        logger.info(f"Connected to MongoDB: {DB_NAME}.{COLLECTION_NAME}")

        # Retrieve data - Fixed the query to match actual document structure
        documents = list(collection.find(
            {},
            {"_id": 0}
        ).limit(10))

        if len(documents) == 0:
            logger.warning("No documents found in MongoDB, using fallback")
            fallback_data = _get_fallback_data()
            return f"Personal Information: {fallback_data}"

        content = []
        for doc in documents:
            # Handle different possible document structures
            if 'page_content' in doc:
                content.append(doc['page_content'])
            elif 'text' in doc:
                content.append(doc['text'])
            # else:
            #     doc_str = str(doc)
            #     if len(doc_str) > 50:  # Only add if it has substantial content
            #         content.append(doc_str)

        if not content:
            logger.warning("No content found in documents, using fallback")
            fallback_data = _get_fallback_data()
            return f"Personal Information: {fallback_data}"

        # Join all content and return
        all_content = "\n".join(content)
        return f"Personal Information from Database: {all_content}"
    
    except Exception as e:
        logger.error(f"MongoDB RAG tool failed: {str(e)}")
        fallback_data = _get_fallback_data()
        return f"Personal Information: {fallback_data}"
    
    finally:
        if client:
            try:
                client.close()
                logger.debug("MongoDB connection closed")
            except Exception as e:
                logger.warning(f"Error closing MongoDB connection: {str(e)}")

def _get_fallback_data() -> dict:
    """Fallback data if RAG mongoDB failed"""
    return {
        "name": "Tom Kurus",
        "favorite_food": "Tom Yum",
        "personality": "Professional AI trash talker",
        "faq": [
            {"question": "what is your name?", "answer": "Tom Kurus"},
            {"question": "what do you like to eat?", "answer": "Tom Yum"},
            {"question": "who are you?", "answer": "I'm Tom Kurus, your friendly neighborhood AI trash talker"}
        ]
    }

tools = [tavily_search, personal_data]