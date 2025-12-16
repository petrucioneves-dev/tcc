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
        self.box.pack_start(self.btn_relogio, True, True, 0)

        # --- NOVOS BOTÕES ADICIONADOS AQUI ---

        # 1. Botão Gerenciador de Arquivos
        self.btn_pastas = Gtk.Button(label="Abrir Meus Arquivos")
        self.btn_pastas.connect("clicked", self.abrir_pastas)
        self.box.pack_start(self.btn_pastas, True, True, 0)

        # 2. Botão Internet
        self.btn_internet = Gtk.Button(label="Acessar Internet")
        self.btn_internet.connect("clicked", self.abrir_internet)
        self.box.pack_start(self.btn_internet, True, True, 0)

        # --------------------------------------

        self.btn_aumentar = Gtk.Button(label="Aumentar Volume")
        self.btn_aumentar.connect("clicked", self.aumentar_volume)
        self.box.pack_start(self.btn_aumentar, True, True, 0)

        self.btn_diminuir = Gtk.Button(label="Diminuir Volume")
        self.btn_diminuir.connect("clicked", self.diminuir_volume)
        self.box.pack_start(self.btn_diminuir, True, True, 0)

        self.btn_wifi = Gtk.Button(label="Configurar Wi-Fi")
        self.btn_wifi.connect("clicked", self.configurar_wifi)
        self.box.pack_start(self.btn_wifi, True, True, 0)

        self.btn_bt_tui = Gtk.Button(label="Bluetooth (Terminal)")
        self.btn_bt_tui.connect("clicked", self.configurar_bluetooth_tui)
        self.box.pack_start(self.btn_bt_tui, True, True, 0)

        self.btn_bt_gui = Gtk.Button(label="Bluetooth (Visual)")
        self.btn_bt_gui.connect("clicked", self.configurar_bluetooth_gui)
        self.box.pack_start(self.btn_bt_gui, True, True, 0)

        self.btn_sair = Gtk.Button(label="Sair do Sistema")
        self.btn_sair.connect("clicked", Gtk.main_quit)
        self.box.pack_start(self.btn_sair, True, True, 0)

        # --- Navegação com Setas ---
        self.connect("key-press-event", self.ao_pressionar_tecla)

        # --- Inicia o Timer do Relógio ---
        self.atualizar_relogio() 
        GLib.timeout_add_seconds(1, self.atualizar_relogio)

    # --- FUNÇÕES DOS NOVOS BOTÕES ---

    def abrir_pastas(self, widget):
        print("Abrindo gerenciador de arquivos...")
        # Tenta abrir o pcmanfm (padrão Raspberry) na pasta do usuário (~)
        if shutil.which("pcmanfm"):
            subprocess.Popen(["pcmanfm", os.path.expanduser("~")])
        else:
            # Fallback genérico se não achar o pcmanfm
            subprocess.Popen(["xdg-open", os.path.expanduser("~")])

    def abrir_internet(self, widget):
        print("Abrindo navegador...")
        url = "https://www.google.com"
        
        # Tenta Chromium (padrão), depois Firefox, depois genérico
        if shutil.which("chromium"):
            subprocess.Popen(["chromium", url])
        elif shutil.which("firefox"):
            subprocess.Popen(["firefox", url])
        else:
            subprocess.Popen(["xdg-open", url])

    # --- Lógica do Relógio ---

    def atualizar_relogio(self):
        agora = datetime.now()
        
        # Mostra apenas Hora:Minuto para não bugar o Orca
        novo_texto = agora.strftime("Data: %d/%m/%Y\n\nHora: %H:%M")
        
        if self.btn_relogio.get_label() != novo_texto:
            self.btn_relogio.set_label(novo_texto)
            
        return True 

    def abrir_dialogo_data_hora(self, widget):
        dialogo = Gtk.Dialog(title="Ajustar Data e Hora", transient_for=self, flags=0)
        dialogo.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            "Confirmar", Gtk.ResponseType.OK
        )
        dialogo.set_default_size(350, 300)
        
        box_conteudo = dialogo.get_content_area()
        box_conteudo.set_spacing(10)
        box_conteudo.set_border_width(20)

        agora = datetime.now()

        # --- Área da Data ---
        lbl_data = Gtk.Label(label="<b>Data (Dia / Mês / Ano)</b>")
        lbl_data.set_use_markup(True)
        box_conteudo.pack_start(lbl_data, False, False, 0)

        box_data = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        box_data.set_halign(Gtk.Align.CENTER) 
        box_conteudo.pack_start(box_data, False, False, 0)

        # SpinButtons
        adj_dia = Gtk.Adjustment(value=agora.day, lower=1, upper=31, step_increment=1)
        self.spin_dia = Gtk.SpinButton(adjustment=adj_dia)
        box_data.pack_start(self.spin_dia, False, False, 0)

        box_data.pack_start(Gtk.Label(label="/"), False, False, 0)

        adj_mes = Gtk.Adjustment(value=agora.month, lower=1, upper=12, step_increment=1)
        self.spin_mes = Gtk.SpinButton(adjustment=adj_mes)
        box_data.pack_start(self.spin_mes, False, False, 0)

        box_data.pack_start(Gtk.Label(label="/"), False, False, 0)

        adj_ano = Gtk.Adjustment(value=agora.year, lower=2020, upper=2050, step_increment=1)
        self.spin_ano = Gtk.SpinButton(adjustment=adj_ano)
        box_data.pack_start(self.spin_ano, False, False, 0)

        # --- Área da Hora ---
        lbl_hora = Gtk.Label(label="<b>Horário (Hora : Minuto)</b>")
        lbl_hora.set_use_markup(True)
        box_conteudo.pack_start(lbl_hora, False, False, 10)

        box_hora = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        box_hora.set_halign(Gtk.Align.CENTER)
        box_conteudo.pack_start(box_hora, False, False, 0)

        adj_hora = Gtk.Adjustment(value=agora.hour, lower=0, upper=23, step_increment=1)
        self.spin_hora = Gtk.SpinButton(adjustment=adj_hora)
        box_hora.pack_start(self.spin_hora, False, False, 0)

        box_hora.pack_start(Gtk.Label(label=":"), False, False, 0)

        adj_min = Gtk.Adjustment(value=agora.minute, lower=0, upper=59, step_increment=1)
        self.spin_min = Gtk.SpinButton(adjustment=adj_min)
        box_hora.pack_start(self.spin_min, False, False, 0)

        dialogo.show_all()

        resposta = dialogo.run()

        if resposta == Gtk.ResponseType.OK:
            d = int(self.spin_dia.get_value())
            m = int(self.spin_mes.get_value())
            a = int(self.spin_ano.get_value())
            h = int(self.spin_hora.get_value())
            minuto = int(self.spin_min.get_value())

            nova_data = f"{a:04d}-{m:02d}-{d:02d} {h:02d}:{minuto:02d}:00"
            
            dialogo.destroy()
            self.aplicar_nova_data(nova_data)
        else:
            dialogo.destroy()

    def aplicar_nova_data(self, nova_data_string):
        print(f"Tentando alterar para: {nova_data_string}")
        terminal = shutil.which("lxterminal") or shutil.which("x-terminal-emulator") or shutil.which("xterm")
        
        if terminal:
            comando_shell = (
                f"sudo timedatectl set-ntp false; "
                f"sudo date -s '{nova_data_string}'; "
                f"echo '--- Data Alterada com Sucesso ---'; "
                f"echo 'Pressione Enter para fechar'; "
                f"read input"
            )
            
            subprocess.Popen([terminal, "-e", f"bash -c \"{comando_shell}\""])
        else:
            print("Terminal não encontrado para ajustar data.")

    # --- Demais Funções ---

    def aumentar_volume(self, widget):
        # Ajuste aqui se necessário (HDMI, PCM, Master)
        os.system("amixer sset HDMI 5%+") 

    def diminuir_volume(self, widget):
        os.system("amixer sset HDMI 5%-")

    def configurar_wifi(self, widget):
        terminal = shutil.which("lxterminal") or shutil.which("x-terminal-emulator") or shutil.which("xterm")
        if terminal:
            subprocess.Popen([terminal, "-e", "nmtui"])

    def configurar_bluetooth_tui(self, widget):
        terminal = shutil.which("lxterminal") or shutil.which("x-terminal-emulator") or shutil.which("xterm")
        if shutil.which("bluetuith") and terminal:
            subprocess.Popen([terminal, "-e", "bluetuith"])
        else:
            print("Erro: Bluetuith ou Terminal não encontrado.")

    def configurar_bluetooth_gui(self, widget):
        if shutil.which("blueman-manager"):
            subprocess.Popen(["blueman-manager"])
        else:
            print("Erro: Blueman-manager não encontrado.")

    def ao_pressionar_tecla(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        
        if keyname in ["Down", "Up"]:
            foco_atual = self.get_focus()
            botoes = self.box.get_children()
            
            # Filtra para ter certeza que só pegamos botões (caso tenha labels soltas)
            # Mas no layout atual todos os filhos de 'box' são botões
            
            if foco_atual not in botoes:
                botoes[0].grab_focus()
                return True
            
            indice = botoes.index(foco_atual)
            
            if keyname == "Down":
                proximo = (indice + 1) % len(botoes)
            else: 
                proximo = (indice - 1) % len(botoes)
            
            botoes[proximo].grab_focus()
            return True 
        return False

# --- Inicia o Programa ---
win = PainelAcessivel()
win.show_all()
Gtk.main()
