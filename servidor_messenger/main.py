import sys
import threading
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QSize
from App import Ui_Inicial  # Importa a classe gerada pelo pyside6-uic
from log import Ui_log
from clienteui import Ui_cliente
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
        
        self.ui.Enviar.clicked.connect(self.envia_mensagem)
        
    def envia_mensagem(self):
        if self.cliente_instance is not None:  # Verifica se o cliente_instance foi criado
            mensagem = self.ui.Input.text()
            if mensagem:  # Verifica se a mensagem não está vazia
                self.cliente_instance.enviar_mensagens(mensagem)
                self.ui.Input.clear()
        
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
