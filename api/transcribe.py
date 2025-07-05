from openai import OpenAI
from dotenv import load_dotenv
import os
import io

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def handler(request):
    if request.method != "POST":
        return {"statusCode": 405, "body": "Method Not Allowed"}

    content_type = request.headers.get("content-type", "")
    if "multipart/form-data" not in content_type:
        return {"statusCode": 400, "body": "Expected multipart/form-data"}

    form = request.files
    file = form.get("audio")
    if not file:
        return {"statusCode": 400, "body": "No audio provided"}

    file_stream = io.BytesIO(file.read())

    try:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=("speech.webm", file_stream)
        )
        return {
            "statusCode": 200,
            "body": {"transcript": transcript.text}
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": {"error": str(e)}
        }
