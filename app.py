# Streamlit app template that reads Excel data from a OneDrive share link
# Includes placeholder for Google login integration

import streamlit as st
import pandas as pd
import requests
import io

# --- Google Login Placeholder ---
# You can integrate Google login using streamlit-authenticator or OAuth libraries
# For now, we simulate a login screen
st.title("Cold Calling App")

# Simulated login (replace with Google OAuth integration)
username = st.text_input("Enter your username")
role = st.selectbox("Select your role", ["Admin", "User"])
if not username:
    st.warning("Please enter your username to proceed.")
    st.stop()

# --- OneDrive Excel File Access ---
st.subheader("Loading Contact Data from OneDrive")

# Replace this with your actual OneDrive share link
onedrive_share_link = "https://koaletproperties-my.sharepoint.com/:x:/g/personal/kobuserasmus_koaletproperties_onmicrosoft_com/EXMoZknl5wVFnsKJwcXUS9cBJ1AnmCLfl7JBfYmPjxapZg?download=1"
# Function to convert OneDrive share link to direct download link
def get_direct_download_link(share_link):
    if "1drv.ms" in share_link:
        import urllib.parse
        return "https://api.onedrive.com/v1.0/shares/u!" + urllib.parse.quote(share_link.split('/')[-1], safe='') + "/root/content"
    elif "sharepoint.com" in share_link:
        return share_link.replace("guestaccess.aspx", "download.aspx")
    else:
        return share_link

direct_link = get_direct_download_link(onedrive_share_link)

# Try to download and read the Excel file
try:
    response = requests.get(direct_link)
    excel_data = pd.ExcelFile(io.BytesIO(response.content), engine='openpyxl')
    df = excel_data.parse("TB_1")  # Replace with your actual sheet name
    st.success("Excel file loaded successfully.")
except Exception as e:
    st.error(f"Failed to load Excel file: {e}")
    st.stop()

# --- Role-Based Filtering ---
if role == "User":
    allowed_suburbs = st.multiselect("Select your allowed suburbs", df["Suburb"].unique())
    df = df[df["Suburb"].isin(allowed_suburbs)]

# --- Multi-Filter Search ---
st.subheader("Filter Contacts")
selected_suburb = st.selectbox("Suburb", ["All"] + sorted(df["Suburb"].dropna().unique()))
selected_status = st.selectbox("Call Status", ["All"] + sorted(df["CallStatus"].dropna().unique()))

filtered_df = df.copy()
if selected_suburb != "All":
    filtered_df = filtered_df[filtered_df["Suburb"] == selected_suburb]
if selected_status != "All":
    filtered_df = filtered_df[filtered_df["CallStatus"] == selected_status]

st.dataframe(filtered_df)

# --- Call Logging ---
st.subheader("Log a Call")
if not filtered_df.empty:
    selected_contact = st.selectbox("Select Contact", filtered_df["Name"].dropna().unique())
    call_status = st.selectbox("Call Status", ["Called", "No Answer", "Interested", "Not Interested"])
    call_notes = st.text_area("Call Notes")
    if st.button("Log Call"):
        st.success(f"Call logged for {selected_contact} with status '{call_status}'.")
else:
    st.info("No contacts available for logging.")

# --- Admin Panel Placeholder ---
if role == "Admin":
    st.subheader("Admin Panel")
    st.info("Here you can manage users and view all data. (Feature under development)")
