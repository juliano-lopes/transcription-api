"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
import base64
import google.generativeai as genai
class GenAi:
  def __init__(self):
    # Create the model
    # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
    self.generation_config = {
      "temperature": 0,
      "top_p": 0.95,
      "top_k": 64,
      "max_output_tokens": 8192,
      "response_mime_type": "text/plain",
    }
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

  def upload_to_gemini(self, path, mime_type=None):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

  def transcribe(self, blob, audio_language, translation_language):
    
    model = genai.GenerativeModel(
      model_name="gemini-1.5-flash",
      generation_config=self.generation_config,
      # safety_settings = Adjust safety settings
      # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    # TODO Make these files available on the local file system
    # You may need to update the file paths
    files = [
      #self.upload_to_gemini(file, mime_type="audio/wav"),
    ]
    #signed_url = blob.generate_signed_url(3600)
    #data = blob.download_as_string()
    name = blob.name
    name = f"{name.split("/").pop()}.wav"
    print("o nome foi ", name)
    print(blob)
    with open(name, "wb") as f:
      blob.download_to_file(f)
      file = self.upload_to_gemini(name, mime_type="audio/wav")
    #print(f"url assinada: {signed_url}")
    """chat_session = model.start_chat(
      history=[
        {
          "role": "user",
          "parts": [
            file,
            #{
              #"mime_type": "audio/wav",  # Specify audio format
              #"data": data,  # Use the generated signed URL for access
            #}
          ],
        },
      ]
    )"""
    
    prompt = f"""
    transcreva o audio conforme as orientações a seguir:
    1. a transcrição deve estar no idioma {audio_language}.
    2. indique no início de cada frase, o timestamp exato que cada frase começa no áudio.
    3. Considere o final de uma frase quando for encontrado o sinal de ponto '.'.
    4. Faça a tradução de cada frase para o idioma {translation_language}.
    5. Separe o timestamp, a frase em {audio_language} e frase em {translation_language} utilizando o sinal --$.
    6. Não adicione nada além do que está no áudio.
    Assim, de acordo com as orientações anteriores, dado que timestamp = t, transcrição = tc e tradução = td, cada frase deve seguir a seguinte formatação de exemplo:
    t --$ tc --$ td.\n
    """

    #response = chat_session.send_message(prompt)
    response = model.generate_content([file, prompt])
    
    #response = chat_session.send_message("transcreva o audio conforme o seguinte: a transcrição deve estar em português brasileiro. Indique no início de cada frase, o tempo exato, convertido em segundos, que cada frase começa no áudio. Considere o final de uma frase quando for encontrado o sinal de ponto '.'. Separe os segundos da frase utilizando o sinal --$,  Por exemplo: 1 --$ Agradeço pela gentileza.\n 5 --$ Meu nome é Juliano.\n")
    print("resposta: ")

    return response.text