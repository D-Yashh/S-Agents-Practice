Create a comprehensive AI SQL Agent application with the following specifications:
Build a complete Streamlit application that acts as an intelligent data analysis assistant. The app should allow users to upload CSV files and ask natural language questions that get converted to SQL queries and executed locally with visualizations.
Core Requirements:
1. Architecture & Technology Stack

Use Streamlit for the web interface
Integrate Google's Gemini AI models (2.0 Flash, 2.0 Flash-Lite, 1.5 Pro) for natural language processing
Use DuckDB for in-memory SQL execution (local and secure)
Support matplotlib/seaborn for dynamic visualizations
Include pandas for data manipulation

2. Key Features

Natural Language to SQL: Convert plain English questions into DuckDB SQL queries
Local Data Processing: All data stays on user's machine, only schema sent to LLM
Dynamic Prompt Suggestions: Analyze uploaded data schema and suggest 4 relevant questions
Multiple Visualization Types: Bar charts, line charts, pie charts generated on-demand
Smart Date Handling: Automatically detect and parse date columns in various formats
Schema Analysis: Display table structure and column types

3. Application Flow

User uploads CSV file
App loads data into DuckDB in-memory database
Schema is extracted and displayed
System generates curated prompt suggestions based on data structure
User asks question (natural language) or clicks a suggestion
Question + schema sent to Gemini to generate SQL
SQL executed locally against DuckDB
Results displayed as data table
If visualization selected, results + question sent to Gemini to generate matplotlib code
Visualization code executed and chart displayed

4. File Structure
Create a modular structure with:

src/app.py - Main Streamlit application
src/agent.py - LLM interaction functions
src/config.py - Configuration constants
src/__init__.py - Empty init file
requirements.txt - Dependencies
README.md - Comprehensive documentation

5. Specific Implementation Details
Date Handling Intelligence

Detect VARCHAR/TEXT date columns in schema
Use DuckDB's strptime() function for parsing string dates
Auto-detect common date formats (e.g., "January 2023", "2023-01-25", "25/01/2023")
Handle monthly/yearly aggregations properly

Prompt Engineering

Create system prompts that emphasize DuckDB SQL syntax
Include specific rules for date parsing and formatting
Generate visualization code that doesn't include imports (pre-imported environment)
Use regex patterns to extract SQL and Python code from LLM responses

User Experience

Sidebar for API key configuration and model selection
Expandable section for prompt suggestions
Real-time feedback and error handling
Session state management for uploaded files
Clean, professional UI with emojis and clear sections

Security & Performance

In-memory database (no persistent storage)
Temporary file cleanup
API key protection (password input)
Error handling for LLM failures and SQL execution

6. Advanced Features

Smart Column Detection: Automatically identify text, numeric, and date columns
Curated Suggestions: Generate reliable questions based on data structure
Code Generation: Dynamic matplotlib code creation for chosen visualization types
Session Management: Persist user selections and clear state on new file upload

7. Configuration Options

Support multiple Gemini models with user selection
Configurable plot types (None, Bar Chart, Line Chart, Pie Chart)
Centralized configuration for easy maintenance

8. Documentation Requirements

Comprehensive README with setup instructions
Clear feature descriptions
Usage examples and screenshots
API key setup instructions
Installation and running steps

The application should be production-ready with proper error handling, clean code organization, and a polished user interface. Focus on making it user-friendly for non-technical users while maintaining the power for advanced data analysis.

Additional Technical Specifications:

Use regex patterns for reliable code extraction from LLM responses
Implement proper state management to handle file uploads and user interactions
Create helper functions for column type identification and suggestion generation
Ensure matplotlib plots are properly managed (figure creation/cleanup)
Handle edge cases like empty datasets, invalid queries, and API failures
Make the interface responsive and intuitive with clear visual hierarchy 