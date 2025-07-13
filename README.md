# 💬 Efraín Granados Resume Chatbot API

This is a lightweight Django-based API that connects to a conversational AI assistant trained on the resume of **Efraín Granados**. It uses **Gemini 1.5 Flash** to answer questions related to his professional background, experience, and technical skills.

---

## 🧠 What does this project do?

- ✅ Reads and parses a PDF resume file
- ✅ Uses Google’s Gemini API to generate context-aware, natural responses
- ✅ Exposes endpoints to ask questions and reset the conversation
- ✅ Maintains basic session-based context
- ✅ Designed to act as a smart, interactive portfolio

---

## 📁 Project Structure

```
api/
├── chatbot/
│   ├── views.py          # Handles AI prompt + PDF extraction
│   ├── urls.py           # /ask and /reset endpoints
│   └── data/             # Resume PDF stored here
├── api/
│   ├── settings.py       # Core Django settings
│   └── urls.py           # Root URL routing
├── .env                  # API keys and secrets (not committed)
└── manage.py
```

---

## 🔐 Environment Variables

All sensitive data is stored in a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
DJANGO_SECRET_KEY=your_django_secret_key_here
```

Load the environment with `python-dotenv`.

---

## 📡 API Endpoints

| Method | Endpoint          | Description                          |
| ------ | ----------------- | ------------------------------------ |
| POST   | `/chatbot/ask/`   | Sends a question and gets a response |
| POST   | `/chatbot/reset/` | Resets the session/chat history      |

Example request to `/chatbot/ask/`:

```json
{
  "question": "What technologies has Efraín worked with?"
}
```

---

## ⚙️ Setup & Run

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/help-bot-api.git
   cd help-bot-api
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up `.env` and run the server:
   ```bash
   python manage.py runserver
   ```

---

## 🚫 Best Practices

- ✅ Never commit your `.env` file – it's already listed in `.gitignore`
- ✅ Keep your API keys and `SECRET_KEY` out of `settings.py`
- ✅ Set `DEBUG = False` for production
- ✅ Set `ALLOWED_HOSTS` with your domain/IP in production

---

## 📄 License

MIT License – feel free to use, modify, and share.

---
