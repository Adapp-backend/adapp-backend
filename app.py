import os
import signal
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Print current environment mode
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
print(f"Starting Adapp in {ENVIRONMENT} mode...")

# Health check or root route
@app.route("/")
def home():
    return """
    <html>
        <head><title>Adapp</title></head>
        <body style='font-family:sans-serif;padding:40px;'>
            <h1>✅ Adapp backend is live!</h1>
            <p>This is your Flask app running on Replit. You’re golden. 💛</p>
        </body>
    </html>
    """

from flask import request, jsonify
from vision_wrapper import analyze_image_with_openai

@app.route("/analyzeImage", methods=["POST"])
def analyze_image():
    data = request.get_json()
    base64_image = data.get("image")

    if not base64_image:
        return jsonify({"error": "Missing 'image' in request body."}), 400

    result = analyze_image_with_openai(base64_image)
    return jsonify({"result": result})

# Graceful shutdown function
def shutdown_server(signal_received, frame):
    print("🛑 Shutdown signal received. Stopping server...")
    exit(0)

# Main entry point
if __name__ == "__main__":
    # Register signal handlers for clean exit
    signal.signal(signal.SIGTERM, shutdown_server)
    signal.signal(signal.SIGINT, shutdown_server)

    # Start Flask app on Replit-compatible settings
    app.run(
        host="0.0.0.0",
        port=3000,
        debug=(ENVIRONMENT == "development")
    )
