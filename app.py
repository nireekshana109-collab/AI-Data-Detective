import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from utils.data_analysis import profile_dataset, calculate_kpis, build_verified_summary
from utils.anomaly_detection import detect_anomalies
from utils.ai_insights import generate_ai_insights, answer_data_question
from utils.report_generator import build_html_report
from utils.visualizations import render_visualizations

load_dotenv()

st.set_page_config(page_title="AI Data Detective", page_icon="🔎", layout="wide")

st.markdown("""
<style>
.main-title {font-size: 2.5rem; font-weight: 800; margin-bottom: 0;}
.subtitle {font-size: 1.05rem; color: #6b7280; margin-bottom: 1.2rem;}
.card {padding: 1rem; border-radius: 12px; border: 1px solid #e5e7eb; background: #ffffff;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🔎 AI DATA DETECTIVE</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Python-Powered Analytics + Generative AI Insights</div>', unsafe_allow_html=True)

@st.cache_data
def load_demo():
    return pd.read_csv("sample_data/demo_dataset.csv")

if "df" not in st.session_state:
    st.session_state.df = None
if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "ai_report" not in st.session_state:
    st.session_state.ai_report = ""
if "chat" not in st.session_state:
    st.session_state.chat = []

with st.sidebar:
    st.header("📂 Data Upload")
    uploaded = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
    if st.button("Load Demo Dataset", use_container_width=True):
        st.session_state.df = load_demo()
        st.session_state.analysis = None
        st.session_state.ai_report = ""
        st.session_state.chat = []
        st.rerun()

    st.divider()
    st.caption("Privacy: uploaded data is analyzed in Python. Only a compact verified analytical summary is sent to Gemini when you request AI features.")

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)
        st.session_state.df = df
        st.session_state.analysis = None
        st.session_state.ai_report = ""
    except Exception as e:
        st.error(f"Could not read the file: {e}")

df = st.session_state.df

if df is None:
    st.info("Upload a dataset or load the demo dataset to begin the investigation.")
    st.stop()

if df.empty:
    st.error("The dataset is empty. Please provide a dataset containing at least one row.")
    st.stop()

try:
    profile = profile_dataset(df)
    kpis = calculate_kpis(df)
    anomalies = detect_anomalies(df)
    verified = build_verified_summary(profile, kpis, anomalies)
    st.session_state.analysis = {"profile": profile, "kpis": kpis, "anomalies": anomalies, "verified": verified}
except Exception as e:
    st.error(f"Analysis could not be completed: {e}")
    st.stop()

analysis = st.session_state.analysis

st.header("🔍 Dataset Overview")
p = analysis["profile"]
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Records", f"{p['rows']:,}")
m2.metric("Columns", p["columns"])
m3.metric("Missing Values", f"{p['missing_total']:,}")
m4.metric("Duplicate Rows", f"{p['duplicate_rows']:,}")

c1, c2 = st.columns(2)
with c1:
    st.write("**Numerical columns**")
    st.write(", ".join(p["numeric_columns"]) or "None detected")
with c2:
    st.write("**Categorical columns**")
    st.write(", ".join(p["categorical_columns"]) or "None detected")
st.write("**Date/time columns:** " + (", ".join(p["date_columns"]) or "None detected"))

with st.expander("Preview dataset", expanded=True):
    st.dataframe(df.head(20), use_container_width=True)

st.header("📊 Automatic Analytics")
if analysis["kpis"]:
    cols = st.columns(min(4, len(analysis["kpis"])))
    for i, (name, value) in enumerate(analysis["kpis"].items()):
        cols[i % len(cols)].metric(name, value)

with st.expander("Detailed numerical statistics"):
    if p["numeric_stats"]:
        st.dataframe(pd.DataFrame(p["numeric_stats"]).T, use_container_width=True)
    else:
        st.info("No numerical columns were detected.")

st.header("📈 Visualizations")
render_visualizations(df, p)

st.header("🚨 Anomaly Detection")
anom = analysis["anomalies"]
if anom["total_anomalies"] == 0:
    st.success("No IQR-based numerical anomalies were detected.")
else:
    a1, a2 = st.columns(2)
    a1.metric("Anomalous cells", f"{anom['total_anomalies']:,}")
    a2.metric("Affected rows", f"{len(anom['affected_rows']):,}")
    st.warning("An anomaly is a statistical outlier, not automatically an error or fraud.")
    if anom["details"]:
        st.dataframe(pd.DataFrame(anom["details"]), use_container_width=True)

st.header("🤖 AI Insights")
st.caption("Gemini receives verified results calculated by Python, not the raw dataset.")
if st.button("Generate AI Insights", type="primary"):
    with st.spinner("Generating evidence-based insights..."):
        try:
            st.session_state.ai_report = generate_ai_insights(analysis["verified"])
        except Exception as e:
            st.error(str(e))

if st.session_state.ai_report:
    st.markdown(st.session_state.ai_report)

st.header("💬 Ask Your Data")
question = st.chat_input("Ask something about the uploaded dataset...")
if question:
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        with st.spinner("Checking the dataset..."):
            try:
                answer = answer_data_question(question, df, analysis["verified"])
                st.write(answer)
                st.session_state.chat.append({"question": question, "answer": answer})
            except Exception as e:
                st.error(str(e))

st.header("📄 Download Report")
html_report = build_html_report(df, analysis, st.session_state.ai_report)
st.download_button(
    "Download Analysis Report (HTML)",
    data=html_report,
    file_name="ai_data_detective_report.html",
    mime="text/html",
    use_container_width=True
)
