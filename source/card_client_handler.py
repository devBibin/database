#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui as qg
from PyQt4 import QtCore
import card_client_interface as cci
import search_client_handler as sci
import db_methods as db
from utils import *


class ClientCard(qg.QMainWindow, cci.Ui_MainWindow):
    def fillTables(self, tbl, lst_upper, lst_side = []):
        if (len(lst_side) > 0):
            for i in range (1,tbl.rowCount()):
                tbl.setItem(i,0,self.createUnEditableItm(lst_side[i-1]))
        for j in range (tbl.columnCount()):
            tbl.setItem(0,j,self.createUnEditableItm(lst_upper[j]))

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.id = 0
        self.window2 = None

        self.front_table_upper = [ u"Наименование"+"\n"+u"платежей",
        u"Членские взносы"+"\n"+u"руб.",
        u"Уличное"+"\n"+u"освещение, руб.",
        u"Целевые"+"\n"+u"взносы, руб."]

        self.front_table_side = [u"Задолженнность"+"\n"+u"на начало года",
        u"Январь",
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
        u"Декабрь",
        u"Итого:",
        u"Всего"]

        self.back1_table_upper = self.front_table_upper
        self.back1_table_upper[0] = u"Период"

        self.back2_table_upper = [u"Наименование", u"Сумма"]

        self.fillTables(self.tbl_front, self.front_table_upper, self.front_table_side)
        self.fillTables(self.tbl_back1, self.back1_table_upper)
        self.fillTables(self.tbl_back2, self.back2_table_upper)

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

        self.cleanForm()

        self.btn_save.clicked.connect(self.saveInfo)
        self.btn_search.clicked.connect(self.showSearchWindow)
        self.btn_add_back1.clicked.connect(self.addBack1Row)
        self.btn_add_back2.clicked.connect(self.addBack2Row)

    def addBack1Row(self):
        self.tbl_back1.setRowCount(self.tbl_back1.rowCount()+ 1)

    def addBack2Row(self):
        self.tbl_back2.setRowCount(self.tbl_back2.rowCount()+ 1)

    def saveInfo(self):
        client_fields = self.getPersonInfo()
        payment_fields = self.getTableInfo(self.tbl_front ,2, 13, 1, self.tbl_front.columnCount(), self.getFrontCell)
        debt_fields = self.getTableInfo(self.tbl_back1, 1, self.tbl_back1.rowCount(), 0, self.tbl_back1.columnCount(), self.getBack1Cell)
        target_contribution_fields = self.getTableInfo(self.tbl_back2, 1, self.tbl_back2.rowCount(), 0, self.tbl_back2.columnCount(), self.getBack2Cell)
        if (client_fields is not None) and (payment_fields is not None) and (debt_fields is not None) and (target_contribution_fields is not None):
            if (self.id == 0):
                person_id = db.insert_person(client_fields)
                for el in payment_fields: db.insert_payment(el, person_id)
                for el in debt_fields: db.insert_debt(el, person_id)
                for el in target_contribution_fields: db.insert_target_contribution(el, self.id)
                info_str = u"Данные клиента "+qstr_to_str(client_fields.get("name")+" "+client_fields.get("surname")) + u" успешно добавлены в базу данных."
                self.showDialog(qg.QMessageBox.Information,info_str,u"Клиент добавлен")
            else:
                db.update_person(client_fields, self.id)
                db.delete_target_contribution_by_id(self.id)
                db.delete_debts_by_id(self.id)
                db.delete_payments_by_id(self.id)
                for el in payment_fields: db.insert_payment(el, self.id)
                for el in debt_fields: db.insert_debt(el, self.id)
                for el in target_contribution_fields: db.insert_target_contribution(el, self.id)
                info_str = u"Данные клиента "+qstr_to_str(client_fields.get("name")+" "+client_fields.get("surname")) + u" успешно отредактированы."
                self.showDialog(qg.QMessageBox.Information,info_str,u"Данные обновлены")
            self.cleanForm()

    def getPersonInfo(self):
        fields = {}
        fields["name"]  = self.ln_name.text()
        fields["second_name"]  = self.ln_secondname.text()
        fields["surname"]  = self.ln_surname.text()
        fields["ph_home"] = self.ln_phone_home.text()
        fields["ph_mobile"] = self.ln_phone_mobile.text()
        fields["ph_work"]  = self.ln_phone_work.text()
        fields["email"]  = self.ln_email.text()
        fields["street"] = self.ln_street.text()
        fields["house"] = self.ln_house.text()
        fields["building"]  = self.ln_building.text()
        return fields

    def getTableInfo(self, tbl, start_row, finish_row, start_column, finish_column, getfields):
        fields_list = []
        for i in range (start_row, finish_row):
            for j in range (start_column, finish_column):
                fields = getfields(tbl, i, j)
                if (fields == False):
                    return None
                if (len(fields) > 0):
                    fields_list.append(fields)
        return fields_list

    def getFrontCell(self, tbl, i, j):
        fields = {}
        txt = tbl.item(i,j).text()
        if (txt != '0') and (txt != ''):
            fields["year"] = self.spn_year.value()
            fields["month"] = i - 1
            fields["type"] = tbl.item(0,j).text()
            try:
                fields["sum"] = float(tbl.item(i,j).text())
            except ValueError:
                self.showDialog(qg.QMessageBox.Critical,u"Некорректный формат ввода суммы",u"Ошибка")
                return False
        return fields

    def getBack1Cell(self, tbl, i, j):
        fields = {}
        period = qstr_to_str(tbl.item(i,0).text())
        if (j != 0) and (period != ""):
            txt = tbl.item(i,j).text()
            try:
                parse_period(period, ["-","."])
            except ValueError:
                self.showDialog(qg.QMessageBox.Critical,u"Некорректный формат ввода периода в таблице _Расшифровка задолженности на начало года_. Необходим формат: мм.гг-мм.гг",u"Ошибка")
                return False
            if (txt != '0') and (txt != ''):
                fields["period"] = period
                fields["type"] = tbl.item(0,j).text()
                try:
                    fields["sum"] = float(tbl.item(i,j).text())
                except ValueError:
                    self.showDialog(qg.QMessageBox.Critical,u"Некорректный формат ввода суммы",u"Ошибка")
                    return False
        return fields

    def getBack2Cell(self, tbl, i, j):
        fields = {}
        if (j == 0):
            if (tbl.item(i,0).text() != "") and (tbl.item(i,1).text() != "") and (tbl.item(i,1).text() != "0"):
                fields["name"] = tbl.item(i,0).text()
                try:
                    fields["sum"] = float(tbl.item(i,1).text())
                except ValueError:
                    self.showDialog(qg.QMessageBox.Critical,u"Некорректный формат ввода суммы",u"Ошибка")
                    return False
        return fields

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

    def setTableInfo(self, fields_list, tbl, start_row, finish_row, setData):
        if (finish_row - start_row < len(fields_list)):
            tbl.setRowCount(len(fields_list) + 1)
        i = start_row
        for el in (fields_list):
            setData(el, i, tbl)
            i = i + 1

    def setFrontRow(self, fields, i, tbl):
        row = fields.get("month") + 1
        column = self.front_table_upper.index(fields.get("type"))
        tbl.setItem(row,column,qg.QTableWidgetItem(str(fields.get("sum"))))

    def setBack1Row(self, fields, i, tbl):
        tbl.setItem(i,0,qg.QTableWidgetItem(fields.get("period")))
        column = self.back1_table_upper.index(fields.get("type"))
        tbl.setItem(i,column,qg.QTableWidgetItem(str(fields.get("sum"))))

    def setBack2Row(self, fields, i, tbl):
        tbl.setItem(i,0,qg.QTableWidgetItem(fields.get("name")))
        tbl.setItem(i,1,qg.QTableWidgetItem(str(fields.get("sum"))))

    def showClientCard(self):
        indexes = self.window2.tbl_search_res.selectionModel().selectedRows()
        if (len(indexes) > 1):
            self.showDialog(qg.QMessageBox.Critical,u"Были выбраны несколько карточек клиента. Пожалуйста, выберете одну.",u"Ошибка")
        else:
            self.id = self.window2.id_lst[indexes[0].row()-1]
            client_info = db.get_person_by_id(self.id)
            payments = db.get_payments_by_id(self.id)
            past_years = db.get_debts_by_id(self.id)
            target_contribution_info = db.get_target_contribution_by_id(self.id)
            self.setPersonInfo(client_info)
            self.setTableInfo(target_contribution_info, self.tbl_back2, 1, self.tbl_back2.rowCount(), self.setBack2Row)
            self.setTableInfo(payments, self.tbl_front, 1, 100, self.setFrontRow)
            self.setTableInfo(past_years, self.tbl_back1, 1, 100, self.setBack1Row)
            self.window2.close()

    def cleanForm(self):
        self.cleanTable(self.tbl_front, 1)
        self.cleanTable(self.tbl_back1, 0)
        self.cleanTable(self.tbl_back2, 0)
        self.cleanEdits()
        self.id = 0

    def cleanTable(self, tbl, start):
        for i in range (1, tbl.rowCount()):
            for j in range (start, tbl.columnCount()):
                tbl.setItem(i,j,qg.QTableWidgetItem(""))

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

    def closeEvent(self, event):
        if (self.window2 is not None):
            self.window2.close()

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

# Make widet uneditable
    def unEditItm(self, itm):
        flg = QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
        itm.setFlags(flg)
        return itm

    def showSearchWindow(self):
        if self.window2 is None:
            self.window2 = sci.searchWindow(self)
            self.window2.btn_edit.clicked.connect(self.showClientCard)
        self.window2.show()

    def showDialog(self, dialog_type, text, title):
        msg = qg.QMessageBox()
        msg.setIcon(dialog_type)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(qg.QMessageBox.Ok)
        retval = msg.exec_()