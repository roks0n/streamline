#
#   Copyright (C) 2014  Miha Zelnik
#

from __future__ import absolute_import
from flask import current_app
import rethinkdb as r


def connect():
    global conn
    conn = r.connect(host='localhost', port=28015)
    return conn


def db_list():
    return r.db_list().run(conn)


def db_exist(db_name):
    if db_name in db_list():
        return True
    else:
        return False


def db_create(db_name):
    if not db_exist(db_name):
        return r.db_create(db_name).run(conn)


def db_drop(db_name):
    return r.db_drop(db_name).run(conn)


def table_list(db_name):
    return r.db(db_name).table_list().run(conn)


def table_exist(db_name, table_name):
    if table_name in table_list(db_name):
        return True
    else:
        return False


def table_create(db_name, table_name, primary_key='id'):
    if not table_exist(db_name, table_name):
        return r.db(db_name).table_create(table_name, primary_key=primary_key).run(conn)


def table_drop(db_name, table_name):
    return r.db(db_name).table_drop(table_name).run(conn)


def insert(db_name, table_name, item):
    return r.db(db_name).table(table_name).insert(item).run(conn)


def get(db_name, table_name, id):
    return r.db(db_name).table(table_name).get(id).run(conn)


def get_all(db_name, table_name):
    return r.db(db_name).table(table_name).run(conn)


def get_filter(db_name, table_name, query, limit=None, order_by=None, sort_order='desc'):
    items = []

    if limit:
        if order_by:
            if 'asc' in sort_order:
                query = r.db(db_name).table(table_name).filter(query).order_by(r.asc(order_by)).limit(limit).run(conn)
            else:
                query = r.db(db_name).table(table_name).filter(query).order_by(r.desc(order_by)).limit(limit).run(conn)
        else:
            query = r.db(db_name).table(table_name).filter(query).limit(limit).run(conn)
    else:
        query = r.db(db_name).table(table_name).filter(query).run(conn)

    for x in query:
        items.append(x)
    return items


def find_item(db_name, table_name, key, value):
    return r.db(db_name).table(table_name).filter(r.row[key].eq(value)).run(conn)


# USER

def email_exist(email):
    if r.db(current_app.config['DATABASE']).table(current_app.config['USER_TABLE']).filter(r.row['email'].eq(email)).count().run(conn) > 0:
        return True
    else:
        return False


def username_exist(username):
    if r.db(current_app.config['DATABASE']).table(current_app.config['USER_TABLE']).get(username).run(conn):
        return True
    else:
        return False


def create_user(user):
    return insert(current_app.config['DATABASE'], current_app.config['USER_TABLE'], user)


def get_user_data(username):
    return get(current_app.config['DATABASE'], current_app.config['USER_TABLE'], username)


def get_password(username):
    return get(current_app.config['DATABASE'], current_app.config['USER_TABLE'], username)['password']


def get_role(username):
    return get(current_app.config['DATABASE'], current_app.config['USER_TABLE'], username)['type']


def delete_user(username):
    return r.db(current_app.config['DATABASE']).table(current_app.config['USER_TABLE']).get(username).delete().run(conn)


def update_user(username, email, role, password=None):
    if password:
        return r.db(current_app.config['DATABASE']).table(current_app.config['USER_TABLE']).get(username).update({ 'email': email, 'type': role, 'password': password }).run(conn)
    return r.db(current_app.config['DATABASE']).table(current_app.config['USER_TABLE']).get(username).update({ 'email': email, 'type': role }).run(conn)
