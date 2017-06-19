#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui as qg
from PyQt4 import QtCore
import card_client_interface as cci
import search_client_handler as sci
import db_methods as db
from utils import *


class ClientCard(qg.QMainWindow, cci.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.id = 0
        self.window2 = None

        self.tbl_front.setItem(0,1,self.createUnEditableItm(u"Членские взносы"+"\n"+u"руб."))
        self.tbl_front.setItem(0,2,self.createUnEditableItm(u"Уличное"+"\n"+u"освещение, руб."))
        self.tbl_front.setItem(0,3,self.createUnEditableItm(u"Целевые"+"\n"+u"взносы, руб."))
        self.tbl_front.setItem(0,0,self.createUnEditableItm(u"Наименование"+"\n"+u"платежей"))
        self.tbl_front.setItem(1,0,self.createUnEditableItm(u"Задолженнность"+"\n"+u"на начало года"))
        self.tbl_front.setItem(2,0,self.createUnEditableItm(u"Январь"))
        self.tbl_front.setItem(3,0,self.createUnEditableItm(u"Февраль"))
        self.tbl_front.setItem(4,0,self.createUnEditableItm(u"Март"))
        self.tbl_front.setItem(5,0,self.createUnEditableItm(u"Апрель"))
        self.tbl_front.setItem(6,0,self.createUnEditableItm(u"Май"))
        self.tbl_front.setItem(7,0,self.createUnEditableItm(u"Июнь"))
        self.tbl_front.setItem(8,0,self.createUnEditableItm(u"Июль"))
        self.tbl_front.setItem(9,0,self.createUnEditableItm(u"Август"))
        self.tbl_front.setItem(10,0,self.createUnEditableItm(u"Сентябрь"))
        self.tbl_front.setItem(11,0,self.createUnEditableItm(u"Октябрь"))
        self.tbl_front.setItem(12,0,self.createUnEditableItm(u"Ноябрь"))
        self.tbl_front.setItem(13,0,self.createUnEditableItm(u"Декабрь"))
        self.tbl_front.setItem(14,0,self.createUnEditableItm(u"Итого"))
        self.tbl_front.setItem(15,0,self.createUnEditableItm(u"Всего"))

        self.tbl_back1.setItem(0,0,self.createUnEditableItm(u"Период"))
        self.tbl_back1.setItem(0,1,self.createUnEditableItm(u"Членские взносы"+"\n"+u"руб."))
        self.tbl_back1.setItem(0,2,self.createUnEditableItm(u"Уличное"+"\n"+u"освещение, руб."))
        self.tbl_back1.setItem(0,3,self.createUnEditableItm(u"Целевые"+"\n"+u"взносы, руб."))

        self.tbl_back2.setItem(0,0,self.createUnEditableItm(u"Наименование"))
        self.tbl_back2.setItem(0,1,self.createUnEditableItm(u"Сумма, руб."))

        self.tbl_front.resizeRowsToContents()
        self.tbl_front.resizeColumnsToContents()
        self.tbl_front.setColumnWidth(1,123)
        self.tbl_front.setColumnWidth(2,123)
        self.tbl_front.setColumnWidth(3,123)
        
        self.tbl_back1.resizeRowsToContents()
        self.tbl_back1.resizeColumnsToContents()
        self.tbl_back1.setColumnWidth(0,123)
        self.tbl_back1.setColumnWidth(1,123)
        self.tbl_back1.setColumnWidth(2,123)
        self.tbl_back1.setColumnWidth(3,123)
        self.tbl_back2.resizeRowsToContents()
        self.tbl_back2.resizeColumnsToContents()
        self.tbl_back2.setColumnWidth(0,3*123)
        self.tbl_back2.setColumnWidth(1,123)

        self.btn_save.clicked.connect(self.saveInfo)
        self.btn_search.clicked.connect(self.showSearchWindow)
        self.btn_add_back1.clicked.connect(self.addBack1Row)
        self.btn_add_back2.clicked.connect(self.addBack2Row)

# Create uneditable widget
    def createUnEditableItm(self, text):
        itm = qg.QTableWidgetItem()
        itm.setText(text)
        font = qg.QFont()
        font.setWeight(65)
        font.setPixelSize(12)
        itm.setFont(font)
        itm = self.unEditItm(itm)
        return itm

# Create uneditable widget
    def createEditableItm(self, text):
        itm = qg.QTableWidgetItem()
        itm.setText(text)
        return itm

# Make widet uneditable
    def unEditItm(self, itm):
        flg = QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
        itm.setFlags(flg)
        return itm

    def addBack1Row(self):
        self.tbl_back1.setRowCount(self.tbl_back1.rowCount()+ 1)

    def addBack2Row(self):
        self.tbl_back2.setRowCount(self.tbl_back2.rowCount()+ 1)

    def saveInfo(self):
        client_fields = getPersonInfo()
        debtfront_fields = getListFromTable(self.tbl_front ,1, 13, 1, 4, createFrontField)
        if (self.id == 0):
            db.insert_person(client_fields)
            info_str = u"Данные клиента "+qstr_to_str(client_fields.get("name")+" "+client_fields.get("surname")) + u" успешно добавлены в базу данных."
            self.showDialog(qg.QMessageBox.Information,info_str,u"Клиент добавлен")
        else:
            db.update_person(client_fields, self.id)
            info_str = u"Данные клиента "+qstr_to_str(client_fields.get("name")+" "+client_fields.get("surname")) + u" успешно отредактированы."
            self.showDialog(qg.QMessageBox.Information,info_str,u"Данные обновлены")
        self.cleanForm()

    def getListFromTable(self, tbl, start_row, finish_row, start_column, finish_column, func):
        fields_list = []
        for i in range (start_row, finish_row):
            for j in range (start_column, finish_column):
                fields = func(tbl, i, j)
                if (fields is None):
                    fields_list = []
                    break;
        return fields_list

    def createFrontField(self, tbl, i, j):
        txt = self.getTextFromCell(tbl, i, j)
        if (txt != '0') or (txt != ''):
            fields["year"] = self.spn_year.value()
            fields["month"] = i - 1
            fields["period"] = ""
            fields["type"] = self.tbl.item(0,j).text()
            try:
                fields["sum"] = float(self.tbl.item(i,j).text())
            except ValueError:
                self.showDialog(qg.QMessageBox.Critical,u"Некорректный формат ввода суммы",u"Ошибка")
                return None
        return fields


    def getTextFromCell(self, tbl, i, j):
        return tbl.item(i,j).text()

    def setPersonInfo(self, fields):
        self.ln_name.setText(fields["name"])
        self.ln_secondname.setText( fields["second_name"])
        self.ln_surname.setText( fields["surname"]) 
        self.ln_phone_home.setText( fields["ph_home"]) 
        self.ln_phone_mobile.setText( fields["ph_mobile"])
        self.ln_phone_work.setText( fields["ph_work"])
        self.ln_email.setText( fields["email"]) 
        self.ln_street.setText(  fields["street"]) 
        self.ln_house.setText(fields["house"]) 
        self.ln_building.setText( fields["building"])

    def cleanTable(self, tbl, start):
        for i in range (1, tbl.rowCount()):
            for j in range (start, tbl.ColumnCount()):
                tbl.setItem(i,j,self.createEditableItm(""))

    def cleanEdits(self):
        fields = {}
        fields["name"]  = ""
        fields["second_name"]  = ""
        fields["surname"]  = ""
        fields["ph_home"] = ""
        fields["ph_mobile"] = ""
        fields["ph_work"]  = ""
        fields["email"]  = ""
        fields["street"] = ""
        fields["house"] = ""
        fields["building"]  = ""
        self.setPersonInfo(fields)

    def cleanForm(self):
        self.cleanTable(self.tbl_front, 1)
        self.cleanTable(self.tbl_back1, 0)
        self.cleanTable(self.tbl_back2, 0)
        self.cleanEdits()
        self.id = 0

    def showSearchWindow(self):
        if self.window2 is None:
            self.window2 = sci.searchWindow(self)
            self.window2.btn_edit.clicked.connect(self.searchClose)
        self.window2.show()

    def showDialog(self, dialog_type, text, title):
        msg = qg.QMessageBox()
        msg.setIcon(dialog_type)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(qg.QMessageBox.Ok)
        retval = msg.exec_()

    def searchClose(self):
        indexes = self.window2.tbl_search_res.selectionModel().selectedRows()
        if (len(indexes) > 1):
            self.showDialog(qg.QMessageBox.Critical,u"Были выбраны несколько карточек клиента. Пожалуйста, выберете одну.",u"Ошибка")
        else:
            client_info = db.get_person_by_id(self.window2.tbl_lst[indexes[0].row()-1])
            self.id = self.window2.tbl_lst[indexes[0].row()-1]
            self.setPersonInfo(client_info)
            self.window2.close()

    def closeEvent(self, event):
        if (self.window2 is not None):
            self.window2.close()