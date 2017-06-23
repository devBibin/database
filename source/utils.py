#! /usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore as qc

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
    return lst

def pack_into_years(past_years):
    lst_fields = []
    i = 0
    flag = True
    for el in past_years:
        for i in range(len(lst_fields)):
            if ((lst_fields[i].get("period") == "01."+str(el.get("year"))[2:]+"-12."+str(el.get("year"))[2:]) and (lst_fields[i].get("type") == el.get("type"))):
                lst_fields[i]["sum"] = lst_fields[i].get("sum")+ el.get("sum")
                flag = False
        if (flag):
            fields = {}
            fields["period"] = "01."+str(el.get("year"))[2:]+"-12."+str(el.get("year"))[2:]
            fields["sum"] = el.get("sum")
            fields["type"] = el.get("type")
            lst_fields.append(fields)
        flag = True
    return lst_fields

def split_debts(debts_list, current_year):
    lst_current_year = []
    lst_past_years = []
    lst_temp = []
    for el in debts_list:
        if (el.get("year") == ""):
            lst_past_years.append(el)
        else:
            if (el.get("year") == current_year):
                lst_current_year.append(el)
            if (el.get("year") < current_year):
                lst_temp.append(el)
    lst_sorted_from_2017 = pack_into_years(lst_temp)
    return lst_current_year, lst_past_years, lst_sorted_from_2017

def set_summ_lst(elements, lst):
    for el in elements:
        for i in range(len(lst)):
            if (lst[i].get("type") == el.get("type")):
                lst[i]["sum"] = lst[i].get("sum") + el.get("sum")
                break

def get_summ_debts(lst_elements, lst):
    for el in lst_elements:
        set_summ_lst(el, lst)

def init_res_lst(header):
    res_lst = []
    for i in range(1,len(header)):
        fields = {}
        fields["type"] = header[i]
        fields["sum"] = 0
        res_lst.append(fields)
    return res_lst

def get_total(lst):
    summ = 0
    for el in lst:
        summ = summ + el.get("sum")
    return summ