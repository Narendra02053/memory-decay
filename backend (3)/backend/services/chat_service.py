import os
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
from transformers import pipeline
from transformers.pipelines import TextGenerationPipeline

load_dotenv()


@lru_cache(maxsize=1)
def _get_client() -> Optional[OpenAI]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


@lru_cache(maxsize=1)
def _get_local_bot() -> Optional[TextGenerationPipeline]:
    try:
        return pipeline("text-generation", model="distilgpt2")
    except Exception as err:
        print(f"[CHAT] Local model load failed: {err}")
        return None


FALLBACK_REPLY = (
    "Hi! I couldn't reach the AI model right now, but keep reviewing your notes "
    "and try spaced repetition or a quick summary to reinforce your memory."
)


def _extract_text(response) -> Optional[str]:
    try:
        return response.choices[0].message.content
    except Exception:
        pass
    return None


def chat_with_ai(user_message: str) -> str:
    if not user_message or not user_message.strip():
        return "Please provide a message to chat about."
    
    client = _get_client()

    if client is not None:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful study assistant who gives concise, encouraging replies.",
                    },
                    {"role": "user", "content": user_message},
                ],
                temperature=0.7,
                max_tokens=200,
            )

            text = _extract_text(response)
            if text:
                return text.strip()
        except Exception as err:
            print(f"[CHAT] OpenAI error: {err}")
            # Continue to try local bot

    local_bot = _get_local_bot()
    if local_bot is not None:
        try:
            generated = local_bot(
                f"User: {user_message}\nAssistant:",
                max_length=100,
                num_return_sequences=1,
                do_sample=True,
                temperature=0.9,
                pad_token_id=local_bot.tokenizer.eos_token_id,
            )[0]["generated_text"]

            reply = generated.split("Assistant:", 1)[-1].strip()
            if reply and len(reply) > 5:  # Ensure we have a meaningful reply
                return reply
        except Exception as err:
            print(f"[CHAT] Local generation error: {err}")

    return FALLBACK_REPLY
