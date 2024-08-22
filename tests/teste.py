from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog, QLineEdit, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Entrada de Texto")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Rótulo
        self.label = QLabel("Digite a senha:")
        layout.addWidget(self.label)
        
        # Campo de entrada
        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit)
        
        # Botões
        self.button_ok = QPushButton("OK")
        self.button_cancel = QPushButton("Cancelar")
        layout.addWidget(self.button_ok)
        layout.addWidget(self.button_cancel)
        
        # Conectar botões aos slots
        self.button_ok.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)
        
        self.setLayout(layout)
    
    def get_input(self):
        return self.line_edit.text()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Janela Principal")
        
        # Layout principal e botão
        layout = QVBoxLayout()
        self.button = QPushButton("Abrir Caixa de Diálogo")
        self.button.clicked.connect(self.show_input_dialog)
        layout.addWidget(self.button)
        
        # Configura a janela central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def show_input_dialog(self):
        dialog = InputDialog(self)
        if dialog.exec() == QDialog.Accepted:
            user_input = dialog.get_input()
            print(f"Texto digitado: {user_input}")

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
