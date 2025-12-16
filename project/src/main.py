import os
import queue
import sounddevice as sd
import vosk
import sys
import json
import subprocess
import time

MODEL_PATH = "/home/petrucio/tcc/project/vosk-model-small-pt-0.3"

if not os.path.exists(MODEL_PATH):
    print("Modelo não encontrado!")
    sys.exit(1)

model = vosk.Model(MODEL_PATH)
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def falar(mensagem):
    subprocess.run(['espeak', '-vbrazil-mbrola-1', mensagem, '-s 120'])

def executar_comando(comando):
    if comando == "navegador":
        falar("Abrindo navegador")
        subprocess.Popen(["google-chrome"])
    
    elif comando == "desligar":
        falar("Desligando o sistema")
        # subprocess.run(["shutdown", "now"])
    
    elif comando == "reiniciar":
        falar("Reiniciando o sistema")
        # subprocess.run(["reboot"])
    
    elif comando == "tocar":
        falar("Tocando música")
        teste = subprocess.Popen(["mpg123", "/home/petrucio/Músicas/music.mp3"])
        print('teste', teste)
        time.sleep(10)
        teste.args('s')
        time.sleep(10)
        subprocess.Popen(["s"])

    
    elif comando == "pausar":
        falar("pausando música")
        subprocess.Popen(["s"])
    elif comando == "sair":
        falar("sair musica")
        subprocess.Popen(["q"])
    
    elif comando == "parar":
        falar("Encerrando o programa")
        sys.exit(0)
    
    else:
        falar("Comando não reconhecido")

# --- Loop principal com wake word ---
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    print("Sistema iniciado. Fale 'Ok' para ativar.")

    rec = vosk.KaldiRecognizer(model, 16000)

    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            texto = result.get("text", "").lower()
            print(f"Você disse: {texto}")

            # # Wake word
            # if "ok" in texto:
                # falar("Estou ouvindo, qual comando?")
            print(">> Aguardando comando...")

            # Espera outro comando
            while True:
                data_comando = q.get()
                if rec.AcceptWaveform(data_comando):
                    result_comando = json.loads(rec.Result())
                    comando_texto = result_comando.get("text", "").lower()
                    print(f"Comando: {comando_texto}")

                    if comando_texto:
                        executar_comando(comando_texto)
                        break  # volta a escutar pela wake word
            if "sair" in texto:
                break
