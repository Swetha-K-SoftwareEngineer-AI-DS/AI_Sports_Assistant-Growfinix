import streamlit as st
import pandas as pd
import json
import re
from assistant import get_intent

df = pd.read_csv("data/matches.csv")

st.title("🏏 AI Sports Analytics Assistant")

def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            return None
    return None

question = st.text_input("Ask a question about IPL data:")

if question:
    response = get_intent(question, list(df.columns))
    st.write("RAW AI:", response)

    intent = extract_json(response)

    if intent:
        op = intent.get("operation")
        col = intent.get("column")

        if col not in df.columns:
            col = "winner" if "winner" in df.columns else df.columns[0]

        if op in ["most_frequent", "groupby_max", "team_wins"]:
            result = df[col].value_counts().idxmax()

        elif op == "count":
            result = df[col].count()

        else:
            result = "Unsupported operation"

        st.success(f"Answer: {result}")
    else:
        st.error("Could not understand question")