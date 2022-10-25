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
        
        print("Aguardando comando")        
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
        
        if tokens[0].lower() == nome_assistente.lower():
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
    global PEDIDOS
    if(acao == 'listar'):
        if(objeto == 'menu'):
            # Cardápio
            print("---------------------------------------------------")
            print("--- Menu ---")
            print("_____________________________________________")
            print("Quibe -> R$1,00")
            print("_____________________________________________")
            print("coxinha -> R$1,50 ")
            print("_____________________________________________")
            print("pastel -> R$2,00")
            print("_____________________________________________")
            print("---------------------------------------------------")
            return 1
    
    if( acao == 'vou'):
        if( objeto.split(" ")[0] == "querer"):
                print("PEDIDO>>"+str(objeto.split(" ")[1]+" "+str(objeto.split(" ")[2])))
                # adicionar os pedidos em um array que posteriormente seria feito um loop para somar 
                PEDIDOS.append([objeto.split("querer")[1],1])
                
                # em um chatbot haveria uma condicional para ficar em loop até que não exista mais pedidos
                #print("Seu item foi adicionado, vai querer mais alguma coisa?")
                
                return 2
        else:
            pass
    if acao == "quero":
        if( objeto.split(" ")[0] == "encerrar"):
                print("Seu pedido foi finalizado!!")
                valor = 0
                # somatório dos pedidos
                for pedido in PEDIDOS:
                    valor = valor + int(pedido[1] )
                    
                print("O valor total foi de: "+str(valor))
                # reseta os pedidos
                PEDIDOS = []
                return 0
        else:
            return 0
    if(acao == 'adicionando'):
        pass

if __name__ == '__main__':
    # inicialização base do programa
    iniciar()
    # variavel para controle de estágio -> similar a um chatterbot
    ESTAGE = 0
    # flag de controle
    CONTINUAR = True
    while CONTINUAR:
        try:
            
            if ESTAGE == 0:
                print("Olá, no que posso ajudar?")
                # simula o comando de voz para pedir o cardápio
                comando = "rafa listar menu"
            if ESTAGE == 1:
                print("O que você vai querer?")
                # simula um comando de voz para fazer um pedido
                comando = "vou querer 1 coxinha"
            if ESTAGE == 2:
                # simula o comando de voz para encerrar o pedido
                comando = "quero encerrar pedido"
                
                # para o teste executar apenas uma vez
                CONTINUAR = False
                
            # para realizar testes comentar o comando a baixo já que não será recebido nenhum comando por voz
            #comando = escutar_comando()
            print("----------------------------------------")
            print("O comando recebido foi>>"+str(comando))
            print("----------------------------------------")

            if comando:
                acao, tipo = tokenizar_comando(comando)
                VALIDO = validar_comando(acao, tipo)
                if VALIDO:
                    ESTAGE = executar_comando(acao, tipo)
                else:
                    print("Não entendi o comando. Repita, por favor!")
        except KeyboardInterrupt:
            print("Volte sempre!")

            continuar = False
