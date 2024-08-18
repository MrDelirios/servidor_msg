import sys
import threading
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QSize
from App import Ui_Inicial  # Importa a classe gerada pelo pyside6-uic
from log import Ui_log
from clienteui import Ui_cliente
from cliente import Cliente
from servidor import Servidor

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Inicial()
        self.ui.setupUi(self)  # Inicializa a interface gráfica
        
        self.cliente_instance = None
        
        self.ui.InciarServidor.clicked.connect(self.log)
        self.ui.Conectar.clicked.connect(self.cliente)
        
    def log(self):
        self.ui = Ui_log()
        self.ui.setupUi(self)
        
        Tservidor = threading.Thread(target=Servidor(self.write_to_text_area).start)
        Tservidor.start()
    
    def cliente(self):
        self.setStyleSheet("")
        self.setWindowFlags(Qt.Window)  # Remove flags anteriores
        self.setMinimumSize(QSize(400, 300))  # Tamanho mínimo para a tela do cliente
        self.setMaximumSize(QSize(16777215, 16777215))  # Permite maximizar
        self.ui = Ui_cliente()
        self.ui.setupUi(self)
        self.show()

        
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
    
    def write_to_text_area(self, message):
        self.ui.Log.append(message)
        
    def keyPressEvent(self, event):
        # Verifica se a tecla pressionada é "Enter"
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            # Emite o sinal clicked do botão
            self.ui.Enviar.click()
    
    def closeEvent(self, event):
        # Desconectar do servidor quando a janela for fechada
        if self.cliente_instance:  # Verifica se o cliente foi inicializado
            self.cliente_instance.disconnect()
        event.accept()  # Aceita o evento de fechamento


        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
