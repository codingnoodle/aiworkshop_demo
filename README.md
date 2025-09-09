# 🏥 Clinical Trials Navigator

An AI-powered web application that helps patients and caregivers find and understand clinical trials for their medical conditions.

## 🎯 **What This App Does**

- **Find relevant clinical trials** for your specific condition
- **Understand eligibility criteria** in simple, plain language
- **See trial locations** on an interactive world map
- **Get personalized recommendations** based on your profile
- **Learn about trial phases** and what they mean for you

## 🚀 **Quick Start**

### **🎓 For Workshop Participants**

**Option 1: Fork & Codespace (Recommended)**
1. **Fork this repository** (click "Fork" button)
2. **Go to your fork** → **"Code" → "Codespaces" → "Create codespace"**
3. **Wait 2-3 minutes** for setup
4. **Run**: `streamlit run app.py`
5. **Click the URL** that appears
6. **Start exploring**: Enter "diabetes" in the chat box

**Option 2: Direct Codespace**
1. **Click "Code" → "Codespaces" → "Create codespace"** on this repository
2. **Wait 2-3 minutes** for setup
3. **Run**: `streamlit run app.py`
4. **Note**: Changes will be lost when Codespace closes

**Complete setup guide**: See `WORKSHOP_SETUP.md` for API key configuration and exercises

### **🏠 For Local Setup**

1. **Clone the repository**
2. **Create virtual environment**: `python -m venv venv`
3. **Activate environment**: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Run the app**: `streamlit run app.py`
6. **Open browser**: Go to `http://localhost:8501`

## 🔑 **API Key Setup (Optional)**

The app works without an API key using fallback responses. For enhanced AI features:

1. **Get OpenAI API key** from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Set environment variable**: `export OPENAI_API_KEY='your-key-here'`
3. **Restart the app**

## 🎯 **How to Use**

1. **Enter your condition** in the chat box (e.g., "diabetes", "breast cancer")
2. **Set your profile** in the sidebar (age, location, preferences)
3. **Explore results**:
   - Interactive map showing trial locations
   - Trial details with simplified eligibility criteria
   - Personalized recommendations
   - Risk analysis and safety information

## 🧠 **How It Works**

The app uses AI to:
- **Clarify** your condition if needed
- **Search** thousands of clinical trials
- **Simplify** complex medical terminology
- **Match** trials to your personal situation
- **Explain** everything in plain language

See `LANGGRAPH_WORKFLOW.md` for a detailed explanation of the AI system.

## 📁 **Repository Structure**

- **`app.py`**: Main Streamlit application
- **`WORKSHOP_SETUP.md`**: Complete workshop setup guide
- **`LANGGRAPH_WORKFLOW.md`**: AI system explanation
- **`requirements.txt`**: Python dependencies
- **`.devcontainer/`**: GitHub Codespace configuration

## 🌿 **Branches**

- **`main`**: OpenAI integration (default, workshop-ready)
- **`ollama-integration`**: Local AI version using Ollama

## 🛠️ **Troubleshooting**

### **Common Issues**
- **"Command not found"**: Wait for Codespace setup to complete
- **"API Key Required"**: App still works with fallback responses
- **App not loading**: Check if port 8501 is forwarded

### **Need Help?**
- **Workshop participants**: See `WORKSHOP_SETUP.md`
- **Technical issues**: Check the troubleshooting section in `WORKSHOP_SETUP.md`
- **AI system**: Read `LANGGRAPH_WORKFLOW.md`


## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**🎯 Ready to explore clinical trials? Start with the Quick Start guide above!**