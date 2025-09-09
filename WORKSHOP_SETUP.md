# 🎓 Workshop Setup Guide

## 🚀 Quick Start (5 minutes)

### For Participants
1. **Fork repository**: Go to `https://github.com/codingnoodle/aiworkshop_demo` → Click "Fork"
2. **Create Codespace**: In your fork → "Code" → "Codespaces" → "Create codespace"
3. **Wait 2-3 minutes** for setup
4. **Run the app** (see Commands section below)
5. **Start exploring**: Enter "diabetes" in the chat box



## 🔑 API Key Setup

### For Participants
1. **Get workshop key** from instructor
2. **In your fork** → **Settings** → **Secrets and variables** → **Actions**
3. **New repository secret**:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: Workshop key from instructor
4. **Create new Codespace** (will use the key automatically)


## 🎯 Workshop Exercises (20 minutes)

1. **Search "diabetes"** - See AI clarification in action
2. **Set up profile** - Age, gender, location, risk tolerance
3. **Try "cancer"** - Explore interactive map and trial details
4. **Search "multiple sclerosis"** - Check AI eligibility summaries

## 🔧 Codespace Commands

### Setup (First Time)
```bash
# Navigate to project directory
cd /workspaces/aiworkshop_demo

# Create virtual environment (for Alpine Linux)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run app on port 8501
streamlit run app.py --server.port 8501
```

### Restart App
```bash
# Kill running Streamlit process
pkill -f "streamlit run app.py"

# Restart on port 8501
streamlit run app.py --server.port 8501
```

### Quick Restart (if venv exists)
```bash
cd /workspaces/aiworkshop_demo
source venv/bin/activate
streamlit run app.py --server.port 8501
```
---

**Ready to start? Use the setup commands above!** 🚀