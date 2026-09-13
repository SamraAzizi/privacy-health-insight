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