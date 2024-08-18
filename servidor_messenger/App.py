# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'App.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLayout, QMainWindow,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Inicial(object):
    def setupUi(self, Inicial):
        if not Inicial.objectName():
            Inicial.setObjectName(u"Inicial")
        Inicial.setWindowModality(Qt.WindowModality.NonModal)
        Inicial.setEnabled(True)
        Inicial.resize(259, 359)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Inicial.sizePolicy().hasHeightForWidth())
        Inicial.setSizePolicy(sizePolicy)
        Inicial.setMinimumSize(QSize(259, 359))
        Inicial.setMaximumSize(QSize(259, 359))
        Inicial.setStyleSheet(u"QMainWindow{\n"
                                "	border-radius: 10px\n"
                                "}\n"
                                "\n"
                                "QWidget{\n"
                                "	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
                                "}")
        self.centralwidget = QWidget(Inicial)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QPushButton{\n"
                                        "	border-radius: 10px;\n"
                                        "	background-color: rgb(0, 0, 0);\n"
                                        "	color: rgb(255, 255, 255);\n"
                                        "}\n"
                                        "QPushButton:hover {\n"
                                        "	border-radius: 10px;\n"
                                        "	background-color: rgb(0, 0, 0);\n"
                                        "	color: rgb(170, 170, 255);\n"
                                        "	font-size: 30px;\n"
                                        "}")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"vertilcalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"System"])
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setStyleSheet(u"font: 700 9pt \"System\";")
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.InciarServidor = QPushButton(self.centralwidget)
        self.InciarServidor.setObjectName(u"InciarServidor")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.InciarServidor.sizePolicy().hasHeightForWidth())
        self.InciarServidor.setSizePolicy(sizePolicy1)
        self.InciarServidor.setCheckable(False)

        self.verticalLayout.addWidget(self.InciarServidor)

        self.Conectar = QPushButton(self.centralwidget)
        self.Conectar.setObjectName(u"Conectar")
        sizePolicy1.setHeightForWidth(self.Conectar.sizePolicy().hasHeightForWidth())
        self.Conectar.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.Conectar)

        Inicial.setCentralWidget(self.centralwidget)

        self.retranslateUi(Inicial)
        QMetaObject.connectSlotsByName(Inicial)
    # setupUi

    def retranslateUi(self, Inicial):
        Inicial.setWindowTitle(QCoreApplication.translate("Inicial", u"BlakeMSG", None))
        self.label.setText(QCoreApplication.translate("Inicial", u"BlakeMSG", None))
        self.InciarServidor.setText(QCoreApplication.translate("Inicial", u"Iniciar Servidor", None))
        self.Conectar.setText(QCoreApplication.translate("Inicial", u"Conectar", None))
    # retranslateUi

