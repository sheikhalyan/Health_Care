from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import os
from dotenv import load_dotenv
from googletrans import Translator
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

# Initialize SocketIO for real-time communication
socketio = SocketIO(app, cors_allowed_origins="*")  # "*" allows any origin

# Supported languages
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'zh-cn': 'Chinese',
    'ja': 'Japanese',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'pt': 'Portuguese',
    'ru': 'Russian'
}

# Initialize Google Translate
translator = Translator()

# Function to translate text
def get_medical_translation(text, source_lang, target_lang):
    try:
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        return translation.text
    except Exception as e:
        raise Exception(f"Translation error: {str(e)}")

# Home page route
@app.route('/')
def index():
    return render_template('index.html', languages=SUPPORTED_LANGUAGES)

# WebSocket event for real-time translation
@socketio.on('translate_text')
def handle_translation(data):
    try:
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang')
        target_lang = data.get('target_lang')

        if not text:
            emit('translation_error', {'error': 'Empty text provided'})
            return

        translation = get_medical_translation(text, source_lang, target_lang)

        emit('translation_response', {
            'original_text': text,
            'translated_text': translation,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        emit('translation_error', {'error': str(e)})

# Run locally
if __name__ == '__main__':
    # Use socketio.run() for WebSocket support
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
