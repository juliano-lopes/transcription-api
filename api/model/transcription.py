import json
from schemas.Content import TranscriptionPhraseSchema, TranscriptionViewSchema


class Transcription:
    def __init__(self, transcripted_words: str):
        self.transcripted_words = transcripted_words
    def get_transcription(self):
        phrases =json.loads(self.transcripted_words)
        return TranscriptionViewSchema(transcripted_phrases=phrases).json()