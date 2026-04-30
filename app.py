import streamlit as st
import pandas as pd

# --- WEBSITE DESIGN & TAB SETTINGS ---
st.set_page_config(page_title="Medical RE Portal", page_icon="🏢", layout="wide")

# --- CUSTOM BRANDING (CSS) ---
# You can change the hex codes below to match your exact company colors!
st.markdown("""
    <style>
    /* Change the main background color */
    .stApp { background-color: #F8F9FA; }
    
    /* Change the top header color */
    h1 { color: #1F4E78; font-family: 'Arial Black', sans-serif; }
    h2, h3 { color: #ED7D31; }
    
    /* Style the lock screen button */
    .stButton>button { background-color: #1F4E78; color: white; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- PASSCODE LOCK SYSTEM ---
def check_password():
    """Returns True if the user enters the correct password."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("<h1>🔒 Client Access Portal</h1>", unsafe_allow_html=True)
        st.write("Please enter your exclusive passcode to view the Greater Orlando Medical Sales Data.")
        
        # The password box
        password_input = st.text_input("Passcode", type="password")
        
        if st.button("Unlock Data"):
            if password_input == "LeeCentral2026": # <-- CHANGE YOUR PASSWORD HERE
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Incorrect Passcode. Please contact Nico Bañez for access.")
        return False
    return True

# --- MAIN DASHBOARD (Only shows if unlocked) ---
if check_password():
    
    st.markdown("<h1>Greater Orlando Medical Office Market (2020-2025)</h1>", unsafe_allow_html=True)
    st.write("Welcome to the proprietary data portal. Select a view below to interact with the market data.")

    # Load Data from your Excel file
    @st.cache_data
    def load_data():
        # Loads the "Market Overview" tab from your uploaded sheet
        df = pd.read_excel("Updated Claude LACF HCRE Sales DataBase.xlsx", sheet_name="Market Overview", skiprows=1)
        return df
    
    try:
        data = load_data()
        
        # Create a layout with two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3>Market Overview Data</h3>", unsafe_allow_html=True)
            st.dataframe(data, use_container_width=True)
            
        with col2:
            st.markdown("<h3>Quick Insights</h3>", unsafe_allow_html=True)
            st.info("💡 **Institutional Trend:** Notice the massive concentration of capital in Tier 3 assets in the CBD and Tourist Corridors.")
            st.success("📈 **Pricing:** Standalone clinics under 5,000 SF command the highest price-per-square-foot premiums across all submarkets.")

    except Exception as e:
        st.error(f"Could not load the Excel file. Please ensure the file name exactly matches. Error: {e}")
