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
        self.set_default_size(300, 400)
        self.set_border_width(10)
        
        # Conecta o evento de fechar a janela ao encerramento do script
        self.connect("destroy", Gtk.main_quit)

        # --- Layout Principal (Caixa Vertical) ---
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        # --- Criação dos Botões ---
        # No GTK, o Orca lê o "label" do botão automaticamente

        self.btn_aumentar = Gtk.Button(label="Aumentar Volume")
        self.btn_aumentar.connect("clicked", self.aumentar_volume)
        self.box.pack_start(self.btn_aumentar, True, True, 0)

        self.btn_diminuir = Gtk.Button(label="Diminuir Volume")
        self.btn_diminuir.connect("clicked", self.diminuir_volume)
        self.box.pack_start(self.btn_diminuir, True, True, 0)

        self.btn_wifi = Gtk.Button(label="Configurar Wi-Fi")
        self.btn_wifi.connect("clicked", self.configurar_wifi)
        self.box.pack_start(self.btn_wifi, True, True, 0)

        self.btn_bluetooth = Gtk.Button(label="Configurar Bluetooth")
        self.btn_bluetooth.connect("clicked", self.configurar_bluetooth)
        self.box.pack_start(self.btn_bluetooth, True, True, 0)

        self.btn_sair = Gtk.Button(label="Sair do Sistema")
        self.btn_sair.connect("clicked", Gtk.main_quit)
        self.box.pack_start(self.btn_sair, True, True, 0)

        # --- Navegação com Setas ---
        # O padrão do GTK é TAB, mas vamos forçar as setas para ficar igual ao seu pedido
        self.connect("key-press-event", self.ao_pressionar_tecla)

    # --- Funções de Lógica (Comandos do Sistema) ---

    def aumentar_volume(self, widget):
        print("Aumentando...")
        os.system("amixer sset PCM 5%+") # Se não funcionar, tente "Master" em vez de "PCM"

    def diminuir_volume(self, widget):
        print("Diminuindo...")
        os.system("amixer sset PCM 5%-")

    def configurar_wifi(self, widget):
        # Abre o nmtui no xterm
        terminal = shutil.which("lxterminal")
        if terminal:
            subprocess.Popen([terminal, "-e", "nmtui"])

    def configurar_bluetooth(self, widget):
        # Tenta abrir o bluetuith (se instalado) ou blueman
        terminal = shutil.which("lxterminal")
        if shutil.which("bluetuith") and terminal:
             subprocess.Popen([terminal, "-e", "bluetuith"])
        elif shutil.which("blueman-manager"):
             subprocess.Popen(["blueman-manager"])

    # --- Lógica da Tecla (Setas) ---
    def ao_pressionar_tecla(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        
        # Se apertar Seta Baixo ou Cima
        if keyname in ["Down", "Up"]:
            foco_atual = self.get_focus()
            botoes = self.box.get_children()
            
            # Se ninguém tem foco, pega o primeiro
            if foco_atual not in botoes:
                botoes[0].grab_focus()
                return True
            
            indice = botoes.index(foco_atual)
            
            if keyname == "Down":
                proximo = (indice + 1) % len(botoes)
            else: # Up
                proximo = (indice - 1) % len(botoes)
            
            # Muda o foco (O Orca vai ler automaticamente!)
            botoes[proximo].grab_focus()
            return True # Impede o comportamento padrão
            
        return False # Deixa outras teclas funcionarem normal (Enter, Espaço)

# --- Inicia o Programa ---
win = PainelAcessivel()
win.show_all()
Gtk.main()
