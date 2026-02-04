# Personal AI Assistant

A personal assistant powered by a self-hosted large language model (LLM) that can understand user queries and respond with contextually relevant information. The assistant uses a vector database (Pinecone) for storing and retrieving knowledge and provides a conversational interface via a chatbot UI.

## Features

- Self-hosted LLM (LLAMA 2) for natural language understanding and generation
- Vector database (Pinecone) for knowledge storage and retrieval
- Conversational chatbot UI built with Streamlit
- RESTful API backend with FastAPI

## Prerequisites

- Python 3.8+
- Pinecone account and API key
- Groq account and API key (for LLAMA model access)

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Jeevankumar312/Personal-AI-Assistant.git
   cd Personal-AI-Assistant
   ```

2. Install backend dependencies:

   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

3. Install frontend dependencies:

   ```bash
   cd frontend
   pip install -r requirements.txt
   cd ..
   ```

4. Set up Groq:
   - Create a Groq account at [groq.com](https://groq.com)
   - Get your API key
   - Set the environment variable: `export GROQ_API_KEY=your_api_key_here`

5. Set up Pinecone:
   - Create a Pinecone account at [pinecone.io](https://pinecone.io)
   - Get your API key
   - Set the environment variable: `export PINECONE_API_KEY=your_api_key_here`

## Running the Assistant

1. Start the backend server:

   ```bash
   cd backend
   python app.py
   ```

   The backend will run on http://localhost:8000

2. Start the frontend (in a new terminal):
   ```bash
   cd frontend
   streamlit run app.py
   ```
   The chatbot UI will open in your browser

## Usage

- Use the chat interface to ask questions
- The assistant will use the LLM to generate responses and retrieve relevant knowledge from the vector database
- Add new knowledge through the sidebar to expand the assistant's knowledge base

## API Endpoints

- `POST /chat`: Send a chat message and receive a response
- `POST /add_knowledge`: Add new knowledge to the vector database

## Architecture

- **Backend**: FastAPI server handling LLM inference via Ollama API and vector database operations
- **Frontend**: Streamlit web app providing the chatbot interface
- **LLM**: LLAMA 2 model via Groq API for natural language processing
- **Vector DB**: Pinecone for efficient knowledge retrieval
