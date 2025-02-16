import os
import getpass
from dotenv import load_dotenv
import google.generativeai as genai
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API using the API key from .env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Sample knowledge base (Replace with actual knowledge base)
documents = [
    "Aura AI can manage tasks and schedule meetings.",
    "Gemini Pro is an advanced AI model by Google optimized for text generation.",
    "FAISS enables fast vector searches for AI retrieval systems."
]

# Convert text into embeddings
doc_vectors = np.array([embedding_model.encode(doc) for doc in documents])

# Create FAISS index
index = faiss.IndexFlatL2(doc_vectors.shape[1])
index.add(doc_vectors)

# Store documents with index mappings
doc_mapping = {i: doc for i, doc in enumerate(documents)}

def retrieve_context(query, top_k=1):
    """Retrieve relevant document based on query"""
    query_vector = np.array([embedding_model.encode(query)])
    distances, indices = index.search(query_vector, top_k)
    return [doc_mapping[idx] for idx in indices[0]]

# Global dictionaries to maintain conversation history and personal info per owner
CONVERSATION_MEMORY = {}
PERSONAL_INFO_DATA = {}

def ask_gemini(user_query, chat_history=None, personal_info=None):
    """Fetch relevant context and generate response using Gemini.
    
    It accumulates conversation history and personal info (with consent)
    for improved context. It includes a greeting only for the first message.
    """
    # Retrieve owner name from environment or fall back to the system username.
    owner = os.getenv("AURA_OWNER", getpass.getuser() or "User")
    
    # Initialize owner's conversation memory if not present
    if owner not in CONVERSATION_MEMORY:
        CONVERSATION_MEMORY[owner] = []
    
    # If new chat history is provided, add it to the owner's memory.
    if chat_history:
        # Expecting chat_history as a list of dicts like:
        # [{"sender": "user", "text": "..."}, {"sender": "ai", "text": "..."}, ...]
        CONVERSATION_MEMORY[owner].extend(chat_history)
    
    # Prepare a history text from the accumulated conversation memory.
    history_text = "\n".join(
        f"{msg['sender'].capitalize()}: {msg['text']}" for msg in CONVERSATION_MEMORY[owner]
    )
    if history_text:
        history_text = f"Previous Conversation:\n{history_text}\n\n"
    
    # Update and retrieve personal information if provided (with user consent)
    if personal_info:
        PERSONAL_INFO_DATA[owner] = personal_info
    personal_info_text = PERSONAL_INFO_DATA.get(owner, "")
    if personal_info_text:
        personal_info_text = f"Personal Information Provided:\n{personal_info_text}\n\n"
    
    # Retrieve context from your FAISS index based on the user query.
    context = retrieve_context(user_query)
    
    # Determine greeting instructions:
    if history_text.strip() == "":
        # No previous conversation: provide a greeting once.
        greeting_instruction = (f"Begin your response with a warm greeting such as "
                                f"'Hey {owner}, how may I help you?' and then proceed with your answer.")
    else:
        # Already in a conversation: no greeting required.
        greeting_instruction = "Do not include an extra greeting. Simply provide a clear, concise answer."
    
    # Prepare the prompt for the Gemini API.
    prompt = f"""
    {history_text}{personal_info_text}
    You are Aura, a versatile and intelligent desktop assistant.
    You are designed to support your owner in multiple domains.
    {greeting_instruction}
    
    Your core capabilities include:
    
      • Text-based AI Chat - engaging in natural conversation and answering questions.
      • File Management - creating, moving, and deleting files via system APIs.
      • Document Generation - producing professional Word documents, Excel spreadsheets, and PowerPoint presentations.
      • Voice Command Support - processing voice commands for hands-free operation.
      • Web Search Integration - retrieving and summarizing search results from the web.
      • Prompt Filtering - ensuring queries are secure and appropriate.
      • Task Automation - launching applications, scheduling events, and performing other system actions.
    
    When responding, use the conversation context below along with the user's input to generate a clear, concise, and actionable answer.
    If applicable, suggest next steps or commands to help your owner accomplish the task.
    
    Context: {context}
    User Query: {user_query}
    """
    
    response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
    
    # Optionally: Append the current AI response back into the conversation memory.
    CONVERSATION_MEMORY[owner].append({"sender": "ai", "text": response.text})
    
    return response.text
