from flask import Flask, request, jsonify
import hmac, hashlib
import os

app = Flask(__name__)

WEBHOOK_SECRET = os.environ.get("FYERS_SECRET_ID", "jayguru123")

@app.route('/fyers-webhook', methods=['POST'])
def fyers_webhook():
    data = request.json
    signature = request.headers.get('X-Hub-Signature-256', '')
    if not verify_signature(data, signature):
        return jsonify({"status": "error", "message": "Invalid signature"}), 403
    print("✅ Received Trade Signal:", data)
    return jsonify({"status": "success"}), 200

@app.route('/ping', methods=['GET'])
def ping():
    return "Bot Running ✅"

def verify_signature(payload, signature_header):
    expected_signature = 'sha256=' + hmac.new(
        WEBHOOK_SECRET.encode(),
        msg=str(payload).encode(),
        digestmod=hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)

# Note: No app.run() — gunicorn will start the server in production
