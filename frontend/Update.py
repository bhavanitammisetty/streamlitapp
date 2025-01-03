import streamlit as st 
from add_update import add_update_tab
from Data import data_tab
from addmonthSalary import add_monthSalary
import time
st.title("Expense Tracking System")
def show_data():
    time.sleep(3)
    st.toast('Enter the Details in expense_form...',icon='👇')
    time.sleep(3)
    st.toast('Check your monthly data click on Data Tab', icon='👉')
    time.sleep(3)
    st.toast('Enter details  correctly.....',icon='👍')
    time.sleep(3)
    st.toast('Submit expense_form',icon='🎉')

  
tab1,tab2=st.tabs(["Add/Update Expenses","View Data"])



with tab1:
    add_update_tab()
    
with tab2:
    data_tab()
show_data() 
    
    



    
    
    

            
        
        