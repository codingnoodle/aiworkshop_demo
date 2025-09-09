# 🎓 Clinical Trials Navigator - Workshop Setup Guide

Complete setup guide for the Clinical Trials Navigator workshop with OpenAI integration.

## 🚀 Quick Start (5 minutes)

### For Workshop Participants

**🎓 Recommended: Fork First (Personal Copy)**
1. **Go to**: `https://github.com/codingnoodle/aiworkshop_demo`
2. **Click "Fork"** button (creates your personal copy)
3. **Verify you're in your fork**: URL should show `github.com/YOUR_USERNAME/aiworkshop_demo`
4. **Go to your fork** → **"Code"** → **"Codespaces"** → **"Create codespace"**
5. **Wait 2-3 minutes** for setup
6. **Run**: `streamlit run app.py`
7. **Click the URL** that appears in the terminal
8. **Start exploring**: Enter "diabetes" in the chat box
9. **Experiment freely**: Make changes, try different approaches!

**✅ How to Know You Forked Correctly:**
- **URL shows your username**: `github.com/YOUR_USERNAME/aiworkshop_demo`
- **You see "forked from codingnoodle/aiworkshop_demo"** at the top
- **You can see the "Fork" button** (it will show your fork count)

**⚡ Quick Demo (No Fork)**
1. **Go to**: `https://github.com/codingnoodle/aiworkshop_demo`
2. **Click "Code"** → **"Codespaces"** → **"Create codespace"**
3. **Wait 2-3 minutes** for setup
4. **Run**: `streamlit run app.py`
5. **Note**: Changes will be lost when Codespace closes

### For Instructors

1. **Set up repository secret** (see API Key Setup section below)
2. **Share repository link** with participants
3. **Emphasize forking** - Make it clear this is required, not optional
4. **Guide through exercises** (see Workshop Exercises section)

#### **Preventing "Forgot to Fork" Issues:**

**Before Workshop:**
- **Send instructions early** - Include fork requirement in pre-workshop email
- **Create a checklist** - "Step 1: Fork the repository"
- **Show the fork button** - Point out exactly where to click

**During Workshop:**
- **Start with forking** - First 5 minutes dedicated to forking
- **Check everyone** - "Raise your hand if you see your username in the URL"
- **Verify forks** - Have participants confirm they're in their own repository

#### **Recovery: If Someone Forgot to Fork**

**Option 1: Fork Now (Recommended)**
1. **Go to**: `https://github.com/codingnoodle/aiworkshop_demo`
2. **Click "Fork"** button
3. **Close current Codespace**
4. **Go to your fork** → **"Code"** → **"Codespaces"** → **"Create codespace"**
5. **Start over** - You'll have your personal copy

**Option 2: Continue Without Fork (Limited)**
- **Can still participate** - App works the same
- **Changes will be lost** - When Codespace closes
- **No experimentation** - Can't modify code
- **Good for**: Just following along, not experimenting

**Option 3: Export Changes (Advanced)**
- **Download files** - Save any modifications locally
- **Fork later** - Apply changes to your fork
- **Complex** - Not recommended for beginners

## 🔑 API Key Setup (Instructors Only)

### Option 1: Repository Secret (Recommended)
1. **Get workshop API key** from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Set repository secret**:
   - Go to `https://github.com/codingnoodle/aiworkshop_demo/settings/secrets/actions`
   - Click **"New repository secret"**
   - **Name**: `OPENAI_API_KEY`
   - **Value**: Your workshop API key
   - Click **"Add secret"**
3. **Participants automatically get access** - no individual setup needed!

### Option 2: Individual API Keys
If participants use their own keys:
1. **In Codespace**: Settings → Environment Variables
2. **Add**: `OPENAI_API_KEY` = their personal key
3. **Restart Codespace**

## 🎯 Workshop Exercises (20 minutes)

### Exercise 1: Basic AI Search (5 minutes)
- **Search for "diabetes"**
- **Try "cancer"** (see AI clarification in action)
- **Explore the interactive map**
- **Click on trial markers** to see details

### Exercise 2: Profile Setup (5 minutes)
- **Open the left sidebar**
- **Fill out your user profile**:
  - Age, gender, location
  - Risk tolerance, travel preferences
- **See how AI enhances recommendations**
- **Try different risk tolerance levels**

### Exercise 3: Advanced Features (10 minutes)
- **Search for "multiple sclerosis"**
- **Look at the Story Journey section** (workflow visualization)
- **Check AI-powered eligibility summaries**
- **Try different medical conditions**
- **Compare AI responses** across different models

## 🧪 Testing Checklist

- [ ] App launches without errors
- [ ] Can search for "diabetes"
- [ ] AI clarification works for ambiguous terms
- [ ] Map loads with trial markers
- [ ] Can expand trial cards
- [ ] Profile sidebar works
- [ ] AI-enhanced recommendations appear
- [ ] Story Journey section shows workflow

