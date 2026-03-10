from flask import Flask, render_template, request, jsonify, g
import os
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Request ID middleware
@app.before_request
def before_request():
    g.request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{g.request_id}] {request.method} {request.path}")

@app.after_request
def after_request(response):
    logger.info(f"[{g.request_id}] Status: {response.status_code}")
    response.headers['X-Request-ID'] = g.request_id
    return response

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'request_id': g.request_id}), 200

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not Found', 'message': 'Resource not found'}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"500 Internal Error: {e}")
    return jsonify({'error': 'Internal Server Error', 'message': 'Something went wrong'}), 500

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
