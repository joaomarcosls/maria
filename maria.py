import speech_recognition as sr

def interpretar_microphone():
    reconhecedor = sr.Recognizer()

    with sr.Microphone() as fonte_audio:
        reconhecedor.adjust_for_ambient_noise(fonte_audio)

        print("fale alguma coisa...")
        fala = reconhecedor.listen(fonte_audio, timeout=3)

        try:
            texto = reconhecedor.recognize_google(fala, language="pt-BR")
            print("você disse:", texto)
        except sr.UnknownValueError:
            print("não entendi o que você disse!")

if __name__ == "__main__":
    interpretar_microphone()