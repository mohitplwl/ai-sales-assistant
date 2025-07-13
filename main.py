from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

# Add your OpenAI key here
openai.api_key = "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"

@app.route('/rewrite', methods=['POST'])
def rewrite_message():
    data = request.get_json()
    message = data.get('message')
    context = data.get('context', '')

    prompt = f"""You are a sales and customer service communication expert.
Your task is to rewrite the following message in 5 different tones:
1. Persuasive
2. Empathetic
3. Confident
4. Friendly
5. Formal

Message: "{message}"
Context: "{context}"

Provide the rewritten message for each tone in a clearly labeled format."""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in sales messaging and tonality."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=600
    )

    # Basic parser to split GPT response into tones (assumes it follows numbered output)
    raw_output = response['choices'][0]['message']['content']
    versions = []
    for line in raw_output.strip().split('\n\n'):
        if line.strip():
            parts = line.strip().split("\n", 1)
            if len(parts) == 2:
                tone = parts[0].replace(":", "").strip()
                text = parts[1].strip()
                versions.append({"tone": tone, "text": text})
    
    return jsonify({"versions": versions})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)