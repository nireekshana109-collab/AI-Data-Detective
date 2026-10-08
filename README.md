# AI Data Detective – Intelligent Data Analysis and Insight Generation System

## Overview
AI Data Detective is a Streamlit GenAI application that combines **real Python/Pandas analytics** with **Google Gemini** for explanation, interpretation and recommendations. It is designed as a transparent college-level data analytics + GenAI project.

## Problem Statement
Many users can view charts but struggle to convert raw datasets into understandable findings. The system automates dataset profiling, statistical analysis, visualization and explainable anomaly detection, then uses Generative AI to communicate verified findings.

## Objectives
- Profile uploaded datasets automatically.
- Calculate statistics and business KPIs with Python.
- Detect explainable statistical anomalies using IQR.
- Generate meaningful visualizations.
- Send only verified analytical summaries to Gemini.
- Provide natural-language insights and dataset Q&A.
- Generate a downloadable report.

## Features
- CSV and Excel upload
- Demo business dataset
- Dataset overview and profiling
- Numerical statistics
- Dynamic KPI detection
- Automatic charts
- Correlation analysis
- IQR anomaly detection
- Gemini insight generation
- Ask Your Data
- HTML report download
- Environment-variable API key management
- User-friendly error handling

## Technology Stack
Python, Streamlit, Pandas, NumPy, Plotly, Google Gemini API, python-dotenv, OpenPyXL.

## System Workflow
1. User uploads or loads a dataset.
2. Pandas profiles the data.
3. Python calculates statistics, KPIs and anomalies.
4. Plotly renders relevant visualizations.
5. A compact verified analytical summary is created.
6. Gemini receives that summary with a constrained prompt.
7. Gemini explains findings and proposes recommendations.
8. User can ask questions; exact calculations are performed locally where supported.
9. A report can be downloaded.

## Project Structure
```text
AI-Data-Detective/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── utils/
│   ├── data_analysis.py
│   ├── anomaly_detection.py
│   ├── ai_insights.py
│   ├── visualizations.py
│   └── report_generator.py
└── sample_data/
    └── demo_dataset.csv
```

## Installation

### 1. Create and activate a virtual environment
Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:
```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

## Gemini API configuration
Create a `.env` file:
```text
GEMINI_API_KEY=your_api_key_here
```
Never commit `.env` to GitHub. Add `.env` to `.gitignore`.

For Streamlit Community Cloud, add `GEMINI_API_KEY` under the app's Secrets settings.

## Run locally
```bash
streamlit run app.py
```

## GitHub deployment
```bash
git init
git add .
git commit -m "Initial AI Data Detective project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/AI-Data-Detective.git
git push -u origin main
```

## Streamlit Community Cloud
1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Create a new app.
4. Select the repository, branch `main`, and `app.py`.
5. Add a secret:
```toml
GEMINI_API_KEY = "your_api_key_here"
```
6. Deploy.

## Screenshots
Capture:
1. Landing/upload screen
2. Dataset overview metric cards
3. Automatic analytics
4. Visualization dashboard
5. Anomaly detection
6. AI Insights
7. Ask Your Data
8. Download report area

## Limitations
- Very large datasets may require optimization or sampling.
- IQR detects statistical outliers, not confirmed errors or fraud.
- Exact natural-language Q&A is intentionally conservative when a direct Python calculation is not implemented.
- Gemini output depends on model/API availability.

## Future Enhancements
Predictive analytics, automated ML model selection, natural-language SQL, multimodal document analysis, real-time dashboards, advanced anomaly detection, RAG-based organizational knowledge, multi-agent analytics, database connectivity and cloud-scale analytics.

## Academic Value
The application demonstrates data preprocessing, descriptive statistics, KPI engineering, anomaly detection, visualization, prompt engineering, GenAI integration, hallucination control, interactive UI design and deployment.
