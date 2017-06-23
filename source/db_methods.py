#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
from utils import *

def get_db():
    con = sqlite3.connect('TSG.db')
    return con

def db_decorator(func):
    def f(*args, **kwargs):
        db = get_db()
        db.row_factory = dict_factory
        cursor = db.cursor()

        try:
            res = func(db, cursor, *args, **kwargs)
        except sqlite3.Error as er:
            print 'er:', er.message
            return False
        cursor.close()
        return res
    return f

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@db_decorator
def insert_person(db, cursor, fields):
    cursor.execute("""insert into person (name,second_name,surname,street,house,building,ph_home,ph_mobile,ph_work,email, is_TSG_member, is_rubbish_user) 
        values (?,?,?,?,?,?,?,?,?,?,?,?)""",
     (qstr_to_str(fields.get("name")),
    qstr_to_str(fields.get("second_name")),
    qstr_to_str(fields.get("surname")),
    qstr_to_str(fields.get("street")),
    qstr_to_str(fields.get("house")),
    qstr_to_str(fields.get("building")),
    qstr_to_str(fields.get("ph_home")),
    qstr_to_str(fields.get("ph_mobile")),
    qstr_to_str(fields.get("ph_work")),
    qstr_to_str(fields.get("email")),
    qstr_to_str(fields.get("is_TSG_member")),
    qstr_to_str(fields.get("is_rubbish_user")),)
    )
    db.commit()
    cursor.execute("""select * FROM person ORDER BY id DESC LIMIT 1""")
    return cursor.fetchone()["id"]

@db_decorator
def insert_debt(db, cursor, fields,person_id):
    cursor.execute("""insert into debts (year, month, period, type, sum, person_id) 
        values (?,?,?,?,?,?)""",
     (qstr_to_str(fields.get("year")),
    qstr_to_str(fields.get("month")),
    qstr_to_str(fields.get("period")),
    qstr_to_str(fields.get("type")),
    qstr_to_str(fields.get("sum")),
    person_id,)
    )
    db.commit()
    return cursor.rowcount > 0

@db_decorator
def insert_target_contribution(db, cursor, fields, person_id):
    cursor.execute("""insert into target_contribution (name, sum, person_id) 
        values (?,?,?)""",
     (qstr_to_str(fields.get("name")),
    qstr_to_str(fields.get("sum")),
    person_id,)
    )
    db.commit()
    return cursor.rowcount > 0


@db_decorator
def update_debt(db, cursor, fields, person_id):
    cursor.execute("""update debts set sum = ? where person_id = ? and year = ? and month = ? and type = ?""",
     (fields.get("sum"),
    person_id,
    fields.get("year"),
    fields.get("month"),
    qstr_to_str(fields.get("type")),
    ))
    db.commit()
    return cursor.rowcount > 0


@db_decorator
def update_person(db, cursor, fields, pers_id):
    cursor.execute("""update person set name=?,second_name=?,surname=?,street=?,house=?,building=?,ph_home=?,ph_mobile=?,ph_work=?,email=?, 
        is_TSG_member = ?, is_rubbish_user = ?
        where id = ?""",
     (qstr_to_str(fields.get("name")),
    qstr_to_str(fields.get("second_name")),
    qstr_to_str(fields.get("surname")),
    qstr_to_str(fields.get("street")),
    qstr_to_str(fields.get("house")),
    qstr_to_str(fields.get("building")),
    qstr_to_str(fields.get("ph_home")),
    qstr_to_str(fields.get("ph_mobile")),
    qstr_to_str(fields.get("ph_work")),
    qstr_to_str(fields.get("email")),
    qstr_to_str(fields.get("is_TSG_member")),
    qstr_to_str(fields.get("is_rubbish_user")),
    pers_id,)
    )
    db.commit()
    return cursor.rowcount > 0

@db_decorator
def get_persons(db, cursor):
    cursor.execute("""select * from person""",
    )
    return cursor.fetchall()

@db_decorator
def get_person_by_name(db, cursor, name):
    cursor.execute("""select * from person where surname like ?""",
     (qstr_to_str(name),)
    )
    return cursor.fetchall()

@db_decorator
def get_person_by_street(db, cursor, street):
    cursor.execute("""select * from person where street like ?""",
     (qstr_to_str(street),)
    )
    return cursor.fetchall()

@db_decorator
def get_person_by_id(db, cursor, person_id):
    cursor.execute("""select * from person where id=(?)""",
     (person_id,)
    )
    return cursor.fetchone()

@db_decorator
def get_debts_by_id(db, cursor, person_id):
    cursor.execute("""select * from debts where person_id=(?)""",
     (person_id,)
    )
    return cursor.fetchall()

@db_decorator
def get_debts_by_filters(db, cursor, fields, person_id):
    cursor.execute("""select * from debts where person_id=(?) and type = (?) and year = (?) and month = (?)""",
     (qstr_to_str(person_id),
    qstr_to_str(fields.get("type")),
    qstr_to_str(fields.get("year")),
    qstr_to_str(fields.get("month")),)
    )
    return cursor.fetchone()

@db_decorator
def get_target_contribution_by_id(db, cursor, person_id):
    cursor.execute("""select  * from target_contribution where person_id=(?)""",
     (person_id,)
    )
    return cursor.fetchall()

@db_decorator
def delete_target_contribution_by_id(db, cursor, person_id):
    cursor.execute("""delete from target_contribution where person_id =(?)""",
     (person_id,)
    )
    db.commit()
    return cursor.rowcount

@db_decorator
def delete_debts_by_id(db, cursor, person_id, year):
    cursor.execute("""delete from debts where person_id =? and year = ?""",
     (person_id,
    year)
    )
    cursor.execute("""delete from debts where person_id = ? and period <> ?""",
     (person_id,
    "")
    )
    db.commit()
    return cursor.rowcount

@db_decorator
def delete_person_by_id(db, cursor, person_id):
    cursor.execute("""delete from person where id =(?)""",
     (person_id,)
    )
    db.commit()
    return cursor.rowcount