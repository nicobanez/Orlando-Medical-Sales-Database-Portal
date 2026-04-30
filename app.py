import streamlit as st
import pandas as pd

# --- WEBSITE DESIGN & TAB SETTINGS ---
st.set_page_config(page_title="Medical RE Portal", page_icon="🏢", layout="wide")

# --- PREMIUM EXCEL-STYLE CSS ---
# This forces the website tables to look like a high-end Excel brochure
st.markdown("""
    <style>
    /* Main background */
    .stApp { background-color: #F4F7F6; }
    
    /* Headers and Text */
    h1 { color: #1F4E78; font-family: 'Arial Black', sans-serif; border-bottom: 3px solid #ED7D31; padding-bottom: 10px; margin-bottom: 20px;}
    h2, h3 { color: #1F4E78; font-family: 'Arial', sans-serif; }
    
    /* The Premium Table Design */
    table { width: 100%; border-collapse: collapse; background-color: white; font-size: 14px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); margin-bottom: 30px;}
    th { background-color: #1F4E78 !important; color: white !important; padding: 12px; text-align: left; border: 1px solid #ddd; font-weight: bold;}
    td { padding: 10px; border: 1px solid #ddd; color: #333; }
    tr:nth-child(even) { background-color: #F9FAFB; } /* Alternating row colors */
    tr:hover { background-color: #E2E8F0; } /* Highlight row when mouse hovers */
    
    /* Lock Screen Button */
    .stButton>button { background-color: #1F4E78; color: white; border-radius: 5px; width: 100%; font-weight: bold; height: 50px;}
    </style>
    """, unsafe_allow_html=True)

# --- MULTI-USER PASSCODE SYSTEM ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<h1 style='text-align: center;'>🔒 Client Access Portal</h1>", unsafe_allow_html=True)
            st.write("Please enter your credentials to view the Greater Orlando Medical Sales Data.")
            
            username = st.text_input("Email Address")
            password_input = st.text_input("Passcode", type="password")
            
            if st.button("Unlock Data"):
                if username in st.secrets["passwords"] and password_input == st.secrets["passwords"][username]:
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("Incorrect Email or Passcode. Please contact Nico Bañez for access.")
        return False
    return True

# --- MAIN DASHBOARD ---
if check_password():
    
    st.markdown("<h1>Greater Orlando Medical Office Market (2020-2025)</h1>", unsafe_allow_html=True)

    @st.cache_data
    def load_data():
        # Load the data. We use fillna("") to make blank Excel cells look clean instead of saying "NaN"
        df = pd.read_excel("Updated Claude LACF HCRE Sales DataBase.xlsx", sheet_name="Market Overview", skiprows=3)
        df = df.fillna("") 
        return df
    
    try:
        data = load_data()
        
        st.markdown("<h3>Market Overview Data</h3>", unsafe_allow_html=True)
        
        # Instead of using the default web table, we inject our Premium CSS Table
        st.markdown(data.to_html(index=False, escape=False), unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Could not load the Excel file. Error: {e}")
