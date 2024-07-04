from model.transcription import Transcription
from service.authentication import Authentication
from config.config import Config
from service.trans_service import TransService
from schemas.error import ErrorSchema
from schemas.Content import TranscriptionAISchema, TranscriptionViewSchema, TranscriptionPhraseSchema
from flask_openapi3 import OpenAPI, Info, Tag
from flask import jsonify, redirect

from logger import logger
from flask_cors import CORS

info = Info(title="API Transcription and Translation DubVideos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app, origins=['*'])

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
transcription_tag = Tag(name="Transcrição", description="Transcrição automatizada de áudios")
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

#gs://b_dub_videos/audio_original_video_mono_MVPDubVideos-Desenvolvimentofu.wav
@app.post('/transcription_gen_ai', tags=[transcription_tag],
          responses={"200": TranscriptionViewSchema, "400": ErrorSchema})
async def transcribe_audio_AI(form: TranscriptionAISchema):
    """ realiza transcrição e tradução do audio passado pela uri no GCP

    Retorna uma representação dos dados referente à transcrição e tradução
    """
    
    #logger.debug(f"Realizando transcrição do audio com a uri: '{form.uri}'")
    print(f"Realizando transcrição do audio com a uri: '{form.uri}'")
    try:
        print("autenticando")
        auth = Authentication(Config.credential_key, Config.bucket_name)
        print("passando dados para serviço")
        trans_service = TransService(auth, form.uri, form.audio_language, form.translation_language)
        print("chamando serviço de transcrição")
        transcripted_words = trans_service.transcribe_with_gemini()
        transcription = Transcription(transcripted_words)
        print("Iniciando retorno de uma transcrição")
        print(transcription.get_transcription())
        return transcription.get_transcription()
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível transcrever o audio ({form.uri}):\n{e}"
        logger.warning(f"Erro ao transcrever audio. {error_msg}")
        return {"message": error_msg}, 400
