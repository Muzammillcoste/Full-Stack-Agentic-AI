from mem0 import Memory
from dotenv import load_dotenv
import os 

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

config = {
    "vector_store":{
        "provider": "qdrant",
        "config": {"host": "localhost", "port": 6333}
    },
     "llm": {
        "provider": "gemini",
        "config": {"model": "gemini-2.5-flash","api_key": GEMINI_API_KEY},
     },
    "embedder":{
        "provider":"gemini",
        "config":{"model":"models/gemini-embedding-001","api_key": GEMINI_API_KEY},
    }
}

mem_client = Memory.from_config(config)