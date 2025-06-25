# src/app.py

import streamlit as st
import pandas as pd
import duckdb
import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns

from config import MODEL_OPTIONS
from agent import get_sql_query_from_llm, get_plot_code_from_llm, get_prompt_suggestions

# Initialize session state for suggestions and query text
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = []
if 'query_text' not in st.session_state:
    st.session_state.query_text = ""

def main():
    st.set_page_config(page_title="Comprehensive SQL Agent", page_icon="📊", layout="wide")
    st.title("📊 Comprehensive AI SQL Agent")
    st.write("Upload a CSV, and I'll answer your questions. Get started with one of the auto-generated prompts!")

    with st.sidebar:
        st.header("⚙️ Configuration")
        st.session_state.google_api_key = st.text_input("Google AI API Key", type="password")
        st.markdown("[Get a Google AI API Key](https://aistudio.google.com/app/apikey)")
        selected_model_name = st.selectbox("Select Gemini Model", options=list(MODEL_OPTIONS.keys()))
        st.session_state.model_name = MODEL_OPTIONS[selected_model_name]

    uploaded_file = st.file_uploader("1. Upload your CSV file", type="csv", key="file_uploader")

    if uploaded_file is not None:
        try:
            user_df = pd.read_csv(uploaded_file)
            st.write("### Dataset Preview")
            st.dataframe(user_df.head())

            con = duckdb.connect(database=':memory:')
            con.register('my_data', user_df)
            schema_df = con.execute("DESCRIBE my_data;").df()
            db_schema = schema_df.to_string()

            # --- DYNAMIC PROMPT SUGGESTIONS ---
            if st.session_state.suggestions == []:
                with st.spinner("Analyzing data and generating prompt suggestions..."):
                    if st.session_state.google_api_key:
                        st.session_state.suggestions = get_prompt_suggestions(
                            db_schema, st.session_state.google_api_key, st.session_state.model_name
                        )
                    else:
                        st.warning("Enter your API key to generate prompt suggestions.")

            if st.session_state.suggestions:
                with st.expander("✨ Click for Prompt Suggestions"):
                    for suggestion in st.session_state.suggestions:
                        if st.button(suggestion):
                            st.session_state.query_text = suggestion # Update session state

            # --- USER-SELECTED VISUALIZATION ---
            plot_type = st.selectbox(
                "Select visualization type",
                options=["None", "Bar Chart", "Line Chart", "Pie Chart"],
                index=0
            )

            query = st.text_area("2. Ask your question", value=st.session_state.query_text, key="query_input")

            if st.button("3. Analyze", use_container_width=True):
                if not st.session_state.google_api_key:
                    st.error("🚨 Please enter your Google AI API key.")
                else:
                    with st.spinner("Gemini is generating a SQL query..."):
                        sql_query = get_sql_query_from_llm(
                            user_query=query,
                            google_api_key=st.session_state.google_api_key,
                            model_name=st.session_state.model_name,
                            db_schema=db_schema
                        )
                    if sql_query:
                        st.success("SQL query generated:")
                        st.code(sql_query, language="sql")
                        with st.spinner("Executing query locally..."):
                            result_df = con.execute(sql_query).df()
                            st.write("### Query Result")
                            st.dataframe(result_df)
                            
                            if plot_type != "None":
                                with st.spinner(f"Gemini is generating {plot_type.lower()} code..."):
                                    plot_code = get_plot_code_from_llm(
                                        user_query=query,
                                        sql_result=result_df,
                                        plot_type=plot_type, # Pass selected plot type
                                        google_api_key=st.session_state.google_api_key,
                                        model_name=st.session_state.model_name
                                    )
                                if plot_code:
                                    st.success("Plotting code generated:")
                                    st.code(plot_code, language="python")
                                    
                                    with st.spinner("Generating plot..."):
                                        # Create a fresh figure for each plot
                                        plt.figure()
                                        
                                        # Define the scope for exec()
                                        plot_scope = {
                                            "df": result_df,
                                            "plt": plt,
                                            "np": np,
                                            "sns": sns
                                        }
                                        
                                        # Execute the generated code
                                        exec(plot_code, plot_scope)
                                        
                                        # Display the plot in Streamlit
                                        st.write("### Generated Visualization")
                                        st.pyplot(plt.gcf())
                                        # Clear the figure to prevent it from affecting the next plot
                                        plt.clf()
            con.close()
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 