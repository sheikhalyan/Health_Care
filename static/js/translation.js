class TranslationService {
    constructor() {
        this.socket = io();
        this.setupSocketListeners();
    }

    setupSocketListeners() {
        this.socket.on('translation_response', (data) => {
            document.getElementById('translatedText').innerHTML = this.formatText(data.translated_text);
            document.getElementById('translationLoader').classList.add('hidden');
            document.getElementById('speakTranslation').disabled = false;
        });

        this.socket.on('translation_error', (data) => {
            this.showError(`Translation error: ${data.error}`);
            document.getElementById('translationLoader').classList.add('hidden');
        });
    }

    translate(text, sourceLang, targetLang) {
        document.getElementById('translationLoader').classList.remove('hidden');
        document.getElementById('speakTranslation').disabled = true;
        
        this.socket.emit('translate_text', {
            text,
            source_lang: sourceLang,
            target_lang: targetLang
        });
    }

    formatText(text) {
        return text.split('\n').map(line => `<p class="mb-2">${line}</p>`).join('');
    }

    showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
        setTimeout(() => {
            errorDiv.classList.add('hidden');
        }, 5000);
    }
}