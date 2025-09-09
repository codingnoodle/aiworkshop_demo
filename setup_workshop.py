#!/usr/bin/env python3
"""
Workshop Setup Script for Clinical Trials Navigator
This script helps workshop participants get started quickly.
"""

import subprocess
import sys
import os
import time

def run_command(command, description):
    """Run a command and print the result."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible!")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible. Need Python 3.8+")
        return False

def install_dependencies():
    """Install required dependencies."""
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def test_streamlit():
    """Test if Streamlit can be imported."""
    print("\n🧪 Testing Streamlit installation...")
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False

def test_openai():
    """Test if OpenAI can be imported."""
    print("\n🤖 Testing OpenAI integration...")
    try:
        from langchain_openai import ChatOpenAI
        print("✅ OpenAI integration ready!")
        return True
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False

def create_workshop_instructions():
    """Create workshop-specific instructions."""
    instructions = """
# 🎯 Workshop Quick Start Guide

## 🚀 Getting Started (2 minutes)

1. **Run the app**: `streamlit run app.py`
2. **Open your browser**: Click the link that appears in the terminal
3. **Test the app**: Enter "diabetes" in the chat box
4. **Explore features**: Try the interactive map and trial details

## 🧪 Workshop Exercises

### Exercise 1: OpenAI Setup (2 minutes)
- Get your OpenAI API key from https://platform.openai.com/api-keys
- Enter the API key in the left sidebar
- Test the model connection
- Select your preferred OpenAI model

### Exercise 2: AI-Enhanced Search (5 minutes)
- Search for "breast cancer"
- Try ambiguous terms like "cancer" to see AI clarification
- Explore the interactive map
- Click on different trial markers
- Expand trial cards to see AI-simplified details

### Exercise 3: Profile Setup with AI (5 minutes)
- Open the left sidebar
- Fill out your user profile
- See how AI enhances recommendations
- Try different risk tolerance levels
- Notice AI-powered personalization

### Exercise 4: Advanced AI Features (10 minutes)
- Search for "multiple sclerosis"
- Look at the Story Journey section with AI workflow
- Examine the AI-powered workflow visualization
- Try different medical conditions
- Compare AI responses across different models

## 🔧 Troubleshooting

### If the app doesn't start:
```bash
pip install --upgrade streamlit
streamlit run app.py
```

### If you see import errors:
```bash
pip install -r requirements.txt
```

### If the map doesn't load:
- Check your internet connection
- Try refreshing the page
- The app works without the map too!

## 📞 Need Help?

- Check the main README.md for detailed instructions
- Ask your workshop instructor
- Look at the troubleshooting section in the README

## 🎉 You're Ready!

The app is now running and ready for the workshop!
"""
    
    with open("WORKSHOP_GUIDE.md", "w") as f:
        f.write(instructions)
    
    print("✅ Workshop guide created: WORKSHOP_GUIDE.md")

def main():
    """Main setup function."""
    print("🏥 Clinical Trials Navigator - Workshop Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation.")
        sys.exit(1)
    
    # Test Streamlit
    if not test_streamlit():
        print("\n❌ Setup failed at Streamlit test.")
        sys.exit(1)
    
    # Test OpenAI integration
    if not test_openai():
        print("\n❌ Setup failed at OpenAI integration test.")
        sys.exit(1)
    
    # Create workshop guide
    create_workshop_instructions()
    
    print("\n" + "=" * 50)
    print("🎉 Workshop setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run: streamlit run app.py")
    print("2. Open the URL in your browser")
    print("3. Read WORKSHOP_GUIDE.md for exercises")
    print("\n🚀 Ready for the workshop!")

if __name__ == "__main__":
    main()
