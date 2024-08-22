import sys
import threading
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog
from PySide6.QtCore import Qt
from App import Ui_Inicial  # Importa a classe gerada pelo pyside6-uic
from log import Ui_log
from clienteui import Ui_cliente, InputDialog
from cliente import Cliente
from servidor import Servidor

class Serv(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_log()
        self.ui.setupUi(self)
    
        self.serv = Servidor(self.write_to_text_area)
        Tservidor = threading.Thread(target=self.serv.start)
        Tservidor.start()
    
    def write_to_text_area(self, message):
        self.ui.Log.append(message)
    
    def closeEvent(self, event):
        if self.serv:
            self.serv.stop()  # Supondo que você tenha um método para parar o servidor
        QApplication.quit()  # Encerra a aplicação
        event.accept()


class Client(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_cliente()
        self.ui.setupUi(self)
        
        self.cliente_instance = Cliente(self.write_to_text_area)
        Tcliente = threading.Thread(target=self.cliente_instance.start)
        Tcliente.start()
        
        self.ui.items = self.cliente_instance.sala
        self.ui.model.setStringList(self.ui.items)
                
        self.ui.Enviar.clicked.connect(self.envia_mensagem)
        self.ui.definir.clicked.connect(self.definir_senha)
        self.ui.criar.clicked.connect(self.criar_sala)
        
    def envia_mensagem(self):
        if self.cliente_instance is not None:  # Verifica se o cliente_instance foi criado
            mensagem = self.ui.Input.text()
            if mensagem:  # Verifica se a mensagem não está vazia
                self.cliente_instance.enviar_mensagens(mensagem)
                self.ui.Input.clear()
    
    def definir_senha(self):
        dialog = InputDialog(self)
        if dialog.exec() == QDialog.Accepted:
            user_input = dialog.get_input()
            self.cliente_instance.senha = user_input
            self.ui.definir.setText(user_input)

    def criar_sala(self):
        dialog = InputDialog(self)
        dialog.label.setText("Nome da sala:")
        if dialog.exec() == QDialog.Accepted:
            nome_sala = dialog.get_input()
            comando = f"/criar_sala {nome_sala}"
            self.cliente_instance.cliente_socket.send(comando.encode('utf-8'))
            # Atualize a lista de salas após o comando ser enviado
            self.atualiza_salas()


    def keyPressEvent(self, event):
        # Verifica se a tecla pressionada é "Enter"
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            # Emite o sinal clicked do botão
            self.ui.Enviar.click()
    
    def closeEvent(self, event):
        if self.cliente_instance:
            self.cliente_instance.disconnect()
        QApplication.quit()  # Encerra a aplicação
        event.accept()
    
    def write_to_text_area(self, message):
        self.ui.Log.append(message)
    
    def atualiza_salas(self):
        self.cliente_instance.cliente_socket.send("/get".encode('utf-8'))
        self.ui.items = self.cliente_instance.sala
        self.ui.model.setStringList(self.ui.items)

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Inicial()
        self.ui.setupUi(self)
        
        self.ui.InciarServidor.clicked.connect(self.start_server)
        self.ui.Conectar.clicked.connect(self.connect_client)
        
    def start_server(self):
        self.serv_window = Serv()  # Cria uma instância de Serv
        self.serv_window.show()
        self.hide()  # Esconde a janela principal

    def connect_client(self):
        self.client_window = Client()  # Cria uma instância de Client
        self.client_window.show()
        self.hide()  # Esconde a janela principal

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
