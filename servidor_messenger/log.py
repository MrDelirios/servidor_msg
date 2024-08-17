# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'log.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QTextEdit, QWidget)

class Ui_log(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setMinimumSize(QSize(640, 480))
        MainWindow.setMaximumSize(QSize(640, 480))
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QTextEdit{\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(0, 0, 0);\n"
"}\n"
"")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.Log = QTextEdit(self.centralwidget)
        self.Log.setObjectName(u"Log")
        self.Log.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.gridLayout.addWidget(self.Log, 0, 0, 1, 2)

        self.command = QLineEdit(self.centralwidget)
        self.command.setObjectName(u"command")

        self.gridLayout.addWidget(self.command, 1, 0, 1, 1)

        self.Enviar = QPushButton(self.centralwidget)
        self.Enviar.setObjectName(u"Enviar")

        self.gridLayout.addWidget(self.Enviar, 1, 1, 1, 1)

        self.Encerrar = QPushButton(self.centralwidget)
        self.Encerrar.setObjectName(u"Encerrar")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Encerrar.sizePolicy().hasHeightForWidth())
        self.Encerrar.setSizePolicy(sizePolicy)
        self.Encerrar.setMaximumSize(QSize(191, 31))

        self.gridLayout.addWidget(self.Encerrar, 2, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"BlakeMSG", None))
        self.Enviar.setText(QCoreApplication.translate("MainWindow", u"Enviar", None))
        self.Encerrar.setText(QCoreApplication.translate("MainWindow", u"Encerrar Servidor", None))
    # retranslateUi

