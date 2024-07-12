# API de transcrição e tradução para aplicação DubVideos
* [Front-end Dub Videos](https://github.com/juliano-lopes/dub-videos-front-end)
## Como utilizar  
Essa aplicação tem como objetivo realizar transcrição e tradução da transcrição dos áudios dos vídeos enviados. Para isso são utilizadas APIs da Google:
* google-auth para autenticação no Google Cloud;
* google-cloud-storage para armazenar arquivos;
* google-generativeai para utilizar inteligência artificial (Gemini) para transcrever os áudios e realizar a tradução da transcrição.
### Passos para utilização:
* Faça o clone ou baixe o projeto:  
**git clone https://github.com/juliano-lopes/transcription-api.git**  
* Entre na pasta do projeto:  
**cd transcription-api**
* Insira o arquivo com a chave de serviço no caminho:  
**api/config/**
* Crie a variável de ambiente GEMINI_API_KEY e insira a chave de API. Por exemplo no Windows:  
**set GEMINI_API_KEY=SUA_CHAVE**  
* Será necessário instalar o docker para executar a aplicação em um container.
* Na raiz do projeto, Crie a imagem por meio do Dockerfile:  
**docker build -t dub_videos_transcription .**  
* Após criar a imagem, certifique-se que uma rede foi criada para que este container e os containers das outras APIs possam se comunicar:
**docker network create dub_videos_network**
* Após criar a rede, execute o comando:  
**docker run -it --network=dub_videos_network --hostname=dub_videos_transcription -e GEMINI_API_KEY=SUA_CHAVE -p 5001:5001 dub_videos_transcription**  
* Observe que nesse caso a chave de API foi passada ao subir o container via docker. Substitua SUA_CHAVE pela chave de api correta.
* A aplicação estará disponível pela porta local 5001
* Abra o endereço:  
http://localhost:5001   
no navegador.  

 ## Como testar
* Acesse a URL http://localhost:5001  e escolha a documentação (Swagger). Após isso execute as rotas com os valores padrão de exemplo.

## Apresentação da Aplicação
* [Assista a o vídeo de aprensentação da aplicação Dub Videos](https://youtu.be/tfAVGTcRtCA)