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
    # --- PROMPT ENHANCEMENT for Type Casting ---
    system_prompt = f"""
You are an expert data analyst. You are a powerful SQL agent.
Your task is to convert a user's natural language question into a single, valid DuckDB SQL query.
The user's data is in a table named 'my_data'.

This is the schema of the 'my_data' table:
{db_schema}

IMPORTANT: If the user asks a question that requires a time-based calculation (e.g., grouping by month, finding trends over time) and the relevant date column is of type VARCHAR (text), you MUST cast it to a date or timestamp first.
Use the CAST function like this: `CAST(your_column_name AS DATE)` or `CAST(your_column_name AS TIMESTAMP)`.

For example, to group by month on a VARCHAR column named 'essay_date', you would use:
`STRFTIME('%Y-%m', CAST(essay_date AS DATE))`

If the user asks about the table's schema, you can use `PRAGMA table_info('my_data')`. This returns columns `name` and `type`.

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
    plot_type: str,
    google_api_key: str,
    model_name: str,
) -> Optional[str]:
    """Takes a user query, a DataFrame, and a plot type, and returns Python code for a plot."""
    data_sample = sql_result.to_string()

    # --- NEW, MORE ROBUST PROMPT ---
    system_prompt = f"""
You are an expert data visualization programmer. Your task is to write Python code to visualize data based on a user's request.

The user has specifically requested a **{plot_type}**.

Your code will be executed in a special environment where the following libraries and variables are ALREADY IMPORTED and available for you to use:
- `plt` (from `matplotlib.pyplot`)
- `np` (from `numpy`)
- `sns` (from `seaborn`)
- `df` (a pandas DataFrame containing the data to be plotted)

RULES:
- You MUST write Python code.
- Do NOT include any import statements (e.g., `import numpy as np`), as they are already provided.
- The data you need to plot is in the pandas DataFrame named `df`.
- Use the provided libraries (`plt`, `np`, `sns`) to create a clear and relevant {plot_type}.
- Use `plt.tight_layout()` to prevent labels from overlapping.
- You do NOT need to save the file. The plot will be captured directly. Do NOT include `plt.savefig()` or `plt.show()`.

Wrap your Python code in a single markdown code block: ```python\n[YOUR CODE HERE]\n```
Only output the code. No explanations.
"""

    prompt = f"""
User's original question: "{user_query}"

Data to plot (`df`):
{data_sample}

Write the Python code to create a {plot_type} of this data.
"""
    try:
        genai.configure(api_key=google_api_key)
        # Use a more capable model for code generation if available
        code_gen_model = "gemini-1.5-pro-latest"
        model = genai.GenerativeModel(model_name=code_gen_model, system_instruction=system_prompt)
        response = model.generate_content(prompt)
        return extract_code(response.text, python_pattern)
    except Exception as e:
        st.error(f"An error occurred while generating the plot code: {e}")
        return None 