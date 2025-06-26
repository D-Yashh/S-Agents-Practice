# Comprehensive AI SQL Agent

This Streamlit application functions as an interactive data analysis assistant. Users can upload a CSV file, and the agent, powered by Google's Gemini models, answers natural language questions by generating and executing SQL queries. It can return data tables and create visualizations on the fly.

## Features

-   **Natural Language to SQL:** Ask questions in plain English (e.g., "What were the total sales last month?").
-   **Google Gemini Integration:** Leverages Google's Gemini models for high-quality SQL generation.
-   **Local & Secure Execution:** Uses an in-memory DuckDB instance to process data locally. No data leaves your machine except for the table schema sent to the LLM.
-   **Dynamic Prompt Suggestions:** Analyzes your data to automatically suggest relevant questions.
-   **On-the-Fly Visualizations:** Generate Bar, Line, or Pie charts from your query results using `matplotlib`.
-   **Simplified Architecture:** Requires only a single Google AI API Key to operate.

## How It Works

1.  **Upload:** The user uploads a CSV file via the Streamlit interface.
2.  **Schema Analysis:** The data is loaded into a local in-memory DuckDB table and its schema is extracted.
3.  **Query Generation:** The user's natural language question and the table schema are sent to the Gemini model to generate a precise DuckDB SQL query.
4.  **Local Execution:** The generated SQL query is executed against the local DuckDB instance.
5.  **Visualization (Optional):** If a chart type is selected, the query result is sent to Gemini again to generate and execute Python `matplotlib` code.
6.  **Display:** The results (data table and/or chart) are displayed in the Streamlit app.

## Building the Agent: The Core LLM Prompt

This agent was developed using a single, targeted prompt that instructs the LLM on its role, capabilities, and output format.

You can find the complete prompt used to create this agent in the file below. It is designed to be versatile and can be adapted for use with other major LLM providers (e.g., OpenAI, Anthropic) to achieve similar results.

-   **[SQL_AGENT_PROMPT.md](SQL_AGENT_PROMPT.md)**

## Setup and Usage

It is assumed you have already cloned the repository and are in the `agents/sql_agent` directory.

### Prerequisites

-   A **Google AI API Key**. You can get one from the [Google AI Studio](https://aistudio.google.com/app/apikey).

### Instructions

1.  **Create a virtual environment and install dependencies:**
    ```bash
    # Create and activate a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

    # Install required packages
    pip install -r requirements.txt
    ```

2.  **Run the Streamlit application:**
    ```bash
    streamlit run src/app.py
    ```

3.  **Use the Agent:**
    -   Your browser will open with the application running.
    -   In the sidebar, enter your **Google AI API Key** and select a Gemini model.
    -   Upload a CSV file.
    -   Ask a question or click on a generated suggestion.
    -   Optionally, select a visualization type and click "Analyze".

## License

This project is licensed under the MIT License. See the `LICENSE` file in the root of the repository for more information. 