from flask import Flask, render_template, request, jsonify
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
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        return translation.text
    except Exception as e:
        raise Exception(f"Translation error: {str(e)}")

# Home page route
@app.route('/')
def index():
    return render_template('index.html', languages=SUPPORTED_LANGUAGES)

# Translation API route (POST request)
@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.json
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang')
        target_lang = data.get('target_lang')

        if not text:
            return jsonify({'error': 'Empty text provided'}), 400

        translation = get_medical_translation(text, source_lang, target_lang)

        return jsonify({
            'original_text': text,
            'translated_text': translation,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
