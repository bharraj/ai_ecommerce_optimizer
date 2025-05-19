import json
import logging
from flask import Flask, request, jsonify
from config import FLASK_HOST, FLASK_PORT, N8N_WEBHOOK_URL, N8N_AUTH
from services.webhook_client import forward_to_n8n
from services.ml_service import predict_item

# Configure logging to STDOUT
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def healthcheck():
    return 'OK', 204

@app.route('/submit-item', methods=['POST'])
def submit_item():
    # 1) Capture raw request body
    raw = request.get_data(as_text=True)
    app.logger.info(f">>> Raw body received: {raw!r}")

    # 2) Try normal Flask JSON parsing
    try:
        data = request.get_json(force=True)
    except Exception as e:
        app.logger.warning(f"get_json failed: {e}. Trying fallback parse…")
        # 3) Fallback: strip one layer of wrapping quotes, if present
        stripped = raw.strip()
        if stripped.startswith(("'", '"')) and stripped.endswith(("'", '"')):
            stripped = stripped[1:-1]
        try:
            data = json.loads(stripped)
        except Exception as e2:
            app.logger.error(f"Fallback JSON parse also failed: {e2}")
            return jsonify({
                "status": "error",
                "message": "Invalid JSON received",
                "raw": raw
            }), 400

    app.logger.info(f"Parsed JSON data: {data}")

    # 4) Enrich with a prediction and forward to n8n
    data['prediction'] = predict_item(data)
    status, detail = forward_to_n8n(data)

    # 5) Return appropriate HTTP code
    code = 200 if status == 'success' else 502
    return jsonify(status=status, detail=detail), code

if __name__ == '__main__':
    # Launch Flask on the configured host and port
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)