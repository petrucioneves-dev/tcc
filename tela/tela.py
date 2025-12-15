import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import shutil
from datetime import datetime

# --- Funções de Ação (Comandos de Sistema) ---

def aumentar_volume():
    os.system("amixer sset Master 5%+") 

def diminuir_volume():
    os.system("amixer sset Master 5%-")

def configurar_wifi():
    terminal = shutil.which("x-terminal-emulator") or shutil.which("gnome-terminal") or shutil.which("xterm")
    if terminal:
        subprocess.Popen([terminal, "-e", "nmtui"])

def configurar_bluetooth_tui():
    terminal = shutil.which("x-terminal-emulator") or shutil.which("gnome-terminal") or shutil.which("xterm")
    if shutil.which("bluetuith") and terminal:
        subprocess.Popen([terminal, "-e", "bluetuith"])

def configurar_bluetooth_gui():
    if shutil.which("blueman-manager"):
        subprocess.Popen(["blueman-manager"])

def aplicar_nova_data(nova_data_string):
    """
    Recebe a string formatada "YYYY-MM-DD HH:MM:SS" e aplica no sistema via terminal.
    """
    print(f"Tentando alterar para: {nova_data_string}")
    terminal = shutil.which("x-terminal-emulator") or shutil.which("gnome-terminal") or shutil.which("xterm")
    
    if terminal:
        comando_shell = f"sudo date -s '{nova_data_string}'; echo '--- Concluido. Pressione Enter para fechar ---'; read input"
        subprocess.Popen([terminal, "-e", f"bash -c \"{comando_shell}\""])
    else:
        messagebox.showerror("Erro", "Terminal não encontrado.")

# --- Nova Janela de Diálogo Acessível ---

def abrir_dialogo_data_hora():
    """
    Cria uma janela personalizada com campos separados (Spinboxes)
    para facilitar a navegação por teclado.
    """
    # Cria janela secundária (modal)
    dialogo = tk.Toplevel(root)
    dialogo.title("Ajustar Data e Hora")
    dialogo.geometry("400x350")
    dialogo.grab_set() # Impede clicar na janela principal enquanto essa estiver aberta
    
    # Fonte grande para acessibilidade
    fonte_padrao = ("Arial", 14)
    fonte_grande = ("Arial", 18, "bold")

    agora = datetime.now()

    # --- Função interna para confirmar ---
    def confirmar_alteracao():
        # Pega os valores de cada caixinha
        d = spin_dia.get().zfill(2)
        m = spin_mes.get().zfill(2)
        a = spin_ano.get()
        h = spin_hora.get().zfill(2)
        minuto = spin_min.get().zfill(2)
        
        # Monta a string final
        data_formatada = f"{a}-{m}-{d} {h}:{minuto}:00"
        
        dialogo.destroy() # Fecha a janela
        aplicar_nova_data(data_formatada) # Aplica

    # --- Layout Visual ---
    
    tk.Label(dialogo, text="Data (Dia / Mês / Ano)", font=fonte_padrao).pack(pady=(20, 5))
    
    frame_data = tk.Frame(dialogo)
    frame_data.pack(pady=5)

    # Dia
    spin_dia = tk.Spinbox(frame_data, from_=1, to=31, width=3, font=fonte_grande, format="%02.0f")
    spin_dia.delete(0, "end")
    spin_dia.insert(0, agora.day)
    spin_dia.pack(side="left", padx=5)
    
    tk.Label(frame_data, text="/", font=fonte_grande).pack(side="left")

    # Mês
    spin_mes = tk.Spinbox(frame_data, from_=1, to=12, width=3, font=fonte_grande, format="%02.0f")
    spin_mes.delete(0, "end")
    spin_mes.insert(0, agora.month)
    spin_mes.pack(side="left", padx=5)

    tk.Label(frame_data, text="/", font=fonte_grande).pack(side="left")

    # Ano
    spin_ano = tk.Spinbox(frame_data, from_=2020, to=2050, width=5, font=fonte_grande)
    spin_ano.delete(0, "end")
    spin_ano.insert(0, agora.year)
    spin_ano.pack(side="left", padx=5)

    # --- Hora ---
    tk.Label(dialogo, text="Horário (Hora : Minuto)", font=fonte_padrao).pack(pady=(20, 5))
    
    frame_hora = tk.Frame(dialogo)
    frame_hora.pack(pady=5)

    # Hora
    spin_hora = tk.Spinbox(frame_hora, from_=0, to=23, width=3, font=fonte_grande, format="%02.0f")
    spin_hora.delete(0, "end")
    spin_hora.insert(0, agora.hour)
    spin_hora.pack(side="left", padx=5)

    tk.Label(frame_hora, text=":", font=fonte_grande).pack(side="left")

    # Minuto
    spin_min = tk.Spinbox(frame_hora, from_=0, to=59, width=3, font=fonte_grande, format="%02.0f")
    spin_min.delete(0, "end")
    spin_min.insert(0, agora.minute)
    spin_min.pack(side="left", padx=5)

    # --- Botões de Ação ---
    frame_botoes = tk.Frame(dialogo)
    frame_botoes.pack(pady=30)

    btn_ok = tk.Button(frame_botoes, text="CONFIRMAR", command=confirmar_alteracao, bg="#dddddd", font=("Arial", 12, "bold"))
    btn_ok.pack(side="left", padx=10, ipadx=10, ipady=5)

    btn_cancel = tk.Button(frame_botoes, text="Cancelar", command=dialogo.destroy, font=("Arial", 12))
    btn_cancel.pack(side="left", padx=10, ipadx=10, ipady=5)

    # Teclas de atalho dentro da janela
    dialogo.bind("<Return>", lambda e: confirmar_alteracao())
    dialogo.bind("<Escape>", lambda e: dialogo.destroy())
    
    # Foco inicial no dia
    spin_dia.focus_set()


