from schemas.Content import TranscriptionPhraseSchema, TranscriptionViewSchema


class Transcription:
    def __init__(self, transcripted_words: str):
        self.transcripted_words = transcripted_words
    def get_transcription(self):
        phrases = self.transcripted_words.split("\n")
        transcription_phrases = []
        for phrase in phrases:
            if phrase == "":
                continue
            line = phrase.split("--$")
            time = line[0].strip()
            original_phrase = line[1]
            translated_phrase = line[2]
            transcription_phrases.append(TranscriptionPhraseSchema(time=time, original_phrase=original_phrase, translated_phrase=translated_phrase))
        return TranscriptionViewSchema(transcripted_phrases=transcription_phrases).json()