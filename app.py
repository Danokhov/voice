from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    file = request.files.get('audio')
    if not file:
        return jsonify({'error': 'No audio file'}), 400

    filename = secure_filename(file.filename)
    file_bytes = file.read()

    try:
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=(filename, file_bytes)
        )
        return jsonify({'transcript': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)



