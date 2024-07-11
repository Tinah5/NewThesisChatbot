import streamlit as st
import pandas as pd
import os
import yaml
from utils.file_handler import handle_uploaded_file
from utils.openai_integration import analyze_ambiguities

# Function to load OpenAI API key from config.yaml
def load_openai_api_key():
    with open('config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        return config.get('OPENAI_API_KEY', None)

# Function to configure the sidebar for API key input
def config_sidebar():
    st.sidebar.subheader("Backend Configuration")
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password", key="openai_api_key")
    return openai_api_key

# Main function to run the Streamlit application
def main():
    st.set_page_config(page_title="Requirements Ambiguity Analyzer", page_icon="🔍")
    st.title("RAD CHATBOT: Requirements Ambiguity Detection Tool")

    # Configure sidebar for API key input
    openai_api_key = config_sidebar()

    # Handle file upload
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            # Check if required columns exist in the dataframe
            expected_columns = ['ID', 'Description']
            missing_columns = [col for col in expected_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Required column(s) {', '.join(missing_columns)} not found in the uploaded CSV file.")

            # Extract requirements from 'Description' column
            requirements_texts = df["Description"].dropna().tolist()

            if not openai_api_key:
                st.warning("Please configure the OpenAI API Key in the sidebar.")
                st.stop()

            st.write("Analyzing ambiguities in uploaded requirements...")
            ambiguous_requirements = []

            # Process each requirement text using OpenAI
            for idx, text in enumerate(requirements_texts, start=1):
                result = analyze_ambiguities(text, openai_api_key)
                if result["has_ambiguity"]:
                    ambiguous_requirements.append({
                        "ID": df.loc[df["Description"] == text, "ID"].iloc[0],  # Get corresponding ID
                        "Requirement Text": text,
                        "Ambiguity Type": result["ambiguity_type"],
                        "Ambiguity Reason": result["ambiguity_reason"]
                    })

            # Display results if ambiguities were found
            if len(ambiguous_requirements) > 0:
                st.subheader("Ambiguous Requirements")
                ambiguous_df = pd.DataFrame(ambiguous_requirements)
                st.dataframe(ambiguous_df)
            else:
                st.success("No ambiguous requirements found in the uploaded file.")

        except ValueError as ve:
            st.error(f"Error processing CSV file: {str(ve)}")

        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
