from flask import Flask, render_template, request
import os
import base64
import requests

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# create folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 🔥 ImgBB Upload Function
def upload_to_imgbb(image_path):
    with open(image_path, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": "46d0d67e98196d8f7e360123776d7c00",
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
                # 🔥 Step 1: Upload to ImgBB → get URL
                image_url = upload_to_imgbb(filepath)

                # 🔥 Step 2: Send to OpenRouter
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": "Bearer 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",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "openai/gpt-4o-mini",
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Generate a short, catchy Instagram caption for this image"},
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
                caption = "✨ Living the moment 😎"

    return render_template("index.html", caption=caption, image_path=image_path)

if __name__ == "__main__":
  if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)