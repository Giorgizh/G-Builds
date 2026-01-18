from ext import app
from flask import request, jsonify
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/ai/chat")
def ai_chat():
    data = request.get_json(silent=True) or {}
    user_msg = data.get("message", "").strip()

    if not user_msg:
        return jsonify({"reply": "Please type a message."})

    try:
        resp = client.responses.create(
            model="gpt-4.1-mini",
            input=user_msg
        )
        return jsonify({"reply": resp.output_text})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    import routes   
    app.run(debug=True, port=5001)
