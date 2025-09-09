# 🏥 Patient & Caregiver Trial Navigator

A comprehensive Streamlit web application that helps patients and caregivers find and understand clinical trials for specific medical conditions. The app uses LangGraph to create a stateful, multi-step agent that interacts with the ClinicalTrials.gov API to provide personalized trial information.

---

## 📖 **Understanding the App**

### 🎯 **What This App Does**

This application is designed to bridge the gap between complex clinical trial information and patients who need it. It transforms technical medical jargon into understandable insights, helping you:

- **Find relevant clinical trials** for your specific condition
- **Understand if you might qualify** based on age, gender, and other factors
- **See where trials are happening** with an interactive world map
- **Learn about trial phases** and what they mean for you
- **Get simplified explanations** of complex eligibility criteria

### 🆕 **What's New**

**🤖 AI Integration**: The app now uses OpenAI API by default for enhanced AI responses:
- **OpenAI Integration** (main branch): Cloud-based AI using OpenAI API for enhanced responses
- **Smart Fallbacks**: All AI features work out of the box with intelligent fallback responses
- **Alternative Options**: Ollama integration available on `ollama-integration` branch for local AI

**🔄 Reflexion Workflow**: The system now continuously improves search results through intelligent feedback loops, ensuring you get the best possible matches for your condition.

**🎯 Personalized Matching**: Set your profile preferences and get trials scored specifically for you, with clear explanations of why each trial matches.

---

## 🚀 **Quick Start Guide**

### **🎓 For Workshop Participants (GitHub Codespaces)**

**🎓 For Workshop Participants (Fork First!):**
1. **Fork this repository** (click "Fork" button) - **This creates your personal copy**
2. **Go to your fork** → **"Code" → "Codespaces" → "Create codespace"**
3. **Wait for setup** (2-3 minutes for first time)
4. **Run**: `streamlit run app.py`
5. **Click the URL** that appears in the terminal
6. **Start exploring**: Enter "diabetes" in the chat box
7. **Experiment freely**: Make changes, try different approaches!

**⚡ Quick Demo (No Fork):**
1. **Click "Code" → "Codespaces" → "Create codespace"** on this repository
2. **Wait for setup** (2-3 minutes for first time)
3. **Run**: `streamlit run app.py`
4. **Click the URL** that appears in the terminal
5. **Note**: Changes will be lost when Codespace closes

**Workshop-specific instructions**: See `WORKSHOP_SETUP.md` for complete setup and exercises

### **For First-Time Users (Local Setup)**

1. **Open the App**: Navigate to the provided URL (usually `http://localhost:8501`)
2. **Enter Your Condition**: Type a specific medical condition in the chat box
   - Examples: "breast cancer", "diabetes", "multiple sclerosis", "depression"
   - Be specific: "lung cancer" works better than just "cancer"
3. **Wait for Results**: The app will search ClinicalTrials.gov and process the data
4. **Explore the Results**: Use the interactive features to understand your options

### **What You'll See**

After entering a condition, you'll get:

1. **📊 Trial Overview**: Number of recruiting trials found
2. **🌍 Interactive Map**: Trial locations with color-coded markers
3. **📈 Phase Distribution**: What stages of research are available
4. **👥 Demographic Analysis**: Age groups, gender requirements, study types
5. **📋 Trial Details**: Expandable cards with specific trial information
6. **✅ Simplified Eligibility**: AI-powered translation of technical criteria into plain language

---

## 🌿 **Available Branches**

This repository includes multiple versions optimized for different use cases:

### **Main Branch** (Default)
- **OpenAI Integration**: Uses OpenAI API for enhanced AI responses
- **Smart Fallbacks**: Works without API key setup
- **Perfect for**: Workshops and production use

### **Ollama Integration Branch** (`ollama-integration`)
- **Local AI**: Uses Ollama for privacy-focused AI responses
- **Advanced Features**: Same as main branch but runs locally
- **Perfect for**: Privacy-conscious users and offline environments
- **Setup**: Requires Ollama installation

### **Switching Branches**
```bash
# Switch to Ollama version (local AI)
git checkout ollama-integration

# Switch back to main (OpenAI integration)
git checkout main
```

---

## 🔧 **Installation & Setup**

### **Prerequisites**

- Python 3.8 or higher
- pip (Python package installer)

