import os
from langchain_groq import ChatGroq

def get_llm(temperature=0.2):
    return ChatGroq(
        model=os.getenv("GROQ_MODEL", "llama3-8b-8192"),
        temperature=temperature,
    )
