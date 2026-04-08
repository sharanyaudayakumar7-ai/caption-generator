# ⚡ AI Caption Generator

An AI-powered web application that generates Instagram-style captions from images using multimodal AI.

---

## 🌐 Live Demo
👉 (Add your Render link here after deployment)

---

## ✨ Features

- 📸 Upload any image
- 🤖 AI generates captions based on image content
- 🎨 Modern dark UI with subtle glow design
- 📋 One-click copy caption
- ☁️ Image hosting using ImgBB
- 🔐 Secure API key handling using environment variables

---

## 🧠 How It Works

1. User uploads an image  
2. Image is uploaded to ImgBB → returns public URL  
3. URL is sent to OpenRouter AI  
4. AI analyzes image and generates caption  
5. Caption is displayed on UI  

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS  
- **Backend:** Python (Flask)  
- **APIs Used:**
  - OpenRouter (AI caption generation)
  - ImgBB (image hosting)

---
## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
OPENROUTER_API_KEY=your_api_key_here
IMGBB_API_KEY=your_api_key_here

## 📦 Installation (Run Locally)

```bash
git clone https://github.com/your-username/caption-generator.git
cd caption-generator
pip install -r requirements.txt
