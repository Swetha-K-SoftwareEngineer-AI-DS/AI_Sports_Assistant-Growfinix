import subprocess

def get_intent(question, columns):

    prompt = f"""
You are an IPL data analyst.

Return ONLY JSON.

Columns:
{columns}

Question:
{question}

Return format:
{{"operation": "most_frequent", "column": "winner"}}
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2"],
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8"
        )

        output = result.stdout.strip()

        # 🔥 DEBUG SAFETY
        if not output:
            return '{"operation": "most_frequent", "column": "winner"}'

        return output

    except Exception as e:
        return '{"operation": "most_frequent", "column": "winner"}'