### **Step-by-Step Installation**

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd clinical_trials
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501` to access the application.

### **Optional: Enhanced AI Setup (5 minutes)**

**Without Ollama**: The app uses smart fallback responses for AI features  
**With Ollama**: Get enhanced disease clarification and eligibility simplification

```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Download a model
ollama pull llama3.1:8b    # Best balance of performance/quality

# 3. Test in the app sidebar
# Use "Test Model Connection" button
```

---

## 🧪 **Testing the App**

### **Basic Functionality Test**

1. **Launch the app**: `streamlit run app.py`
2. **Test search**: Enter "diabetes" in the chat box
3. **Verify results**: Check that trials appear and map loads
4. **Test interactions**: Click on map markers and expand trial cards

### **Advanced Features Test**

1. **Profile setup**: Fill out the user profile in the left sidebar
2. **Personalization**: Verify that trial recommendations change based on your profile
3. **Risk assessment**: Check that risk levels are displayed correctly
4. **Story Journey**: Look for the workflow visualization at the bottom

### **AI Features Test**

1. **Basic AI**: Test disease clarification with ambiguous terms
2. **Ollama integration**: If installed, test enhanced AI responses
3. **Eligibility summarization**: Check that complex criteria are simplified

---

## ✨ **Features Overview**

### **Core Features**

- **Conversational Interface**: Chat-based interaction with an AI agent that can clarify ambiguous disease inputs
- **Real-time Trial Search**: Direct integration with ClinicalTrials.gov API v2
- **Interactive Visualizations**:
  - 🌍 **Interactive World Map**: Shows trial locations with color-coded markers by phase
  - 📊 **Trial Phase Distribution**: Swimlane chart showing distribution of trial phases
  - 📊 **Demographic Analysis**: Age groups, gender requirements, and study types
  - 📈 **Enrollment Statistics**: Total, average, largest, and smallest study sizes
- **Simplified Eligibility Criteria**: AI-powered translation of technical criteria into plain language
- **Detailed Trial Information**: Expandable cards with comprehensive trial details

### **🆕 Advanced Features**

#### **🎯 Personalized Trial Matching**
- **User Profile System**: Set your age, gender, location, risk tolerance, and travel preferences
- **Intelligent Scoring**: Trials are scored 0-100 based on how well they match your profile
- **Real-time Updates**: Results change immediately as you modify your profile
- **Match Explanations**: See exactly why each trial matches your profile

#### **⚠️ Risk Assessment & Safety Analysis**
- **Phase-based Risk Levels**: Clear risk assessment (Low, Medium, Medium-High, High)
- **Safety Considerations**: Plain language explanations of risks and benefits
- **Color-coded Risk Display**: Visual indicators for easy understanding
- **Study Type Analysis**: Different risk profiles for interventional vs. observational studies

#### **🔄 Reflexion Workflow & Quality Improvement**
- **Smart Search Refinement**: The system automatically improves search results through feedback loops
- **Quality Evaluation**: Continuous assessment of result relevance and accuracy
- **Profile Refinement**: Dynamic adjustment of search strategies based on user feedback
- **Story Journey Visualization**: See how the system improved your results step-by-step
- **Workflow Status Tracking**: Real-time monitoring of the search and refinement process

---

## 🔄 **LangGraph Workflow Architecture**

The app uses **LangGraph** to create an intelligent, multi-step workflow that continuously improves search results:

### **Core Workflow Nodes**
1. **🔍 Disease Clarifier**: Understands and clarifies user input
2. **📊 API Searcher**: Queries ClinicalTrials.gov with refined search terms
3. **📋 Results Processor**: Analyzes and structures trial data
4. **🎯 Patient Profile Matcher**: Scores trials based on user preferences
5. **⚠️ Risk Assessor**: Evaluates safety and risk levels
6. **📝 Eligibility Summarizer**: Simplifies complex medical criteria

### **🔄 Reflexion Enhancement Nodes**
7. **🔍 Quality Evaluator**: Assesses result relevance and accuracy
8. **🔄 Search Refiner**: Improves search strategies based on feedback
9. **👤 Profile Refiner**: Adjusts matching algorithms dynamically

### **How It Works**
- **Initial Search**: Basic search based on user input
- **Quality Check**: System evaluates if results meet user needs
- **Refinement Loop**: If quality is insufficient, the system refines the search
- **Continuous Improvement**: Multiple feedback loops ensure optimal results
- **User Experience**: See the entire journey through the "Story Journey" feature

### **📊 Workflow Visualization**
The LangGraph workflow is visualized in the generated image:
- **`langgraph_workflow.png`**: Overview of the complete workflow with nodes and connections

**🎨 Enhanced Visualization Features:**
- **Centered Layout**: Main workflow nodes are positioned in a clear horizontal flow
- **Intuitive Reflexion Loops**: Feedback loops are shown with curved dashed lines and clear direction
- **Clean Design**: Minimal visual clutter with focus on the workflow structure
- **Color-Coded Nodes**: Different colors for core, personalization, and reflexion nodes
- **Clear Flow Direction**: Forward flow and feedback loops are visually distinct
- **Optimal Legend Placement**: Legend positioned at bottom left to avoid overlapping with nodes

For technical details, see `LANGGRAPH_WORKFLOW.md` in the project directory.

---

## 📖 **Detailed User Instructions**

### **🎯 How to Use the App**

#### **Step 1: Enter Your Medical Condition**
- **Be Specific**: Instead of "cancer", try "breast cancer", "lung cancer", or "melanoma"
- **Use Medical Terms**: "diabetes mellitus" or "type 2 diabetes" work well
- **Try Different Variations**: If "depression" doesn't work, try "major depressive disorder"

**Good Examples:**
- ✅ "breast cancer"
- ✅ "multiple sclerosis"
- ✅ "type 2 diabetes"
- ✅ "rheumatoid arthritis"
- ✅ "Alzheimer's disease"

**Less Effective:**
- ❌ "cancer" (too broad)
- ❌ "sick" (not specific)
- ❌ "pain" (too general)

#### **Step 2: Understanding the Results**

**Interactive Map Features:**
- **Red Markers**: Phase 1 trials (early safety testing)
- **Blue Markers**: Phase 2 trials (effectiveness testing)
- **Green Markers**: Phase 3 trials (comparison with standard treatment)
- **Purple Markers**: Phase 4 trials (post-approval studies)
- **Gray Markers**: Other phases or observational studies

**Click on any marker to see:**
- Trial facility name and location
- Brief trial description
- Trial phase
- Direct link to ClinicalTrials.gov

#### **Step 3: Analyzing Trial Phases**

**What Trial Phases Mean:**
- **Phase 1**: Tests safety and dosage (small groups, 20-80 people)
- **Phase 2**: Tests effectiveness and side effects (larger groups, 100-300 people)
- **Phase 3**: Compares with standard treatment (large groups, 1,000-3,000 people)
- **Phase 4**: Studies after FDA approval (monitoring long-term effects)

#### **Step 4: Understanding Demographics**

**Age Groups:**
- **CHILD**: Under 18 years
- **ADULT**: 18-65 years
- **OLDER_ADULT**: 65+ years

**Gender Requirements:**
- **All Genders**: Open to everyone
- **Male Only**: Specific to men
- **Female Only**: Specific to women (often pregnancy-related studies)

**Study Types:**
- **Interventional**: Tests new treatments or procedures
- **Observational**: Studies existing conditions without intervention
- **Healthy Volunteers**: Studies that need healthy participants

#### **Step 5: Reading Trial Details**

**Expand any trial card to see:**
- **Condition**: What the trial is studying
- **Status**: Current recruitment status
- **Phase**: Trial phase and what it means
- **Locations**: Where the trial is happening
- **Direct Link**: Click to see full details on ClinicalTrials.gov

### **🆕 Step 6: Using Personalized Features**

#### **Setting Your Profile**
1. **Look at the left sidebar** for "👤 User Profile & Preferences"
2. **Expand the profile section** and fill in your details:
   - **Age**: Your current age
   - **Gender**: Your gender preference
   - **Location**: Your preferred trial location
   - **Risk Tolerance**: How comfortable you are with experimental treatments
   - **Travel Preference**: How far you're willing to travel
3. **Profile updates automatically** - no save button needed!

#### **Understanding Risk Levels**
- **🟢 Low Risk**: Phase 3-4 trials with established safety records
- **🟡 Medium Risk**: Phase 2-3 trials with some safety data
- **🟠 Medium-High Risk**: Phase 2 trials testing effectiveness
- **🔴 High Risk**: Phase 1 trials with cutting-edge experimental treatments

#### **Reading Personalized Results**
- **🎯 Personalized Recommendations**: Top 5 trials that match your profile
- **Match Scores**: 0-100 scale showing how well each trial fits you
- **Match Reasons**: Clear explanations of why each trial matches
- **Personalized Statistics**: Enrollment numbers for trials you're eligible for

#### **Step 7: Understanding the Reflexion Workflow**

The app now includes an intelligent workflow that continuously improves your results:

**Story Journey Feature:**
- **Chapter 1**: Initial search results
- **Chapter 2**: Smart analysis of your profile
- **Chapter 3**: Quality evaluation and refinement
- **Chapter 4**: Final personalized recommendations

**What This Means:**
- The system doesn't just search once - it learns and improves
- Results get better through multiple refinement cycles
- You can see exactly how the system improved your search
- Quality metrics show the improvement over time

**Workflow Status:**
- Real-time monitoring of the search process
- Visual indicators of workflow progress
- Clear explanations of what's happening behind the scenes

### **💡 Tips for Better Results**

1. **Start Specific**: Use precise medical terms
2. **Try Variations**: If one term doesn't work, try synonyms
3. **Check Multiple Conditions**: Related conditions might have different trials
4. **Look at Locations**: Consider travel distance to trial sites
5. **Read Eligibility**: Make sure you meet the basic requirements
6. **Contact Sites**: Use the ClinicalTrials.gov links to contact trial coordinators

### **⚠️ Important Notes**

- **This app is for informational purposes only**
- **Always consult with your healthcare provider** before considering clinical trials
- **Trial information may change** - always verify details with the trial site
- **Not all trials are suitable for everyone** - eligibility criteria are strict for safety
- **Participation is voluntary** - you can withdraw at any time

---

## ❓ **Frequently Asked Questions**

### **What is this app?**
This is a **clinical trial search and analysis tool** that helps patients and caregivers find relevant clinical trials and understand if they might qualify.

### **Is this medical advice?**
**No.** This app provides information about clinical trials but does not give medical advice. Always consult with your healthcare provider.

### **How current is the trial information?**
The app pulls data directly from ClinicalTrials.gov, which is updated regularly. However, trial status can change quickly, so always verify with the trial site.

### **What if I don't see any trials for my condition?**
- Try different variations of your condition name
- Check related conditions
- Some rare conditions may have limited trial options
- Consider expanding your search geographically

### **How do I contact a trial site?**
Click on any trial marker on the map or expand a trial card to get the direct link to ClinicalTrials.gov, where you can find contact information.

### **Are these trials free?**
Clinical trials often provide the treatment at no cost, but you should discuss costs with the trial coordinator. Some trials may cover travel expenses.

### **What if I'm not eligible for any trials?**
This is common and normal. Clinical trials have strict criteria for safety reasons. Discuss other treatment options with your healthcare provider.

---

## 🚫 **What This App Is NOT**

- **Medical advice** - Always consult healthcare professionals
- **A replacement for doctor consultation** - Use this as a starting point
- **A guarantee of trial participation** - Eligibility is determined by trial sites
- **Real-time trial status** - Information may have slight delays
- **A comprehensive medical database** - Focuses on clinical trials only

---

## 🏗️ **Technical Architecture**

### **LangGraph Agent Structure**

The application uses LangGraph to create a sophisticated, stateful workflow with **9 intelligent nodes**:

**Core Workflow Nodes:**
1. **`clarify_disease`**: Checks if user input needs clarification
2. **`search_clinical_trials`**: Queries ClinicalTrials.gov API
3. **`summarize_eligibility`**: Uses LLM to simplify eligibility criteria
4. **`prepare_visualizations`**: Processes data for charts and maps
5. **`patient_profile_matcher`** 🆕: Analyzes user profile and matches with most relevant trials
6. **`risk_analyzer`** 🆕: Evaluates risks and benefits of each trial

**🔄 Reflexion Enhancement Nodes:**
7. **`quality_evaluator`** 🆕: Assesses result relevance and accuracy
8. **`search_refiner`** 🆕: Improves search strategies based on feedback
9. **`profile_refiner`** 🆕: Adjusts matching algorithms dynamically

### **State Management**

The agent maintains state through an enhanced `TypedDict` structure:
- `messages`: Conversation history
- `disease_name`: Current search term
- `api_results`: Raw API response data
- `simplified_criteria`: LLM-processed eligibility criteria
- `visualization_data`: Processed data for charts
- **Personalization fields**:
  - `user_profile`: User demographics and preferences
  - `risk_assessments`: Trial risk analysis results
- **🔄 Reflexion workflow fields**:
  - `quality_metrics`: Assessment of result quality
  - `search_strategy`: Current search approach
  - `profile_refinement`: Dynamic profile adjustments
  - `personalized_recommendations`: Profile-matched trial suggestions

### **Workflow Flow**
```
START → clarify_disease → search_clinical_trials → summarize_eligibility → 
prepare_visualizations → patient_profile_matcher → risk_analyzer → END
```

### **🔧 Technical Improvements**

#### **Enhanced Data Processing**
- **Robust Age Parsing**: Handles various API age formats ("18 Years", "65+", "Unknown")
- **Type Safety**: Proper integer conversion and error handling
- **Efficient Algorithms**: Single-pass processing for optimal performance

#### **Smart State Management**
- **Auto-save Profiles**: Real-time profile updates without manual intervention
- **Conditional Rendering**: UI adapts based on user profile availability
- **Persistent State**: Profile preferences maintained across sessions

#### **Advanced Error Handling**
- **Graceful Degradation**: App continues working even if some features fail
- **User-friendly Messages**: Clear explanations when things go wrong
- **Fallback Mechanisms**: Smart defaults when data is unavailable

---

## 🔧 **Configuration & Customization**

### **AI Model Setup**

The app automatically detects and uses the best available AI model:

**Default (No Setup Required)**: Smart fallback responses for all AI features  
**With Ollama**: Enhanced AI responses using local models  
**With API Keys**: OpenAI/Anthropic integration (requires configuration)

**Quick Ollama Setup**:
```bash
# Install and run Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.1:8b
ollama serve

