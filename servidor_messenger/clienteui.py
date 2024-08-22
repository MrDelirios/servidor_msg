# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cliente.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QStringListModel)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLineEdit,
    QListView, QMainWindow, QPushButton, QSizePolicy,
    QStackedWidget, QTextEdit, QWidget, QDialog, QVBoxLayout, QLabel)


class Ui_cliente(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(300, 400)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(300, 400))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.Central = QStackedWidget(self.centralwidget)
        self.Central.setObjectName(u"Central")
        sizePolicy.setHeightForWidth(self.Central.sizePolicy().hasHeightForWidth())
        self.Central.setSizePolicy(sizePolicy)
        self.Central.setFrameShape(QFrame.Shape.NoFrame)
        self.Inicial = QWidget()
        self.Inicial.setObjectName(u"Inicial")
        self.gridLayout = QGridLayout(self.Inicial)
        self.gridLayout.setObjectName(u"gridLayout")
        
        self.listView = QListView(self.Inicial)
        self.listView.setObjectName(u"listView")
        self.listView.setGeometry(QRect(0, 0, 281, 351))
        self.listView.setSelectionMode(QListView.SingleSelection)  # Seleção de um item por vez
        
        self.model = QStringListModel()
        self.items = []
        self.model.setStringList(self.items)
        self.listView.setModel(self.model)
        
        self.selection_model = self.listView.selectionModel()
        self.current_index = 0
        self.select_item(self.current_index)
        
         # Inicializar a seleção
        self.selection_model = self.listView.selectionModel()
        self.current_index = 0
        self.select_item(self.current_index)
        
        #self.selection_model.selectionChanged.connect(self.on_selection_changed)
        self.model.modelReset.connect(self.on_model_reset)


        self.gridLayout.addWidget(self.listView, 0, 0, 1, 2)

        self.definir = QPushButton(self.Inicial)
        self.definir.setObjectName(u"definir")

        self.gridLayout.addWidget(self.definir, 1, 0, 1, 1)

        self.criar = QPushButton(self.Inicial)
        self.criar.setObjectName(u"criar")

        self.gridLayout.addWidget(self.criar, 1, 1, 1, 1)

        self.Central.addWidget(self.Inicial)
        self.Chat = QWidget()
        self.Chat.setObjectName(u"Chat")
        self.Log = QTextEdit(self.Chat)
        self.Log.setObjectName(u"Log")
        self.Log.setGeometry(QRect(0, 0, 281, 351))
        sizePolicy.setHeightForWidth(self.Log.sizePolicy().hasHeightForWidth())
        self.Log.setSizePolicy(sizePolicy)
        self.Log.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.Central.addWidget(self.Chat)

        self.gridLayout_2.addWidget(self.Central, 0, 0, 1, 2)

        self.Input = QLineEdit(self.centralwidget)
        self.Input.setObjectName(u"Input")

        self.gridLayout_2.addWidget(self.Input, 1, 0, 1, 1)

        self.Enviar = QPushButton(self.centralwidget)
        self.Enviar.setObjectName(u"Enviar")

        self.gridLayout_2.addWidget(self.Enviar, 1, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.Central.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"BlakeMSG", None))
        self.definir.setText(QCoreApplication.translate("MainWindow", u"Definir Senha", None))
        self.criar.setText(QCoreApplication.translate("MainWindow", u"Criar Sala", None))
        self.Enviar.setText(QCoreApplication.translate("MainWindow", u"Enviar", None))
    # retranslateUi

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.navigate_up()
        elif event.key() == Qt.Key_Down:
            self.navigate_down()
        else:
            super().keyPressEvent(event)

    def navigate_up(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.select_item(self.current_index)

    def navigate_down(self):
        if self.current_index < len(self.items) - 1:
            self.current_index += 1
            self.select_item(self.current_index)

    def select_item(self, index):
        self.listView.setCurrentIndex(self.model.index(index, 0))
        self.listView.scrollTo(self.listView.currentIndex())  # Garante que o item esteja visível

    """def on_selection_changed(self):
        selected_indexes = self.selection_model.selectedIndexes()
        if selected_indexes:
            selected_text = self.model.data(selected_indexes[0])
            print(self, "Item Selecionado", f"Item selecionado: {selected_text}")"""
    
    def on_model_reset(self):
        self.listView.setModel(self.model)
    
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