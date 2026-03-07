from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# 模拟的多模型
MODELS = {
    "gpt": {"name": "GPT-4", "color": "#10a37f"},
    "claude": {"name": "Claude", "color": "#d97757"},
    "gemini": {"name": "Gemini", "color": "#8e44ad"},
    "llama": {"name": "Llama", "color": "#e74c3c"}
}

@app.route('/')
def index():
    return render_template('index.html', models=MODELS)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    model = data.get('model', 'gpt')
    message = data.get('message', '')
    
    # 模拟回复
    responses = {
        "gpt": "🤖 [GPT-4] 这是一个示例回复。我理解你的问题是关于: " + message[:50] + "...",
        "claude": "🧠 [Claude] 我理解你的需求。让我分析一下: " + message[:50] + "...",
        "gemini": "✨ [Gemini] 这是一个很有趣的问题！让我来解答: " + message[:50] + "...",
        "llama": "🦙 [Llama] 你好！让我用开源的方式回答: " + message[:50] + "..."
    }
    
    return jsonify({
        "response": responses.get(model, responses["gpt"]),
        "model": model,
        "model_name": MODELS.get(model, {}).get("name", "Unknown")
    })

@app.route('/api/models')
def models():
    return jsonify(MODELS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
