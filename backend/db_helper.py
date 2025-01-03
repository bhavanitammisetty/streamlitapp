import mysql.connector 
from contextlib import contextmanager
import datetime
from logging_setup import setup_logger
logger=setup_logger('db_helper')

@contextmanager
def getdb_cursor(commit=False):
    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@009",
        database="expense_manager"
    )
    cursor = mydb.cursor(dictionary=True)
    yield cursor
    if commit:
        mydb.commit()
    cursor.close()
    mydb.close()

def fetch_expense_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with getdb_cursor() as cursor:
        cursor.execute("SELECT * FROM expense WHERE expense_date = %s", (expense_date,))
        data = cursor.fetchall()
        return data


def delete_expense_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}") 
    with getdb_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expense WHERE expense_date = %s", (expense_date,))


def insert_expense(expense_date, salary, category, amount, gender, description, payment_method, vendor, account, notes):
    logger.info(f"insert_expense called with date: {expense_date}, salary:{salary},category: {category}, amount: {amount}, gender: {gender}, description: {description}, payment_method: {payment_method}, vendor: {vendor}, account: {account}, notes: {notes}")
    
    with getdb_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expense (expense_date,salary, category, amount, gender, description, payment_method, vendor, account, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (expense_date,  category, amount, gender, description, payment_method, vendor, account, notes)
        )

def insert_contactform(name,emailcontact,notes):
    logger.info(f"insert_contactform  Name:{name},email:{emailcontact},Note:{notes}")
    with getdb_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO contactform_new (name,emailcontact,notes) VALUES (%s,%s,%s)",
            (name,emailcontact,notes)
        )
       
    
def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
    with getdb_cursor() as cursor:
        cursor.execute(
            '''SELECT *
               FROM expense WHERE expense_date
               BETWEEN %s and %s  
            ;''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data
      
if __name__ == "__main__":
  
    expenses = fetch_expense_for_date('2024-05-22') 
    print(expenses)
    summary = fetch_expense_summary("2024-01-15", "2024-03-10")
    print(summary)
    # salary_year_Month = "2024 january"
    # salary = 50000
    # insert_salary(salary_year_Month,salary)
    # print(f"Salary inserted:{salary_year_Month} {salary}")
    # for record in summary:
    #     print(record) 
    