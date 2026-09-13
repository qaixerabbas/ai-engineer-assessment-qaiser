# Superhero Q&A API

A FastAPI service that answers questions using the local knowledge base, the Superhero API, and a configured Groq-compatible LLM endpoint.

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn httpx python-dotenv
```

Create a `.env` file with:

```env
GROQ_API_KEY=your-groq-api-key
SUPERHERO_API_TOKEN=your-superhero-api-token
GROQ_URL=your-groq-compatible-chat-endpoint
MODEL=your-model-name
```

## Run

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Send questions to `POST /ask` with a JSON body such as:

```json
{"question": "Who is Batman?"}
```