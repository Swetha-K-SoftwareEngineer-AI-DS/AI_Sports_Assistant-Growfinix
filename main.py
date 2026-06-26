import pandas as pd
import json
import re
from assistant import get_intent

# Load dataset
df = pd.read_csv("data/matches.csv")

print("🏏 AI Sports Assistant Ready!")

def extract_json(text):
    if not text:
        return None

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            return None
    return None


while True:
    q = input("\nAsk question (type exit): ")

    if q.lower() == "exit":
        break

    response = get_intent(q, list(df.columns))
    print("\nRAW:", response)

    # ✅ SAFE CHECK (FIX FOR YOUR ERROR)
    if not response:
        print("❌ AI returned empty response")
        continue

    intent = extract_json(response)

    if not intent:
        print("❌ Could not understand question")
        continue

    op = intent.get("operation")
    col = intent.get("column")

    try:
        # 🔥 SAFE COLUMN HANDLING
        if col not in df.columns:
            col = "winner" if "winner" in df.columns else df.columns[0]

        # 🔥 OPERATIONS
        if op in ["most_frequent", "groupby_max", "team_wins"]:
            result = df[col].value_counts().idxmax()

        elif op == "count":
            result = df[col].count()

        else:
            result = f"Unsupported operation: {op}"

        print("\n📊 Answer:", result)

    except Exception as e:
        print("Error:", e)