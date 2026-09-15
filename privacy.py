import streamlit as st
import pandas as pd
import json
import db

def render_privacy_policy():
    """Renders the in-app privacy note explaining data locality guarantees."""
    st.markdown("## 🛡️ Privacy Policy & Data Sovereignty Note")
    
    st.info(
        """
        **Zero-Cloud Commitment:** This application operates on a **Local-First** model. 
        Your health metrics, mood logs, and personal notes are saved exclusively to a local database on your device.
        """
    )
    
    st.markdown(
        """
        ### How Your Data Is Handled:
        1. **Local Database:** All daily logs are stored inside a local SQLite file (`health_data.db`) located in your project directory. No central server or third-party cloud database receives this data.
        2. **Analytics & Charts:** All trends, summary metrics, and visualizations (Plotly) are rendered locally inside your web browser engine.
        3. **Local AI Summaries:** When enabled, metrics are formatted and processed locally using **Ollama** (`http://localhost:11434`). Text context remains entirely on your machine.
        4. **Data Ownership:** You can export or erase your dataset at any time using the tools on this page.
        """
    )