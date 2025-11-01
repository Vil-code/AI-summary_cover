# 📚 AI Book Assistant

Site: https://ai-summary-cover.vercel.app/ (it can take up to a minute for the server to start working due to free tier)

An interactive web app that lets you **search books**, **summarize their descriptions using AI**, and **generate illustrated book covers** via Hugging Face models.  
Built with **React + TypeScript (Vite)** for the frontend and **Flask (Python)** for the backend.

---

## 🚀 Features

- 🔍 Search for books via Open Library API  
- 🧠 Summarize book descriptions using a Hugging Face text model  
- 🎨 Generate custom book cover images using a Hugging Face diffusion model  
- ✨ Clean comic-style UI with pastel cards and sticky AI panels  
- 🆓 Fully deployable on **Render (backend)** + **Vercel (frontend)** free tiers

---

## 🛠️ Tech Stack

| Part | Technology |
|------|-------------|
| Frontend | React + TypeScript + Vite |
| Backend | Flask + Python |
| AI APIs | Hugging Face Inference API |
| Styling | Custom CSS |
| Deployment | Vercel (frontend), Render (backend) |

---

## 🧩 Project Structure

```
AI-summary-cover/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Procfile
│   └── providers.py, summarizer.py
└── frontend/
    ├── src/
    ├── vite.config.ts
    ├── package.json
    ├── tsconfig.json
    ├── public/
    └── dist/
```


## 🧾 License

MIT License © 2025 – Vilhelmi Rintanen  
For learning and portfolio use only.
