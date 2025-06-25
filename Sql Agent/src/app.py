# src/app.py

import streamlit as st
import pandas as pd
import duckdb
import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns
from typing import List, Tuple, Optional

# Import configuration and agent functions from other files
from config import MODEL_OPTIONS, PLOT_TYPES
from agent import get_sql_query_from_llm, get_plot_code_from_llm

# --- State Management Initialization ---
if "query_text" not in st.session_state:
    st.session_state.query_text = ""
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []
if "last_uploaded_filename" not in st.session_state:
    st.session_state.last_uploaded_filename = None

# --- Helper Functions ---
def identify_column_types(schema_df: pd.DataFrame) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Identifies the first text, numeric, and date column from a schema DataFrame."""
    text_col, num_col, date_col = None, None, None
    for _, row in schema_df.iterrows():
        col_name, col_type = row["column_name"], row["column_type"].upper()
        if not text_col and col_type in ["VARCHAR", "TEXT", "CHAR"]:
            text_col = col_name
        if not num_col and col_type in ["BIGINT", "DOUBLE", "INTEGER", "FLOAT", "DECIMAL"]:
            num_col = col_name
        if not date_col and col_type in ["DATE", "TIMESTAMP", "DATETIME"]:
            date_col = col_name
    return text_col, num_col, date_col

def generate_curated_suggestions(schema_df: pd.DataFrame) -> List[str]:
    """Generates a list of reliable, curated questions based on the table schema."""
    text_col, num_col, date_col = identify_column_types(schema_df)
    suggestions = []
    if text_col:
        suggestions.append(f"Count the number of unique entries in the '{text_col}' column.")
    if num_col and text_col:
        suggestions.append(f"What is the total of '{num_col}' for each '{text_col}'? Show the top 10.")
    if num_col and date_col:
        suggestions.append(f"Show the monthly trend of '{num_col}' using the '{date_col}' column.")
    if num_col:
        suggestions.append(f"What are the basic statistics (average, min, max) for the '{num_col}' column?")
    if not suggestions:
        suggestions.append("Count all rows in the table.")
    return suggestions[:4]

# --- Main Application UI and Logic ---
def main():
    st.set_page_config(page_title="AI SQL Agent", page_icon="🚀", layout="wide")
    st.title("🚀 AI SQL Agent")
    st.write("Upload a CSV file and ask questions to get answers and visualizations.")

    with st.sidebar:
        st.header("⚙️ Configuration")
        st.session_state.google_api_key = st.text_input("Google AI API Key", type="password", key="api_key_input")
        st.markdown("[Get a Google AI API Key](https://aistudio.google.com/app/apikey)")
        selected_model_name = st.selectbox("Select Gemini Model", options=list(MODEL_OPTIONS.keys()), key="model_selector")
        st.session_state.model_name = MODEL_OPTIONS[selected_model_name]

    uploaded_file = st.file_uploader("1. Upload your CSV file", type="csv", key="file_uploader")

    if uploaded_file:
        if uploaded_file.name != st.session_state.get("last_uploaded_filename"):
            st.session_state.suggestions = []
            st.session_state.query_text = ""
            st.session_state.last_uploaded_filename = uploaded_file.name
        
        temp_file_path, con = None, None
        try:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            temp_file_path = uploaded_file.name

            con = duckdb.connect(database=':memory:')
            con.execute(f"CREATE OR REPLACE TABLE my_data AS SELECT * FROM read_csv_auto('{temp_file_path}')")
            
            schema_df = con.execute("DESCRIBE my_data;").df()
            st.write("### Dataset Schema")
            st.dataframe(schema_df)

            if not st.session_state.suggestions:
                st.session_state.suggestions = generate_curated_suggestions(schema_df)
            
            if st.session_state.suggestions:
                with st.expander("✨ Click for Reliable Prompt Suggestions"):
                    for suggestion in st.session_state.suggestions:
                        if st.button(suggestion, key=suggestion):
                            st.session_state.query_text = suggestion
                            st.rerun()

            plot_type = st.selectbox("Select visualization type", PLOT_TYPES, key="plot_selector")
            query = st.text_area("2. Ask your question", value=st.session_state.query_text, key="query_input")

            if st.button("3. Analyze", use_container_width=True, key="analyze_button"):
                if not st.session_state.google_api_key:
                    st.error("🚨 Please enter your Google AI API key in the sidebar.")
                elif not query:
                    st.warning("⚠️ Please enter a question.")
                else:
                    with st.container():
                        st.session_state.query_text = query
                        sql_query = get_sql_query_from_llm(
                            query, schema_df.to_string(), st.session_state.google_api_key, st.session_state.model_name
                        )

                        if sql_query:
                            st.success("✅ SQL Query Generated:")
                            st.code(sql_query, language="sql")
                            
                            try:
                                result_df = con.execute(sql_query).df()
                                st.write("### Query Result")
                                st.dataframe(result_df)

                                if plot_type != "None":
                                    plot_code = get_plot_code_from_llm(
                                        query, result_df, plot_type, st.session_state.google_api_key, st.session_state.model_name
                                    )
                                    if plot_code:
                                        st.success("✅ Plotting Code Generated:")
                                        st.code(plot_code, language="python")
                                        
                                        plt.figure()
                                        plot_scope = {"df": result_df, "plt": plt, "np": np, "sns": sns}
                                        exec(plot_code, plot_scope)
                                        st.write("### Generated Visualization")
                                        st.pyplot(plt.gcf())
                                        plt.clf()
                                    else:
                                        st.warning("⚠️ The agent could not generate plotting code.")
                            except Exception as e:
                                st.error(f"❌ An error occurred during SQL execution: {e}")
                        else:
                            st.warning("⚠️ The agent could not generate a SQL query for your request. Please try rephrasing.")
        
        except Exception as e:
            st.error(f"A critical error occurred: {e}")
        finally:
            if con:
                con.close()
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)

if __name__ == "__main__":
    main() 