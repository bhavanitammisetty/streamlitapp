import streamlit as st
from streamlit_custom_toggle import st_custom_toggle
from datetime import datetime
import requests
import time

API_URL = "http://localhost:8000"
categories = [
    "Rent", "Food", "Shopping", "Entertainment", "Utilities", "Transportation",
    "Healthcare", "Insurance", "Education", "Savings", "Investments", "Debt Payments",
    "Gifts and Donations", "Travel", "Personal Care", "Household Supplies", "Clothing",
    "Subscriptions", "Dining Out", "Pets", "Childcare", "Hobbies", "Fitness", "Taxes",
    "Maintenance and Repairs", "Emergency Fund", "Miscellaneous", "Other"
]

accounts = [
    "Checking Account", "Savings Account", "Credit Card", "Loan Account", "Investment Account",
    "Retirement Account", "Mortgage Account", "Emergency Fund", "Health Savings Account (HSA)",
    "Education Savings Account (ESA)", "Brokerage Account", "Money Market Account",
    "Certificate of Deposit (CD)", "Taxable Investment Account", "Roth IRA", "Traditional IRA",
    "401(k)", "403(b)", "529 Plan", "Flexible Spending Account (FSA)", "Business Account",
    "Trust Account", "Joint Account", "Custodial Account", "PayPal Account", "Prepaid Card Account",
    "Travel Card Account", "Gift Card Account", "Crypto Wallet", "Pension Fund"
]

payment_methods = [
    "Cash", "Debit Card", "Credit Card", "Bank Transfer", "Check", "Mobile Payment",
    "Digital Wallet", "Cryptocurrency", "Prepaid Card", "Direct Debit", "Money Order",
    "Wire Transfer", "PayPal", "Apple Pay", "Google Pay", "Samsung Pay", "Venmo", "Zelle",
    "Cashier's Check", "ACH Transfer", "Western Union", "Square", "Stripe", "Amazon Pay",
    "WeChat Pay", "Alipay", "Gift Card", "Contactless Payment", "E-Check", "Postal Order"
]


st.toast('Hello, Welcome! Visit my Expense Analysis', icon='🖐️')
time.sleep(1)
def add_update_tab():
    selected_date = st.date_input("Enter Date", datetime(2024, 8, 1), label_visibility="collapsed")
    # Display the first toast message
    col1,col2=st.columns(2, gap="small")
    with col1:
        pass
        # with st.form(key="Salary_form"):
        #     monthly_salary = []
        #     for i in range(1):
        #         year_month = st.text_input("salary_year_Month", placeholder="Enter your year_month", key=f"year_month_{i}", label_visibility="collapsed")
        #         # salary = st.text_input("salary", placeholder="Enter your Salary",key=f"salary_{i}",label_visibility="collapsed")
        #         salary = st.number_input("salary", min_value=0, step=1, value=0, placeholder="Enter salary", key=f"salary_{i}", label_visibility="collapsed")
        #         monthly_salary.append({
        #             'salary_year_Month': year_month,
        #             'salary': salary
        #         })
        #     submit_button = st.form_submit_button("Submit")
        #     if submit_button:
        #         # Send the form data as JSON in the POST request
        #         response = requests.post(f"{API_URL}/salary/", json=monthly_salary)
                
        #         if response.status_code == 200:
        #             st.success("Salary updated successfully")
        #         else:
        #             st.error(response)     
    with col2:
        response = requests.get(f"{API_URL}/expense/{selected_date}")
        if response.status_code == 200:
            existing_expenses = response.json()
            # st.write(existing_expenses)  # Display existing expenses (optional)
        else: 
            st.error('Failed to retrieve expenses')
            existing_expenses = []
        with st.form(key="expense_form"):
            expenses = []
            for i in range(1):
                Salary=st.number_input("salary",  min_value=0, step=1, value=0, placeholder="Enter your Salary", key=f"salary_{i}",label_visibility="collapsed")
                category = st.selectbox("Category", options=categories, placeholder="Select Category", key=f"category_{i}", label_visibility="collapsed")
                amount = st.number_input("Amount", min_value=0, step=1, value=0, placeholder="Enter Expense Amount", key=f"amount_{i}", label_visibility="collapsed")
                gender = st.text_input("Gender", value="", placeholder="Enter Gender", key=f"gender_{i}", label_visibility="collapsed")
                description = st.text_input("Description", value="", placeholder="Enter Description", key=f"description_{i}", label_visibility="collapsed")
                payment_method = st.selectbox("Payment Method", options=payment_methods, placeholder="Select Payment", key=f"payment_{i}", label_visibility="collapsed")
                vendor = st.text_input("Vendor", value="", placeholder="Enter Vendor", key=f"vendor_{i}", label_visibility="collapsed")
                account = st.selectbox("Account", options=accounts, placeholder="Select Account", key=f"account_{i}", label_visibility="collapsed")
                notes = st.text_input("Notes", value="", placeholder="Enter Notes", key=f"notes_{i}", label_visibility="collapsed")
                expenses.append({
                    'salary':Salary,
                    
                    'category': category,
                    'amount': amount,
                    'gender': gender,
                    'description': description,
                    'payment_method': payment_method,
                    'vendor': vendor,
                    'account': account,
                    'notes': notes
                })
            
            submit_button = st.form_submit_button("Submit")
            if submit_button:
                filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]
                response = requests.post(f"{API_URL}/expense/{selected_date}", json=filtered_expenses)
                if response.status_code == 200:
                    st.success("Expenses updated successfully")
                else:
                    st.error("Failed to update expenses.")