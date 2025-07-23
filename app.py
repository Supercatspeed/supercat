import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Cold Calling App", layout="wide")

# --- Simulated Login ---
st.sidebar.title("Login")
username = st.sidebar.text_input("Username")
role = st.sidebar.selectbox("Role", ["User", "Admin"])

if not username:
    st.warning("Please enter a username to continue.")
    st.stop()

st.sidebar.success(f"Logged in as {username} ({role})")

# --- OneDrive Excel File ---
onedrive_share_link = "https://koaletproperties-my.sharepoint.com/:x:/g/personal/kobuserasmus_koaletproperties_onmicrosoft_com/EXMoZknl5wVFnsKJwcXUS9cBJ1AnmCLfl7JBfYmPjxapZg?download=1"

@st.cache_data
def load_excel_from_onedrive(url):
    response = requests.get(url)
    excel_data = pd.ExcelFile(io.BytesIO(response.content), engine='openpyxl')
    return excel_data.parse("Master")

df = load_excel_from_onedrive(onedrive_share_link)

# --- Role-Based Filtering ---
if role == "User":
    allowed_suburbs = st.sidebar.multiselect("Allowed Suburbs", sorted(df["Suburb"].dropna().unique()))
    if allowed_suburbs:
        df = df[df["Suburb"].isin(allowed_suburbs)]

# --- Multi-Filter Search ---
st.subheader("Filter Contacts")
selected_suburb = st.selectbox("Suburb", ["All"] + sorted(df["Suburb"].dropna().unique()))
selected_status = st.selectbox("Call Status", ["All"] + sorted(df["Response"].dropna().unique()))

filtered_df = df.copy()
if selected_suburb != "All":
    filtered_df = filtered_df[filtered_df["Suburb"] == selected_suburb]
if selected_status != "All":
    filtered_df = filtered_df[filtered_df["Response"] == selected_status]

st.write(f"Showing {len(filtered_df)} contacts:")
st.dataframe(filtered_df.head(100))  # Limit display to 100 rows

# --- Call Logging ---
st.subheader("Log a Call")
selected_contact = st.selectbox("Select Contact", filtered_df["Name"].dropna().unique())
call_status = st.selectbox("Call Status", ["Interested", "Not Interested", "Follow-up", "No Answer"])
notes = st.text_area("Notes")

if st.button("Log Call"):
    st.success(f"Call logged for {selected_contact} with status '{call_status}' and notes: {notes}")

# --- Admin Panel Placeholder ---
if role == "Admin":
    st.subheader("Admin Panel")
    st.info("Admin features coming soon...")
