# 🏥 Clinical Trials Navigator - Workshop Edition

Welcome to the Clinical Trials Navigator workshop! This application helps patients and caregivers find and understand clinical trials using AI-powered search and analysis.

## 🚀 Quick Start (2 minutes)

### Option 1: Automatic Setup (Recommended)
```bash
python setup_workshop.py
streamlit run app.py
```

### Option 2: Manual Setup
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Option 3: Using Codespaces (Already Done!)
If you're in GitHub Codespaces, everything is already set up! Just run:
```bash
streamlit run app.py
```

## 🎯 Workshop Exercises

### Exercise 1: Basic Search (5 minutes)
1. **Launch the app**: `streamlit run app.py`
2. **Test search**: Enter "diabetes" in the chat box
3. **Explore results**: 
   - Look at the trial count
   - Check the interactive map
   - Click on map markers
   - Expand trial cards

### Exercise 2: Profile Personalization (5 minutes)
1. **Open sidebar**: Look for "👤 User Profile & Preferences"
2. **Fill your profile**:
   - Age: Your current age
   - Gender: Your preference
   - Location: Your preferred trial location
   - Risk Tolerance: How comfortable with experimental treatments
   - Travel Preference: How far you're willing to travel
3. **See changes**: Notice how recommendations update automatically

### Exercise 3: Advanced Features (10 minutes)
1. **Search different conditions**:
   - "breast cancer"
   - "multiple sclerosis" 
   - "Alzheimer's disease"
2. **Explore Story Journey**: Look at the workflow visualization
3. **Check risk assessments**: See how trials are categorized by risk
4. **Try eligibility summaries**: See how AI simplifies complex criteria

### Exercise 4: Interactive Features (5 minutes)
1. **Map exploration**: Click different colored markers
2. **Trial details**: Expand cards to see full information
3. **Demographics**: Check age groups and gender requirements
4. **Phase analysis**: Understand what different trial phases mean

## 🧪 Testing Checklist

- [ ] App launches without errors
- [ ] Can search for "diabetes"
- [ ] Map loads with trial markers
- [ ] Can expand trial cards
- [ ] Profile sidebar works
- [ ] Personalized recommendations appear
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

### Import errors?
```bash
# Install missing packages
pip install streamlit requests pandas plotly folium streamlit-folium

# For LangGraph features
pip install langgraph langchain-core langchain-openai
```

### Map not loading?
- Check internet connection
- Try refreshing the page
- App works without map too!

### Slow performance?
- This is normal for first-time setup
- Subsequent searches will be faster
- Large datasets may take a moment to process

## 🎓 Learning Objectives

By the end of this workshop, you'll understand:

1. **Clinical Trial Basics**: What trials are and how they work
2. **AI-Powered Search**: How LangGraph creates intelligent workflows
3. **Data Visualization**: Interactive maps and charts for trial data
4. **Personalization**: How user profiles improve recommendations
5. **Risk Assessment**: Understanding trial phases and safety levels

## 🏗️ Technical Architecture

This app demonstrates:

- **LangGraph Workflows**: Multi-step AI agents with state management
- **Streamlit UI**: Interactive web applications in Python
- **API Integration**: Real-time data from ClinicalTrials.gov
- **Data Visualization**: Plotly charts and Folium maps
- **Personalization**: User profile matching algorithms

## 📊 Key Features to Explore

### Core Features
- **Conversational Interface**: Chat with an AI agent
- **Real-time Search**: Live data from ClinicalTrials.gov
- **Interactive Map**: Global trial locations
- **Trial Details**: Comprehensive trial information
- **Eligibility Simplification**: AI-powered criteria translation

### Advanced Features
- **Personalized Matching**: Profile-based trial scoring
- **Risk Assessment**: Safety level categorization
- **Reflexion Workflow**: Continuous result improvement
- **Story Journey**: Visual workflow progression
- **Demographic Analysis**: Age, gender, and study type breakdowns

## 🎯 Workshop Goals

1. **Understand the Problem**: Why clinical trial discovery is challenging
2. **See the Solution**: How AI can help patients find relevant trials
3. **Explore the Technology**: LangGraph, Streamlit, and data visualization
4. **Hands-on Experience**: Interactive exploration of the application
5. **Real-world Application**: Practical use case for healthcare technology

## 📞 Need Help?

- **Instructor**: Ask your workshop leader
- **Documentation**: Check the main README.md
- **Code Comments**: Look at the source code for explanations
- **Community**: GitHub issues and discussions

## 🎉 Next Steps

After the workshop:

1. **Explore More**: Try different medical conditions
2. **Customize**: Modify the code for your needs
3. **Extend**: Add new features or visualizations
4. **Share**: Use this tool to help others find trials
5. **Learn**: Dive deeper into LangGraph and Streamlit

## ⚠️ Important Notes

- **Educational Purpose**: This is for learning and demonstration
- **Not Medical Advice**: Always consult healthcare professionals
- **Data Accuracy**: Verify trial information with official sources
- **Privacy**: No personal data is stored or transmitted

---

**Ready to start? Run `streamlit run app.py` and begin exploring!** 🚀
