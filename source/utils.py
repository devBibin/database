#! /usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore as qc

def is_empty(str):
    if (len(str) == 0):
        return "NULL"
    else:
        return str

def qstr_to_str(qstr):
    if (type(qstr) is qc.QString):
        return str(qstr.toUtf8()).decode('utf-8')
    else:
        return qstr

def parse_period(period, split_symbols):
    if (len(period) != 11):
        raise ValueError("Wrong number of characters")
    lst = []
    cur_element = u""
    for character in period:
        if character in split_symbols:
            lst.append(cur_element)
            cur_element = u""
        else:
            cur_element = cur_element + character
    lst.append(cur_element)

def split_debts(debts_list, current_year):
    lst_current_year = []
    lst_past_years = []
    for el in debts_list:
        if (el.get("year") < current_year) or (el.get("year") == ""):
            lst_past_years.append(el)
        else:
            lst_current_year.append(el)
    #pack_into_quaters(past_years)
    return lst_current_year, lst_past_years