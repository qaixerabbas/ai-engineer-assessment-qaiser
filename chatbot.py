import httpx
import json

from config import GROQ_API_KEY, GROQ_URL, MODEL
from superhero import search_superhero


async def call_llm(prompt: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": 0.2,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            GROQ_URL,
            headers=headers,
            json=payload,
        )

        response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


def load_dataset():
    with open("data/knowledge.jsonl", "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]
        # return f.read()


async def classify_question(question: str):
    prompt = f"""
            Classify this question into exactly one category:

            TEXT
            SUPERHERO
            BOTH

            TEXT = question is about the provided text dataset.
            SUPERHERO = question is about superheroes.
            BOTH = requires both sources.

            Question:
            {question}

            Return only one word.
        """

    result = await call_llm(prompt)

    result = result.strip().upper()

    if result not in {"TEXT", "SUPERHERO", "BOTH"}:
        return "TEXT"

    return result


async def answer_question(question: str):

    category = await classify_question(question)

    context = []
    sources = []

    # Local text dataset
    if category in {"TEXT", "BOTH"}:
        dataset = load_dataset()

        context.append(
            f"TEXT DATASET:\n{dataset}"
        )

        sources.append("Text dataset")

    # Superhero API
    if category in {"SUPERHERO", "BOTH"}:

        # Ask LLM to identify the superhero name
        name_prompt = f"""
            Extract the superhero name from this question.
            Question:
            {question}
            Return only the superhero name.
        """

        hero_name = await call_llm(name_prompt)

        hero_name = hero_name.strip()

        try:
            heroes = await search_superhero(hero_name)

            if heroes:
                hero = heroes[0]

                context.append(
                    f"SUPERHERO API DATA:\n{hero}"
                )

                sources.append("Superhero API")

        except Exception:
            # dont raise an error if the superhero API fails, just continue with the other sources
            pass

    if not context:
        return {
            "answer": "I could not find information to answer this question.",
            "sources": [],
        }

    final_prompt = f"""
        Answer the user's question using ONLY the information below.

        USER QUESTION:
        {question}

        SOURCE INFORMATION:
        {"".join(context)}

        Rules:
        - Do not invent facts.
        - If the information is insufficient, say so.
        - Give a concise answer.
        - Mention the source at the end.

        Answer:
    """

    answer = await call_llm(final_prompt)

    return {
        "answer": answer,
        "sources": sources,
    }