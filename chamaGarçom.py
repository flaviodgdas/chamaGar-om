import socket
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
# Chama o garçom
class MesaApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Entrada inicial para número da mesa
        self.label = Label(text='Digite o número da mesa:')
        self.layout.add_widget(self.label)

        self.input = TextInput(multiline=False)
        self.layout.add_widget(self.input)

        self.enter_button = Button(text='Entrar')
        self.enter_button.bind(on_press=self.entrar_menu)
        self.layout.add_widget(self.enter_button)

        # Layout do menu
        self.menu_layout = BoxLayout(orientation='vertical')
        self.menu_label = Label(text='Pressione para chamar o garçom')
        self.menu_layout.add_widget(self.menu_label)

        self.chamar_button = Button(text='Chamar Garçom')
        self.chamar_button.bind(on_press=self.chamar_garcom)
        self.menu_layout.add_widget(self.chamar_button)

        self.obrigado_button = Button(text='Obrigado')
        self.obrigado_button.bind(on_press=self.registrar_saida)
        self.obrigado_button.disabled = True  # Desativado até o atendimento
        self.menu_layout.add_widget(self.obrigado_button)

        # Thread para escutar resposta do garçom
        threading.Thread(target=self.escutar_resposta, daemon=True).start()

        return self.layout

    def entrar_menu(self, instance):
        mesa_num = self.input.text.strip()
        if mesa_num.isdigit():
            self.mesa_num = int(mesa_num)
            self.layout.clear_widgets()
            self.layout.add_widget(self.menu_layout)
        else:
            self.label.text = 'Número inválido. Por favor, tente novamente.'

    def chamar_garcom(self, instance):
        host = '127.0.0.1'  # IP do receptor
        port = 12345        # Porta do receptor
        mensagem = f'Mesa {self.mesa_num} está chamando o garçom!'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(mensagem.encode('utf-8'))
            self.menu_label.text = 'Chamando o garçom...'
            self.chamar_button.disabled = True
            print(f'Mensagem enviada: {mensagem}')

    def escutar_resposta(self):
        host = '127.0.0.1'  # IP local para escutar respostas
        port = 12346        # Porta para receber mensagens do garçom
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    mensagem = conn.recv(1024).decode('utf-8')
                    self.menu_label.text = mensagem
                    self.obrigado_button.disabled = False  # Habilita botão "Obrigado"
                    print(f'Resposta recebida: {mensagem}')

    def registrar_saida(self, instance):
        print(f'Número da mesa registrado até sair: {self.mesa_num}')
        self.chamar_button.disabled = False  # Reativa botão "Chamar Garçom"
        self.obrigado_button.disabled = True  # Desativa botão "Obrigado"
        self.menu_label.text = 'Pressione para chamar o garçom'

if __name__ == '__main__':
    MesaApp().run()