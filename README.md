# 🌿 Privacy-First Health Insight App

A local-first, privacy-respecting dashboard for logging daily health metrics, visualizing long-term wellbeing trends, and generating automated AI insights. 

Unlike conventional health-tracking apps that upload sensitive personal data to third-party cloud servers, this application keeps **100% of your data on your local device**. All logs are saved to a local database, and AI summaries are generated locally using **Ollama**.

---

##  Features

- ** Daily Metrics Logging:** Easily log sleep duration, step counts, mood ratings (1–10), and optional journal notes.
- ** Interactive Analytics:** Multi-metric time-series visualizations powered by Plotly with synchronized hover tooltips and dynamic time-range filtering (Last 7 Days, Last 30 Days, All Time).
- ** Local AI Summaries:** Opt-in, privacy-preserving AI reflections using local open-source LLMs (via Ollama) with zero data leaving your machine.
- ** Complete Data Sovereignty:** Export your dataset to CSV or JSON format, restore/import backups, and delete entries anytime.
- ** Built-in Privacy Disclosures:** Clear, accessible in-app documentation detailing local data storage mechanics.

---

## 🛠️ Tech Stack

- **Frontend & UI:** Python, [Streamlit](https://streamlit.io/)
- **Database:** SQLite (`sqlite3` parameterized queries)
- **Data Processing:** Pandas
- **Visualizations:** Plotly Express / Plotly Graph Objects
- **Local AI Engine:** [Ollama REST API](https://ollama.com/) (`llama3.2` / `mistral`)

---

##  Project Architecture

```text
health-insight-app/
├── app.py                 # Main Streamlit dashboard & tab navigation
├── db.py                  # SQLite schema & CRUD operations
├── ai.py                  # Local Ollama AI integration & prompt formatting
├── privacy.py             # Data export/import & privacy policy views
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation
└── health_data.db         # Local SQLite database (created on first run)
```

## Getting Started

### Prerequisites
- Python 3.10+ installed on your machine.
- VS Code (or your preferred IDE).
- (Optional for AI summaries) Ollama installed locally from ollama.com.

### Installation
1. Clone or download the repository:
```bash
git clone "https://github.com/SamraAzizi/privacy-health-insight.git"
cd privacy-health-insight-app
```
2. Create and activate a virtual environment:
- Windows
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

3. Install required packages:
```bash
pip install -r requirements.txt
```
4. Launch the application:
```
streamlit run app.py
```
The app will automatically open in your default browser at `http://localhost:8501`.

### Optinal 
1. Download and install Ollama from ollama.com.

2. Start the local model in your system terminal
```bash
ollama run llama3.2
```
3. In the app, navigate to the Local AI Wellbeing Summary section, check Enable AI Insights Engine (Opt-In), and click Generate Summary.