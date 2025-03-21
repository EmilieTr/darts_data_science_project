import streamlit as st

def navigation():
    # Sidebar for Navigation

    st.markdown("""
    <style>
        /* Sidebar-Hintergrundfarbe */
        [data-testid="stSidebar"] {
            background-color: #D2B48C;
            padding: 20px;
        }
        
        /* Textfarbe der Sidebar */
        [data-testid="stSidebar"] * {
            color: white;
        }

        /* Breite der Sidebar */
        section[data-testid="stSidebar"] {
            width: 300px !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Tournaments", "Matches", "Players", "Data Pipeline"])
    
    # --- Erweiterbare Dropdowns für Unterseiten ---
    if page == "Tournaments":
        with st.sidebar.expander("🏆 Tournament Options"):
            st.write("🎯 Select an option:")
            st.button("📅 Upcoming Tournaments")
            st.button("🏅 Past Winners")

    elif page == "Matches":
        with st.sidebar.expander("⚔️ Match Analysis"):
            st.write("📊 Choose a Match Stat:")
            st.button("🔥 Best Checkouts")
            st.button("🎯 Highest Averages")

    elif page == "Players":
        with st.sidebar.expander("🎯 Player Stats"):
            st.write("👤 Compare Players:")
            st.button("💪 Top Performers")
            st.button("📈 Career Progression")

    elif page == "Data Pipeline":
        with st.sidebar.expander("🔄 Data Processing"):
            st.write("📡 Select a Task:")
            st.button("📥 Import Data")
            st.button("📊 Transform & Clean Data")

    # --- Hauptbereich der App ---
    st.title(f"📌 {page}")
    st.write(f"Welcome to the {page} section!")