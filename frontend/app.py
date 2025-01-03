import streamlit as st 

st.set_page_config(layout="wide")

about_page = st.Page(
    "about_me.py",
    title="About Me",
    icon=":material/account_circle:",
    default=True,
)
project_1_page = st.Page(
    "Update.py",
    title="Add/Update",
    icon=":material/database:",
)

project_2_page = st.Page(
    "Expenses_dashboard.py",

    title="Expenses Dashboard",
    icon=":material/bar_chart:",
    
)
project_3_page = st.Page(
    "Chatbot.py",
    title="Chat Bot",
    icon=":material/smart_toy:",
)
# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
pg = st.navigation(pages=[about_page, project_1_page, project_2_page, project_3_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Info": [about_page],
        "Project": [project_1_page,project_2_page,project_3_page],
        
    }
)


# --- SHARED ON ALL PAGES ---
# st.logo("assets/codingisfun_logo.png")
st.sidebar.markdown("Made with ❤️ by [Bhavani](https://www.linkedin.com/in/bhavanitammisetty)")


# --- RUN NAVIGATION ---
pg.run()



