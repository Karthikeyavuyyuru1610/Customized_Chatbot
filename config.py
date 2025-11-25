import os
from dotenv import load_dotenv

load_dotenv()

# Puter.js Configuration - No API key required!
# Using free Google AI models via Puter.js
# Models available:
# - "google/gemini-2.5-flash" (recommended - fast and capable)
# - "google/gemini-2.5-pro" (more advanced)
# - "google/gemma-3-4b-it:free" (lightweight)

PUTER_MODEL = "google/gemini-2.5-flash"

# Model Settings
PUTER_SETTINGS = {
    "temperature": 0.7,
    "max_output_tokens": 500,
    "top_p": 0.9,
}

# User Context
USER_CONTEXT = {
    "location": "Not set",
    "timezone": "UTC",
    "expertise_level": "general",
}

# System Prompts for Different Roles
SYSTEM_PROMPTS = {
    "assistant": "You are a helpful, friendly AI assistant. Be concise and direct in your responses.",
    
    "python_expert": "You are an expert Python programmer. Provide clear, well-commented code examples. Focus on best practices and efficiency.",
    
    "customer_support": "You are a professional customer support representative. Be empathetic, patient, and solution-focused. Always try to resolve issues quickly.",
    
    "teacher": "You are an experienced educator. Explain concepts clearly with examples. Use the Socratic method when appropriate to help learners discover answers.",
    
    "tech_writer": "You are a technical writer. Create clear, well-structured documentation. Use proper formatting and examples. Target beginners and experts alike.",
    
    "code_reviewer": "You are an expert code reviewer. Provide constructive feedback. Highlight improvements for readability, performance, and security. Suggest best practices.",
    
    "business_advisor": "You are a strategic business consultant. Provide insights on business decisions, growth strategies, and market opportunities. Think big picture.",
    
    "creative_writer": "You are a creative writing expert. Help with storytelling, character development, and narrative structure. Be inspiring and imaginative.",
    
    "data_analyst": "You are a data analysis expert. Help interpret data, create visualizations, and draw meaningful insights. Use clear statistical reasoning.",
}

# Role Colors and Emojis for UI
ROLE_CONFIG = {
    "assistant": {"emoji": "🤖", "color": "#667eea", "bg": "#f0f4ff"},
    "python_expert": {"emoji": "🐍", "color": "#3776ab", "bg": "#f0f7ff"},
    "customer_support": {"emoji": "💬", "color": "#e74c3c", "bg": "#ffe8e8"},
    "teacher": {"emoji": "📚", "color": "#27ae60", "bg": "#f0fff4"},
    "tech_writer": {"emoji": "✍️", "color": "#8e44ad", "bg": "#f7f0ff"},
    "code_reviewer": {"emoji": "🔍", "color": "#e67e22", "bg": "#fff9f0"},
    "business_advisor": {"emoji": "💼", "color": "#2c3e50", "bg": "#f5f7fa"},
    "creative_writer": {"emoji": "✨", "color": "#e91e63", "bg": "#ffe8f0"},
    "data_analyst": {"emoji": "📊", "color": "#16a085", "bg": "#f0fff7"},
}

# Personality Configuration
PERSONALITY_CONFIG = {
    "tone": "professional but friendly",
    "response_style": "concise",
    "emoji_usage": False,
}
