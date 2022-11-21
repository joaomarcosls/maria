#deve-se baixar estas biblioetas antes da sua utilizaçao 
import speech_recognition as sr #biblioteca do reconheimento de fala
import os #bibliotea de acesso ao sistema operaional
import gtts
from playsound import playsound

repete = True #variavel de controle
def ouvir_mirofone(): #funçao que ouve e reconhee a fala   
    microfone = sr.Recognizer() #habilita o microfone  
    with sr.Microphone() as source:#com o objeto (sr) utilizamos a funçao (microphone) e atribuimos a variavel (source)      
        microfone.adjust_for_ambient_noise(source)#chama o algoritmo de reduçao de ruidos 
        print('LISTEN: ...')           
        audio = microfone.listen(source)#funçao q ouve oq foi dito e armazena na variavel    
    try: #tratamento de exceçoes       
        frase = microfone.recognize_google(audio,language='pt-BR')#funçao de reconhecimento da fala/de padroes, base de dados do deep learning
        if "navegador" in frase:
            with open('navegador.txt', 'r') as arquivo:#abrindo o arquivo de texto, [arquivo] e o objeto,  'r' é read/leitura.
                for linha in arquivo:#laço for q cria a variavel linha q recebe os dados do arquivo 
                    fraseN = gtts.gTTS(linha,lang='pt-br')#variavel frase recebe a transcriçao do arquivo txt, lang='portugues'
                    fraseN.save('arquivo.mp3') #objeto frase usa o metodo save e define o nome do arquivo mp3
                    playsound('arquivo.mp3')#tocando o arquivo
            os.system("start Opera.exe")#passa o arquivo que deve ser aberto apos encontrar a palavra determinada no (if)
        elif "Spotify" in frase:
            with open('musica.txt', 'r') as arquivo:#abrindo o arquivo de texto, [arquivo] e o objeto - 'r' é read/leitura.
                for linha in arquivo:#laço for q cria a variavel linha q recebe os dados do arquivo 
                    fraseS = gtts.gTTS(linha,lang='pt-br')#variavel frase recebe a transriçao do arquivo txt, lang='portugues'
                    fraseS.save('musica.mp3') #objeto frase usa o metodo save e define o nome do arquivo mp3
                    playsound('musica.mp3')#tocando o arquivo
            os.system("start Spotify.exe")       
        elif "desativar" in frase:  #desativar a escuta
            global repete 
            repete = False      
    except sr.UnknownValueError:#caso n seja reconhecido nenhum padrao de fala gera a exceçao
        print('não entendi')
        repete = False
        #return frase #retorna a frase falada que n foi entendido pelo algoritmo
while repete != False:    
    ouvir_mirofone()#chama a funçao para q o codigo seja exeutado
print('END')