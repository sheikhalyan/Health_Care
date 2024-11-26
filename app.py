from flask import Flask, render_template, request, jsonify, url_for
from flask_socketio import SocketIO, emit
import os
from dotenv import load_dotenv
import openai
import json
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
socketio = SocketIO(app, cors_allowed_origins="*")

openai.api_key = os.getenv('OPENAI_API_KEY')

SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'pt': 'Portuguese',
    'ru': 'Russian'
}

def get_medical_translation(text, source_lang, target_lang):
    try:
        system_prompt = f"""You are a highly skilled medical translator with expertise in both {SUPPORTED_LANGUAGES[source_lang]} 
        and {SUPPORTED_LANGUAGES[target_lang]} medical terminology. Translate the following text while:
        1. Maintaining medical accuracy
        2. Preserving technical terms
        3. Ensuring cultural appropriateness
        4. Keeping the same level of formality"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.3  # Lower temperature for more consistent translations
        )
        
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Translation error: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html', languages=SUPPORTED_LANGUAGES)

@socketio.on('translate_text')
def handle_translation(data):
    try:
        text = data['text']
        source_lang = data['source_lang']
        target_lang = data['target_lang']

        if not text.strip():
            raise ValueError("Empty text provided")

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

if __name__ == '__main__':
    socketio.run(app, debug=True)