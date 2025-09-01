# 🤖 Ollama Integration Setup Guide

This branch adds local AI model support using Ollama, allowing you to run the clinical trials app with local LLM inference instead of cloud-based APIs.

## 🚀 Quick Start

### 1. Install Ollama

First, install Ollama on your system:

**macOS:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from [https://ollama.ai](https://ollama.ai)

### 2. Install Models

Install the recommended models:

```bash
# Install Llama 3.1 8B (recommended)
ollama pull llama3.1:8b

# Or install Phi-3 Mini (faster, smaller)
ollama pull phi3:mini
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Test the Integration

```bash
python test_ollama.py
```

### 5. Run the App

```bash
streamlit run app.py
```

## 🎯 Features

### Model Selection
- Choose from available Ollama models in the sidebar
- Test model connection before using
- Real-time model status display

### Enhanced AI Responses
- **Smart Disease Detection**: Better clarification for ambiguous disease terms
- **Simplified Eligibility**: AI-powered translation of complex medical criteria
- **Local Processing**: All AI responses generated locally for privacy

### UI Improvements
- Model configuration sidebar
- Connection testing
- Real-time status indicators
- Enhanced styling for model information

## 🔧 Configuration

### Available Models

The app supports any Ollama model. Recommended models:

- **llama3.1:8b**: Best balance of performance and quality
- **phi3:mini**: Faster inference, good for testing
- **llama3.1:70b**: Higher quality (requires more RAM)

### Model Settings

You can customize model behavior by modifying the `get_ollama_llm()` function in `app.py`:

```python
llm = ChatOllama(
    model=model_name,
    temperature=0.1,  # Lower = more focused responses
    # Add other parameters as needed
)
```

## 🧪 Testing

Run the test script to verify everything is working:

```bash
python test_ollama.py
```

This will test:
1. Ollama installation
2. Available models
3. API connection
4. Basic inference

## 🔍 How It Works

### LLM Integration
- Replaces mock responses with real AI-generated content
- Uses structured prompts for better results
- Handles errors gracefully with fallback responses

### Prompt Engineering
The app uses specialized prompts for different tasks:

1. **Disease Clarification**: Asks for specific disease types
2. **Eligibility Simplification**: Translates medical jargon to plain language
3. **General Assistance**: Provides helpful responses for trial searches

### State Management
- Model selection persists across sessions
- Agent state includes selected model
- Cached LLM instances for performance

## 🐛 Troubleshooting

### Common Issues

**"No Ollama models found"**
```bash
# Install a model
ollama pull llama3.1:8b
```

**"Model connection failed"**
```bash
# Start Ollama service
ollama serve
```

**Import errors**
```bash
# Reinstall dependencies
pip install --upgrade langchain-ollama
```

### Performance Tips

1. **Use smaller models** for faster responses (phi3:mini)
2. **Adjust temperature** for more focused responses
3. **Cache LLM instances** (already implemented)
4. **Monitor memory usage** with larger models

## 🔒 Privacy & Security

### Local Processing
- All AI responses generated locally
- No data sent to external APIs
- Complete privacy for medical queries

### Data Handling
- Clinical trial data from public APIs only
- No personal information stored
- Session data cleared on app restart

## 📊 Performance Comparison

| Model | Size | Speed | Quality | RAM Usage |
|-------|------|-------|---------|-----------|
| llama3.1:8b | 4.9GB | Medium | High | ~8GB |
| phi3:mini | 2.2GB | Fast | Good | ~4GB |
| llama3.1:70b | 40GB | Slow | Very High | ~80GB |

## 🚀 Next Steps

### Potential Enhancements
1. **Model Fine-tuning**: Custom models for medical domain
2. **Response Caching**: Cache common queries
3. **Batch Processing**: Process multiple trials simultaneously
4. **Advanced Prompts**: More sophisticated medical reasoning

### Contributing
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📞 Support

For issues with:
- **Ollama**: Check [Ollama documentation](https://ollama.ai/docs)
- **App Integration**: Check the main README.md
- **Model Performance**: Try different models or adjust settings

---

**Note**: This integration provides local AI capabilities while maintaining the same user experience as the cloud-based version.
