import gi
import os
import subprocess
import shutil

# Exige a versão 3.0 do GTK
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class PainelAcessivel(Gtk.Window):
    def __init__(self):
        super().__init__(title="Painel Acessível")
        self.set_default_size(300, 450) # Aumentei um pouco a altura
        self.set_border_width(10)
        
        self.connect("destroy", Gtk.main_quit)

        # --- Layout Principal ---
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        # --- Botões ---

        self.btn_aumentar = Gtk.Button(label="Aumentar Volume")
        self.btn_aumentar.connect("clicked", self.aumentar_volume)
        self.box.pack_start(self.btn_aumentar, True, True, 0)

        self.btn_diminuir = Gtk.Button(label="Diminuir Volume")
        self.btn_diminuir.connect("clicked", self.diminuir_volume)
        self.box.pack_start(self.btn_diminuir, True, True, 0)

        self.btn_wifi = Gtk.Button(label="Configurar Wi-Fi")
        self.btn_wifi.connect("clicked", self.configurar_wifi)
        self.box.pack_start(self.btn_wifi, True, True, 0)

        # Botão 1: Bluetooth Terminal (TUI)
        self.btn_bt_tui = Gtk.Button(label="Bluetooth (Terminal)")
        self.btn_bt_tui.connect("clicked", self.configurar_bluetooth_tui)
        self.box.pack_start(self.btn_bt_tui, True, True, 0)

        # Botão 2: Bluetooth Visual (GUI)
        self.btn_bt_gui = Gtk.Button(label="Bluetooth (Visual)")
        self.btn_bt_gui.connect("clicked", self.configurar_bluetooth_gui)
        self.box.pack_start(self.btn_bt_gui, True, True, 0)

        self.btn_sair = Gtk.Button(label="Sair do Sistema")
        self.btn_sair.connect("clicked", Gtk.main_quit)
        self.box.pack_start(self.btn_sair, True, True, 0)

        # --- Navegação com Setas ---
        self.connect("key-press-event", self.ao_pressionar_tecla)

    # --- Funções de Lógica ---

    def aumentar_volume(self, widget):
        os.system("amixer sset Master 5%+") 

    def diminuir_volume(self, widget):
        os.system("amixer sset Master 5%-")

    def configurar_wifi(self, widget):
        # Adicionei lxterminal para garantir compatibilidade com Wayland
        terminal = shutil.which("lxterminal") or shutil.which("x-terminal-emulator") or shutil.which("gnome-terminal") or shutil.which("xterm")
        if terminal:
            subprocess.Popen([terminal, "-e", "nmtui"])

    # --- Funções de Bluetooth Separadas ---

    def configurar_bluetooth_tui(self, widget):
        # Prioriza lxterminal para evitar erro "Can't open display"
        terminal = shutil.which("lxterminal") or shutil.which("x-terminal-emulator") or shutil.which("gnome-terminal") or shutil.which("xterm")
        
        # Só abre se achar o bluetuith E um terminal
        if shutil.which("bluetuith") and terminal:
            subprocess.Popen([terminal, "-e", "bluetuith"])
        else:
            print("Erro: Bluetuith ou Terminal não encontrado.")

    def configurar_bluetooth_gui(self, widget):
        if shutil.which("blueman-manager"):
            subprocess.Popen(["blueman-manager"])
        else:
            print("Erro: Blueman-manager não encontrado.")

    # --- Lógica da Tecla (Setas) ---
    def ao_pressionar_tecla(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        
        if keyname in ["Down", "Up"]:
            foco_atual = self.get_focus()
            botoes = self.box.get_children()
            
            if foco_atual not in botoes:
                botoes[0].grab_focus()
                return True
            
            indice = botoes.index(foco_atual)
            
            if keyname == "Down":
                proximo = (indice + 1) % len(botoes)
            else: # Up
                proximo = (indice - 1) % len(botoes)
            
            botoes[proximo].grab_focus()
            return True 
            
        return False

# --- Inicia o Programa ---
win = PainelAcessivel()
win.show_all()
Gtk.main()
