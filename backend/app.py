from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from groq import Groq
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import numpy as np

app = FastAPI(title="Personal AI Assistant Backend")

# Initialize models
groq_client = None
pc = None
embedder = SentenceTransformer('all-MiniLM-L6-v2')

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default"

class KnowledgeRequest(BaseModel):
    text: str
    metadata: dict = {}

@app.on_event("startup")
async def startup_event():
    global groq_client, pc
    # Initialize Groq
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        groq_client = Groq(api_key=groq_api_key)
    else:
        print("Groq API key not set.")

    # Initialize Pinecone
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    if pinecone_api_key:
        pc = Pinecone(api_key=pinecone_api_key)
        # Create index if not exists
        if 'personal-assistant' not in pc.list_indexes().names():
            pc.create_index(name='personal-assistant', dimension=384, metric='cosine')
    else:
        print("Pinecone API key not set.")

@app.post("/chat")
async def chat(request: ChatRequest):
    if not groq_client:
        raise HTTPException(status_code=500, detail="Groq client not initialized")

    # Retrieve relevant knowledge
    context = ""
    if pc:
        try:
            index = pc.Index('personal-assistant')
            query_embedding = embedder.encode([request.message])[0].tolist()
            results = index.query(vector=query_embedding, top_k=3, include_metadata=True)
            context = "\n".join([match['metadata']['text'] for match in results['matches']])
        except Exception as e:
            print(f"Error retrieving from Pinecone: {e}")

    # Generate response using Groq
    prompt = f"Context: {context}\n\nUser: {request.message}\nAssistant:"
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama2-70b-4096",  # LLAMA 2 70B model
        )
        assistant_response = chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling Groq: {e}")
        assistant_response = "Error connecting to LLM service."

    return {"response": assistant_response}

@app.post("/add_knowledge")
async def add_knowledge(request: KnowledgeRequest):
    if not pc:
        raise HTTPException(status_code=500, detail="Pinecone not initialized")

    try:
        index = pc.Index('personal-assistant')
        embedding = embedder.encode([request.text])[0].tolist()
        index.upsert(vectors=[{
            'id': str(hash(request.text)),
            'values': embedding,
            'metadata': {'text': request.text, **request.metadata}
        }])
        return {"message": "Knowledge added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)