class SpeechHandler {
    constructor(translationService) {
        this.translationService = translationService;
        this.recognition = null;
        this.isRecording = false;
        this.setupSpeechRecognition();
    }

    setupSpeechRecognition() {
        if ('webkitSpeechRecognition' in window) {
            this.recognition = new webkitSpeechRecognition();
            this.recognition.continuous = true;
            this.recognition.interimResults = true;
            this.setupRecognitionHandlers();
        } else {
            document.getElementById('startRecording').disabled = true;
            this.translationService.showError('Speech recognition is not supported in your browser');
        }
    }

    setupRecognitionHandlers() {
        this.recognition.onresult = (event) => {
            const transcript = Array.from(event.results)
                .map(result => result[0].transcript)
                .join('');
            
            document.getElementById('originalText').innerHTML = 
                this.translationService.formatText(transcript);
            
            if (event.results[event.results.length - 1].isFinal) {
                this.translationService.translate(
                    transcript,
                    document.getElementById('sourceLang').value,
                    document.getElementById('targetLang').value
                );
            }
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.translationService.showError(`Speech recognition error: ${event.error}`);
            this.stopRecording();
        };
    }

    startRecording() {
        if (!this.isRecording) {
            this.recognition.start();
            this.isRecording = true;
            document.getElementById('startRecording').disabled = true;
            document.getElementById('stopRecording').disabled = false;
            document.getElementById('recordingIndicator').classList.remove('hidden');
        }
    }

    stopRecording() {
        if (this.isRecording) {
            this.recognition.stop();
            this.isRecording = false;
            document.getElementById('startRecording').disabled = false;
            document.getElementById('stopRecording').disabled = true;
            document.getElementById('recordingIndicator').classList.add('hidden');
        }
    }

    speakTranslation() {
        const text = document.getElementById('translatedText').textContent;
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = document.getElementById('targetLang').value;
        window.speechSynthesis.speak(utterance);
    }
}