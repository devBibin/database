#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui as qg
from PyQt4 import QtCore
import add_debt_interface as adi
import db_methods as db
from utils import *


class addDebt(qg.QMainWindow, adi.Ui_MainWindow):
    def __init__(self, type_lst, parent=None):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.lst = [u"Январь",
        u"Февраль",
        u"Март",
        u"Апрель",
        u"Май",
        u"Июнь",
        u"Июль",
        u"Август",
        u"Сентябрь",
        u"Октябрь",
        u"Ноябрь",
        u"Декабрь"]
        self.type_lst = type_lst[1:]
        for el in self.lst:
            self.cmb_month .addItem(el)
        for el in self.type_lst:
            self.cmb_type.addItem(el)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def showDialog(self, dialog_type, text, title):
        msg = qg.QMessageBox()
        msg.setIcon(dialog_type)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(qg.QMessageBox.Ok)
        retval = msg.exec_()

    def getYear(self):
        return self.spn_year_edit.value()

    def getMonth(self):
        return [self.cmb_month.itemText(i) for i in range(self.cmb_month.count())].index(unicode(self.cmb_month.currentText())) +1

    def getDebt(self):
        return float(self.ln_summ.text())

    def getType(self):
        return self.cmb_type.currentText()