"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import json
import os
import base64
import time
import google.generativeai as genai
class GenAi:
  def __init__(self):
    # Create the model
    # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
    self.generation_config = {
      "temperature": 0,
      "top_p": 0.95,
      "top_k": 64,
      #"max_output_tokens": 8192,
      "response_mime_type": "text/plain",
    }
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

  def upload_to_gemini(self, path, mime_type=None):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    file = genai.upload_file(path, mime_type=mime_type)
    #print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

  def wait_for_files_active(self, files):
    """Waits for the given files to be active.

    Some files uploaded to the Gemini API need to be processed before they can be
    used as prompt inputs. The status can be seen by querying the file's "state"
    field.

    This implementation uses a simple blocking polling loop. Production code
  should probably employ a more sophisticated approach.
  """
    print("Waiting for file processing...")
    for name in (file.name for file in files):
      file = genai.get_file(name)
      while file.state.name == "PROCESSING":
        print(".", end="", flush=True)
        time.sleep(10)
        file = genai.get_file(name)
      if file.state.name != "ACTIVE":
        raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()

  def transcribe(self, blob, audio_language, translation_language):
    
    model = genai.GenerativeModel(
      model_name="gemini-1.5-flash",
      generation_config=self.generation_config,
      # safety_settings = Adjust safety settings
      # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    #signed_url = blob.generate_signed_url(3600)
    #data = blob.download_as_string()
    name = blob.name
    name = f"{name.split("/").pop()}.wav"
    print("o nome foi ", name)
    with open(name, "wb") as f:
      blob.download_to_file(f)
      file = self.upload_to_gemini(name, mime_type="audio/wav")
      self.wait_for_files_active([file])
    json_data = '[{"time":"timestamp", "original_phrase":"...", "translated_phrase":"...", "voice_timbre":"..."}, {"time":"timestamp", "original_phrase":"...", "translated_phrase":"...", "voice_timbre":"..."}]'
    
    prompt = f"""
transcreva o audio conforme as orientações a seguir:
1. Formate como um arquivo json com as seguintes propriedades: time, original_phrase, translated_phrase e voice_timbre.
2. A propriedade time deve conter o timestamp.
3. A propriedade original_phrase deve conter a frase no idioma {audio_language}.
4. A propriedade translated_phrase  deve conter a tradução da respectiva frase no idioma {translation_language}.
5. A propriedade voice_timbre deve conter m caso o timbre da voz do falante seja masculino, ou f caso seja feminino.
6. Considere o final da frase quando houver o sinal de ponto '.'. A frase termina quando chega no ponto final.
7. Não acrescente nenhum texto além do json. Nenhum caracter antes e nem depois do json. Deve seguir como exemplo: {json_data}
"""
    response = model.generate_content([file, prompt])
    first_candidate = response.candidates[0]
    finish_reason = first_candidate.finish_reason
    print("resposta: ", response)
    if finish_reason == 1:
      print("Finish_reason foi stop")
      return response.text
    else:
      raise Exception([f"Ocorreu um erro ao gerar transcrição, parada: {finish_reason}"])