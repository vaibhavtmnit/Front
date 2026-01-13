import streamlit as st
import requests
import pandas as pd
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Data Search Interface",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Aesthetics ---
# This injects custom CSS to style the inputs, buttons, and general layout
st.markdown("""
<style>
    /* Main background accent */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Styling the text areas to look like distinct "Chat" boxes */
    .stTextArea textarea {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        font-size: 16px;
        color: #333;
    }
    .stTextArea textarea:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
    }
    
    /* Styling the Search Button */
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        font-size: 18px;
        font-weight: 600;
        border-radius: 30px;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        background-color: #45a049;
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    /* Headers */
    h1 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Table Styling */
    div[data-testid="stDataFrame"] {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar (Future Expansion) ---
with st.sidebar:
    st.header("Configuration")
    st.markdown("Use this panel for future settings.")
    
    # Placeholder for future input boxes
    # You can uncomment these as you need more inputs
    # extra_param_1 = st.text_input("Extra Filter 1")
    # extra_param_2 = st.date_input("Date Range")
    
    st.info("Backend Status Check: Ensure your FastAPI server is running on port 8000.")

# --- Main Interface ---
st.title("🔍 Semantic Search & Analysis")
st.markdown("Enter your query text below to retrieve structured data analysis.")

st.write("---")

# Layout: Two large input columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📝 Input Source A")
    text_input_1 = st.text_area(
        "Enter first text block:",
        height=250,
        placeholder="Paste long text here...",
        help="Primary text source for analysis."
    )

with col2:
    st.markdown("### 📝 Input Source B")
    text_input_2 = st.text_area(
        "Enter second text block:",
        height=250,
        placeholder="Paste comparison text here...",
        help="Secondary text source for comparison."
    )

# --- Action Area ---
st.markdown("<br>", unsafe_allow_html=True)
search_col1, search_col2, search_col3 = st.columns([1, 2, 1])

with search_col2:
    search_clicked = st.button("🚀 Run Analysis", use_container_width=True)

# --- Logic & Results ---
if search_clicked:
    if not text_input_1 and not text_input_2:
        st.warning("⚠️ Please provide at least one text input to proceed.")
    else:
        # Prepare payload
        payload = {
            "text_input_1": text_input_1 or "",
            "text_input_2": text_input_2 or ""
        }
        
        API_URL = "http://127.0.0.1:8000/analyze"
        
        with st.spinner("Processing request with backend..."):
            try:
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    data = result.get("data", [])
                    
                    if data:
                        df = pd.DataFrame(data)
                        
                        st.success("✅ Analysis Complete")
                        st.markdown("### 📊 Results Table")
                        
                        # Display interactive dataframe
                        st.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "Confidence_Score": st.column_config.ProgressColumn(
                                    "Confidence",
                                    format="%.2f",
                                    min_value=0,
                                    max_value=1,
                                ),
                                "Status": st.column_config.TextColumn(
                                    "Status",
                                    help="Verification status of the entity"
                                )
                            }
                        )
                    else:
                        st.info("No data returned from the analysis.")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to backend. Is FastAPI running on port 8000?")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

