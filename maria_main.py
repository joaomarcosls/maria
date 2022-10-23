import speech_recognition as sr
from nltk import word_tokenize, corpus
import json
import pyautogui

IDIOMA_CORPUS = "portuguese"
IDIOMA_FALA = "pt-BR"
CAMINHO_CONFIGURACAO = "config.json"


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
        
        print("Olá sou Maria me informe oque deseja...")        
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
        
        if len(tokens) >= 3:
            if nome_assistente == tokens[0].lower():
                acao = tokens[1].lower()
                objeto = tokens[2].lower()            
    
    return acao, objeto
    

def validar_comando(acao, objeto):
    global acoes
    
    valido = False
    
    if acao and objeto:
        for acaoCadastrada in acoes:
            if acao == acaoCadastrada["nome"]:
                if objeto in acaoCadastrada["objetos"]:
                    valido = True
                    
                break
    
    return valido


def executar_comando(acao, objeto):
   
    print("vou executar o comando:", acao, objeto)
    
    if acao == "aumentar":
     pyautogui.hotkey("volumeup")
    
    if objeto == "mudo":
     pyautogui.hotkey("volumemute")
      
    if objeto == "e-mail":
     pyautogui.press('win') #Pressiona a tecla Iniciar do Windows
     pyautogui.typewrite('e-mail') #Digita o texto no local atual do cursor
     pyautogui.press('enter') #Pressiona a tecla [ENTER]
     pyautogui.press('enter') #Pressiona a tecla [ENTER]
      
  

if __name__ == '__main__':
    iniciar()

    continuar = True
    while continuar:
        try:
            comando = escutar_comando()
            print(f"Vou executar: {comando}")

            if comando:
                acao, objeto = tokenizar_comando(comando)
                valido = validar_comando(acao, objeto)
                if valido:
                    executar_comando(acao, objeto)
                else:
                    print("Não entendi. Pode repetir!")
        except KeyboardInterrupt:
            print("Tchau!")

            continuar = False
