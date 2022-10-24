from operator import contains
from tokenize import Number
import speech_recognition as sr
from nltk import word_tokenize, corpus
import json

IDIOMA_CORPUS = "portuguese"
IDIOMA_FALA = "pt-BR"
CAMINHO_CONFIGURACAO = "config.json"
ESTAGE = 0
PEDIDOS = []

def iniciar():
    global reconhecedor
    global palavras_de_parada
    global nome_assistente
    global acoes
    

    reconhecedor = sr.Recognizer()
    palavras_de_parada = set(corpus.stopwords.words(IDIOMA_CORPUS))

    with open(CAMINHO_CONFIGURACAO, "r") as arquivo_configuracao:
        configuracao = json.load(arquivo_configuracao)

        nome_assistente = configuracao["nome"]
        acoes = configuracao["acoes"]

        arquivo_configuracao.close()


def escutar_comando():
    global reconhecedor
    
    comando = None
    
    with sr.Microphone() as fonte_audio:
        reconhecedor.adjust_for_ambient_noise(fonte_audio)
        
        print("Fale alguma coisa...")        
        fala = reconhecedor.listen(fonte_audio, timeout=5, phrase_time_limit=5)
        try:
            comando = reconhecedor.recognize_google(fala, language=IDIOMA_FALA)
        except sr.UnknownValueError:
            pass
    
    return comando
    


def eliminar_palavras_de_parada(tokens):
    global palavras_de_parada
    
    tokens_filtrados = []
    for token in tokens:
        if token not in palavras_de_parada:
            tokens_filtrados.append(token)
    
    return tokens_filtrados


def tokenizar_comando(comando):
    global nome_assistente
    
    acao = None
    objeto = None
    
    tokens = word_tokenize(comando, IDIOMA_CORPUS)
    if tokens:
        tokens = eliminar_palavras_de_parada(tokens)
        #print(tokens)
        
        
        if tokens[0] == nome_assistente:
            acao = tokens[1].lower()
            objeto = tokens[2].lower()  
        else:
                acao = tokens[0].lower()
                for x,tk in enumerate(tokens):
                    if x > 1:
                        
                        objeto = str(objeto) + " " + str(tk)
                    if x == 1:
                        objeto = tokens[1]
                       # objeto = str(objeto)
                                  
    
    return acao, objeto
    

def validar_comando(acao, objeto):
    global acoes
    
    valido = False
    
    if acao and objeto:

        for acaoCadastrada in acoes:
            if acao == acaoCadastrada["nome"]:
                if objeto in acaoCadastrada["objetos"]:
                    valido = True
                else:
                    print(objeto.split(" ")[0])
                    try:
                        if objeto.split(" ")[0] in acaoCadastrada["objetos"]:
                            valido = True
                    except:
                        print("erro")
                        pass    
                break
    
    return valido

def retornarNumero(txt):
    if txt == 'um':
        return 1
    if txt == 'dois':
        return 2
    if txt == 'três':
        return 3
    if txt == 'quatro':
        return 4
    if txt == 'cinco':
        return 5
    if txt == 'seis':
        return 6
    if txt == 'sete':
        return 7
    if txt == 'oito':
        return 8
    if txt == 'nove':
        return 9
    if txt == 'dez':
        return 10
def executar_comando(acao, objeto):
    
    if(acao == 'listar'):
        if(objeto == 'menu'):
            
            print("--- Menu ---")
            print("_____________________________________________")
            print("Quibe -> R$1,00")
            print("_____________________________________________")
            print("coxinha -> R$1,50 ")
            print("_____________________________________________")
            print("pastel -> R$2,00")
            print("_____________________________________________")
            return 1
    
    if( acao == 'vou'):
        if( objeto.split(" ")[0] == "querer"):
                print("PEDIDO>>"+str(objeto))
                print("Seu item foi adicionado, vai querer mais alguma coisa?")
                return 2
        else:
            pass
    if acao == "quero":
        if( objeto.split(" ")[0] == "fechar"):
                print("Seu pedido foi finalizado")
                
                for item,n in enumerate(PEDIDOS):
                    valor = int(valor) + int(n)    
                    
                print("O valor total foi de:"+str(valor))
                return 0
        else:
            pass
           
    
    if(acao == 'adicionando'):
        pass

if __name__ == '__main__':
    iniciar()
    ESTAGE = 0
    continuar = True
    while continuar:
        try:
            
            if ESTAGE == 0:
                print("Olá, no que posso ajudar?")
            if ESTAGE == 1:
                print("O que você vai querer?")
            if ESTAGE == 2:
                pass
            comando = escutar_comando()
            print(f"processando o comando: {comando}")

            if comando:
                acao, objeto = tokenizar_comando(comando)
                valido = validar_comando(acao, objeto)
                if valido:
                    ESTAGE = executar_comando(acao, objeto)
                else:
                    print("Não entendi o comando. Repita, por favor!")
        except KeyboardInterrupt:
            print("Tchau!")

            continuar = False