# The app will automatically detect and use it!
```

### **API Configuration**

The app uses the ClinicalTrials.gov API v2. No API key is required, but you can customize:
- `pageSize`: Number of trials per request (default: 50)
- `fields`: Specific data fields to retrieve
- `filter.overallStatus`: Trial status filter (default: "RECRUITING")

### **Styling Customization**

The app uses custom CSS for styling. Modify the CSS in the `st.markdown` section to change:
- Colors and fonts
- Layout spacing
- Card styling
- Header appearance

### **Visualization Customization**

Customize charts by modifying:
- **Map**: Change pin colors, sizes, or add custom popups
- **Pie Chart**: Adjust colors, labels, or chart type
- **Word Cloud**: Modify colors, word limits, or layout

### **Agent Logic Extension**

Extend the LangGraph workflow by:
- Adding new nodes for additional processing
- Implementing conditional edges for complex workflows
- Enhancing the clarification logic for better disease detection

---

## 📊 **Data Sources**

- **ClinicalTrials.gov API v2**: Primary source for trial data
- **Fields Retrieved**:
  - Trial identifiers (NCT ID)
  - Basic information (title, condition, status)
  - Location data (city, country, coordinates)
  - Sponsor information
  - Eligibility criteria
  - Intervention details

---

## 🐛 **Troubleshooting**

### **Common Issues**

1. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

2. **API Timeouts**
   - The ClinicalTrials.gov API may be slow. Increase timeout in the `requests.get()` call
   - Consider implementing retry logic for failed requests

3. **Memory Issues**
   - Large datasets may cause memory problems
   - Reduce `pageSize` in API requests
   - Implement pagination for large result sets

4. **LLM Integration**
   - **For Ollama**: Ensure Ollama is running (`ollama serve`) and models are downloaded
   - **For OpenAI/Anthropic**: Ensure API keys are properly configured
   - Check rate limits for your chosen LLM provider

5. **Ollama Issues** (if using enhanced AI features)
   - **Model not found**: Run `ollama pull llama3.1:8b`
   - **Connection failed**: Run `ollama serve` in terminal
   - **Slow responses**: Try `ollama pull phi3:mini` for faster inference

### **Performance Optimization**

- Use `@st.cache_resource` for expensive operations
- Implement lazy loading for large datasets
- Consider using async requests for API calls

---

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 **Acknowledgments**

- ClinicalTrials.gov for providing the API
- Streamlit for the web framework
- LangGraph for the agent orchestration
- The open-source community for the visualization libraries

---

## 📞 **Support**

For questions or issues:
1. Check the troubleshooting section
2. Review the code comments
3. Open an issue on the repository

### **🤖 Ollama Support**

For enhanced AI features:
1. **Quick Test**: Run `python test_ollama.py` to verify setup
2. **Documentation**: Visit [ollama.ai/docs](https://ollama.ai/docs)
3. **Community**: Check Ollama GitHub discussions

---

**Note**: This application is for educational and informational purposes. Always consult with healthcare professionals before making medical decisions based on clinical trial information.
