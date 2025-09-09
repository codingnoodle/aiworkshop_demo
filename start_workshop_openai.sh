#!/bin/bash

# Clinical Trials Navigator - OpenAI Workshop Launch Script
# This script sets up and launches the workshop environment with OpenAI integration

echo "🏥 Clinical Trials Navigator - OpenAI Workshop Setup"
echo "====================================================="

# Check if we're in a virtual environment or Codespace
if [[ "$VIRTUAL_ENV" != "" ]] || [[ "$CODESPACES" == "true" ]]; then
    echo "✅ Environment detected: $(if [[ "$CODESPACES" == "true" ]]; then echo "GitHub Codespace"; else echo "Virtual Environment"; fi)"
else
    echo "⚠️  No virtual environment detected. Creating one..."
    python -m venv venv
    source venv/bin/activate
    echo "✅ Virtual environment created and activated"
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if Streamlit is working
echo "🧪 Testing Streamlit..."
python -c "import streamlit; print('✅ Streamlit ready!')" 2>/dev/null || {
    echo "❌ Streamlit test failed. Installing..."
    pip install --upgrade streamlit
}

# Check OpenAI integration
echo "🤖 Testing OpenAI integration..."
python -c "from langchain_openai import ChatOpenAI; print('✅ OpenAI integration ready!')" 2>/dev/null || {
    echo "❌ OpenAI integration failed. Installing..."
    pip install --upgrade langchain-openai
}

# Check environment variable
echo "🔑 Checking OpenAI API key..."
if [[ -n "$OPENAI_API_KEY" ]]; then
    echo "✅ OpenAI API key is configured"
else
    echo "⚠️  OpenAI API key not found in environment variables"
    echo "📋 Please set OPENAI_API_KEY environment variable:"
    echo "   - In Codespaces: Settings → Environment Variables"
    echo "   - Locally: export OPENAI_API_KEY='your-key-here'"
fi

# Launch the application
echo "🚀 Launching Clinical Trials Navigator with OpenAI..."
echo "📋 Workshop instructions are in WORKSHOP_SETUP.md"
echo "🎯 Quick start: Enter 'diabetes' in the chat box to test"
echo ""
echo "The app will open in your browser automatically."
echo "If it doesn't, look for a URL like: http://localhost:8501"
echo ""

# Run Streamlit
streamlit run app.py --server.headless true --server.port 8501
