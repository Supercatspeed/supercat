
import streamlit as st
import pandas as pd
import io
import requests

# --- Login Simulation ---
st.title("Cold Calling App")

username = st.text_input("Enter your username")
role = st.selectbox("Select your role", ["User", "Admin"])

if username and role:
    st.success(f"Logged in as {username} ({role})")

    # --- Load Excel File from OneDrive ---
    onedrive_share_link = "https://koaletproperties-my.sharepoint.com/:x:/g/personal/kobuserasmus_koaletproperties_onmicrosoft_com/EXMoZknl5wVFnsKJwcXUS9cBJ1AnmCLfl7JBfYmPjxapZg?download=1"
    try:
        response = requests.get(onedrive_share_link)
        excel_data = pd.ExcelFile(io.BytesIO(response.content), engine='openpyxl')
        df = excel_data.parse("Master")  # Updated sheet name
    except Exception as e:
        st.error(f"Failed to load Excel file: {e}")
        st.stop()

    # --- Role-Based Filtering ---
    if "Suburb" in df.columns and role == "User":
        allowed_suburbs = st.multiselect("Select allowed suburbs", sorted(df["Suburb"].dropna().unique()))
        df = df[df["Suburb"].isin(allowed_suburbs)]

    # --- Multi-Filter Search ---
    st.subheader("Filter Contacts")
    if "Suburb" in df.columns:
        selected_suburb = st.selectbox("Suburb", ["All"] + sorted(df["Suburb"].dropna().unique()))
    else:
        selected_suburb = "All"

    if "Response" in df.columns:
        selected_status = st.selectbox("Call Status", ["All"] + sorted(df["Response"].dropna().unique()))
    else:
        selected_status = "All"

    filtered_df = df.copy()
    if selected_suburb != "All" and "Suburb" in df.columns:
        filtered_df = filtered_df[filtered_df["Suburb"] == selected_suburb]
    if selected_status != "All" and "Response" in df.columns:
        filtered_df = filtered_df[filtered_df["Response"] == selected_status]

    st.dataframe(filtered_df)

    # --- Call Logging ---
    st.subheader("Log a Call")
    if "Name" in filtered_df.columns:
        selected_contact = st.selectbox("Select Contact", filtered_df["Name"].dropna().unique())
    else:
        selected_contact = ""

    if "Response" in df.columns:
        call_status = st.selectbox("Set Call Status", sorted(df["Response"].dropna().unique()))
    else:
        call_status = ""

    notes = st.text_area("Enter notes")

    if st.button("Log Call"):
        st.success(f"Call logged for {selected_contact} with status '{call_status}' and notes: {notes}")

    # --- Admin Panel Placeholder ---
    if role == "Admin":
        st.subheader("Admin Panel")
        st.info("Admin features will be implemented here.")

else:
    st.warning("Please enter your username and select a role to continue.")
