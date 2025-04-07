import os
import signal
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from vision_wrapper import analyze_image_with_openai

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
            <p>This is your Flask app running on Render. You’re golden. 💛</p>
        </body>
    </html>
    """

# Visual triage image analysis route
@app.route("/analyzeImage", methods=["POST"])
def analyze_image():
    data = request.get_json()
    image_url = data.get("image")

    if not image_url:
        return jsonify({"error": "Missing 'image' in request body."}), 400

    result = analyze_image_with_openai(image_url)
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

    port = int(os.environ.get("PORT", 5000))  # Use PORT from Render, fallback to 5000 for local
    app.run(
        host="0.0.0.0",
        port=port,
        debug=(ENVIRONMENT == "development")
    )
