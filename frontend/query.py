import mysql.connector 
import streamlit as st 
# from contextlib import contextmanager
# @contextmanager

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@009",
    database="expense_manager"
)
cur = mydb.cursor()
#fetch 
def view_all_data():
    cur.execute('SELECT * FROM expense' )
    data=cur.fetchall()
    return data

