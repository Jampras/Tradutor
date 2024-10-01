import tkinter as tk
from tkinter import messagebox
import threading
import speech_recognition as sr
from googletrans import Translator

class CaptacaoAudioGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Captura de Áudio")
        
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)
        
        self.botao_iniciar = tk.Button(self.frame, text="Iniciar Captura", command=self.iniciar_captura)
        self.botao_iniciar.pack(side=tk.LEFT)
        
        self.botao_parar = tk.Button(self.frame, text="Parar Captura", command=self.parar_captura, state=tk.DISABLED)
        self.botao_parar.pack(side=tk.LEFT)
        
        self.texto_transcrito = ""
        self.captura_ativa = False  # Variável para controlar se a captura de áudio está ativa
        
        self.translator = Translator()
        
    def iniciar_captura(self):
        self.botao_iniciar.config(state=tk.DISABLED)
        self.botao_parar.config(state=tk.NORMAL)
        self.captura_ativa = True  # Define a captura como ativa
        
        self.arquivo_saida = open("texto_transcrito.txt", "w")  # Abre o arquivo para escrita
        
        # Inicia uma thread para executar o loop de captura de áudio
        self.thread_captura = threading.Thread(target=self.transcrever_audio_loop)
        self.thread_captura.start()
        
    def parar_captura(self):
        self.botao_iniciar.config(state=tk.NORMAL)
        self.botao_parar.config(state=tk.DISABLED)
        self.captura_ativa = False  # Define a captura como inativa
        
        self.arquivo_saida.close()  # Fecha o arquivo
        
    def transcrever_audio_loop(self):
        while self.captura_ativa:  # Executa enquanto a captura estiver ativa
            texto = self.transcrever_audio()
            if texto:
                self.texto_transcrito += texto + "\n"
                texto_traduzido = self.traduzir_texto(texto, "en")  # Traduz para inglês
                if texto_traduzido:
                    self.arquivo_saida.write(texto_traduzido + "\n")  # Escreve o texto traduzido no arquivo
            else:
                messagebox.showerror("Erro", "Não foi possível entender a fala.")
                break
        
    def transcrever_audio(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Aguardando comando...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Transcrevendo...")
            texto_transcrito = recognizer.recognize_google(audio, language="pt-BR")
            print("Texto transcrevido:", texto_transcrito)
            return texto_transcrito
        except sr.UnknownValueError:
            print("Não foi possível entender a fala")
            return ""
        except sr.RequestError as e:
            print("Erro ao solicitar serviço de reconhecimento de fala; {0}".format(e))
            return ""

    def traduzir_texto(self, texto, idioma_destino):
        try:
            traducao = self.translator.translate(texto, dest=idioma_destino)
            return traducao.text
        except Exception as e:
            print("Erro ao traduzir texto:", e)
            return ""

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptacaoAudioGUI(root)
    root.mainloop()
