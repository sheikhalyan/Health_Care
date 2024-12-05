from flask import Flask, render_template, request, jsonify, url_for
from flask_socketio import SocketIO, emit
import os
from dotenv import load_dotenv
from googletrans import Translator
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure secret key for Flask sessions (fallback to default if not in .env)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

# Initialize Flask-SocketIO for real-time communication
socketio = SocketIO(app, cors_allowed_origins="*")   # "*" => Allows WebSocket connections from any origin

# Dictionary for supported languages
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

# Initialize the Google Translate API
translator = Translator()

# Function to perform translations using Google Translate
def get_medical_translation(text, source_lang, target_lang):
    try:
        # Perform translation using Google Translate
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        return translation.text
    except Exception as e:
        raise Exception(f"Translation error: {str(e)}")

# Flask route for the home page
@app.route('/')
def index():
    return render_template('index.html', languages=SUPPORTED_LANGUAGES)

# WebSocket event handler for real-time translations
@socketio.on('translate_text')
def handle_translation(data):
    try:
        # Extract data from the incoming request
        text = data['text']
        source_lang = data['source_lang']
        target_lang = data['target_lang']

        # Validate input text
        if not text.strip():
            raise ValueError("Empty text provided")

        # Perform translation
        translation = get_medical_translation(text, source_lang, target_lang)

        emit('translation_response', {
            'original_text': text,
            'translated_text': translation,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        # Emit an error message back to the client
        emit('translation_error', {'error': str(e)})

# Main entry point for the application
if __name__ == '__main__':
    socketio.run(app, debug=True)  # Run the app with SocketIO support in debug mode
