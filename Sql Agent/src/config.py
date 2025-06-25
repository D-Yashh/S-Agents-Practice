"""
Centralized configuration for the AI SQL Agent.
This file contains settings and options that are shared across the application,
such as the list of available Large Language Models from Google AI.
"""

# A dictionary mapping user-friendly model names to their specific identifiers
# for the Google AI API.
# THIS LIST SHOULD ONLY CONTAIN GOOGLE GEMINI MODELS.
MODEL_OPTIONS = {
    "Google Gemini 1.5 Flash": "gemini-1.5-flash-latest",
    "Google Gemini 1.5 Pro": "gemini-1.5-pro-latest",
    "Google Gemini 1.0 Pro": "gemini-pro",
} 