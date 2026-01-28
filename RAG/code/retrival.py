from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

vector_store = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name='learning',
    embedding=embeddings
)

user_input = input("Enter your question: ")

# return relevant chunks from vector store
search_results = vector_store.similarity_search(query=user_input)


context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

# chatmodel
SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on the context availabl and it is retrive from the PDF file along with page_content, and page number. 

you only answer the user based on the following context and navigate the user to right page number to know more details.

context: {context}

"""

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {   "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
)

print(response.choices[0].message.content)