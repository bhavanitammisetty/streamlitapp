import streamlit as st
from contactform import contact_form
@st.dialog("Contact Me")
def show_contact_form():
    
    contact_form()
# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.markdown(
    """
    <style>
    body {
        background-color: lightgray; /* Change to your desired background color */
    }
    img {
        border-radius:100%; /* Makes the image round */
       
        width:150px; /* Adjust the size as needed */
        height: 300px; /* Keep it equal to make the image a perfect circle */
        object-fit: cover; /* Ensures the image content fits well */
    }
    </style>
    """,
    unsafe_allow_html=True,
)
    
    # st.image("bhanu1.jpg", width=300)
    st.image("Bhanu.jpg",width=300)
with col2:
    st.title("Bhavani Tammisetty", anchor=False)
    st.write(
        "Data Engineer, assisting enterprises by supporting data-driven decision-making."
    )
    if st.button("✉️ Contact Me"):
        show_contact_form()
# --- EXPERIENCE & QUALIFICATIONS ---
st.write("\n")
st.subheader("Experience & Qualifications", anchor=False)
st.write(
    """
    - 2.5 Years experience extracting actionable insights from data
    - Strong hands-on experience and knowledge in Python and Excel
    - Good understanding of statistical principles and their respective applications
    - Excellent team-player and displaying a strong sense of initiative on tasks
    """
)
# --- SKILLS ---
st.write("\n")
st.subheader("Hard Skills", anchor=False)
st.write(
    """
    - Programming: Python (Numpy-learn, Pandas), SQL
    - Data Visualization: PowerBi, MS Excel, Plotly
    - Cloud: Azure
    - Databases: SQL,MySQL
    - Framework: Streamlit
    """
)