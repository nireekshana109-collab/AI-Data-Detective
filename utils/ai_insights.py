import os
import json
import pandas as pd

try:
    from google import genai
except ImportError:
    genai = None


_CLIENT = None


def _client():
    global _CLIENT

    key = os.getenv("GEMINI_API_KEY")

    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to .env locally "
            "or Streamlit Secrets in deployment."
        )

    if genai is None:
        raise RuntimeError(
            "The Google GenAI package is not installed. "
            "Run pip install -r requirements.txt."
        )

    if _CLIENT is None:
        _CLIENT = genai.Client(api_key=key)

    return _CLIENT


def _prompt(verified, question=None):
    context = json.dumps(verified, indent=2, default=str)

    base = f"""You are an expert data analyst.

Analyze ONLY the verified analytical results below, calculated by Python.

VERIFIED ANALYTICAL RESULTS:
{context}

CONSTRAINTS:
- Do not invent numbers.
- Do not modify calculated values.
- Clearly distinguish calculated facts from interpretations.
- Keep facts tied to the supplied results.
- If evidence is insufficient, explicitly say so.
- Explain findings in simple professional language.
"""

    if question:
        return base + f"""
USER QUESTION:
{question}

For exact numerical/factual questions, use only values supported by
the verified results.

If the verified results do not contain enough information, say:
"The uploaded dataset does not contain enough information to answer this question."
"""

    return base + """
Return these sections:

## Key Findings
Give 3–5 important findings.

## Possible Explanations
Give 2–4 plausible explanations and label them as interpretations.

## Recommendations
Give 3–5 actionable recommendations.

## Risk / Warning
Mention important anomalies or suspicious patterns.

## Executive Summary
Give a concise professional summary.
"""


def generate_ai_insights(verified):
    client = _client()

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=_prompt(verified)
        )

        return response.text

    except Exception as e:
        message = str(e)

        if (
            "503" in message
            or "UNAVAILABLE" in message
            or "high demand" in message
        ):
            return (
                "⚠️ Gemini is temporarily busy right now.\n\n"
                "Your data analysis and visualizations are still working "
                "normally. Please click **Generate AI Insights** again "
                "after a short while."
            )

        raise


def _simple_exact_answer(question, df):
    q = question.lower().strip()

    numeric = df.select_dtypes(include="number").columns.tolist()
    categorical = df.select_dtypes(exclude="number").columns.tolist()

    if any(word in q for word in ["highest", "top", "best", "most"]):

        metric = None

        for c in numeric:
            if c.lower() in q:
                metric = c
                break

        if metric is None and "revenue" in q:
            metric = next(
                (c for c in numeric if "sales" in c.lower()),
                None
            )

        group_col = None

        for c in categorical:
            if c.lower() in q:
                group_col = c
                break

        if group_col is None:
            for c in categorical:
                if c.lower() + "s" in q:
                    group_col = c
                    break

        if metric and group_col:
            grouped = (
                df.groupby(group_col)[metric]
                .sum()
                .sort_values(ascending=False)
            )

            if not grouped.empty:
                return (
                    f"The {group_col} with the highest total {metric} "
                    f"is {grouped.index[0]} with "
                    f"{grouped.iloc[0]:,.2f}."
                )

    if any(word in q for word in ["average", "mean"]):

        for c in numeric:
            if c.lower() in q:
                return (
                    f"The verified average {c} is "
                    f"{df[c].mean():,.2f}."
                )

    if any(word in q for word in ["total", "sum"]):

        for c in numeric:
            if c.lower() in q:
                return (
                    f"The verified total {c} is "
                    f"{df[c].sum():,.2f}."
                )

    return None


def answer_data_question(question, df, verified):
    exact = _simple_exact_answer(question, df)

    if exact:
        return exact

    client = _client()

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=_prompt(verified, question)
    )

    return response.text