# 📊 Comprehensive AI SQL Agent

This is an interactive Streamlit application that acts as a powerful data analysis assistant. Users can upload a CSV file, and the agent, powered by Google's Gemini models, will answer natural language questions by generating and executing SQL queries locally. It can provide answers as data tables and generate various types of visualizations.

## ✨ Features

-   **Natural Language to SQL:** Ask questions in plain English (e.g., "What were the total sales last month?").
-   **Direct Google Gemini Integration:** Leverages the power of Gemini 1.5 Flash, Pro, and Gemini 1.0 for high-quality SQL generation.
-   **Local & Secure Execution:** Uses an in-memory DuckDB instance to process data locally. No data leaves your machine except for the schema sent to the LLM.
-   **Dynamic Prompt Suggestions:** Analyzes your uploaded data and automatically suggests relevant, insightful questions to get you started.
-   **User-Selected Visualizations:** Choose to visualize your query results as a Bar Chart, Line Chart, or Pie Chart. The agent writes the necessary Python `matplotlib` code on the fly.
-   **Simple UI:** Built with Streamlit for a clean, interactive, and user-friendly experience.
-   **Single API Key:** Greatly simplified architecture that only requires a Google AI API Key to function.

## ⚙️ How It Works

1.  **Upload:** The user uploads a CSV file.
2.  **Schema Analysis:** The application loads the data into an in-memory DuckDB table and extracts its schema.
3.  **Prompt Suggestion (Optional):** The schema is sent to Gemini to generate 5 insightful starting questions, which are displayed as clickable buttons.
4.  **User Query:** The user asks a question (or clicks a suggestion).
5.  **SQL Generation:** The user's query and the table schema are sent to Gemini, which generates a precise DuckDB SQL query.
6.  **Local Execution:** The generated SQL query is executed against the local DuckDB instance.
7.  **Visualization (Optional):** If a plot type is selected, the query result and original question are sent to Gemini again to generate Python `matplotlib` code. This code is executed locally to create a chart.
8.  **Display:** The results (data table and/or chart) are displayed to the user in the Streamlit interface.

## 🚀 Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone https://your-repo-url/comprehensive-sql-agent.git
    cd comprehensive-sql-agent
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

## 🏃‍♀️ Usage

1.  **Run the Streamlit application:**
    ```bash
    streamlit run src/app.py
    ```

2.  **Configure the application:**
    -   Your browser will open with the application running.
    -   In the sidebar, enter your **Google AI API Key**. You can get one from the [Google AI Studio](https://aistudio.google.com/app/apikey).
    -   Select the Gemini model you wish to use.

3.  **Analyze your data:**
    -   Upload a CSV file.
    -   Wait for the prompt suggestions to appear, or write your own question.
    -   Select a visualization type if desired.
    -   Click "Analyze"! 