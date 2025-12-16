import gi
import os
import subprocess
import shutil
from datetime import datetime

# Exige a versão 3.0 do GTK
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

class PainelAcessivel(Gtk.Window):
    def __init__(self):
        super().__init__(title="Painel Acessível")
        self.set_default_size(320, 600) 
        self.set_border_width(10)
        
        self.connect("destroy", Gtk.main_quit)

        # --- Layout Principal ---
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        # --- Botão Relógio ---
        self.btn_relogio = Gtk.Button(label="Carregando...")
        self.btn_relogio.connect("clicked", self.abrir_dialogo_data_hora)
        self.btn_relogio.get_accessible().set_name("Botão de Data e Hora")
        self.box.pack_start(self.btn_relogio, True, True, 0)

        # --- NOVOS BOTÕES ---

        # 1. Botão Gerenciador de Arquivos (Pastas)
        self.btn_pastas = Gtk.Button(label="Abrir Meus Arquivos")
        self.btn_pastas.connect("clicked", self.abrir_pastas)
        self.box.pack_start(self.btn_pastas, True, True, 0)

        # 2. Botão Internet
        self.btn_internet = Gtk.Button(label="Acessar Internet")
        self.btn_internet.connect("clicked", self.abrir_internet)
        self.box.pack_start(self.btn_internet, True, True, 0)

        # --- Botões Antigos (Volume/Wi-Fi/BT) ---
        
        self.btn_aumentar = Gtk.Button(label="Aumentar Volume")
        self.btn_aumentar.connect("clicked", self.aumentar_volume)
        self.box.pack_start(self.btn_aumentar, True, True, 0)

        self.btn_diminuir = Gtk.Button(label="Diminuir Volume")
        self.btn_diminuir.connect("clicked", self.diminuir_volume)
        self.box.pack_start(self.btn_diminuir, True, True, 0)

        self.btn_wifi = Gtk.Button(label="Configurar Wi-Fi")
        self.btn_wifi.connect("clicked", self.configurar_wifi)
        self.box.pack_start(self.btn_wifi, True, True, 0)

        self.btn_bt_gui = Gtk.Button(label="Bluetooth (Visual)")
        self.btn_bt_gui.connect("clicked", self.configurar_bluetooth_gui)
        self.box.pack_start(self.btn_bt_gui, True, True, 0)

        self.btn_sair = Gtk.Button(label="Sair do Sistema")
        self.btn_sair.connect("clicked", Gtk.main_quit)
        self.box.pack_start(self.btn_sair, True, True, 0)

        # --- Navegação com Setas ---
        self.connect("key-press-event", self.ao_pressionar_tecla)

        # --- Inicia o Relógio ---
        self.atualizar_relogio() 
        GLib.timeout_add_seconds(1, self.atualizar_relogio)

    # --- FUNÇÕES DOS NOVOS BOTÕES ---

    def abrir_pastas(self, widget):
        """
        Abre o Gerenciador de Arquivos na pasta do usuário (/home/tcc ou /home/pi).
        Usa o 'pcmanfm' que é o padrão do Raspberry Pi.
        """
        print("Abrindo pastas...")
        # Tenta o pcmanfm (padrão do Pi), senão tenta o genérico xdg-open
        if shutil.which("pcmanfm"):
            # O símbolo ~ abre a pasta home do usuário atual
            subprocess.Popen(["pcmanfm", os.path.expanduser("~")])
        else:
            # Fallback: xdg-open abre qualquer coisa com o programa padrão
            subprocess.Popen(["xdg-open", os.path.expanduser("~")])

    def abrir_internet(self, widget):
        """
        Abre o Navegador de Internet (Chromium ou Firefox).
        """
        print("Abrindo internet...")
        url_inicial = "https://www.google.com"

        # Tenta achar o Chromium (padrão do Pi)
        if shutil.which("chromium-browser"):
            subprocess.Popen(["chromium-browser", url_inicial])
        # Se não tiver, tenta Firefox
        elif shutil.which("firefox"):
            subprocess.Popen(["firefox", url_inicial])
        # Último caso: usa o comando genérico do Linux para abrir URL
        else:
            subprocess.Popen(["xdg-open", url_inicial])

    # --- Demais Funções (Mantidas) ---

    def aumentar_volume(self, widget):
        os.system("amixer sset HDMI 5%+") 

    def diminuir_volume(self, widget):
        os.system("amixer sset HDMI 5%-")

    def configurar_wifi(self, widget):
        terminal = shutil.which("lxterminal") or shutil.which("x-terminal-emulator") or shutil.which("xterm")
        if terminal:
            subprocess.Popen([terminal, "-e", "nmtui"])

    def configurar_bluetooth_gui(self, widget):
        if shutil.which("blueman-manager"):
            subprocess.Popen(["blueman-manager"])

    # --- Relógio e Data ---
    def atualizar_relogio(self):
        agora = datetime.now()
        novo_texto = agora.strftime("Data: %d/%m/%Y\n\nHora: %H:%M:%S")
        if self.btn_relogio.get_label() != novo_texto:
            self.btn_relogio.set_label(novo_texto)
        return True

    def abrir_dialogo_data_hora(self, widget):
        # ... (Sua função de data completa aqui) ...
        # Se quiser que eu cole ela inteira de novo, avise!
        print("Abrir diálogo de data...") 
        # Lembre de manter a lógica do 'aplicar_nova_data' que fizemos antes!

    # --- Navegação ---
    def ao_pressionar_tecla(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        if keyname in ["Down", "Up"]:
            foco_atual = self.get_focus()
            botoes = self.box.get_children()
            # Filtra apenas botões
            botoes = [b for b in botoes if isinstance(b, Gtk.Button)]
            
            if not botoes: return False
            if foco_atual not in botoes:
                botoes[0].grab_focus()
                return True
            
            indice = botoes.index(foco_atual)
            proximo = (indice + 1) % len(botoes) if keyname == "Down" else (indice - 1) % len(botoes)
            botoes[proximo].grab_focus()
            return True 
        return False

# --- Inicia ---
win = PainelAcessivel()
win.show_all()
Gtk.main()
