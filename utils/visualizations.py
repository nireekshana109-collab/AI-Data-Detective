import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

def _find(df, words):
    for c in df.columns:
        if any(w in str(c).lower() for w in words):
            return c
    return None

def render_visualizations(df, profile):
    numeric = profile["numeric_columns"]
    categorical = profile["categorical_columns"]
    dates = profile["date_columns"]

    if numeric:
        col = st.selectbox("Numerical distribution", numeric, key="hist_col")
        fig = px.histogram(df, x=col, marginal="box", title=f"Distribution of {col}")
        st.plotly_chart(fig, use_container_width=True)

    if categorical and numeric:
        c1, c2 = st.columns(2)
        with c1:
            cat = st.selectbox("Category", categorical, key="bar_cat")
        with c2:
            num = st.selectbox("Metric", numeric, key="bar_num")
        grouped = df.groupby(cat, dropna=False)[num].sum().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(grouped, x=cat, y=num, title=f"Top {cat} by {num}")
        st.plotly_chart(fig, use_container_width=True)

    if dates and numeric:
        dcol = dates[0]
        ncol = _find(df, ["sales", "revenue", "profit"]) or numeric[0]
        tmp = df.copy()
        tmp[dcol] = pd.to_datetime(tmp[dcol], errors="coerce")
        tmp = tmp.dropna(subset=[dcol])
        if not tmp.empty:
            monthly = tmp.set_index(dcol)[ncol].resample("ME").sum().reset_index()
            fig = px.line(monthly, x=dcol, y=ncol, markers=True, title=f"{ncol} over time")
            st.plotly_chart(fig, use_container_width=True)

    if len(numeric) >= 2:
        corr = df[numeric].corr(numeric_only=True)
        fig = px.imshow(corr, text_auto=".2f", aspect="auto", title="Numerical Correlation Heatmap")
        st.plotly_chart(fig, use_container_width=True)
