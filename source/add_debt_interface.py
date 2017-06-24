# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_debt.ui'
#
# Created: Fri Jun 23 18:33:45 2017
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(255, 244)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.btn_save_edit = QtGui.QPushButton(self.centralwidget)
        self.btn_save_edit.setGeometry(QtCore.QRect(20, 170, 221, 23))
        self.btn_save_edit.setObjectName(_fromUtf8("btn_save_edit"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 30, 27, 31))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.cmb_type = QtGui.QComboBox(self.centralwidget)
        self.cmb_type.setGeometry(QtCore.QRect(72, 12, 161, 51))
        self.cmb_type.setObjectName(_fromUtf8("cmb_type"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(21, 70, 211, 84))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.spn_year_edit = QtGui.QSpinBox(self.widget)
        self.spn_year_edit.setMinimum(2017)
        self.spn_year_edit.setMaximum(2100)
        self.spn_year_edit.setObjectName(_fromUtf8("spn_year_edit"))
        self.gridLayout.addWidget(self.spn_year_edit, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.cmb_month = QtGui.QComboBox(self.widget)
        self.cmb_month.setObjectName(_fromUtf8("cmb_month"))
        self.gridLayout.addWidget(self.cmb_month, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.ln_summ = QtGui.QLineEdit(self.widget)
        self.ln_summ.setObjectName(_fromUtf8("ln_summ"))
        self.gridLayout.addWidget(self.ln_summ, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 255, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Добавить долг", None))
        self.btn_save_edit.setText(_translate("MainWindow", "ОК", None))
        self.label_4.setText(_translate("MainWindow", "Тип:", None))
        self.label_2.setText(_translate("MainWindow", "Год:", None))
        self.label.setText(_translate("MainWindow", "Месяц:", None))
        self.label_3.setText(_translate("MainWindow", "Сумма:", None))

