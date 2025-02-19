import streamlit as st
import pandas as pd
import re

# Helper Function to Detect C-Level Titles

def is_executive_title(title):
    # Define patterns for executive roles
    patterns = [
        r'\bCEO\b', r'\bCFO\b', r'\bCTO\b', r'\bCIO\b', r'\bCOO\b', r'\bCMO\b', r'\bCHRO\b', r'\bCLO\b', r'\bCPO\b', r'\bCRO\b',
        r'\bVice President\b', r'\bVP\b', r'\bV\.P\.\b',
        r'\bManaging Director\b', r'\bDirector\b', r'\bSenior Director\b', r'\bExecutive Director\b',
        r'\bSenior\b', r'\bSr\.\b', r'\bPrincipal\b', r'\bLead\b', r'\bHead\b', r'\bChief\b',
        r'\bPresident\b', r'\bPartner\b', r'\bOwner\b', r'\bFounder\b', r'\bChairman\b', r'\bExecutive\b', r'\bLeader\b',
        r'\bManager\b', r'\bExecutive\b', r'\bMD\b'
    ]

    exclusion_patterns = [
        r'\bHR\b', r'\bHuman Resources\b'
    ]

    # First, check for inclusion
    if any(re.search(pattern, str(title), re.IGNORECASE) for pattern in patterns):
        # Then, exclude unwanted titles
        if not any(re.search(excl_pattern, str(title), re.IGNORECASE) for excl_pattern in exclusion_patterns):
            return True

    return False


# Streamlit App

def main():
    st.title("ESI-miEdge Job Title Scrubber (with SalesForce Integration)")
    st.write("Upload your **Excel/CSV** file from miEdge, auto-select **executive roles**, and download the cleaned file.")

    # Step 1: Upload File
    uploaded_file = st.file_uploader("📤 Upload Excel/CSV File", type=["csv", "xlsx"])

    if uploaded_file is not None:
        # Determine file type and read accordingly
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ File Uploaded Successfully!")

        # Display Raw Data
        with st.expander("🔍 View Raw Data"):
            st.dataframe(df)

        # Step 2: Extract Unique Job Titles
        if 'Job Title' in df.columns:
            unique_job_titles = df['Job Title'].dropna().unique().tolist()

            # Step 3: Auto-Select Executive Titles
            preselected_titles = [title for title in unique_job_titles if is_executive_title(title)]
            st.write(f"### 🛠 Select Job Titles to Keep ({len(unique_job_titles)} found):")
            
            # Multi-Select with Pre-Selected Executive Titles
            selected_titles = st.multiselect(
                "✅ Pre-selected C-Level and Executive Titles (Adjust as Needed):",
                unique_job_titles,
                default=preselected_titles
            )

            # Step 4: Filter DataFrame Based on Selection
            filtered_df = df[df['Job Title'].isin(selected_titles)]

            # Display Filtered Data
            st.write(f"### ✅ Filtered Data (Showing {len(filtered_df)} of {len(df)} rows):")
            st.dataframe(filtered_df)

            # Step 5: Download Filtered Data
            def convert_df_to_csv(df):
                return df.to_csv(index=False).encode('utf-8')

            csv_data = convert_df_to_csv(filtered_df)
            st.download_button(
                label="📥 Download Filtered Data as CSV",
                data=csv_data,
                file_name='filtered_executive_data.csv',
                mime='text/csv'
            )
        else:
            st.error("❌ The uploaded file does not contain a 'Job Title' column.")

if __name__ == "__main__":
    main()
