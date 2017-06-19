#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui as qg
from PyQt4 import QtCore
import search_client_interface as sci
import db_methods as db


class searchWindow(qg.QMainWindow, sci.Ui_MainWindow):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        self.id_lst = []
        self.setupUi(self)
        self.btn_edit.setEnabled(False)
        self.btn_search.clicked.connect(self.searchClient)
        self.tbl_search_res.setSelectionBehavior(qg.QAbstractItemView.SelectRows)

# Create uneditable widget
    def createUnEditableItm(self, text):
        itm = qg.QTableWidgetItem()
        itm.setText(text)
        itm = self.unEditItm(itm)
        return itm

# Make widet uneditable
    def unEditItm(self, itm):
        flg = QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable  
        itm.setFlags(flg)
        return itm

    def showDialog(self, dialog_type, text, title):
        msg = qg.QMessageBox()
        msg.setIcon(dialog_type)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(qg.QMessageBox.Ok)
        retval = msg.exec_()

    def searchClient(self):
        name = self.ln_name.text()
        lst_name = db.get_person_by_name(name)

        if (len(lst_name) == 0):
            self.showDialog(qg.QMessageBox.Warning,u"Данных удовлетворяющих Вашему запросу не найдено.",u"Клиентов не найдено")
        else:
            self.tbl_search_res.setRowCount(len(lst_name)+1)
            self.tbl_search_res.setColumnCount(3)

            self.tbl_search_res.setItem(0,0,self.createUnEditableItm(u"ФИО"))
            self.tbl_search_res.setItem(0,1,self.createUnEditableItm(u"Телефон"))
            self.tbl_search_res.setItem(0,2,self.createUnEditableItm(u"Долг"))
            i = 1
            for el in lst_name:
                fio = el["name"] +' '+ el["second_name"] +' '+ el["surname"]
                ph = el["ph_mobile"]
                self.id_lst.append(el["id"])
                self.tbl_search_res.setItem(i,0,self.createUnEditableItm(fio))
                self.tbl_search_res.setItem(i,1,self.createUnEditableItm(ph))
                i = i + 1
            self.tbl_search_res.selectRow(1)
            self.tbl_search_res.resizeColumnsToContents()
            self.btn_edit.setEnabled(True)

    def cleanTable(self, tbl, start):
        for i in range (start, tbl.columnCount()):
            for j in range (1, tbl.rowCount()):
                tbl.setItem(j,i,self.createEditableItm(""))

    def cleanForm(self):
        self.tbl_search_res.setRowCount(0)
        self.tbl_search_res.setColumnCount(0)
        self.ln_name.setText("")
        self.btn_edit.setEnabled(False)

    def closeEvent(self, event):
        self.cleanForm()