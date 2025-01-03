import streamlit as st 
from datetime import datetime
import requests

API_URL="http://localhost:8000"

def data_tab():
    option = st.radio(
        "Select Option",
        ('Select Particular Date Expenses', 'Select Range of Expenses','select delete expense date')
    )
    
    if option == 'Select Particular Date Expenses':   
        select_date=st.date_input("Enter Date",datetime(2024,8,1),label_visibility="collapsed",key="unique_date_1")
        response=requests.get(f"{API_URL}/expense/{select_date}")
        
        if response.status_code==200:
            existing_expenses=response.json()
            # Check if the response data is empty
            if not existing_expenses:  # This checks if the list or data is empty
                st.error("No data available for the selected date. Failed to retrieve.")
                
            else:
                st.dataframe(existing_expenses)
        else:
            
            st.error("No data available for the selected date. Failed to retrieve.")
            
     
            
    elif option=="Select Range of Expenses":
        col1,col2=st.columns(2)
        with col1:
            start_date=st.date_input("Start Date",datetime(2024,8,1),label_visibility="collapsed",key="unique_date_2")
        with col2:
            End_date=st.date_input("End Date",datetime(2024,8,1),label_visibility="collapsed",key="unique_date_3")
        if st.button("Get Data"):
            payload={
                "start_date":start_date.strftime("%Y-%m-%d"),
                "end_date":End_date.strftime("%Y-%m-%d") 
            }
            response=requests.get(f"{API_URL}/analytics/{start_date},{End_date}",json=payload)
            if response.status_code==200:
                existing_expenses=response.json()
            # Check if the response data is empty
            if not existing_expenses:  # This checks if the list or data is empty
                st.error("No data available for the selected date")
                
            else:
                st.dataframe(existing_expenses)
        else:
            
            st.error("No data available for the selected date")
    elif option=="select delete expense date":    
        select_date=st.date_input("Enter Date",datetime(2024,8,1),label_visibility="collapsed",key="unique_date_1")
        
        # submit_button = st.form_submit_button()
        if st.button("delete_expense"):
            
            response=requests.delete(f"{API_URL}/expense/{select_date}")
            if response.status_code == 200:
                existing_expenses=response.json()
                
              
                st.success("Expenses Delete successfully!")
            else:
                
                st.error("Failed to Delete expenses.")
    