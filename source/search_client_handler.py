#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui as qg
from PyQt4 import QtCore
import search_client_interface as sci
import db_methods as db
from utils import *


class searchWindow(qg.QMainWindow, sci.Ui_MainWindow):
    def fillTables(self, tbl, lst_upper, columnCount=1, rowCount = 1):
        tbl.setRowCount(rowCount)
        tbl.setColumnCount(columnCount)
        for j in range (tbl.columnCount()):
            tbl.setItem(0,j,self.createUnEditableItm(lst_upper[j]))

    def __init__(self, year, parent=None):
        super(self.__class__, self).__init__()
        self.id_lst = []
        self.setupUi(self)
        self.year = year

        self.lst_upper = [ u"Фамилия", 
        u"Имя", 
        u"Отчество",
        u"Член ТСЖ",
        u"Вывоз мусора",
        u"Улица" ,
        u"Дом",
        u"Строение",
        u"Долг за "+str(self.year)+u" год",
        u"Общий долг"]

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.fillTables(self.tbl_search_res, self.lst_upper, 10)
        self.btn_edit.setEnabled(False)
        self.tbl_search_res.setSelectionBehavior(qg.QAbstractItemView.SelectRows)
        self.ln_name.textChanged.connect(self.searchByName)
        self.ln_adress.textChanged.connect(self.searchByStreet)
        self.showAll()

    def showAll(self):
        lst_res = db.get_persons()
        self.displayFilterResults(lst_res)

    def displayFilterResults(self, lst_res):
        if (len(lst_res) > 0):
            self.tbl_search_res.setRowCount(len(lst_res) + 1)
            self.tbl_search_res.selectRow(1)
            self.btn_edit.setEnabled(True)
        else:
            self.tbl_search_res.setRowCount(1)
            self.btn_edit.setEnabled(True)
        i = 1
        for fields in lst_res:
            self.id_lst.append(fields["id"])
            self.tbl_search_res.setItem(i,0,self.createUnEditableItm(fields["surname"]))
            self.tbl_search_res.setItem(i,1,self.createUnEditableItm(fields["name"]))
            self.tbl_search_res.setItem(i,2,self.createUnEditableItm(fields["second_name"]))
            self.tbl_search_res.setItem(i,3,self.createUnEditableItm((lambda x: u"ДА" if x else u"НЕТ")(fields.get("is_TSG_member"))))
            self.tbl_search_res.setItem(i,4,self.createUnEditableItm((lambda x: u"ДА" if x else u"НЕТ")(fields.get("is_rubbish_user"))))
            self.tbl_search_res.setItem(i,5,self.createUnEditableItm(fields["street"]))
            self.tbl_search_res.setItem(i,6,self.createUnEditableItm(fields["house"]))
            self.tbl_search_res.setItem(i,7,self.createUnEditableItm(fields["building"]))
            current_year, defined_debts, calculated_debts = split_debts(db.get_debts_by_id(fields["id"]), self.year)
            self.tbl_search_res.setItem(i,8,self.createUnEditableItm(str(get_total(current_year))))
            self.tbl_search_res.setItem(i,9,self.createUnEditableItm(str(get_total(db.get_debts_by_id(fields["id"])))))
            i = i + 1
        self.tbl_search_res.resizeRowsToContents()

    def searchByName(self):
        name = self.ln_name.text() + "%"
        lst_name = db.get_person_by_name(name)
        self.displayFilterResults(lst_name)

    def searchByStreet(self):
        street = self.ln_adress.text() + "%"
        lst_name = db.get_person_by_street(street)
        self.displayFilterResults(lst_name)


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