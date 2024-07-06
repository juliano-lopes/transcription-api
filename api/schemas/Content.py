from typing import List
from pydantic import BaseModel, config, Field
import werkzeug

class TranscriptionAISchema(BaseModel):
    """ define como uma transcrição cerá recebida e traduzida
    """
    uri: str = Field("gs://resourse.wav", description="URL de um áudio armazenado na GCP")
    audio_language: str = Field("Português", description="Idioma de origem do áudio")
    translation_language: str = Field("Inglês", description="O idioma para realizar a tradução da transcrição")
    class Config:
        protected_namespaces = ()  # Empty tuple to disable protection

class TranscriptionPhraseSchema(BaseModel):
    """
    define os dados de cada frase de uma transcrição
    """
    time: str = Field("", description="Timestamp de quando a frase começa em um áudio")
    original_phrase: str = Field("", description="Frase no idioma original")
    translated_phrase: str = Field("", description="Frase traduzida")
    voice_timbre: str = Field("", description="Indica se o timbre da voz que fala a frase é m (masculino), f (feminino) ou i (indefinido).")

class TranscriptionViewSchema(BaseModel):
    """ define como uma transcrição cerá retornada
    """
    transcripted_phrases: List[TranscriptionPhraseSchema] = Field([], description="Lista de objeto TranscriptionPhraseSchema")
