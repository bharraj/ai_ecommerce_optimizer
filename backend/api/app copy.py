import threading
import time
import sys
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

N8N_WEBHOOK_URL = "https://bbbraj1893.app.n8n.cloud/webhook-test/3bd494e9-317b-4eb8-b697-79a607943506"
N8N_USERNAME    = "braj1893"
N8N_PASSWORD    = "1234"

@app.route("/", methods=["GET"])
def healthcheck():
    return "OK", 200

@app.route("/submit-item", methods=["POST"])
def submit_item():
    data = request.json
    resp = requests.post(
        N8N_WEBHOOK_URL,
        json=data,
        auth=(N8N_USERNAME, N8N_PASSWORD)
    )
    if resp.ok:
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "n8n error", "detail": resp.text}), 502

def run_server():
    # disable reloader to avoid double-start
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    # 1) Start Flask in background
    t = threading.Thread(target=run_server, daemon=True)
    t.start()

    # 2) Wait for it to be ready
    time.sleep(1)

    # 3) Fire the test POST
    payload = {"product": "shirt", "color": "blue"}
    r = requests.post("http://127.0.0.1:5000/submit-item", json=payload)
    print(f"POST /submit-item → {r.status_code}\nResponse body: {r.text}")

    # 4) Exit altogether
    sys.exit(0)
