#!/usr/bin/env python3
"""
Test script for Ollama integration
"""

import sys
import subprocess

def test_ollama_installation():
    """Test if Ollama is installed and running"""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama is installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Ollama is not working properly")
            return False
    except FileNotFoundError:
        print("❌ Ollama is not installed")
        return False

def test_ollama_models():
    """Test available Ollama models"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Available Ollama models:")
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            for line in lines:
                if line.strip():
                    print(f"   - {line}")
            return True
        else:
            print("❌ Could not list Ollama models")
            return False
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return False

def test_ollama_api():
    """Test Ollama API connection"""
    try:
        from langchain_ollama import ChatOllama
        
        # Test with llama3.1:8b model
        llm = ChatOllama(model="llama3.1:8b", temperature=0.1)
        response = llm.invoke("Hello, this is a test message.")
        
        print("✅ Ollama API test successful!")
        print(f"   Response: {response.content[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Ollama API test failed: {e}")
        return False

def main():
    print("🧪 Testing Ollama Integration")
    print("=" * 40)
    
    # Test 1: Ollama installation
    print("\n1. Testing Ollama installation...")
    if not test_ollama_installation():
        print("Please install Ollama first: https://ollama.ai")
        sys.exit(1)
    
    # Test 2: Available models
    print("\n2. Testing available models...")
    if not test_ollama_models():
        print("Please install models using: ollama pull llama3.1:8b")
        sys.exit(1)
    
    # Test 3: API connection
    print("\n3. Testing API connection...")
    if not test_ollama_api():
        print("Please ensure Ollama is running: ollama serve")
        sys.exit(1)
    
    print("\n🎉 All tests passed! Ollama integration is working correctly.")
    print("You can now run the Streamlit app with: streamlit run app.py")

if __name__ == "__main__":
    main()