# --- Função do Relógio Principal (Display) ---
def atualizar_relogio():
    agora = datetime.now()
    texto_visual = agora.strftime("Data: %d/%m/%Y\nHora: %H:%M:%S")
    
    if 'btn_relogio' in globals() and btn_relogio.winfo_exists():
        btn_relogio.config(text=texto_visual)
        root.after(1000, atualizar_relogio)

# --- Lógica de Navegação Principal ---
def gerenciar_foco(event):
    try:
        widget_atual = root.focus_get()
        if widget_atual not in botoes_navegaveis:
            indice_atual = 0
        else:
            indice_atual = botoes_navegaveis.index(widget_atual)
    except ValueError:
        indice_atual = 0

    if event.keysym == 'Down':
        proximo_indice = (indice_atual + 1) % len(botoes_navegaveis)
    elif event.keysym == 'Up':
        proximo_indice = (indice_atual - 1) % len(botoes_navegaveis)
    else:
        return

    botoes_navegaveis[proximo_indice].focus_set()
    return "break"

def ativar_botao_focado(event):
    widget = root.focus_get()
    if isinstance(widget, tk.Button):
        widget.invoke()

# --- Interface Gráfica Principal ---

root = tk.Tk()
root.title("Painel Acessível")
root.geometry("300x600") 

estilo_btn = {"font": ("Arial", 12), "pady": 10, "bd": 3, "relief": "raised"}
estilo_relogio = {"font": ("Arial", 14, "bold"), "pady": 15, "bd": 4, "relief": "sunken", "bg": "#d9d9d9"}

# --- Botões ---

# Agora chama a nova função 'abrir_dialogo_data_hora'
btn_relogio = tk.Button(root, text="Carregando...", command=abrir_dialogo_data_hora, **estilo_relogio)
btn_relogio.pack(fill='x', padx=20, pady=10)

btn_aumentar = tk.Button(root, text="Aumentar Volume", command=aumentar_volume, **estilo_btn)
btn_aumentar.pack(fill='x', padx=20, pady=5)

btn_diminuir = tk.Button(root, text="Diminuir Volume", command=diminuir_volume, **estilo_btn)
btn_diminuir.pack(fill='x', padx=20, pady=5)

btn_wifi = tk.Button(root, text="Configurar Wi-Fi", command=configurar_wifi, **estilo_btn)
btn_wifi.pack(fill='x', padx=20, pady=5)

btn_bt_tui = tk.Button(root, text="Bluetooth (Terminal)", command=configurar_bluetooth_tui, **estilo_btn)
btn_bt_tui.pack(fill='x', padx=20, pady=5)

btn_bt_gui = tk.Button(root, text="Bluetooth (Visual)", command=configurar_bluetooth_gui, **estilo_btn)
btn_bt_gui.pack(fill='x', padx=20, pady=5)

botoes_navegaveis = [btn_relogio, btn_aumentar, btn_diminuir, btn_wifi, btn_bt_tui, btn_bt_gui]

root.bind("<Down>", gerenciar_foco)
root.bind("<Up>", gerenciar_foco)
root.bind("<Return>", ativar_botao_focado)

atualizar_relogio()
btn_relogio.focus_set()

root.mainloop()