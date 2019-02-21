#!/usr/bin/env python
import pymysql


def get_conn():
    conn = pymysql.connect(host="localhost",
                           port=3306,
                           user="debian-sys-maint",
                           password="root",
                           database="flaskee",
                           )

    return conn


# def execute(conn, sql):
#    cursor = conn.cursor()
#    cursor.execute(sql)
#    conn.commit()
#    return cursor


def select(cursor,sql):
    cursor.execute(sql)
    n = cursor.fetchone()[0]
    return n


def insert(cursor, sql):
    cursor.execute(sql)


def update(cursor, sql):
    cursor.execute(sql)


