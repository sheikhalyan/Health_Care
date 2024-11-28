class SpeechHandler {
    constructor(translationService) {
        // Store the translation service instance for use in translation functions
        this.translationService = translationService;

        // Initialize properties for speech recognition and recording state
        this.recognition = null;
        this.isRecording = false;

        // Set up speech recognition functionality
        this.setupSpeechRecognition();
    }

    // Initialize speech recognition
    setupSpeechRecognition() {
        if ('webkitSpeechRecognition' in window) {
            // Check if the browser supports webkitSpeechRecognition
            this.recognition = new webkitSpeechRecognition();

            // Enable continuous recognition for long speech input
            this.recognition.continuous = true;

            // Allow processing of interim results for real-time display
            this.recognition.interimResults = true;

            // Set up event handlers for recognition events
            this.setupRecognitionHandlers();
        } else {
            // Disable recording button if speech recognition isn't supported
            document.getElementById('startRecording').disabled = true;

            // Show an error message to the user
            this.translationService.showError('Speech recognition is not supported in your browser');
        }
    }

    // Set up handlers for recognition events
    setupRecognitionHandlers() {
        this.recognition.onresult = (event) => {
            // Process the recognition result and build a transcript
            const transcript = Array.from(event.results)
                .map(result => result[0].transcript) // Extract transcript from each result
                .join('');

            // Display the interim or final text on the page
            document.getElementById('originalText').innerHTML =
                this.translationService.formatText(transcript);

            // If the current result is final, trigger the translation
            if (event.results[event.results.length - 1].isFinal) {
                this.translationService.translate(
                    transcript, // Text to translate
                    document.getElementById('sourceLang').value, // Source language
                    document.getElementById('targetLang').value // Target language
                );
            }
        };

        this.recognition.onerror = (event) => {
            // Log and display recognition errors
            console.error('Speech recognition error:', event.error);
            this.translationService.showError(`Speech recognition error: ${event.error}`);

            // Stop recording in case of an error
            this.stopRecording();
        };
    }

    // Start recording and enable the recording indicator
    startRecording() {
        if (!this.isRecording) {
            this.recognition.start(); // Start speech recognition
            this.isRecording = true; // Update the recording state

            // Update UI to reflect recording state
            document.getElementById('startRecording').disabled = true;
            document.getElementById('stopRecording').disabled = false;
            document.getElementById('recordingIndicator').classList.remove('hidden');
        }
    }

    // Stop recording and reset the UI
    stopRecording() {
        if (this.isRecording) {
            this.recognition.stop(); // Stop speech recognition
            this.isRecording = false; // Update the recording state

            // Update UI to reflect stopped recording state
            document.getElementById('startRecording').disabled = false;
            document.getElementById('stopRecording').disabled = true;
            document.getElementById('recordingIndicator').classList.add('hidden');
        }
    }

    // Speak out the translated text using speech synthesis
    speakTranslation() {
        // Get the translated text from the UI
        const text = document.getElementById('translatedText').textContent;

        // Create a speech synthesis utterance
        const utterance = new SpeechSynthesisUtterance(text);

        // Set the language of the utterance to match the target language
        utterance.lang = document.getElementById('targetLang').value;

        // Speak the text using the browser's speech synthesis engine
        window.speechSynthesis.speak(utterance);
    }
}
