import streamlit as st
from datetime import date

import requests
from datetime import datetime
import time
API_URL = "http://localhost:8000"

def contact_form():
    form_placeholder = st.empty()
    with form_placeholder.form(key="contact form"):
        contact_details = []
        for i in range(1):
           
            
            name = st.text_input("First Name",key=f"name{i}")
            emailcontact = st.text_input("Email Contact Address",key=f"emailcontact{i}")
            notes = st.text_input("Your Message",key=f"notes{i}")
        
        # Submit button with a unique key
        submit_button = st.form_submit_button("Submit")
        
        # Collect form details only when the form is submitted
        if submit_button:  
            contact_details.append({
                
                'name': name,
                'emailcontact': emailcontact,
                'notes': notes,
                
            })
            
            # Send the form data as JSON in the POST request
            response = requests.post(f"{API_URL}/contact/", json=contact_details)
            
            
            if response.status_code == 200:
                
                st.success("Message successfully sent!")
               
                form_placeholder.markdown("Message successfully sent!")
               
                time.sleep(1)
                form_placeholder.empty()
            else:
                st.error("Can't submit the details")
                