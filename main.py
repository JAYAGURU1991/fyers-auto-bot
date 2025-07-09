from flask import Flask, request, jsonify
import hmac, hashlib

app = Flask(__name__)

WEBHOOK_SECRET = "jayguru123"

@app.route('/fyers-webhook', methods=['POST'])
def fyers_webhook():
    data = request.json
    signature = request.headers.get('X-Hub-Signature-256', '')
    if not verify_signature(data, signature):
        return jsonify({"status": "error", "message": "Invalid signature"}), 403
    print("Received Trade Signal:", data)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
