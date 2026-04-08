from flask import Flask, render_template, request
import os
import base64
import requests
from dotenv import load_dotenv

# 🔐 load env variables
load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 🔑 get keys safely
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# 📸 upload image → get URL
def upload_to_imgbb(image_path):
    with open(image_path, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": IMGBB_API_KEY,
            "image": base64.b64encode(file.read())
        }
        res = requests.post(url, data=payload)
        return res.json()["data"]["url"]

@app.route("/", methods=["GET", "POST"])
def home():
    caption = ""
    image_path = ""

    if request.method == "POST":
        file = request.files["image"]

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            image_path = filepath

            try:
                # 🔥 Step 1: upload image → get URL
                image_url = upload_to_imgbb(filepath)

                # 🤖 Step 2: send to OpenRouter
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "openai/gpt-4o-mini",
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Generate a short Instagram caption"},
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": image_url}
                                    }
                                ]
                            }
                        ]
                    }
                )

                caption = response.json()["choices"][0]["message"]["content"]

            except Exception as e:
                print(e)
                caption = "✨ Something went wrong, try again!"

    return render_template("index.html", caption=caption, image_path=image_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)