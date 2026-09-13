import requests
import json
import pandas as pd
from typing import Optional, Dict, Any

# Default local Ollama endpoint
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3.2"  # Or "mistral", "phi3", etc.

def format_logs_for_llm(df: pd.DataFrame) -> str:
    """Formats the DataFrame of metrics into a clean text prompt for the LLM."""
    if df.empty:
        return "No health logs available."

    formatted_text = "Here is the user's daily health log for recent days:\n\n"
    for _, row in df.iterrows():
        notes_str = f" | Notes: {row['notes']}" if pd.notna(row['notes']) and row['notes'] else ""
        formatted_text += (
            f"- Date: {row['log_date']} | Sleep: {row['sleep_hours']} hrs | "
            f"Steps: {row['steps']} | Mood: {row['mood']}/10{notes_str}\n"
        )
    return formatted_text

    def check_local_ollama_status() -> bool:
    """Checks if Ollama service is running locally."""
    try:
        response = requests.get("http://localhost:11434/", timeout=2)
        return response.status_code == 200
    except requests.RequestException:
        return False


def generate_health_summary_ollama(df: pd.DataFrame, model_name: str = DEFAULT_MODEL) -> Dict[str, Any]:
    """
    Generates a privacy-preserving summary using a local Ollama model.
    Data stays completely on the local machine.
    """
    if df.empty:
        return {"success": False, "error": "No health metrics logged yet."}

    logs_context = format_logs_for_llm(df)

    system_prompt = (
        "You are an encouraging, empathetic wellbeing reflection assistant.\n"
        "STRICT GUIDELINES:\n"
        "1. Summarize trends in sleep, steps, and mood in 3 short, actionable bullet points.\n"
        "2. Keep the tone warm and supportive.\n"
        "3. DO NOT offer medical advice, diagnoses, or clinical suggestions under any circumstance.\n"
        "4. Keep the entire response under 150 words."
    )