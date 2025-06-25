# src/agent.py

import re
import google.generativeai as genai
from typing import Optional, List
import streamlit as st
import pandas as pd

# Pre-compile the regex for finding SQL code blocks
sql_pattern = re.compile(r"```sql\n(.*?)\n```", re.DOTALL)
python_pattern = re.compile(r"```python\n(.*?)\n```", re.DOTALL)

def extract_code(text: str, pattern: re.Pattern) -> Optional[str]:
    """Generic function to extract code from a markdown block."""
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return None

# --- NEW FUNCTION for Dynamic Prompts ---
def get_prompt_suggestions(db_schema: str, google_api_key: str, model_name: str) -> List[str]:
    """Takes a db schema and generates a list of suggested user questions."""
    system_prompt = f"""
You are a helpful data analyst assistant. Your task is to generate 5 insightful and relevant questions a user might ask about their data.
The user has provided a dataset with the following schema:
{db_schema}

RULES:
- Generate exactly 5 questions.
- The questions should be analytical in nature (e.g., asking for summaries, comparisons, trends).
- Return ONLY the questions, each on a new line. Do not number them or add any other text.
"""
    try:
        genai.configure(api_key=google_api_key)
        model = genai.GenerativeModel(model_name=model_name, system_instruction=system_prompt)
        response = model.generate_content("Generate 5 questions.")
        suggestions = [line for line in response.text.split('\n') if line.strip()]
        return suggestions
    except Exception as e:
        st.warning(f"Could not generate prompt suggestions: {e}")
        return []

def get_sql_query_from_llm(
    user_query: str,
    google_api_key: str,
    model_name: str,
    db_schema: str
) -> Optional[str]:
    """
    Takes a user's natural language query and returns a SQL query from Google's Gemini.
    """
    # --- PROMPT ENHANCEMENT ---
    # We are adding information about the PRAGMA command to prevent hallucinations.
    system_prompt = f"""
You are an expert data analyst. You are a powerful SQL agent.
Your task is to convert a user's natural language question into a single, valid DuckDB SQL query.
The user's data is in a table named 'my_data'.

This is the schema of the 'my_data' table:
{db_schema}

If the user asks a question about the table's schema, structure, or data types, you can query the database's metadata using the pragma function.
The command is `PRAGMA table_info('my_data')`. This function returns a table with the following columns that you can query: `cid`, `name`, `type`, `notnull`, `dflt_value`, `pk`. The most useful columns are `name` and `type`.

RULES:
- You MUST wrap the SQL query in a single markdown code block like this: ```sql\n[YOUR QUERY HERE]\n```
- Only output the SQL query. Do not add any explanation or commentary.
- The SQL query must be for the DuckDB dialect.
"""
    
    try:
        genai.configure(api_key=google_api_key)
        generation_config = {"temperature": 0.0}
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            system_instruction=system_prompt
        )
        response = model.generate_content(user_query)
        return extract_code(response.text, sql_pattern)

    except Exception as e:
        st.error(f"An error occurred while communicating with Google AI: {e}")
        return None

# --- MODIFIED FUNCTION for User-Selected Plots ---
def get_plot_code_from_llm(
    user_query: str,
    sql_result: pd.DataFrame,
    plot_type: str, # NEW argument
    google_api_key: str,
    model_name: str,
) -> Optional[str]:
    """Takes a user query, a DataFrame, and a plot type, and returns Python code for a plot."""
    data_sample = sql_result.to_string()
    system_prompt = f"""
You are a data visualization expert. Your task is to write Python code to visualize data for a user's request.
You will be given the user's original request and a sample of the data obtained from a database.
The data is available in a pandas DataFrame named `df`.

RULES:
- You MUST write Python code using the `matplotlib.pyplot` library.
- Your code will be executed in a context where `df` (the data) and `plt` (matplotlib.pyplot) are already defined.
- Do NOT include `import matplotlib.pyplot as plt` or code to create the `df`. Just write the plotting logic.
- Your code should generate a single, clear, and relevant plot that answers the user's question.
- The user has specifically requested a **{plot_type}**. Your generated Python code should create this type of chart.
- The plot should be saved to a file named 'plot.png'. Use `plt.savefig('plot.png')`.
- Wrap the Python code in a single markdown code block: ```python\n[YOUR CODE HERE]\n```
- Only output the code. No explanations.
"""
    prompt = f"""
User's original question: "{user_query}"
Data sample:
{data_sample}
Write the Python code to plot this data as a {plot_type}.
"""
    try:
        genai.configure(api_key=google_api_key)
        model = genai.GenerativeModel(model_name=model_name, system_instruction=system_prompt)
        response = model.generate_content(prompt)
        return extract_code(response.text, python_pattern)
    except Exception as e:
        st.error(f"An error occurred while generating the plot code: {e}")
        return None 