#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui as qg
from PyQt4 import QtCore
import card_client_interface as cci
import search_client_handler as sch
import add_debt_handler as adh
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
        u"Вывоз"+"\n"+u"мусора, руб."]

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
        self.spn_year.valueChanged.connect(self.updClientCard)

    def addBack1Row(self):
        self.tbl_back1.setRowCount(self.tbl_back1.rowCount()+ 1)

    def addBack2Row(self):
        self.tbl_back2.setRowCount(self.tbl_back2.rowCount()+ 1)

    def saveInfo(self):
        client_fields = self.getPersonInfo()
        debtfront_fields = self.getTableInfo(self.tbl_front ,2, 13, 1, self.tbl_front.columnCount(), self.getFrontCell)
        debtback1_fields = self.getTableInfo(self.tbl_back1, 1, self.tbl_back1.rowCount(), 0, self.tbl_back1.columnCount(), self.getBack1Cell)
        target_contribution_fields = self.getTableInfo(self.tbl_back2, 1, self.tbl_back2.rowCount(), 0, self.tbl_back2.columnCount(), self.getBack2Cell)
        if (client_fields is not None) and (debtfront_fields is not None) and (debtback1_fields is not None) and (target_contribution_fields is not None):
            if (self.id == 0):
                person_id = db.insert_person(client_fields)
                for el in debtfront_fields: db.insert_debt(el, person_id)
                for el in debtback1_fields: db.insert_debt(el, person_id)
                for el in target_contribution_fields: db.insert_target_contribution(el, self.id)
                info_str = u"Данные клиента "+qstr_to_str(client_fields.get("name")+" "+client_fields.get("surname")) + u" успешно добавлены в базу данных."
                self.showDialog(qg.QMessageBox.Information,info_str,u"Клиент добавлен")
            else:
                db.update_person(client_fields, self.id)
                db.delete_target_contribution_by_id(self.id)
                db.delete_debts_by_id(self.id, int(self.spn_year.value()))
                for el in debtfront_fields: db.insert_debt(el, self.id)
                for el in debtback1_fields: db.insert_debt(el, self.id)
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
        fields["is_TSG_member"] = self.chck_is_member.isChecked()
        fields["is_rubbish_user"] = self.chck_is_rubbish.isChecked()
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
            fields["period"] = ""
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
                fields["year"] = ""
                fields["month"] = ""
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
        self.chck_is_member.setChecked(fields["is_TSG_member"]) 
        self.chck_is_rubbish.setChecked(fields["is_rubbish_user"]) 

    def setTableInfo(self, fields_list, tbl, setData, start_row = 0, finish_row = float("Inf")):
        i = start_row
        for el in (fields_list):
            row = setData(el, i, tbl)
            i = i + 1

    def setFrontRow(self, fields, i, tbl):
        row = fields.get("month") + 1
        column = self.front_table_upper.index(fields.get("type"))
        tbl.setItem(row,column,qg.QTableWidgetItem(str(fields.get("sum"))))
        return row

    def getperiodRow(self, tbl, period):
        for i in range (1, tbl.rowCount()):
            if (qstr_to_str(tbl.item(i,0).text()) == period):
                return i
            if (qstr_to_str(tbl.item(i,0).text()) == ""):
                return i
        return i

    def setBack1Row(self, fields, i, tbl):
        row = self.getperiodRow(tbl, fields.get("period"))
        tbl.setItem(row,0,qg.QTableWidgetItem(fields.get("period")))
        column = self.back1_table_upper.index(fields.get("type"))
        tbl.setItem(row,column,qg.QTableWidgetItem(str(fields.get("sum"))))
        return row

    def setBack2Row(self, fields, i, tbl):
        tbl.setItem(i,0,qg.QTableWidgetItem(fields.get("name")))
        tbl.setItem(i,1,qg.QTableWidgetItem(str(fields.get("sum"))))
        return i

    def updClientCard(self):
        self.cleanTable(self.tbl_front, 1)
        self.cleanTable(self.tbl_back1, 0)
        self.setUneditableFrontItems(self.tbl_front)
        if (self.id != 0):
            current_year_debts, defined_debts, calculated_debts= split_debts(db.get_debts_by_id(self.id), int(self.spn_year.value()))
            self.setTableInfo(current_year_debts, self.tbl_front, self.setFrontRow, 1)
            self.setTableInfo(defined_debts, self.tbl_back1, self.setBack1Row, 1)
            self.calculateFrontTable(defined_debts, calculated_debts, current_year_debts)

    def showClientCard(self):
        indexes = self.window2.tbl_search_res.selectionModel().selectedRows()
        if (len(indexes) > 1):
            self.showAddDebtsWindow()
        else:
            self.id = self.window2.id_lst[indexes[0].row()-1]
            client_info = db.get_person_by_id(self.id)
            current_year_debts, defined_debts, calculated_debts= split_debts(db.get_debts_by_id(self.id), int(self.spn_year.value()))
            target_contribution_info = db.get_target_contribution_by_id(self.id)
            self.setPersonInfo(client_info)
            self.setTableInfo(target_contribution_info, self.tbl_back2, self.setBack2Row, 1, self.tbl_back2.rowCount())
            self.setTableInfo(current_year_debts, self.tbl_front, self.setFrontRow, 1)
            self.setTableInfo(defined_debts, self.tbl_back1, self.setBack1Row, 1)
            self.calculateFrontTable(defined_debts, calculated_debts, current_year_debts)
            self.window2.close()

    def calculateFrontTable(self, defined_debts, calculated_debts, current_year_debts):
        lst_past_year_debts = init_res_lst(self.front_table_upper)
        get_summ_debts([calculated_debts, defined_debts], lst_past_year_debts)
        for i in range(1, len(self.front_table_upper)):
            self.tbl_front.setItem(1,i,self.createUnEditableItm(str(lst_past_year_debts[i-1].get("sum"))))
        lst_current_year_debts = init_res_lst(self.front_table_upper)
        get_summ_debts([current_year_debts], lst_current_year_debts)
        for i in range(1, len(self.front_table_upper)):
            self.tbl_front.setItem(14,i,self.createUnEditableItm(str(lst_current_year_debts[i-1].get("sum"))))
        lst_total_debts = init_res_lst(self.front_table_upper)
        get_summ_debts([calculated_debts, defined_debts, current_year_debts], lst_total_debts)
        for i in range(1, len(self.front_table_upper)):
            self.tbl_front.setItem(15,i,self.createUnEditableItm(str(lst_total_debts[i-1].get("sum"))))

    def cleanForm(self):
        self.cleanTable(self.tbl_front, 1)
        self.cleanTable(self.tbl_back1, 0)
        self.cleanTable(self.tbl_back2, 0)
        self.cleanEdits()
        self.id = 0
        self.setUneditableFrontItems(self.tbl_front)

    def cleanTable(self, tbl, start):
        for i in range (1, tbl.rowCount()):
            for j in range (start, tbl.columnCount()):
                tbl.setItem(i,j,qg.QTableWidgetItem(""))

    def setUneditableFrontItems(self, tbl):
        tbl.setItem(1, 1, self.createUnEditableItm("", False))
        tbl.setItem(1, 2, self.createUnEditableItm("", False))
        tbl.setItem(1, 3, self.createUnEditableItm("", False))
        tbl.setItem(14, 1, self.createUnEditableItm("", False))
        tbl.setItem(14, 2, self.createUnEditableItm("", False))
        tbl.setItem(14, 3, self.createUnEditableItm("", False))
        tbl.setItem(15, 1, self.createUnEditableItm("", False))
        tbl.setItem(15, 2, self.createUnEditableItm("", False))
        tbl.setItem(15, 3, self.createUnEditableItm("", False))

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
        fields["is_TSG_member"] = False
        fields["is_rubbish_user"] = False
        self.setPersonInfo(fields)

    def closeEvent(self, event):
        self.window2.close()
        self.window3.close()

