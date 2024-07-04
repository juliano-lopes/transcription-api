
from service.authentication import Authentication
from service.genai import GenAi

class TransService:
    def __init__(self, auth: Authentication, gcs_uri: str, audio_language: str, translation_language: str):
        self.auth = auth
        self.gcs_uri = gcs_uri
        self.audio_language = audio_language
        self.translation_language = translation_language

    def transcribe_with_gemini(self):
        genai = GenAi()
        file_name = self.gcs_uri
        file_name = file_name.split("/").pop()
        
        blob = self.auth.get_bucket().blob(file_name)
        print(f"chamando GenAi com blob do arquivo {file_name}")
        
        return genai.transcribe(blob, self.audio_language, self.translation_language)
