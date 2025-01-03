import streamlit as st 
from datetime import datetime
import requests

API_URL="http://localhost:8000"
def add_monthSalary():

    with st.form(key="Salary_form"):
                monthly_salary = []
                for i in range(1):
                    year_month = st.text_input("salary_year_Month", placeholder="Enter your year_month", key=f"year_month_{i}", label_visibility="collapsed")
                
                    salary = st.number_input("salary", min_value=0, step=1, value=0, placeholder="Enter salary", key=f"salary_{i}", label_visibility="collapsed")
                    monthly_salary.append({
                        'salary_year_Month': year_month,
                        'salary': salary
                    })
                submit_button = st.form_submit_button("Submit")
                if submit_button:
                    # Send the form data as JSON in the POST request
                    response = requests.post(f"{API_URL}/salary/", json=monthly_salary)
                    
                    if response.status_code == 200:
                        st.success("Salary updated successfully")
                    else:
                        st.error(response)    