## 🔧 Troubleshooting

### App won't start?
```bash
# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Try alternative launch
python -m streamlit run app.py
```

### OpenAI API issues?
```bash
# Check API key format (should start with sk-)
# Verify API key is valid at https://platform.openai.com/api-keys
# Check if you have credits in your OpenAI account
```

### Import errors?
```bash
# Install missing packages
pip install streamlit requests pandas plotly folium streamlit-folium

# For OpenAI features
pip install langchain-openai langgraph langchain-core
```

### API rate limits?
- OpenAI has rate limits based on your plan
- Try using GPT-3.5-turbo instead of GPT-4 for lower costs
- Check your usage at https://platform.openai.com/usage

### Map not loading?
- Check internet connection
- Try refreshing the page
- App works without map too!

## 💰 Cost Information

### Estimated Workshop Costs
- **GPT-3.5-turbo**: ~$0.001-0.002 per request
- **GPT-4**: ~$0.01-0.03 per request
- **Typical workshop usage**: $0.50-2.00 total per participant

### Cost Optimization Tips
- Use GPT-3.5-turbo for most tasks (cheaper and faster)
- Use GPT-4 only for complex medical clarifications
- Monitor usage at [OpenAI Usage Dashboard](https://platform.openai.com/usage)

## 🎓 Learning Objectives

By the end of this workshop, you'll understand:

1. **Clinical Trial Basics**: What trials are and how they work
2. **AI-Powered Search**: How OpenAI models enhance search and clarification
3. **Cloud AI Integration**: Using OpenAI API for real-time AI features
4. **Data Visualization**: Interactive maps and charts for trial data
5. **Personalization**: How user profiles improve recommendations
6. **Risk Assessment**: Understanding trial phases and safety levels

## 🏗️ Technical Architecture

This app demonstrates:

- **OpenAI Integration**: Cloud-based AI models for enhanced responses
- **LangGraph Workflows**: Multi-step AI agents with state management
- **Streamlit UI**: Interactive web applications in Python
- **API Integration**: Real-time data from ClinicalTrials.gov and OpenAI
- **Data Visualization**: Plotly charts and Folium maps
- **Personalization**: User profile matching algorithms

## 📊 Key Features to Explore

### Core Features
- **AI-Enhanced Search**: OpenAI models for better disease understanding
- **Real-time Search**: Live data from ClinicalTrials.gov
- **Interactive Map**: Global trial locations
- **Trial Details**: Comprehensive trial information
- **AI Eligibility Simplification**: OpenAI-powered criteria translation

### Advanced AI Features
- **Disease Clarification**: AI asks for more specific terms when needed
- **Smart Summarization**: Complex medical criteria made understandable
- **Personalized Matching**: Profile-based trial scoring with AI insights
- **Risk Assessment**: AI-powered safety level categorization
- **Reflexion Workflow**: Continuous result improvement using AI feedback

## 🛡️ Security Best Practices

### ✅ Do's
- Use environment variables (never hardcode API keys)
- Use Codespace-scoped variables when possible
- Monitor your API usage regularly
- Use GPT-3.5-turbo for cost efficiency

### ❌ Don'ts
- Never commit API keys to code
- Don't share API keys in chat or documentation
- Don't use production keys for workshops
- Don't leave unused Codespaces running

## 🎯 Workshop Goals

1. **Understand the Problem**: Why clinical trial discovery is challenging
2. **See the AI Solution**: How OpenAI models help patients find relevant trials
3. **Explore Cloud AI**: Hands-on experience with OpenAI API integration
4. **Learn the Technology**: LangGraph, Streamlit, and AI workflows
5. **Real-world Application**: Practical use case for healthcare AI

## 📞 Support

### For Technical Issues:
- **GitHub Codespaces**: [Documentation](https://docs.github.com/en/codespaces)
- **OpenAI API**: [Help Center](https://help.openai.com/)
- **Repository Issues**: Open an issue in the repository

### For Workshop Issues:
- **Instructor Support**: Contact your workshop leader
- **Setup Problems**: Check this guide step by step
- **Cost Questions**: Review OpenAI pricing at [OpenAI Pricing](https://openai.com/pricing)

## 🎉 Next Steps

After the workshop:

1. **Explore More**: Try different medical conditions with AI
2. **Customize**: Modify the code for your needs
3. **Extend**: Add new AI features or visualizations
4. **Share**: Use this tool to help others find trials
5. **Learn**: Dive deeper into OpenAI API and LangGraph

## ⚠️ Important Notes

- **Educational Purpose**: This is for learning and demonstration
- **Not Medical Advice**: Always consult healthcare professionals
- **Data Accuracy**: Verify trial information with official sources
- **Privacy**: API keys are handled securely, no personal data stored
- **Costs**: Monitor your OpenAI usage to avoid unexpected charges

---

**Ready to start? Run `streamlit run app.py` and begin exploring with AI!** 🚀
