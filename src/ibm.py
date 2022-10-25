from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from gravador_de_voz import *

KEY_FILE = "/misc/ifba/workspaces/inteligencia artificial/ibm.key"
TEMP_DIR = "/misc/ifba/workspaces/inteligencia artificial/assistente virtual/temp"

MODELO_BR1 = "pt-BR_BroadbandModel"
MODELO_BR2 = "pt-BR_NarrowbandModel"
MODELO_BR3 = "pt-BR_Telephony"

def configurar_servico():
    global servico

    with open(KEY_FILE, "r") as arquivo_chave_api:
        chave = arquivo_chave_api.readline()

        autenticador = IAMAuthenticator(chave)
        servico = SpeechToTextV1(authenticator=autenticador)
        servico.set_service_url("https://api.us-east.speech-to-text.watson.cloud.ibm.com")

def capturar_audio():
    return gravar_microfone(temp_dir=TEMP_DIR, segundos=4)

def processar_resposta(resposta):
    confianca, texto = 0.0, None

    alternativas = resposta.result["results"][0]["alternatives"]
    for alternativa in alternativas:
        if float(alternativa["confidence"]) > confianca:
            confianca = alternativa["confidence"]
            texto = alternativa["transcript"].strip()

    return confianca, texto

def reconhecer_texto(audio, modelo_pt_br=MODELO_BR1):
    global servico

    confianca, texto, resposta = 0.0, None, None
    with open(audio, "rb") as wav:
        resposta = servico.recognize(audio=wav, content_type="audio/wav", model=modelo_pt_br)
        wav.close()
        
        if resposta:
            confianca, texto = processar_resposta(resposta)

    return confianca, texto

if __name__ == "__main__":
    configurar_servico()

    audio_capturado, audio = capturar_audio()
    if audio_capturado:
        confianca, texto = reconhecer_texto(audio)
        if confianca > 0.70:
            print(f"texto reconhecido: {texto}")
        else:
            print("não foi possível reconhecer a fala")
