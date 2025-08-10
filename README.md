# 🏥 Patient & Caregiver Trial Navigator

A comprehensive Streamlit web application that helps patients and caregivers find and understand clinical trials for specific medical conditions. The app uses LangGraph to create a stateful, multi-step agent that interacts with the ClinicalTrials.gov API to provide personalized trial information.

## 🎯 What This App Does

This application is designed to bridge the gap between complex clinical trial information and patients who need it. It transforms technical medical jargon into understandable insights, helping you:

- **Find relevant clinical trials** for your specific condition
- **Understand if you might qualify** based on age, gender, and other factors
- **See where trials are happening** with an interactive world map
- **Learn about trial phases** and what they mean for you
- **Get simplified explanations** of complex eligibility criteria

## 🚀 Quick Start Guide

### For First-Time Users

1. **Open the App**: Navigate to the provided URL (usually `http://localhost:8501`)
2. **Enter Your Condition**: Type a specific medical condition in the chat box
   - Examples: "breast cancer", "diabetes", "multiple sclerosis", "depression"
   - Be specific: "lung cancer" works better than just "cancer"
3. **Wait for Results**: The app will search ClinicalTrials.gov and process the data
4. **Explore the Results**: Use the interactive features to understand your options

### What You'll See

After entering a condition, you'll get:

1. **📊 Trial Overview**: Number of recruiting trials found
2. **🌍 Interactive Map**: Trial locations with color-coded markers
3. **📈 Phase Distribution**: What stages of research are available
4. **👥 Demographic Analysis**: Age groups, gender requirements, study types
5. **📋 Trial Details**: Expandable cards with specific trial information
6. **✅ Simplified Eligibility**: Plain-language explanation of requirements

## ✨ Features

- **Conversational Interface**: Chat-based interaction with an AI agent that can clarify ambiguous disease inputs
- **Real-time Trial Search**: Direct integration with ClinicalTrials.gov API v2
- **Interactive Visualizations**:
  - 🌍 **Interactive World Map**: Shows trial locations with color-coded markers by phase
  - 📊 **Trial Phase Distribution**: Swimlane chart showing distribution of trial phases
  - 📊 **Demographic Analysis**: Age groups, gender requirements, and study types
  - 📈 **Enrollment Statistics**: Total, average, largest, and smallest study sizes
- **Simplified Eligibility Criteria**: AI-powered translation of technical criteria into plain language
- **Detailed Trial Information**: Expandable cards with comprehensive trial details

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

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

## 📖 Detailed User Instructions

### 🎯 How to Use the App

#### Step 1: Enter Your Medical Condition
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

#### Step 2: Understanding the Results

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

#### Step 3: Analyzing Trial Phases

**What Trial Phases Mean:**
- **Phase 1**: Tests safety and dosage (small groups, 20-80 people)
- **Phase 2**: Tests effectiveness and side effects (larger groups, 100-300 people)
- **Phase 3**: Compares with standard treatment (large groups, 1,000-3,000 people)
- **Phase 4**: Studies after FDA approval (monitoring long-term effects)

#### Step 4: Understanding Demographics

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

#### Step 5: Reading Trial Details

**Expand any trial card to see:**
- **Condition**: What the trial is studying
- **Status**: Current recruitment status
- **Phase**: Trial phase and what it means
- **Locations**: Where the trial is happening
- **Direct Link**: Click to see full details on ClinicalTrials.gov

### 💡 Tips for Better Results

1. **Start Specific**: Use precise medical terms
2. **Try Variations**: If one term doesn't work, try synonyms
3. **Check Multiple Conditions**: Related conditions might have different trials
4. **Look at Locations**: Consider travel distance to trial sites
5. **Read Eligibility**: Make sure you meet the basic requirements
6. **Contact Sites**: Use the ClinicalTrials.gov links to contact trial coordinators

### ⚠️ Important Notes

- **This app is for informational purposes only**
- **Always consult with your healthcare provider** before considering clinical trials
- **Trial information may change** - always verify details with the trial site
- **Not all trials are suitable for everyone** - eligibility criteria are strict for safety
- **Participation is voluntary** - you can withdraw at any time

## ❓ Frequently Asked Questions

### What is this app?
This is a **clinical trial search and analysis tool** that helps patients and caregivers find relevant clinical trials and understand if they might qualify.

