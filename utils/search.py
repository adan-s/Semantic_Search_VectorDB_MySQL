from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")


def semantic_search(articles, query):
    """Perform semantic search on articles."""
    # Extract page content for embedding
    texts = [article[1] for article in articles]  # article[1] = page_content

    # Create FAISS index
    vector_store = FAISS.from_texts(texts, embeddings)

    # Perform search
    results = vector_store.similarity_search(query)
    return results
