import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from App import Ui_Inicial  # Importa a classe gerada pelo pyside6-uic
from log import Ui_log
from clienteui import Ui_cliente
from cliente import Cliente

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Inicial()
        self.ui.setupUi(self)  # Inicializa a interface gráfica
        
        self.ui.InciarServidor.clicked.connect(self.log)
        self.ui.Conectar.clicked.connect(self.cliente)
        
    def log(self):
        self.ui = Ui_log()
        self.ui.setupUi(self)
    
    def cliente(self):
        self.ui = Ui_cliente()
        self.ui.setupUi(self)
        cliente = Cliente()
        cliente.start()

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
