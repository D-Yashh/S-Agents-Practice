# src/agent.py

import re
from typing import Optional, List
import google.generativeai as genai
import pandas as pd
import streamlit as st

# Pre-compile regex patterns for extracting code blocks
sql_pattern = re.compile(r"```sql\n(.*?)\n```", re.DOTALL)
python_pattern = re.compile(r"```python\n(.*?)\n```", re.DOTALL)

def extract_code(text: str, pattern: re.Pattern) -> Optional[str]:
    """Generic function to extract code from a markdown block."""
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return None

def get_sql_query_from_llm(
    user_query: str, db_schema: str, google_api_key: str, model_name: str
) -> Optional[str]:
    """
    Takes a user's natural language query and returns a SQL query from Google's Gemini.
    """
    system_prompt = f"""
You are an expert data analyst and a master of DuckDB SQL.
Your task is to convert a user's question into a single, valid DuckDB SQL query.
The user's data is in a table named 'my_data'.

This is the schema of the 'my_data' table:
{db_schema}

*** VERY IMPORTANT RULES FOR HANDLING DATES ***
1. When the user asks a question involving time or dates (e.g., "monthly sales", "trends over time"), you MUST inspect the schema for a relevant date column.
2. If the date column is of type VARCHAR or TEXT, it means the date is stored as a string and needs to be parsed.
3. To parse a string date, you MUST use the `strptime` function. `strptime` takes the column name and a format string.
4. You must intelligently guess the date format. Examples:
    - "January 2023" -> `strptime(your_column, '%B %Y')`
    - "2023-01-25" -> `strptime(your_column, '%Y-%m-%d')`
    - "25/01/2023" -> `strptime(your_column, '%d/%m/%Y')`
5. Use the result of `strptime` within other date functions, for example: `GROUP BY strftime(strptime(essay_date, '%B %Y'), '%Y-%m')`.

General Rules:
- If the user asks about the table's schema, use `PRAGMA table_info('my_data')` which returns columns `name` and `type`.
- ALWAYS wrap the final SQL query in a single markdown code block: ```sql\n[YOUR QUERY HERE]\n```
- Only output the SQL query. No commentary.
"""
    try:
        genai.configure(api_key=google_api_key)
        model = genai.GenerativeModel(model_name=model_name, system_instruction=system_prompt)
        response = model.generate_content(user_query)
        return extract_code(response.text, sql_pattern)
    except Exception as e:
        st.error(f"An error occurred while generating the SQL query: {e}")
        return None

def get_plot_code_from_llm(
    user_query: str, sql_result: pd.DataFrame, plot_type: str, google_api_key: str, model_name: str
) -> Optional[str]:
    """
    Takes a user query, a DataFrame, and a plot type, and returns Python code for a plot.
    """
    data_sample = sql_result.to_string()
    system_prompt = f"""
You are an expert data visualization programmer. Your task is to write Python code to visualize data based on a user's request.
The user has specifically requested a **{plot_type}**.
Your code will be executed in an environment where these are ALREADY IMPORTED:
- `plt` (from `matplotlib.pyplot`)
- `np` (from `numpy`)
- `sns` (from `seaborn`)
- `df` (a pandas DataFrame containing the data to plot)

RULES:
- You MUST write Python code.
- Do NOT include any import statements.
- The data is in the pandas DataFrame named `df`.
- Use the provided libraries (`plt`, `np`, `sns`) to create a clear and relevant {plot_type}.
- Use `plt.tight_layout()` to prevent labels from overlapping.
- Do NOT save the file (`plt.savefig()`) or show the plot (`plt.show()`). The plot will be captured directly.
- Wrap your Python code in a single markdown code block: ```python\n[YOUR CODE HERE]\n```
- Only output the code. No explanations.
"""
    prompt = f"""
User's original question: "{user_query}"
Data to plot (`df`):
{data_sample}
Write the Python code to create a {plot_type} of this data.
"""
    try:
        genai.configure(api_key=google_api_key)
        code_gen_model = "gemini-1.5-pro-latest"
        model = genai.GenerativeModel(model_name=code_gen_model, system_instruction=system_prompt)
        response = model.generate_content(prompt)
        return extract_code(response.text, python_pattern)
    except Exception as e:
        st.error(f"An error occurred while generating the plot code: {e}")
        return None 