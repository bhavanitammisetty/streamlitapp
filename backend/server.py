from fastapi import FastAPI,HTTPException
from datetime import date
import db_helper
from typing import List
from pydantic import BaseModel

#create the app object
app=FastAPI()
#pydantic uses which we want to data validation  here expense_date skip 
class ExpenseS(BaseModel):
    category:str
    salary :int
    amount:int 
    gender:str
    description:str 
    payment_method:str
    vendor:str 
    account:str
    notes:str
    
class DateRange(BaseModel):
    start_date: date
    end_date: date
    
class form(BaseModel):
    
    name:str
    emailcontact:str
    notes:str
   
    
@app.get('/expense/{expense_date}',response_model=List[ExpenseS])
def get_expense(expense_date:date):
    # return f"Received get_expense request{date}"
    expenses=db_helper.fetch_expense_for_date(expense_date)
    return expenses


@app.post("/expense/{expense_date}")
def add_or_update_expense(expense_date:date,expenses:List[ExpenseS]):
   
    # db_helper.delete_expense_for_date(expense_date)   
    for exp in expenses:
        db_helper.insert_expense(expense_date,exp.salary,exp.category,exp.amount,exp.gender,exp.description,exp.payment_method,exp.vendor,exp.account,exp.notes)
    return {"message": "expense data update successfully"}

@app.delete("/expense/{expense_date}")
def delete_expenses(expense_date:date):
    db_helper.delete_expense_for_date(expense_date)  
    return{"message": "expense data delete successfully"}


@app.get("/analytics/{start_date},{end_date}",response_model=List[ExpenseS])
def get_selected_date(start_date:date,end_date:date):
    data = db_helper.fetch_expense_summary(start_date,end_date)
    if not data:
        raise HTTPException(status_code=500, detail="Failed to retrieve expenses from the database.")
    return data

@app.post("/contact/")
def add_or_update_contact(Form:List[form]):
    print(Form)
    # db_helper.delete_expense_for_date(expense_date)   
    for exp in Form:
        db_helper.insert_contactform(exp.name,exp.emailcontact,exp.notes)
    return {"message": "expense data update successfully"}