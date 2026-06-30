# 🩺🌐 Health Care Translation Web App

### Real-time speech-to-text medical translation, powered by AI

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Socket.IO](https://img.shields.io/badge/Socket.IO-Real--time-010101?style=flat-square&logo=socketdotio&logoColor=white)](https://socket.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--turbo-412991?style=flat-square&logo=openai&logoColor=white)](https://platform.openai.com)

> A real-time translation web app built for healthcare communication, combining speech recognition, AI-powered translation, and text-to-speech to bridge language barriers between patients and medical staff.

---

## What It Does

- **Speech-to-text** — captures spoken input directly from the browser microphone
- **Real-time translation** — translates text via WebSocket communication with low latency
- **Text-to-speech** — converts the translated text back into spoken audio
- **Medical-context aware translation** — preserves medical terminology accuracy, cultural appropriateness, and formality (not just literal translation)
- **Multi-language support** — source and target language selection via dropdowns

---

## Branches & Translation Engines

This project explores two different translation backends, implemented on separate branches:

| Branch | Translation Engine | Notes |
|--------|---------------------|-------|
| `main` | **OpenAI API** (`gpt-3.5-turbo`) | Context-aware medical translation — understands terminology, tone, and cultural nuance. Requires a paid OpenAI subscription for unrestricted use. |
| *(secondary branch)* | **Google Translate API** | Faster, free-tier friendly, but lacks the medical-context awareness of the LLM-based approach |

> The OpenAI-powered branch represents the more advanced implementation — it doesn't just translate words, it adapts medical terminology and tone appropriately for clinical communication.

---

## How It Works

```
User speaks into microphone
        ↓
webkitSpeechRecognition converts speech → text
        ↓
Text + language codes sent via WebSocket (translate_text event)
        ↓
Flask backend receives request → calls OpenAI GPT-3.5-turbo
        ↓
AI translates with medical accuracy + cultural appropriateness
        ↓
translation_response event sent back to client
        ↓
Translated text displayed + converted to speech (SpeechSynthesisUtterance)
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Flask (Python) |
| **Real-time communication** | Flask-SocketIO |
| **Translation Engine (main)** | OpenAI API — `gpt-3.5-turbo` |
| **Translation Engine (alt branch)** | Google Translate API |
| **Speech-to-Text** | webkitSpeechRecognition (Web Speech API) |
| **Text-to-Speech** | SpeechSynthesisUtterance (Web Speech API) |
| **Frontend** | HTML, CSS, JavaScript |
| **Environment Config** | python-dotenv |
| **Deployment** | Vercel |

---

## Project Structure

```
healthcare-translation-app/
│
├── app.py                  # Flask + Socket.IO backend, OpenAI integration
├── requirements.txt        # Python dependencies
├── .env                    # API keys (OPENAI_API_KEY, SECRET_KEY) — gitignored
├── vercel.json              # Vercel deployment configuration
│
├── static/
│   ├── js/
│   │   ├── translation.js  # WebSocket translation requests + UI state handling
│   │   └── speech.js       # Speech-to-text & text-to-speech logic
│   └── css/
│       └── style.css       # UI styling
│
└── templates/
    └── index.html           # Main UI: language selectors, record/translate/speak buttons
```

---

## Core Components

**Backend — `app.py`**
- Initializes Flask, Socket.IO, and environment variables
- Calls OpenAI's `gpt-3.5-turbo` for medically accurate, context-aware translation
- Serves the front-end via `/` route
- Handles real-time translation requests through the `translate_text` WebSocket event
- CORS configured to prevent unauthorized cross-origin requests

**`translation.js`**
- Sends translation requests over WebSocket
- Listens for `translation_response` and `translation_error` events
- Formats translated text and manages UI state (loading spinners, error messages)

**`speech.js`**
- Captures spoken input via `webkitSpeechRecognition`
- Converts translated text to speech via `SpeechSynthesisUtterance`

---

## Security Considerations

- API keys stored securely via `.env`, excluded from version control via `.gitignore`
- CORS configured for Socket.IO to prevent unauthorized cross-origin communication
- Backend input validation (e.g. rejecting empty text) to prevent abuse
- Graceful error handling for translation/connection failures
- ⚠️ Rate limiting recommended as a future improvement to protect the OpenAI API from excessive requests

---

## Getting Started

### Prerequisites
- Python 3.x
- An OpenAI API key (paid subscription recommended — the free trial tier is rate-limited and not suitable for consistent use)

### Setup

1. Clone the repository
   ```bash
   git clone https://github.com/sheikhalyan/healthcare-translation-app.git
   cd healthcare-translation-app
   ```

2. Create a virtual environment and install dependencies
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   SECRET_KEY=your_flask_secret_key_here
   ```

4. Run the app
   ```bash
   python app.py
   ```

5. Open `http://localhost:5000` in your browser

---

## Switching Translation Engines

To try the Google Translate API implementation instead of OpenAI:

```bash
git checkout <google-translate-branch-name>
```

This branch swaps the OpenAI translation call for the Google Translate API — useful for comparing cost, latency, and translation quality between an LLM-based approach and a traditional translation API.

---

## ⚠️ Disclaimer

This is a **prototype** built for demonstration and learning purposes. It is not a certified medical communication tool and should not be relied upon for critical clinical interactions without further validation and professional medical review.

---

## Author

**Sheikh Alyan** — Full-Stack Developer

[![GitHub](https://img.shields.io/badge/GitHub-@sheikhalyan-181717?style=flat-square&logo=github)](https://github.com/sheikhalyan)
