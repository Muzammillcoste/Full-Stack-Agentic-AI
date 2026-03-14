from mem0 import Memory
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {"host": "localhost", "port": 6333}
    },
    "llm": {
        "provider": "gemini",
        "config": {"model": "gemini-2.5-flash", "api_key": GEMINI_API_KEY},
    },
    "embedder": {
        "provider": "gemini",
        "config": {"model": "models/gemini-embedding-001", "api_key": GEMINI_API_KEY},
    }
}

mem_client = Memory.from_config(config)

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

while True:

    user_input = input("> Whats on your mind today?: ")

    # 1. search related memories
    search_memory = mem_client.search(user_input, user_id="john_doe")

    memories = [
        f"ID: {mem.get('id')}\nMemory: {mem.get('memory')}"
        for mem in search_memory
    ]

    SYSTEM_PROMPT = f"""
You are a helpful assistant.

Here is information about the user from past conversations:
{memories}

Use it if relevant when responding.
"""

    print("memory found")

    # 2. generate response
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    ai_response = response.choices[0].message.content
    print("AI:", ai_response)

    # 3. store memory
    mem_client.add(
        user_id="john_doe",
        messages=[
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": ai_response}
        ]
    )

    print("memory updated")