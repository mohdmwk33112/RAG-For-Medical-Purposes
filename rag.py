import chromadb
import google.generativeai as genai
from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction

# Initialize Chroma and Gemini
client = chromadb.PersistentClient(path="./db.sqlite")
google_ef = GoogleGenerativeAiEmbeddingFunction(api_key="API")
collection = client.get_or_create_collection(name="medicine", embedding_function=google_ef)

genai.configure(api_key="API")
model = genai.GenerativeModel("gemini-pro")

def get_response(query):
    results = collection.query(query_texts=[query], n_results=3)
    retrieved_docs = results['documents'][0]

    # Construct context with temperature setting
    context = "\n"
    for doc in retrieved_docs:
        context += f"{doc}\n" 

    full_prompt = f"""

    Context:
    {context}

    Query:
    {query}

    **Parameters:**
    * **Temperature:** 0

    """

    response = model.generate_content(
        full_prompt,
        safety_settings=[
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "HIGH"}]
    )

    return response.text