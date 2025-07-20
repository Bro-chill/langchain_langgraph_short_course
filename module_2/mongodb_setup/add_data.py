# Save data to mongodb
import os
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_KEY")

embeddings = GoogleGenerativeAIEmbeddings(
  model="models/embedding-001",
  google_api_key=api_key
  )

client = MongoClient(os.getenv("MONGODB_ATLAS_CLUSTER_URI"))

DB_NAME = os.getenv("MONGODB_DB_NAME")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME")
ATLAS_VECTOR_SEARCH_INDEX_NAME = "faq-pdf"

MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

# MONGODB_COLLECTION.delete_many({})  # If need to delete what ever in current DB


vector_store = MongoDBAtlasVectorSearch(
  collection=MONGODB_COLLECTION,
  embedding=embeddings,
  index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
  relevance_score_fn="cosine",
)

text_splitter = RecursiveCharacterTextSplitter(
  chunk_size = 500,
  chunk_overlap = 100
)

loader = PyPDFLoader("faq.pdf")

docs = loader.load_and_split(
  text_splitter=text_splitter
)

vector_store.add_documents(docs)

print("Documents Added")
client.close()