# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'search_window.ui'
#
# Created: Tue Jun 20 17:08:03 2017
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
        MainWindow.resize(1039, 394)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tbl_search_res = QtGui.QTableWidget(self.centralwidget)
        self.tbl_search_res.setGeometry(QtCore.QRect(10, 100, 1011, 231))
        self.tbl_search_res.setSizeIncrement(QtCore.QSize(0, 0))
        self.tbl_search_res.setBaseSize(QtCore.QSize(0, 0))
        self.tbl_search_res.setRowCount(0)
        self.tbl_search_res.setColumnCount(0)
        self.tbl_search_res.setObjectName(_fromUtf8("tbl_search_res"))
        self.tbl_search_res.horizontalHeader().setVisible(False)
        self.tbl_search_res.horizontalHeader().setCascadingSectionResizes(False)
        self.tbl_search_res.horizontalHeader().setStretchLastSection(False)
        self.tbl_search_res.verticalHeader().setVisible(False)
        self.tbl_search_res.verticalHeader().setCascadingSectionResizes(False)
        self.tbl_search_res.verticalHeader().setDefaultSectionSize(20)
        self.tbl_search_res.verticalHeader().setHighlightSections(False)
        self.tbl_search_res.verticalHeader().setSortIndicatorShown(False)
        self.tbl_search_res.verticalHeader().setStretchLastSection(False)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 81, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.ln_name = QtGui.QLineEdit(self.centralwidget)
        self.ln_name.setGeometry(QtCore.QRect(110, 20, 113, 23))
        self.ln_name.setObjectName(_fromUtf8("ln_name"))
        self.btn_edit = QtGui.QPushButton(self.centralwidget)
        self.btn_edit.setGeometry(QtCore.QRect(20, 340, 121, 31))
        self.btn_edit.setObjectName(_fromUtf8("btn_edit"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 81, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.ln_adress = QtGui.QLineEdit(self.centralwidget)
        self.ln_adress.setGeometry(QtCore.QRect(110, 50, 113, 23))
        self.ln_adress.setText(_fromUtf8(""))
        self.ln_adress.setObjectName(_fromUtf8("ln_adress"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Фамилия:", None))
        self.btn_edit.setText(_translate("MainWindow", "Редактировать", None))
        self.label_2.setText(_translate("MainWindow", "Адрес:", None))

