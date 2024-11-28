class TranslationService {
    constructor() {
        // Initialize the WebSocket connection using Socket.IO
        this.socket = io();

        // Set up event listeners for WebSocket messages
        this.setupSocketListeners();
    }

    // Set up listeners for WebSocket responses
    setupSocketListeners() {
        // Handle successful translation response from the server
        this.socket.on('translation_response', (data) => {
            // Update the translated text in the UI
            document.getElementById('translatedText').innerHTML = this.formatText(data.translated_text);

            // Hide the loading spinner
            document.getElementById('translationLoader').classList.add('hidden');

            // Enable the "Speak Translation" button
            document.getElementById('speakTranslation').disabled = false;
        });

        // Handle translation error response from the server
        this.socket.on('translation_error', (data) => {
            // Display the error message to the user
            this.showError(`Translation error: ${data.error}`);

            // Hide the loading spinner
            document.getElementById('translationLoader').classList.add('hidden');
        });
    }

    // Send translation request to the server
    translate(text, sourceLang, targetLang) {
        // Show the loading spinner while waiting for the response
        document.getElementById('translationLoader').classList.remove('hidden');

        // Disable the "Speak Translation" button to prevent user actions during processing
        document.getElementById('speakTranslation').disabled = true;

        // Emit a WebSocket event with the text and language preferences
        this.socket.emit('translate_text', {
            text,              // Text to translate
            source_lang: sourceLang, // Source language code
            target_lang: targetLang  // Target language code
        });
    }

    // Format the translated text for display
    formatText(text) {
        // Split the text into lines and wrap each line in a styled <p> tag
        return text.split('\n').map(line => `<p class="mb-2">${line}</p>`).join('');
    }

    // Display an error message to the user
    showError(message) {
        const errorDiv = document.getElementById('errorMessage');

        // Set the error message and make the error div visible
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');

        // Automatically hide the error message after 5 seconds
        setTimeout(() => {
            errorDiv.classList.add('hidden');
        }, 5000);
    }
}
