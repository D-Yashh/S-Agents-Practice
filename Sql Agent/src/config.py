"""
Centralized configuration for the AI SQL Agent.
This file contains settings and options that are shared across the application,
such as the list of available Large Language Models from Google AI,
prioritizing models with high free-tier rate limits.
"""

# A dictionary mapping user-friendly model names to their specific, official API identifiers.
# This list now uses the newer preview models for better rate limits.
# The google-generativeai library will automatically use the correct API version.
MODEL_OPTIONS = {
    # High-rate-limit preview models, as requested.
    "Gemini 2.0 Flash-Lite": "gemini-2.0-flash-lite",
    "Gemini 2.0 Flash": "gemini-2.0-flash",

    # The most powerful available model for complex queries.
    "Gemini 1.5 Pro (Latest)": "gemini-1.5-pro-latest",
}

# A list of plot types for the user to select from.
PLOT_TYPES = ["None", "Bar Chart", "Line Chart", "Pie Chart"] 