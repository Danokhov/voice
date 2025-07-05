from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import io

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

@app.route("/api/transcribe", methods=["POST"])
def transcribe():
    file = request.files.get("audio")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    file_stream = io.BytesIO(file.read())

    try:
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=("audio.webm", file_stream),
            response_format="json"
        )
        return jsonify({"transcript": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
