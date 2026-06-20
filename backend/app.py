from flask import Flask, request, jsonify
from flask_cors import CORS
from deepface import DeepFace
from dotenv import load_dotenv
from groq import Groq
import base64
import numpy as np
import cv2
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_api_key)


def get_emoji_from_groq(emotion):
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You return only one emoji. No words, no explanation."
                },
                {
                    "role": "user",
                    "content": f"Choose one emoji that best represents this facial emotion: {emotion}"
                }
            ],
            temperature=0.7,
            max_tokens=5
        )

        emoji = response.choices[0].message.content.strip()
        return emoji

    except Exception as e:
        print("Groq error:", e)

        fallback_emojis = {
            "happy": "😊",
            "sad": "😢",
            "angry": "😡",
            "surprise": "😲",
            "fear": "😨",
            "neutral": "😐",
            "disgust": "🤢",
            "contempt": "😏"
        }

        return fallback_emojis.get(emotion, "🙂")


@app.route("/")
def home():
    return jsonify({"message": "Emotion backend is running"})


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()

        if not data or "image" not in data:
            return jsonify({"error": "No image provided"}), 400

        image_data = data["image"]

        if "," in image_data:
            image_data = image_data.split(",")[1]

        img_data = base64.b64decode(image_data)
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"error": "Invalid image"}), 400

        result = DeepFace.analyze(
            img,
            actions=["emotion"],
            enforce_detection=False
        )

        if isinstance(result, list):
            emotion = result[0]["dominant_emotion"]
        else:
            emotion = result["dominant_emotion"]

        emoji = get_emoji_from_groq(emotion)

        return jsonify({
            "emotion": emotion,
            "emoji": emoji
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)