# Create uneditable widget
    def createUnEditableItm(self, text, fnt_flag = True):
        itm = qg.QTableWidgetItem()
        itm.setText(text)
        if (fnt_flag):
            font = qg.QFont()
            font.setWeight(65)
            font.setPixelSize(12)
            itm.setFont(font)
        itm = self.unEditItm(itm)
        return itm

    def saveDebts(self):
        try:
            fields = {}
            fields["year"] = self.window3.getYear()
            fields["month"] = self.window3.getMonth()
            fields["sum"] = self.window3.getDebt()
            fields["type"] = self.window3.getType()
            indexes = self.window2.tbl_search_res.selectionModel().selectedRows()
            for i in range(len(indexes)):
                cur_id = self.window2.id_lst[indexes[i].row()-1]
                existing_debt = db.get_debts_by_filters(fields, cur_id)
                print(existing_debt)
                if (existing_debt != None):
                    retval = self.showDialog(qg.QMessageBox.Warning,u"Запись для "+db.get_person_by_id(cur_id).get("surname")+
                        u" уже присутствует и задолженность составляет "+str(existing_debt.get("sum"))+u". Заменить?",u"Внимание!", True)
                    if (retval == 1024):
                        db.update_debt(fields, cur_id)
                else:
                    db.insert_debt(fields, cur_id)
            self.window2.close()
            self.window3.close()
            self.showDialog(qg.QMessageBox.Information,u"Данные о долгах успешно сохранены",u"База данных обновлена")
            self.updClientCard()
        except ValueError, e:
            print(e)
            self.showDialog(qg.QMessageBox.Critical,u"Некорректный формат ввода суммы",u"Ошибка")

# Make widet uneditable
    def unEditItm(self, itm):
        flg = QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
        itm.setFlags(flg)
        return itm

    def showAddDebtsWindow(self):
        self.window3 = adh.addDebt(self.front_table_upper)
        self.window3.btn_save_edit.clicked.connect(self.saveDebts)
        self.window3.show()

    def showSearchWindow(self):
        self.window2 = sch.searchWindow(int(self.spn_year.value()))
        self.window2.btn_edit.clicked.connect(self.showClientCard)
        self.window2.show()

    def showDialog(self, dialog_type, text, title, Cancel_btn_flag = False):
        msg = qg.QMessageBox()
        msg.setIcon(dialog_type)
        msg.setText(text)
        msg.setWindowTitle(title)
        if (Cancel_btn_flag == True):
            msg.setStandardButtons(qg.QMessageBox.Ok | qg.QMessageBox.Cancel)
        else:
            msg.setStandardButtons(qg.QMessageBox.Ok)
        retval = msg.exec_()
        return retval