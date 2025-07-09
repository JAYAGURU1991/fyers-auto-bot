from flask import Flask, request, jsonify
import hmac, hashlib
import os
import requests
import logging

app = Flask(__name__)

# ✅ Configure logging
logging.basicConfig(level=logging.INFO)

# 🔐 Webhook secret & Telegram config from environment variables
WEBHOOK_SECRET = os.getenv("FYERS_SECRET_ID", "jayguru123")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ✅ Health check endpoint
@app.route('/ping', methods=['GET'])
def ping():
    return "✅ Bot is live and running!"

# 📩 Main webhook endpoint to receive trade signal from Fyers
@app.route('/fyers-webhook', methods=['POST'])
def fyers_webhook():
    try:
        data = request.get_json(force=True)
        signature = request.headers.get("X-Hub-Signature-256", "")

        # 🔐 Signature verification
        if not verify_signature(data, signature):
            logging.warning("❌ Signature verification failed.")
            return jsonify({"status": "error", "message": "Invalid signature"}), 403

        logging.info(f"✅ Valid trade signal received: {data}")
        send_telegram_alert(f"📈 Fyers Trade Signal:\n{data}")

        # 🛠️ TODO: Place order to Fyers here (auto trading logic)

        return jsonify({"status": "success", "message": "Signal received"}), 200

    except Exception as e:
        logging.error(f"🔥 Exception: {e}")
        return jsonify({"status": "error", "message": "Something went wrong"}), 500

# 🔐 HMAC SHA256 Signature Verification
def verify_signature(payload, signature_header):
    try:
        expected_signature = 'sha256=' + hmac.new(
            WEBHOOK_SECRET.encode(),
            msg=str(payload).encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected_signature, signature_header)
    except Exception as e:
        logging.error(f"❌ Signature Error: {e}")
        return False

# 🚀 Telegram Alert Sender
def send_telegram_alert(message):
    try:
        if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message
            }
            requests.post(url, json=payload)
    except Exception as e:
        logging.error(f"❌ Telegram error: {e}")

# 🚀 Entry point
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