### Is this medical advice?
**No.** This app provides information about clinical trials but does not give medical advice. Always consult with your healthcare provider.

### How current is the trial information?
The app pulls data directly from ClinicalTrials.gov, which is updated regularly. However, trial status can change quickly, so always verify with the trial site.

### What if I don't see any trials for my condition?
- Try different variations of your condition name
- Check related conditions
- Some rare conditions may have limited trial options
- Consider expanding your search geographically

### How do I contact a trial site?
Click on any trial marker on the map or expand a trial card to get the direct link to ClinicalTrials.gov, where you can find contact information.

### Are these trials free?
Clinical trials often provide the treatment at no cost, but you should discuss costs with the trial coordinator. Some trials may cover travel expenses.

### What if I'm not eligible for any trials?
This is common and normal. Clinical trials have strict criteria for safety reasons. Discuss other treatment options with your healthcare provider.

## 🚫 What This App Is NOT

- **Medical advice** - Always consult healthcare professionals
- **A replacement for doctor consultation** - Use this as a starting point
- **A guarantee of trial participation** - Eligibility is determined by trial sites
- **Real-time trial status** - Information may have slight delays
- **A comprehensive medical database** - Focuses on clinical trials only

## 🏗️ Architecture

### LangGraph Agent Structure

The application uses LangGraph to create a stateful workflow with the following nodes:

1. **`clarify_disease`**: Checks if user input needs clarification
2. **`search_clinical_trials`**: Queries ClinicalTrials.gov API
3. **`summarize_eligibility`**: Uses LLM to simplify eligibility criteria
4. **`prepare_visualizations`**: Processes data for charts and maps

### State Management

The agent maintains state through a `TypedDict` structure:
- `messages`: Conversation history
- `disease_name`: Current search term
- `api_results`: Raw API response data
- `simplified_criteria`: LLM-processed eligibility criteria
- `visualization_data`: Processed data for charts

## 🔧 Configuration

### LLM Integration

The app currently uses a mock LLM function. To integrate with a real LLM:

1. **For OpenAI**:
   ```python
   from langchain_openai import ChatOpenAI
   
   llm = ChatOpenAI(api_key="your-openai-api-key")
   ```

2. **For Anthropic**:
   ```python
   from langchain_anthropic import ChatAnthropic
   
   llm = ChatAnthropic(api_key="your-anthropic-api-key")
   ```

3. **Replace the `mock_llm` function** in `app.py` with your chosen LLM.

### API Configuration

The app uses the ClinicalTrials.gov API v2. No API key is required, but you can customize:
- `pageSize`: Number of trials per request (default: 50)
- `fields`: Specific data fields to retrieve
- `filter.overallStatus`: Trial status filter (default: "RECRUITING")

## 📊 Data Sources

- **ClinicalTrials.gov API v2**: Primary source for trial data
- **Fields Retrieved**:
  - Trial identifiers (NCT ID)
  - Basic information (title, condition, status)
  - Location data (city, country, coordinates)
  - Sponsor information
  - Eligibility criteria
  - Intervention details

## 🎨 Customization

### Styling

The app uses custom CSS for styling. Modify the CSS in the `st.markdown` section to change:
- Colors and fonts
- Layout spacing
- Card styling
- Header appearance

### Visualizations

Customize charts by modifying:
- **Map**: Change pin colors, sizes, or add custom popups
- **Pie Chart**: Adjust colors, labels, or chart type
- **Word Cloud**: Modify colors, word limits, or layout

### Agent Logic

Extend the LangGraph workflow by:
- Adding new nodes for additional processing
- Implementing conditional edges for complex workflows
- Enhancing the clarification logic for better disease detection

## 🐛 Troubleshooting

### Common Issues

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
   - Ensure API keys are properly configured
   - Check rate limits for your chosen LLM provider

### Performance Optimization

- Use `@st.cache_resource` for expensive operations
- Implement lazy loading for large datasets
- Consider using async requests for API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- ClinicalTrials.gov for providing the API
- Streamlit for the web framework
- LangGraph for the agent orchestration
- The open-source community for the visualization libraries

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review the code comments
3. Open an issue on the repository

---

**Note**: This application is for educational and informational purposes. Always consult with healthcare professionals before making medical decisions based on clinical trial information.
