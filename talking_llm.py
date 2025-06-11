import openai
from dotenv import load_dotenv, find_dotenv
from pynput import keyboard
import sounddevice as sd
import wave
import os
import numpy as np
import threading
import whisper
from langchain_openai import ChatOpenAI # Alterado para ChatOpenAI conforme o uso
from queue import Queue
import io
import soundfile as sf # Adicionado soundfile para salvamento/carregamento de áudio robusto

load_dotenv(find_dotenv())

client = openai.Client()

class TalkingLLM():
    def __init__(self, model="gpt-3.5-turbo-0125", whisper_size='small'): # Modelo GPT atualizado para um mais recente
        self.is_recording = False
        self.audio_data = []
        self.samplerate = 44100
        self.channels = 1
        self.dtype = 'int16'
        self.audio_stream = None
        self.keyboard_listener = None
        self.hotkey = keyboard.HotKey(
            keyboard.HotKey.parse('<ctrl>+<alt>+h'),
            self.on_hotkey_activate
        )
        print(f"Carregando modelo Whisper '{whisper_size}'. Isso pode levar alguns segundos na primeira vez...")
        self.whisper_model = whisper.load_model(whisper_size)
        print("Modelo Whisper carregado.")
        self.llm = ChatOpenAI(model=model) # Garante que o modelo seja passado corretamente
        self.llm_queue = Queue() # Corrigido: Inicializar como uma instância de Queue
        self.tts_queue = Queue() # Nova fila para o texto do TTS para garantir o fluxo adequado

        # Inicia a thread TTS imediatamente para que esteja pronta para processar
        self.tts_thread = threading.Thread(target=self.convert_and_play, daemon=True)
        self.tts_thread.start()

        print("TalkingLLM inicializado. Pressione Ctrl+Alt+H para ativar/desativar.")

    def create_agents(self):
        pass

    def start_or_stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            print("Parando gravação. Salvando e transcrevendo...")
            # Executa save_and_transcribe em uma thread separada para evitar bloquear a UI
            threading.Thread(target=self.save_and_transcribe).start()
            self.audio_data = [] # Limpa os dados de áudio após salvar
        else:
            print("Iniciando gravação!")
            self.audio_data = []
            self.is_recording = True

    def save_and_transcribe(self):
        print('Salvando a gravação...')
        file_path = "test.wav"
        
        # Converte audio_data para um array numpy para soundfile
        audio_np = np.array(self.audio_data, dtype=self.dtype)

        try:
            # Usa soundfile para salvar o áudio, que é mais robusto
            sf.write(file_path, audio_np, self.samplerate)
            print(f"Gravação salva como {file_path}")

            print("Transcrevendo áudio com Whisper...")
            result = self.whisper_model.transcribe(file_path)
            user_text = result['text']
            print("Usuário:", user_text)

            print("Enviando para o LLM...")
            # Obtém a resposta do LLM
            response = self.llm.invoke(user_text)
            ai_response_content = response.content
            print("AI:", ai_response_content)
            
            # Coloca o conteúdo da resposta do LLM na fila do TTS
            self.tts_queue.put(ai_response_content)

        except Exception as e:
            print(f"Erro ao salvar ou transcrever: {e}")
        finally:
            if os.path.exists(file_path):
                os.remove(file_path) # Limpa o arquivo de áudio

    def convert_and_play(self):
        while True:
            # Obtém o texto completo da resposta da fila
            tts_text = self.tts_queue.get() 
            if tts_text is None: # Permite uma forma de parar a thread graciosamente
                break

            print(f"Gerando áudio para: \"{tts_text}\"")

            try:
                # Usa client.audio.speech.create para TTS
                spoken_response = client.audio.speech.create(
                    model='tts-1', # Nome do modelo corrigido
                    voice='alloy',
                    response_format='opus', # Formato Opus é bom para streaming
                    input=tts_text
                )
                
                # Transmite o áudio diretamente para sounddevice
                # Usa um objeto BytesIO para simular um arquivo para soundfile
                buffer = io.BytesIO(spoken_response.read())
                
                # Carrega os dados de áudio do buffer usando soundfile
                data, samplerate = sf.read(buffer, dtype='float32')

                # Reproduz o áudio
                sd.play(data, samplerate)
                sd.wait() # Espera até que a reprodução termine
                print("Reprodução concluída.")

            except Exception as e:
                print(f"Erro durante a síntese de voz ou reprodução: {e}")

    def on_hotkey_activate(self):
        print('Hotkey global ativada! Alternando gravação...')
        self.start_or_stop_recording()

    def for_canonical(self, f):
        return lambda k: f(self.keyboard_listener.canonical(k))

    def _audio_callback(self, indata, frame_count, time_info, status):
        """Callback para o stream de áudio. Chamado automaticamente pelo SoundDevice."""
        if status:
            print(f"SoundDevice status: {status}")
        if self.is_recording:
            self.audio_data.extend(indata.copy())

    def run(self):
        print("Estou rodando. O script ficará ativo esperando pelo hotkey.")

        self.audio_stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype=self.dtype,
            callback=self._audio_callback
        )
        self.audio_stream.start()

        self.keyboard_listener = keyboard.Listener(
            on_press=self.for_canonical(self.hotkey.press),
            on_release=self.for_canonical(self.hotkey.release)
        )
        self.keyboard_listener.start()

        try:
            print("Pressione Ctrl+C para sair.")
            while True:
                sd.sleep(1000)
        except KeyboardInterrupt:
            print("\nSaindo do programa...")
        finally:
            if self.audio_stream:
                self.audio_stream.stop()
                self.audio_stream.close()
            if self.keyboard_listener:
                self.keyboard_listener.stop()
            # Sinaliza a thread TTS para parar
            self.tts_queue.put(None) 
            self.tts_thread.join() # Espera a thread TTS terminar
            print("Recursos liberados. Programa encerrado.")

if __name__ == "__main__":
    talking_llm = TalkingLLM(whisper_size='small')
    talking_llm.run()