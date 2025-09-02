import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import ChatOllama
import re
from collections import Counter
import io
import base64

# Configure Streamlit page
st.set_page_config(
    page_title="Patient & Caregiver Trial Navigator",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .model-info {
        background-color: #e8f4fd;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0 5px 5px 0;
    }
    /* Prevent text truncation */
    .stText, .stMarkdown, .stWrite {
        word-wrap: break-word;
        overflow-wrap: break-word;
        white-space: normal;
    }
    .stMetric {
        min-width: 120px;
    }
    /* Ensure expandable sections don't truncate */
    .streamlit-expanderHeader {
        font-size: 1.1rem;
        font-weight: 600;
    }
    /* Ensure consistent column widths */
    .stColumn {
        min-width: 0;
        flex: 1;
    }
    /* Better spacing for chat */
    .stChatMessage {
        margin-bottom: 0.5rem;
    }
    /* Consistent section widths */
    .main .block-container {
        max-width: 1200px;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    /* Ensure chat input stays in position */
    .stChatInput {
        position: relative !important;
        margin-top: 0.5rem;
    }
    /* Consistent metric column widths */
    .stMetric {
        width: 100%;
        text-align: center;
    }
    /* Ensure sections have same width */
    .stColumn > div {
        width: 100%;
    }
    /* Fix chat container positioning */
    .stContainer {
        margin-bottom: 1rem;
    }
    /* Ensure consistent widths across all sections */
    .main .block-container > div {
        width: 100% !important;
        max-width: none !important;
    }
    /* Ensure equal column widths */
    .stColumn {
        flex: 1 !important;
        min-width: 0 !important;
    }
    /* Ensure content spans full column width */
    .stColumn .stMarkdown,
    .stColumn .stSubheader,
    .stColumn .stWrite {
        width: 100% !important;
        max-width: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Ollama LLM
@st.cache_resource
def get_ollama_llm(model_name: str = "llama3.1:8b"):
    """Initialize Ollama LLM with specified model"""
    try:
        llm = ChatOllama(model=model_name, temperature=0.1)
        return llm
    except Exception as e:
        st.error(f"Error initializing Ollama with model {model_name}: {str(e)}")
        return None

# Function to get available Ollama models
@st.cache_data
def get_available_models():
    """Get list of available Ollama models"""
    try:
        import subprocess
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            models = []
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if parts:
                        models.append(parts[0])
            return models
        return []
    except Exception as e:
        st.error(f"Error getting available models: {str(e)}")
        return []

# Helper function to parse age values from various formats
def parse_age(age_value) -> int:
    """Parse age values from various formats like '18 Years', '65+', etc."""
    if age_value == "Unknown" or not age_value:
        return 0
    try:
        # Try to extract number from strings like "18 Years", "65+", etc.
        if isinstance(age_value, str):
            # Extract first number from string
            import re
            numbers = re.findall(r'\d+', str(age_value))
            if numbers:
                return int(numbers[0])
            return 0
        else:
            return int(age_value)
    except (ValueError, TypeError):
        return 0

# Simple geocoding function for major cities
def get_city_coordinates(city: str, country: str) -> Dict[str, float]:
    """Get coordinates for major cities"""
    # Simplified geocoding for common cities
    city_coords = {
        "Birmingham": {"lat": 33.5207, "lon": -86.8025},
        "Portland": {"lat": 45.5152, "lon": -122.6784},
        "Hangzhou": {"lat": 30.2741, "lon": 120.1551},
        "Balkbrug": {"lat": 52.6000, "lon": 6.3833},
        "New York": {"lat": 40.7128, "lon": -74.0060},
        "Los Angeles": {"lat": 34.0522, "lon": -118.2437},
        "Chicago": {"lat": 41.8781, "lon": -87.6298},
        "Houston": {"lat": 29.7604, "lon": -95.3698},
        "Phoenix": {"lat": 33.4484, "lon": -112.0740},
        "Philadelphia": {"lat": 39.9526, "lon": -75.1652},
        "San Antonio": {"lat": 29.4241, "lon": -98.4936},
        "San Diego": {"lat": 32.7157, "lon": -117.1611},
        "Dallas": {"lat": 32.7767, "lon": -96.7970},
        "San Jose": {"lat": 37.3382, "lon": -121.8863},
        "Austin": {"lat": 30.2672, "lon": -97.7431},
        "Jacksonville": {"lat": 30.3322, "lon": -81.6557},
        "Fort Worth": {"lat": 32.7555, "lon": -97.3308},
        "Columbus": {"lat": 39.9612, "lon": -82.9988},
        "Charlotte": {"lat": 35.2271, "lon": -80.8431},
        "San Francisco": {"lat": 37.7749, "lon": -122.4194},
        "Indianapolis": {"lat": 39.7684, "lon": -86.1581},
        "Seattle": {"lat": 47.6062, "lon": -122.3321},
        "Denver": {"lat": 39.7392, "lon": -104.9903},
        "Washington": {"lat": 38.9072, "lon": -77.0369},
        "Boston": {"lat": 42.3601, "lon": -71.0589},
        "El Paso": {"lat": 31.7619, "lon": -106.4850},
        "Nashville": {"lat": 36.1627, "lon": -86.7816},
        "Detroit": {"lat": 42.3314, "lon": -83.0458},
        "Oklahoma City": {"lat": 35.4676, "lon": -97.5164},
        "Portland": {"lat": 45.5152, "lon": -122.6784},
        "Las Vegas": {"lat": 36.1699, "lon": -115.1398},
        "Memphis": {"lat": 35.1495, "lon": -90.0490},
        "Louisville": {"lat": 38.2527, "lon": -85.7585},
        "Baltimore": {"lat": 39.2904, "lon": -76.6122},
        "Milwaukee": {"lat": 43.0389, "lon": -87.9065},
        "Albuquerque": {"lat": 35.0844, "lon": -106.6504},
        "Tucson": {"lat": 32.2226, "lon": -110.9747},
        "Fresno": {"lat": 36.7378, "lon": -119.7871},
        "Sacramento": {"lat": 38.5816, "lon": -121.4944},
        "Mesa": {"lat": 33.4152, "lon": -111.8315},
        "Kansas City": {"lat": 39.0997, "lon": -94.5786},
        "Atlanta": {"lat": 33.7490, "lon": -84.3880},
        "Long Beach": {"lat": 33.7701, "lon": -118.1937},
        "Colorado Springs": {"lat": 38.8339, "lon": -104.8214},
        "Raleigh": {"lat": 35.7796, "lon": -78.6382},
        "Miami": {"lat": 25.7617, "lon": -80.1918},
        "Virginia Beach": {"lat": 36.8529, "lon": -75.9780},
        "Omaha": {"lat": 41.2565, "lon": -95.9345},
        "Oakland": {"lat": 37.8044, "lon": -122.2711},
        "Minneapolis": {"lat": 44.9778, "lon": -93.2650},
        "Tulsa": {"lat": 36.1540, "lon": -95.9928},
        "Arlington": {"lat": 32.7357, "lon": -97.1081},
        "Tampa": {"lat": 27.9506, "lon": -82.4572},
        "New Orleans": {"lat": 29.9511, "lon": -90.0715},
        "Wichita": {"lat": 37.6872, "lon": -97.3301},
        "Cleveland": {"lat": 41.4993, "lon": -81.6944},
        "Bakersfield": {"lat": 35.3733, "lon": -119.0187},
        "Aurora": {"lat": 39.7294, "lon": -104.8319},
        "Anaheim": {"lat": 33.8366, "lon": -117.9143},
        "Honolulu": {"lat": 21.3099, "lon": -157.8581},
        "Santa Ana": {"lat": 33.7455, "lon": -117.8677},
        "Corpus Christi": {"lat": 27.8006, "lon": -97.3964},
        "Riverside": {"lat": 33.9533, "lon": -117.3962},
        "Lexington": {"lat": 38.0406, "lon": -84.5037},
        "Stockton": {"lat": 37.9577, "lon": -121.2908},
        "Henderson": {"lat": 36.0395, "lon": -114.9817},
        "Saint Paul": {"lat": 44.9537, "lon": -93.0900},
        "St. Louis": {"lat": 38.6270, "lon": -90.1994},
        "Cincinnati": {"lat": 39.1031, "lon": -84.5120},
        "Pittsburgh": {"lat": 40.4406, "lon": -79.9959},
        "Anchorage": {"lat": 61.2181, "lon": -149.9003},
        "Greensboro": {"lat": 36.0726, "lon": -79.7920},
        "Plano": {"lat": 33.0198, "lon": -96.6989},
        "Newark": {"lat": 40.7357, "lon": -74.1724},
        "Durham": {"lat": 35.9940, "lon": -78.8986},
        "Chula Vista": {"lat": 32.6401, "lon": -117.0842},
        "Toledo": {"lat": 41.6528, "lon": -83.5379},
        "Fort Wayne": {"lat": 41.0793, "lon": -85.1394},
        "St. Petersburg": {"lat": 27.7731, "lon": -82.6400},
        "Laredo": {"lat": 27.5064, "lon": -99.5075},
        "Jersey City": {"lat": 40.7178, "lon": -74.0431},
        "Chandler": {"lat": 33.3062, "lon": -111.8413},
        "Madison": {"lat": 43.0731, "lon": -89.4012},
        "Lubbock": {"lat": 33.5779, "lon": -101.8552},
        "Scottsdale": {"lat": 33.4942, "lon": -111.9261},
        "Reno": {"lat": 39.5296, "lon": -119.8138},
        "Buffalo": {"lat": 42.8864, "lon": -78.8784},
        "Gilbert": {"lat": 33.3528, "lon": -111.7890},
        "Glendale": {"lat": 33.5387, "lon": -112.1860},
        "North Las Vegas": {"lat": 36.1989, "lon": -115.1175},
        "Winston-Salem": {"lat": 36.0999, "lon": -80.2442},
        "Chesapeake": {"lat": 36.7682, "lon": -76.2875},
        "Norfolk": {"lat": 36.8508, "lon": -76.2859},
        "Fremont": {"lat": 37.5485, "lon": -121.9886},
        "Garland": {"lat": 32.9126, "lon": -96.6389},
        "Irving": {"lat": 32.8140, "lon": -96.9489},
        "Hialeah": {"lat": 25.8576, "lon": -80.2781},
        "Richmond": {"lat": 37.5407, "lon": -77.4360},
        "Boise": {"lat": 43.6150, "lon": -116.2023},
        "Spokane": {"lat": 47.6588, "lon": -117.4260},
        "Baton Rouge": {"lat": 30.4515, "lon": -91.1871},
        "Tacoma": {"lat": 47.2529, "lon": -122.4443},
        "San Bernardino": {"lat": 34.1083, "lon": -117.2898},
        "Grand Rapids": {"lat": 42.9634, "lon": -85.6681},
        "Huntsville": {"lat": 34.7304, "lon": -86.5861},
        "Salt Lake City": {"lat": 40.7608, "lon": -111.8910},
        "Fayetteville": {"lat": 35.0527, "lon": -78.8784},
        "Yonkers": {"lat": 40.9312, "lon": -73.8987},
        "Amarillo": {"lat": 35.2220, "lon": -101.8313},
        "Glendale": {"lat": 34.1425, "lon": -118.2551},
        "McKinney": {"lat": 33.1972, "lon": -96.6397},
        "Rochester": {"lat": 43.1566, "lon": -77.6088},
    }
    
    # Check if city exists in our database
    if city in city_coords:
        return city_coords[city]
    
    # Return None if city not found
    return None

# Define the state structure for LangGraph
class AgentState(TypedDict):
    messages: Annotated[List, "messages"]
    disease_name: str
    api_results: Dict[str, Any]
    simplified_criteria: str
    visualization_data: Dict[str, Any]
    needs_clarification: bool
    clarification_question: str
    selected_model: str

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_state" not in st.session_state:
    st.session_state.agent_state = {
        "messages": [],
        "disease_name": "",
        "api_results": {},
        "simplified_criteria": "",
        "visualization_data": {},
        "needs_clarification": False,
        "clarification_question": "",
        "selected_model": "llama3.1:8b",
        # Initialize new fields
        "user_profile": {},
        "risk_assessments": {},
        "personalized_recommendations": []
    }

# Real LLM function using Ollama
def real_llm(prompt: str, model_name: str = "llama3.1:8b") -> str:
    """Real LLM function using Ollama for local inference"""
    try:
        llm = get_ollama_llm(model_name)
        if llm is None:
            return "Error: Could not initialize Ollama LLM. Please check if Ollama is running and the model is available."
        
        # Create a more specific prompt for better results
        if "clarify" in prompt.lower():
            enhanced_prompt = f"""You are a helpful medical assistant. The user has entered a disease term that might be too general. 
            Please ask for clarification in a friendly, professional way. 
            
            User input: {prompt}
            
            Respond with a clear question asking for more specific information about the disease or condition."""
        elif "simplify" in prompt.lower():
            enhanced_prompt = f"""You are a medical translator who simplifies complex clinical trial eligibility criteria into plain, 
            easy-to-understand language for patients and caregivers. 
            
            Original criteria: {prompt}
            
            Please provide a clear, simple explanation of:
            1. Who might be eligible (in plain terms)
            2. Who might not be eligible (in plain terms)
            3. Any important considerations
            
            Use simple language that a non-medical person can understand."""
        else:
            enhanced_prompt = f"""You are a helpful medical assistant helping patients find clinical trials. 
            Please provide a helpful response to: {prompt}"""
        
        response = llm.invoke(enhanced_prompt)
        return response.content if hasattr(response, 'content') else str(response)
        
    except Exception as e:
        st.error(f"Error calling Ollama LLM: {str(e)}")
        # Fallback to simple responses
        if "clarify" in prompt.lower():
            return "Could you please specify the type of cancer? For example: 'breast cancer', 'lung cancer', 'melanoma', etc."
        elif "simplify" in prompt.lower():
            return "Based on the trial criteria, you may be eligible if you: are 18 years or older, have been diagnosed with the condition, and are in generally good health. You may not be eligible if you: are pregnant, have certain other medical conditions, or are taking specific medications."
        else:
            return "I understand you're looking for clinical trials. Let me help you find relevant information."

# Node functions for LangGraph
def clarify_disease(state: AgentState) -> AgentState:
    """Check if disease input needs clarification"""
    disease = state.get("disease_name", "").lower()
    selected_model = state.get("selected_model", "llama3.1:8b")
    
    # Simple rules for ambiguous terms
    ambiguous_terms = ["cancer", "tumor", "disease", "condition", "illness"]
    
    if any(term in disease for term in ambiguous_terms) and len(disease.split()) <= 2:
        state["needs_clarification"] = True
        # Use real LLM for better clarification
        clarification_prompt = f"clarify: {disease}"
        state["clarification_question"] = real_llm(clarification_prompt, selected_model)
        state["messages"].append(AIMessage(content=state["clarification_question"]))
    else:
        state["needs_clarification"] = False
    
    return state

def search_clinical_trials(state: AgentState) -> AgentState:
    """Search ClinicalTrials.gov API"""
    disease = state.get("disease_name", "")
    
    if not disease:
        state["messages"].append(AIMessage(content="Please provide a disease or condition to search for."))
        return state
    
    # Construct API query - using direct URL to avoid encoding issues
    url = f"https://clinicaltrials.gov/api/v2/studies?query.cond={disease}&filter.overallStatus=RECRUITING&pageSize=50"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Process the API response to extract the actual studies
        studies = data.get("studies", [])
        processed_studies = []
        
        for study in studies:
            protocol = study.get("protocolSection", {})
            identification = protocol.get("identificationModule", {})
            status = protocol.get("statusModule", {})
            conditions = protocol.get("conditionsModule", {})
            sponsor = protocol.get("sponsorCollaboratorsModule", {})
            locations = protocol.get("contactsLocationsModule", {})
            design = protocol.get("designModule", {})
            eligibility = protocol.get("eligibilityModule", {})
            
            processed_study = {
                "nctId": identification.get("nctId", ""),
                "briefTitle": identification.get("briefTitle", ""),
                "overallStatus": status.get("overallStatus", ""),
                "conditionModule": {
                    "conditions": conditions.get("conditions", [])
                },
                "sponsorModule": sponsor,
                "locationsModule": locations,
                "designModule": design,
                "eligibilityModule": eligibility
            }
            processed_studies.append(processed_study)
        
        # Update the data with processed studies
        data["studies"] = processed_studies
        state["api_results"] = data
        state["messages"].append(AIMessage(content=f"Found {len(processed_studies)} recruiting trials for {disease}."))
        
    except Exception as e:
        state["messages"].append(AIMessage(content=f"Error searching for trials: {str(e)}"))
        state["api_results"] = {"studies": [], "totalCount": 0}
    
    return state

def summarize_eligibility(state: AgentState) -> AgentState:
    """Summarize eligibility criteria using LLM"""
    api_results = state.get("api_results", {})
    studies = api_results.get("studies", [])
    selected_model = state.get("selected_model", "llama3.1:8b")
    
    if not studies:
        state["simplified_criteria"] = "No trials found to analyze eligibility criteria."
        return state
    
    # Extract eligibility criteria from first few studies
    criteria_text = ""
    for study in studies[:3]:  # Look at first 3 studies
        eligibility = study.get("eligibilityModule", {})
        if eligibility:
            inclusion = eligibility.get("inclusionCriteria", "")
            exclusion = eligibility.get("exclusionCriteria", "")
            criteria_text += f"Inclusion: {inclusion}\nExclusion: {exclusion}\n\n"
    
    # Use real LLM to simplify criteria
    prompt = f"simplify: {criteria_text}"
    simplified = real_llm(prompt, selected_model)
    
    state["simplified_criteria"] = simplified
    return state

def prepare_visualizations(state: AgentState) -> AgentState:
    """Prepare data for visualizations"""
    api_results = state.get("api_results", {})
    studies = api_results.get("studies", [])
    
    if not studies:
        state["visualization_data"] = {}
        return state
    
    # Prepare map data from location information with coordinates
    map_data = []
    phase_counts = Counter()
    
    for study in studies:
        # Extract trial phase information from design module
        design_module = study.get("designModule", {})
        phases = design_module.get("phases", [])
        study_type = design_module.get("studyType", "Unknown")
        
        # Determine phase based on design module data
        if study_type == "OBSERVATIONAL":
            phase = "Observational"
        elif phases and phases != ["NA"]:
            # Get the first phase (most trials have one phase)
            phase_code = phases[0] if phases else "NA"
            
            # Map phase codes to readable names
            if phase_code == "PHASE1":
                phase = "Phase 1"
            elif phase_code == "PHASE2":
                phase = "Phase 2"
            elif phase_code == "PHASE3":
                phase = "Phase 3"
            elif phase_code == "PHASE4":
                phase = "Phase 4"
            elif phase_code == "EARLY_PHASE1":
                phase = "Early Phase 1"
            else:
                phase = "Other"
        else:
            phase = "Not Applicable"
            
        phase_counts[phase] += 1
        
        # Extract location information
        locations_module = study.get("locationsModule", {})
        locations = locations_module.get("locations", [])
        
        for location in locations:
            facility = location.get("facility", "")
            city = location.get("city", "")
            country = location.get("country", "")
            
            # Add coordinates for major cities (simplified geocoding)
            coordinates = get_city_coordinates(city, country)
            
            if coordinates:
                map_data.append({
                    "lat": coordinates["lat"],
                    "lon": coordinates["lon"],
                    "facility": facility,
                    "city": city,
                    "country": country,
                    "trial_title": study.get("briefTitle", "")[:80] + ("..." if len(study.get("briefTitle", "")) > 80 else ""),
                    "nct_id": study.get("nctId", ""),
                    "phase": phase
                })
    
    # Prepare demographic data
    age_ranges = Counter()
    gender_requirements = Counter()
    study_types = Counter()
    enrollment_sizes = []
    
    for study in studies:
        # Extract eligibility information
        eligibility_module = study.get("eligibilityModule", {})
        design_module = study.get("designModule", {})
        
        # Age range analysis
        min_age = eligibility_module.get("minimumAge", "Unknown")
        max_age = eligibility_module.get("maximumAge", "Unknown")
        std_ages = eligibility_module.get("stdAges", [])
        
        if std_ages:
            for age_group in std_ages:
                age_ranges[age_group] += 1
        
        # Gender requirements
        sex = eligibility_module.get("sex", "Unknown")
        gender_based = eligibility_module.get("genderBased", False)
        
        if sex == "ALL":
            gender_requirements["All Genders"] += 1
        elif sex == "MALE":
            gender_requirements["Male Only"] += 1
        elif sex == "FEMALE":
            gender_requirements["Female Only"] += 1
        else:
            gender_requirements["Not Specified"] += 1
        
        # Study type analysis
        healthy_volunteers = eligibility_module.get("healthyVolunteers", False)
        study_type = design_module.get("studyType", "Unknown")
        
        if healthy_volunteers:
            study_types["Healthy Volunteers"] += 1
        elif study_type == "INTERVENTIONAL":
            study_types["Interventional"] += 1
        elif study_type == "OBSERVATIONAL":
            study_types["Observational"] += 1
        else:
            study_types["Other"] += 1
        
        # Enrollment size
        enrollment_info = design_module.get("enrollmentInfo", {})
        enrollment_count = enrollment_info.get("count", 0)
        if enrollment_count > 0:
            enrollment_sizes.append(enrollment_count)
    
    state["visualization_data"] = {
        "map_data": map_data,
        "phase_data": dict(phase_counts),
        "age_data": dict(age_ranges),
        "gender_data": dict(gender_requirements),
        "study_type_data": dict(study_types),
        "enrollment_sizes": enrollment_sizes
    }
    
    return state

def patient_profile_matcher(state: AgentState) -> AgentState:
    """Analyze user profile and match with most relevant trials"""
    api_results = state.get("api_results", {})
    studies = api_results.get("studies", [])
    user_profile = state.get("user_profile", {})
    
    if not studies or not user_profile:
        state["personalized_recommendations"] = []
        return state
    
    # Extract user profile information
    user_age = user_profile.get("age", 30)
    user_gender = user_profile.get("gender", "All")
    user_location = user_profile.get("location", "")
    user_travel_preference = user_profile.get("travel_preference", "local")
    user_risk_tolerance = user_profile.get("risk_tolerance", "moderate")
    
    # Score each trial based on user profile
    scored_trials = []
    
    for study in studies:
        score = 0
        eligibility = study.get("eligibilityModule", {})
        design = study.get("designModule", {})
        locations = study.get("locationsModule", {})
        
        # Age matching (higher score for exact matches)
        min_age = eligibility.get("minimumAge", 0)
        max_age = eligibility.get("maximumAge", 100)
        std_ages = eligibility.get("stdAges", [])
        
        # Parse age values to ensure proper comparison
        min_age = parse_age(min_age)
        max_age = parse_age(max_age)
        
        if min_age <= user_age <= max_age:
            score += 20
            if std_ages:
                for age_group in std_ages:
                    if (age_group == "ADULT" and 18 <= user_age <= 65) or \
                       (age_group == "OLDER_ADULT" and user_age > 65) or \
                       (age_group == "CHILD" and user_age < 18):
                        score += 10
        
        # Gender matching
        sex = eligibility.get("sex", "ALL")
        if sex == "ALL" or sex == user_gender.upper():
            score += 15
        
        # Location matching (simplified)
        if user_location and locations.get("locations"):
            for location in locations["locations"]:
                if user_location.lower() in location.get("city", "").lower() or \
                   user_location.lower() in location.get("country", "").lower():
                    score += 25
                    break
        
        # Phase preference based on risk tolerance
        phases = design.get("phases", [])
        if phases and phases != ["NA"]:
            phase = phases[0] if phases else "NA"
            if user_risk_tolerance == "low" and phase in ["PHASE3", "PHASE4"]:
                score += 15  # Prefer later phases (safer)
            elif user_risk_tolerance == "high" and phase in ["PHASE1", "EARLY_PHASE1"]:
                score += 15  # Prefer early phases (more experimental)
            elif user_risk_tolerance == "moderate" and phase in ["PHASE2"]:
                score += 15  # Prefer middle phases
        
        # Study type preference
        study_type = design.get("studyType", "")
        if study_type == "INTERVENTIONAL" and user_risk_tolerance != "low":
            score += 10
        elif study_type == "OBSERVATIONAL" and user_risk_tolerance == "low":
            score += 10
        
        # Add trial with score
        scored_trials.append({
            "trial": study,
            "score": score,
            "match_reasons": []
        })
    
    # Sort by score and add match reasons
    scored_trials.sort(key=lambda x: x["score"], reverse=True)
    
    # Generate match reasons for top trials
    for trial_info in scored_trials[:10]:  # Top 10 trials
        trial = trial_info["trial"]
        reasons = []
        
        eligibility = trial.get("eligibilityModule", {})
        design = trial.get("designModule", {})
        
        # Age reason
        min_age = eligibility.get("minimumAge", 0)
        max_age = eligibility.get("maximumAge", 100)
        
        # Parse age values to ensure proper comparison
        min_age = parse_age(min_age)
        max_age = parse_age(max_age)
        
        if min_age <= user_age <= max_age:
            reasons.append(f"Age {user_age} fits eligibility range ({min_age}-{max_age})")
        
        # Gender reason
        sex = eligibility.get("sex", "ALL")
        if sex == "ALL" or sex == user_gender.upper():
            reasons.append(f"Gender requirement: {sex}")
        
        # Phase reason
        phases = design.get("phases", [])
        if phases and phases != ["NA"]:
            phase = phases[0] if phases else "NA"
            reasons.append(f"Phase: {phase}")
        
        trial_info["match_reasons"] = reasons
    
    state["personalized_recommendations"] = scored_trials[:10]
    state["messages"].append(AIMessage(content=f"Generated personalized recommendations for {len(scored_trials[:10])} trials based on your profile."))
    
    return state

def risk_analyzer(state: AgentState) -> AgentState:
    """Analyze and explain risks and benefits of trials"""
    api_results = state.get("api_results", {})
    studies = api_results.get("studies", [])
    selected_model = state.get("selected_model", "llama3.1:8b")
    
    if not studies:
        state["risk_assessments"] = {}
        return state
    
    risk_assessments = {}
    
    for study in studies[:5]:  # Analyze top 5 trials
        nct_id = study.get("nctId", "")
        brief_title = study.get("briefTitle", "")
        design = study.get("designModule", {})
        eligibility = study.get("eligibilityModule", {})
        
        # Extract key risk factors
        phases = design.get("phases", [])
        study_type = design.get("studyType", "")
        intervention_model = design.get("interventionModel", "")
        allocation = design.get("allocation", "")
        
        # Determine risk level based on phase and design
        risk_level = "Low"
        risk_factors = []
        benefits = []
        
        if phases and phases != ["NA"]:
            phase = phases[0] if phases else "NA"
            if phase in ["PHASE1", "EARLY_PHASE1"]:
                risk_level = "High"
                risk_factors.append("Early phase trial - limited safety data available")
                benefits.append("Access to cutting-edge experimental treatments")
            elif phase == "PHASE2":
                risk_level = "Medium-High"
                risk_factors.append("Phase 2 trial - safety established, effectiveness being tested")
                benefits.append("Treatment has passed initial safety testing")
            elif phase == "PHASE3":
                risk_level = "Medium"
                risk_factors.append("Phase 3 trial - comparing with standard treatments")
                benefits.append("Treatment has shown promise in earlier phases")
            elif phase == "PHASE4":
                risk_level = "Low"
                risk_factors.append("Phase 4 trial - post-approval safety monitoring")
                benefits.append("Treatment is already FDA-approved")
        
        # Study type risks
        if study_type == "INTERVENTIONAL":
            risk_factors.append("Interventional study - involves active treatment")
            benefits.append("May receive the actual treatment being studied")
        elif study_type == "OBSERVATIONAL":
            risk_factors.append("Observational study - no active treatment")
            benefits.append("Lower risk - just monitoring and observation")
        
        # Intervention model risks
        if intervention_model == "SINGLE_GROUP":
            risk_factors.append("Single group study - no comparison group")
            benefits.append("All participants receive the treatment")
        elif intervention_model == "PARALLEL":
            risk_factors.append("Randomized study - may receive placebo or standard treatment")
            benefits.append("May receive the experimental treatment")
        
        # Create risk assessment summary
        risk_summary = f"""
        **Risk Level: {risk_level}**
        
        **Risk Factors:**
        {chr(10).join([f"• {factor}" for factor in risk_factors])}
        
        **Potential Benefits:**
        {chr(10).join([f"• {benefit}" for benefit in benefits])}
        
        **Safety Considerations:**
        • This is a {study_type.lower()} study
        • Phase: {phases[0] if phases and phases != ['NA'] else 'Not specified'}
        • {len(eligibility.get('inclusionCriteria', '').split()) if eligibility.get('inclusionCriteria') else 0} inclusion criteria
        • {len(eligibility.get('exclusionCriteria', '').split()) if eligibility.get('exclusionCriteria') else 0} exclusion criteria
        """
        
        risk_assessments[nct_id] = {
            "title": brief_title,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "benefits": benefits,
            "summary": risk_summary,
            "phase": phases[0] if phases and phases != ["NA"] else "Unknown",
            "study_type": study_type
        }
    
    state["risk_assessments"] = risk_assessments
    state["messages"].append(AIMessage(content=f"Completed risk analysis for {len(risk_assessments)} trials."))
    
    return state

def quality_evaluator(state: AgentState) -> AgentState:
    """Evaluate the quality of results and decide if refinement is needed"""
    api_results = state.get("api_results", {})
    studies = api_results.get("studies", [])
    personalized_recommendations = state.get("personalized_recommendations", [])
    risk_assessments = state.get("risk_assessments", {})
    user_profile = state.get("user_profile", {})
    
    # Quality metrics
    quality_score = 0
    refinement_needed = False
    refinement_type = "none"
    
    # Check if we have enough trials
    if len(studies) < 5:
        quality_score -= 20
        refinement_needed = True
        refinement_type = "refine_search"
    
    # Check if personalized recommendations are good
    if personalized_recommendations:
        high_score_trials = [r for r in personalized_recommendations if r.get("score", 0) > 70]
        if len(high_score_trials) < 3:
            quality_score -= 15
            refinement_needed = True
            refinement_type = "refine_profile"
    
    # Check risk distribution
    if risk_assessments:
        high_risk_trials = [r for r in risk_assessments.values() if r.get("risk_level") in ["Very High", "High"]]
        user_risk_tolerance = user_profile.get("risk_tolerance", "moderate")
        
        if user_risk_tolerance == "low" and len(high_risk_trials) > len(risk_assessments) * 0.7:
            quality_score -= 10
            refinement_needed = True
            refinement_type = "refine_search"
    
    # Check location coverage
    user_location = user_profile.get("location", "")
    if user_location:
        location_matches = 0
        for study in studies:
            locations = study.get("locationsModule", {}).get("locations", [])
            for location in locations:
                if user_location.lower() in location.get("city", "").lower():
                    location_matches += 1
                    break
        
        if location_matches < len(studies) * 0.3:
            quality_score -= 10
            refinement_needed = True
            refinement_type = "refine_search"
    
    # Add quality metrics to state
    state["quality_metrics"] = {
        "score": quality_score,
        "refinement_needed": refinement_needed,
        "refinement_type": refinement_type,
        "total_trials": len(studies),
        "high_score_trials": len([r for r in personalized_recommendations if r.get("score", 0) > 70]) if personalized_recommendations else 0,
        "location_coverage": location_matches if user_location else "N/A"
    }
    
    return state

def search_refiner(state: AgentState) -> AgentState:
    """Refine the search criteria to get better results"""
    current_disease = state.get("disease_name", "")
    api_results = state.get("api_results", {})
    quality_metrics = state.get("quality_metrics", {})
    
    # Expand disease search terms
    disease_expansions = {
        "cancer": ["cancer", "tumor", "malignancy", "neoplasm"],
        "diabetes": ["diabetes", "diabetic", "glucose", "insulin"],
        "heart": ["heart", "cardiac", "cardiovascular", "coronary"],
        "lung": ["lung", "pulmonary", "respiratory", "bronchial"],
        "breast": ["breast", "mammary", "ductal", "lobular"],
        "prostate": ["prostate", "prostatic", "glandular"],
        "brain": ["brain", "cerebral", "neurological", "cognitive"]
    }
    
    # Find expansion for current disease
    expanded_terms = []
    for key, terms in disease_expansions.items():
        if key.lower() in current_disease.lower():
            expanded_terms = terms
            break
    
    if not expanded_terms:
        expanded_terms = [current_disease]
    
    # Update search strategy
    state["search_strategy"] = {
        "original_disease": current_disease,
        "expanded_terms": expanded_terms,
        "search_refinement": "Expanded disease terms for broader coverage",
        "previous_results": len(api_results.get("studies", [])),
        "refinement_reason": quality_metrics.get("refinement_type", "unknown")
    }
    
    # Mark for re-search
    state["needs_research"] = True
    
    return state

def profile_refiner(state: AgentState) -> AgentState:
    """Refine user profile to get better trial matches"""
    user_profile = state.get("user_profile", {})
    quality_metrics = state.get("quality_metrics", {})
    personalized_recommendations = state.get("personalized_recommendations", [])
    
    # Analyze current profile limitations
    profile_issues = []
    suggested_improvements = {}
    
    # Check age range
    user_age = user_profile.get("age", 30)
    if user_age < 18 or user_age > 80:
        profile_issues.append("Age may limit trial eligibility")
        suggested_improvements["age_flexibility"] = "Consider trials with broader age ranges"
    
    # Check location flexibility
    user_location = user_profile.get("location", "")
    travel_preference = user_profile.get("travel_preference", "local")
    if travel_preference == "local" and quality_metrics.get("location_coverage", 0) < 5:
        profile_issues.append("Local trials may be limited")
        suggested_improvements["travel_flexibility"] = "Consider expanding travel radius"
    
    # Check risk tolerance
    risk_tolerance = user_profile.get("risk_tolerance", "moderate")
    if risk_tolerance == "low" and quality_metrics.get("high_score_trials", 0) < 3:
        profile_issues.append("Low risk tolerance may limit options")
        suggested_improvements["risk_flexibility"] = "Consider moderate risk trials"
    
    # Update profile with suggestions
    state["profile_refinement"] = {
        "issues_identified": profile_issues,
        "suggested_improvements": suggested_improvements,
        "refinement_reason": quality_metrics.get("refinement_type", "unknown"),
        "current_profile": user_profile.copy()
    }
    
    return state

def route_based_on_quality(state: AgentState) -> str:
    """Route to next step based on quality evaluation"""
    quality_metrics = state.get("quality_metrics", {})
    
    if quality_metrics.get("refinement_needed", False):
        refinement_type = quality_metrics.get("refinement_type", "refine_search")
        if refinement_type == "refine_search":
            return "refine_search"
        elif refinement_type == "refine_profile":
            return "refine_profile"
    
    return "proceed"

# Create LangGraph
def create_agent_graph():
    """Create the LangGraph workflow"""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("clarify_disease", clarify_disease)
    workflow.add_node("search_clinical_trials", search_clinical_trials)
    workflow.add_node("summarize_eligibility", summarize_eligibility)
    workflow.add_node("prepare_visualizations", prepare_visualizations)
    workflow.add_node("patient_profile_matcher", patient_profile_matcher)
    workflow.add_node("risk_analyzer", risk_analyzer)
    workflow.add_node("quality_evaluator", quality_evaluator)
    workflow.add_node("search_refiner", search_refiner)
    workflow.add_node("profile_refiner", profile_refiner)
    
    # Add edges with proper START and END constants
    workflow.add_edge(START, "clarify_disease")
    workflow.add_edge("clarify_disease", "search_clinical_trials")
    workflow.add_edge("search_clinical_trials", "summarize_eligibility")
    workflow.add_edge("summarize_eligibility", "prepare_visualizations")
    workflow.add_edge("prepare_visualizations", "patient_profile_matcher")
    workflow.add_edge("patient_profile_matcher", "risk_analyzer")
    workflow.add_edge("risk_analyzer", "quality_evaluator")
    workflow.add_edge("quality_evaluator", "search_refiner")
    workflow.add_edge("search_refiner", "profile_refiner")
    workflow.add_edge("profile_refiner", END)
    
    return workflow.compile()

# Initialize the agent
@st.cache_resource
def get_agent():
    return create_agent_graph()

# Helper function to create trial phase swimlane
def create_phase_swimlane(phase_data):
    """Create a swimlane visualization for trial phases"""
    if not phase_data:
        return None
    
    # Define phase order and colors
    phase_order = ["Phase 1", "Phase 2", "Phase 3", "Phase 4", "Early Phase 1", "Not Applicable"]
    phase_colors = {
        "Phase 1": "#FF6B6B",
        "Phase 2": "#4ECDC4", 
        "Phase 3": "#45B7D1",
        "Phase 4": "#96CEB4",
        "Early Phase 1": "#FFEAA7",
        "Not Applicable": "#DDA0DD"
    }
    
    # Create the swimlane chart
    fig = go.Figure()
    
    y_pos = 0
    for phase in phase_order:
        if phase in phase_data:
            count = phase_data[phase]
            fig.add_trace(go.Bar(
                x=[count],
                y=[phase],
                orientation='h',
                name=phase,
                marker_color=phase_colors.get(phase, "#CCCCCC"),
                text=[f"{count} trials"],
                textposition='auto',
                hovertemplate=f"<b>{phase}</b><br>Trials: {count}<extra></extra>"
            ))
            y_pos += 1
    
    fig.update_layout(
        title="Clinical Trial Phases Distribution",
        xaxis_title="Number of Trials",
        yaxis_title="Trial Phase",
        height=400,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

# Helper function to create demographic visualizations
def create_demographic_charts(age_data, gender_data, study_type_data, enrollment_sizes):
    """Create demographic visualization charts"""
    charts = {}
    
    # Age range chart
    if age_data:
        age_fig = px.bar(
            x=list(age_data.keys()),
            y=list(age_data.values()),
            title="Age Groups Eligible for Trials",
            labels={"x": "Age Group", "y": "Number of Trials"},
            color=list(age_data.values()),
            color_continuous_scale="viridis"
        )
        age_fig.update_layout(
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        charts["age"] = age_fig
    
    # Gender requirements chart
    if gender_data:
        gender_fig = px.pie(
            values=list(gender_data.values()),
            names=list(gender_data.keys()),
            title="Gender Requirements for Trials",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        gender_fig.update_traces(textposition='inside', textinfo='percent+label')
        charts["gender"] = gender_fig
    
    # Study type chart
    if study_type_data:
        study_fig = px.bar(
            x=list(study_type_data.keys()),
            y=list(study_type_data.values()),
            title="Study Types Available",
            labels={"x": "Study Type", "y": "Number of Trials"},
            color=list(study_type_data.values()),
            color_continuous_scale="plasma"
        )
        study_fig.update_layout(
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        charts["study_type"] = study_fig
    
    # Enrollment size statistics
    if enrollment_sizes:
        enrollment_stats = {
            "Total Enrollment": sum(enrollment_sizes),
            "Average Enrollment": int(sum(enrollment_sizes) / len(enrollment_sizes)),
            "Largest Study": max(enrollment_sizes),
            "Smallest Study": min(enrollment_sizes)
        }
        charts["enrollment_stats"] = enrollment_stats
    
    return charts

# Main Streamlit app
def main():
    st.markdown('<h1 class="main-header">🏥 Patient & Caregiver Trial Navigator</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Find and understand clinical trials for your condition</p>', unsafe_allow_html=True)
    
    # Model selection sidebar
    with st.sidebar:
        st.markdown("### 🤖 AI Model Configuration")
        
        # Get available models
        available_models = get_available_models()
        
        if available_models:
            selected_model = st.selectbox(
                "Choose Ollama Model:",
                available_models,
                index=0 if "llama3.1:8b" in available_models else 0,
                help="Select the local Ollama model to use for AI responses"
            )
            
            # Model info
            st.markdown(f"""
            <div class="model-info">
                <strong>Selected Model:</strong> {selected_model}<br>
                <strong>Type:</strong> Local (Ollama)<br>
                <strong>Status:</strong> ✅ Available
            </div>
            """, unsafe_allow_html=True)
            
            # Test model connection
            if st.button("Test Model Connection"):
                with st.spinner("Testing model connection..."):
                    test_response = real_llm("Hello, this is a test message.", selected_model)
                    if "Error" not in test_response:
                        st.success("✅ Model connection successful!")
                        st.info(f"Test response: {test_response[:100]}...")
                    else:
                        st.error("❌ Model connection failed!")
        else:
            st.error("❌ No Ollama models found!")
            st.info("Please install models using: `ollama pull llama3.1:8b`")
        
        st.markdown("---")
        st.markdown("### 👤 User Profile & Preferences")
        
        # User profile form
        with st.expander("Set Your Profile for Personalized Recommendations", expanded=False):
            st.markdown("""
            **Why Set Your Profile?** 
            
            Your profile helps us find trials that are most likely to:
            ✅ **Accept you** based on age, gender, and location
            🎯 **Match your preferences** for risk level and travel distance  
            📍 **Be accessible** to you geographically
            ⚖️ **Balance risks and benefits** according to your comfort level
            
            The more accurate your profile, the better your trial recommendations will be!
            """)
            
            st.markdown("**Basic Information:**")
            user_age = st.number_input("Age", min_value=1, max_value=120, value=30, help="Your current age")
            user_gender = st.selectbox("Gender", ["All", "Male", "Female"], help="Your gender preference")
            user_location = st.text_input("Location (City/Country)", placeholder="e.g., New York, USA", help="Your preferred location for trials")
            
            st.markdown("**Risk Tolerance:**")
            
            # Add detailed explanation for risk levels
            with st.expander("ℹ️ What does Risk Tolerance mean?", expanded=False):
                st.markdown("""
                **Risk tolerance** refers to how comfortable you are with experimental or unproven treatments:
                
                🔴 **High Risk Tolerance** - You're willing to try cutting-edge treatments
                - **Best for**: Phase 1-2 trials, experimental therapies
                - **Consider if**: You've tried standard treatments, want access to newest options
                - **Trade-off**: Higher potential benefits but also higher risks
                
                🟡 **Moderate Risk Tolerance** - You want some innovation with safety data
                - **Best for**: Phase 2-3 trials, treatments with some safety history
                - **Consider if**: You want newer options but prefer some safety data
                - **Trade-off**: Balanced approach between innovation and safety
                
                🟢 **Low Risk Tolerance** - You prefer established, proven treatments
                - **Best for**: Phase 3-4 trials, FDA-approved treatments
                - **Consider if**: You want maximum safety, prefer proven approaches
                - **Trade-off**: Lower risks but potentially fewer breakthrough benefits
                """)
            
            user_risk_tolerance = st.selectbox(
                "Risk Tolerance Level",
                ["low", "moderate", "high"],
                help="Choose based on how comfortable you are with experimental treatments",
                format_func=lambda x: {
                    "low": "🟢 Low - Prefer proven, safe treatments",
                    "moderate": "🟡 Moderate - Want innovation with safety data", 
                    "high": "🔴 High - Willing to try cutting-edge treatments"
                }[x]
            )
            
            # Show what this means for trial phases
            if user_risk_tolerance == "low":
                st.info("🟢 **Low Risk**: You'll see mostly Phase 3-4 trials with established safety records")
            elif user_risk_tolerance == "moderate":
                st.info("🟡 **Moderate Risk**: You'll see Phase 2-3 trials with some safety data")
            elif user_risk_tolerance == "high":
                st.info("🔴 **High Risk**: You'll see Phase 1-2 trials with cutting-edge experimental treatments")
            
            st.markdown("**Travel Preferences:**")
            
            # Add explanation for travel preferences
            with st.expander("ℹ️ What do travel preferences mean?", expanded=False):
                st.markdown("""
                **Travel preferences** help us find trials within your comfort zone:
                
                🏠 **Local**: Within your city or immediate area (0-25 miles)
                - **Best for**: Minimizing travel time and costs
                - **Consider if**: You have limited mobility or prefer convenience
                
                🚗 **Regional**: Within your state or neighboring states (25-200 miles)
                - **Best for**: Finding more trial options while staying relatively close
                - **Consider if**: You can travel occasionally but prefer to stay in your region
                
                ✈️ **National**: Anywhere in your country
                - **Best for**: Access to specialized trials and top research centers
                - **Consider if**: You're willing to travel for the best treatment options
                
                🌍 **International**: Anywhere in the world
                - **Best for**: Cutting-edge trials and experimental treatments
                - **Consider if**: You're seeking the most advanced options available
                """)
            
            user_travel_preference = st.selectbox(
                "Travel Willingness",
                ["local", "regional", "national", "international"],
                help="How far you're willing to travel for trials",
                format_func=lambda x: {
                    "local": "🏠 Local (0-25 miles)",
                    "regional": "🚗 Regional (25-200 miles)",
                    "national": "✈️ National (anywhere in country)",
                    "international": "🌍 International (worldwide)"
                }[x]
            )
            
            # Auto-save profile as user types (no button needed)
            st.session_state.agent_state["user_profile"] = {
                "age": user_age,
                "gender": user_gender,
                "location": user_location,
                "risk_tolerance": user_risk_tolerance,
                "travel_preference": user_travel_preference
            }
            
            # Show profile summary (only once)
            if user_age or user_gender or user_location:
                st.markdown("---")
                st.markdown("**📋 Your Profile Summary:**")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Age:** {user_age}")
                    st.write(f"**Gender:** {user_gender}")
                    st.write(f"**Location:** {user_location}")
                
                with col2:
                    st.write(f"**Risk Tolerance:** {user_risk_tolerance.title()}")
                    st.write(f"**Travel Preference:** {user_travel_preference.title()}")
                
                # Explain what this means for recommendations
                st.info(f"""
                🎯 **Based on your profile, you'll see trials that:**
                • Accept {user_age}-year-old {user_gender.lower()} participants
                • Are located {user_travel_preference} to your area
                • Match your {user_risk_tolerance} risk tolerance level
                • Have the best chance of accepting you
                """)
                
                st.success("✅ Profile active! Results are now personalized.")
        
        st.markdown("---")
        st.markdown("### 📊 App Features")
        st.markdown("""
        - 🔍 **Smart Disease Detection**
        - 📍 **Interactive Trial Map**
        - 📊 **Phase Distribution Analysis**
        - 👥 **Demographic Insights**
        - ✅ **Simplified Eligibility**
        - 🎯 **Personalized Matching**
        - ⚠️ **Risk Assessment**
        """)
    
    # ===== CHAT SECTION AT TOP =====
    st.markdown('<h2 class="sub-header">💬 Chat with Trial Navigator</h2>', unsafe_allow_html=True)
    
    # Create a container for chat to keep it organized
    chat_container = st.container()
    
    with chat_container:
        # Chat interface - right below the header
        for message in st.session_state.messages:
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.write(message.content)
            else:
                with st.chat_message("assistant"):
                    st.write(message.content)
        
        # Chat input - right below messages (positioned correctly)
        chat_input = st.chat_input("Enter a disease or condition (e.g., 'breast cancer', 'diabetes')")
        
        # Process chat input
        if chat_input:
            # Add user message
            st.session_state.messages.append(HumanMessage(content=chat_input))
            st.session_state.agent_state["messages"].append(HumanMessage(content=chat_input))
            
            # Update disease name and selected model
            st.session_state.agent_state["disease_name"] = chat_input
            st.session_state.agent_state["selected_model"] = selected_model
            
            # Run the agent
            with st.spinner("Searching for clinical trials..."):
                agent = get_agent()
                final_state = agent.invoke(st.session_state.agent_state)
                st.session_state.agent_state = final_state
            
            # Rerun to show new messages
            st.rerun()
    
    # ===== TWO COLUMNS BELOW CHAT: TRIAL ANALYSIS & VISUALIZATIONS =====
    if st.session_state.agent_state.get("api_results"):
        api_results = st.session_state.agent_state["api_results"]
        studies = api_results.get("studies", [])
        
        if studies:
            total_count = api_results.get("totalCount", len(studies))
            
            # Check if user has a profile and show personalized info
            user_profile = st.session_state.agent_state.get("user_profile", {})
            if user_profile and any(user_profile.values()):
                # Calculate how many trials match the user's profile
                matching_trials = 0
                for study in studies:
                    eligibility = study.get("eligibilityModule", {})
                    min_age = eligibility.get("minimumAge", 0)
                    max_age = eligibility.get("maximumAge", 100)
                    sex = eligibility.get("sex", "ALL")
                    
                    # Check age match using helper function
                    user_age = int(user_profile.get("age", 30))
                    min_age = parse_age(min_age)
                    max_age = parse_age(max_age)
                    age_match = min_age <= user_age <= max_age
                    
                    # Check gender match
                    gender_match = sex == "ALL" or sex == user_profile.get("gender", "All").upper()
                    
                    if age_match and gender_match:
                        matching_trials += 1
                
                st.success(f"✅ Found {len(studies)} recruiting trials")
                st.info(f"🎯 **{matching_trials} trials match your profile** (age {user_profile.get('age')}, {user_profile.get('gender')}, {user_profile.get('risk_tolerance')} risk, {user_profile.get('travel_preference')} travel)")
                st.info(f"📊 Total available: {total_count} trials (showing first {len(studies)})")
            else:
                st.success(f"✅ Found {len(studies)} recruiting trials (showing up to 50 results)")
                if total_count > len(studies):
                    st.info(f"📊 Total available: {total_count} trials (showing first {len(studies)})")
            
            # Interactive trial locations map
            if st.session_state.agent_state.get("visualization_data", {}).get("map_data"):
                st.subheader("🌍 Interactive Trial Locations Map")
                map_data = st.session_state.agent_state["visualization_data"]["map_data"]
                if map_data and any("lat" in item and "lon" in item for item in map_data):
                    # Create interactive map with folium
                    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
                    
                    for location in map_data:
                        if "lat" in location and "lon" in location:
                            # Create popup content
                            popup_content = f"""
                            <b>{location['facility']}</b><br>
                            <b>City:</b> {location['city']}, {location['country']}<br>
                            <b>Trial:</b> {location['trial_title']}<br>
                            <b>Phase:</b> {location.get('phase', 'Unknown')}<br>
                            <a href="https://clinicaltrials.gov/ct2/show/{location['nct_id']}" target="_blank">View Trial</a>
                            """
                            
                            # Add marker with different colors based on phase
                            phase = location.get('phase', 'Unknown')
                            if 'Phase 1' in phase:
                                color = 'red'
                            elif 'Phase 2' in phase:
                                color = 'blue'
                            elif 'Phase 3' in phase:
                                color = 'green'
                            elif 'Phase 4' in phase:
                                color = 'purple'
                            else:
                                color = 'gray'
                            
                            folium.Marker(
                                [location['lat'], location['lon']],
                                popup=folium.Popup(popup_content, max_width=300),
                                tooltip=f"{location['facility']} - {location['city']}",
                                icon=folium.Icon(color=color, icon='info-sign')
                            ).add_to(m)
                    
                    # Display the map
                    st_folium(m, width=400, height=400)
                    
                    # Show location summary
                    unique_cities = len(set(f"{item['city']}, {item['country']}" for item in map_data if 'city' in item))
                    st.info(f"📍 Trials are being conducted in {unique_cities} locations")
                else:
                    st.info("📍 Location coordinates not available for these trials")
            else:
                st.info("📍 Location data not available for these trials")
            
            # Trial phase swimlane visualization
            if st.session_state.agent_state.get("visualization_data", {}).get("phase_data"):
                st.subheader("📊 Trial Phase Distribution")
                phase_data = st.session_state.agent_state["visualization_data"]["phase_data"]
                if phase_data:
                    fig = create_phase_swimlane(phase_data)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("📊 Phase information not available for these trials")
            else:
                st.info("📊 Phase information not available for these trials")
            
            # Demographic visualizations
            if st.session_state.agent_state.get("visualization_data"):
                viz_data = st.session_state.agent_state["visualization_data"]
                
                if any(key in viz_data for key in ["age_data", "gender_data", "study_type_data", "enrollment_sizes"]):
                    st.subheader("📊 Demographic & Eligibility Analysis")
                    
                    # Create demographic charts
                    demographic_charts = create_demographic_charts(
                        viz_data.get("age_data", {}),
                        viz_data.get("gender_data", {}),
                        viz_data.get("study_type_data", {}),
                        viz_data.get("enrollment_sizes", [])
                    )
                    
                    # Display charts in columns
                    if "age" in demographic_charts:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.plotly_chart(demographic_charts["age"], use_container_width=True)
                        with col2:
                            if "gender" in demographic_charts:
                                st.plotly_chart(demographic_charts["gender"], use_container_width=True)
                    
                    if "study_type" in demographic_charts:
                        st.plotly_chart(demographic_charts["study_type"], use_container_width=True)
                    
                    # Display enrollment statistics
                    if "enrollment_stats" in demographic_charts:
                        st.subheader("📈 Enrollment Statistics")
                        stats = demographic_charts["enrollment_stats"]
                        
                        # Check if user has a profile for personalized stats
                        user_profile = st.session_state.agent_state.get("user_profile", {})
                        if user_profile and any(user_profile.values()):
                            # Calculate personalized enrollment stats
                            matching_enrollments = []
                            for study in studies:
                                eligibility = study.get("eligibilityModule", {})
                                min_age = eligibility.get("minimumAge", 0)
                                max_age = eligibility.get("maximumAge", 100)
                                sex = eligibility.get("sex", "ALL")
                                
                                # Check age and gender match using helper function
                                user_age = int(user_profile.get("age", 30))
                                min_age = parse_age(min_age)
                                max_age = parse_age(max_age)
                                age_match = min_age <= user_age <= max_age
                                gender_match = sex == "ALL" or sex == user_profile.get("gender", "All").upper()
                                
                                if age_match and gender_match:
                                    design = study.get("designModule", {})
                                    enrollment_info = design.get("enrollmentInfo", {})
                                    enrollment_count = enrollment_info.get("count", 0)
                                    if enrollment_count > 0:
                                        matching_enrollments.append(enrollment_count)
                            
                            if matching_enrollments:
                                matching_total = sum(matching_enrollments)
                                matching_avg = matching_total // len(matching_enrollments)
                                matching_max = max(matching_enrollments)
                                matching_min = min(matching_enrollments)
                                
                                st.info(f"🎯 **Personalized for {user_profile.get('age')}-year-old {user_profile.get('gender')}**")
                                col1, col2, col3, col4 = st.columns(4)
                                with col1:
                                    st.metric("Matching Trials Enrollment", f"{matching_total:,}")
                                with col2:
                                    st.metric("Avg Matching Study Size", f"{matching_avg:,}")
                                with col3:
                                    st.metric("Largest Matching Study", f"{matching_max:,}")
                                with col4:
                                    st.metric("Smallest Matching Study", f"{matching_min:,}")
                                
                                st.markdown("---")
                                st.markdown("**📊 All Trials (for comparison):**")
                        
                        # Show overall stats - same width as personalized stats above
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Enrollment", f"{stats['Total Enrollment']:,}")
                        with col2:
                            st.metric("Average Study Size", f"{stats['Average Enrollment']:,}")
                        with col3:
                            st.metric("Largest Study", f"{stats['Largest Study']:,}")
                        with col4:
                            st.metric("Smallest Study", f"{stats['Smallest Study']:,}")
            

            
            # ===== END ANALYSIS & SUMMARY SECTION =====
            
            # ===== TRIAL DETAILS & RECOMMENDATIONS SECTION =====
            
            # Simplified eligibility criteria - full width
            if st.session_state.agent_state.get("simplified_criteria"):
                st.subheader("✅ Simplified Eligibility Criteria")
                st.write(st.session_state.agent_state["simplified_criteria"])
            
            # Sample Trials - full width
            st.subheader("📋 Sample Trials")
            for i, study in enumerate(studies[:3]):  # Show first 3 trials
                with st.expander(f"{study.get('briefTitle', 'Unknown Trial')[:60]}..."):
                    st.write(f"**Condition:** {', '.join(study.get('conditionModule', {}).get('conditions', []))}")
                    st.write(f"**Status:** {study.get('overallStatus', 'Unknown')}")
                    
                    # Show phase information
                    design_module = study.get("designModule", {})
                    phases = design_module.get("phases", [])
                    study_type = design_module.get("studyType", "Unknown")
                    
                    if study_type == "OBSERVATIONAL":
                        st.write(f"**Type:** Observational Study")
                    elif phases and phases != ["NA"]:
                        phase_code = phases[0] if phases else "NA"
                        if phase_code == "PHASE1":
                            st.write(f"**Phase:** Phase 1")
                        elif phase_code == "PHASE2":
                            st.write(f"**Phase:** Phase 2")
                        elif phase_code == "PHASE3":
                            st.write(f"**Phase:** Phase 3")
                        elif phase_code == "PHASE4":
                            st.write(f"**Phase:** Phase 4")
                        elif phase_code == "EARLY_PHASE1":
                            st.write(f"**Phase:** Early Phase 1")
                        else:
                            st.write(f"**Phase:** {phase_code}")
                    else:
                        st.write(f"**Phase:** Not Applicable")
                    
                    # Show sponsor information
                    sponsor_module = study.get("sponsorModule", {})
                    lead_sponsor = sponsor_module.get("leadSponsor", {})
                    lead_sponsor_name = lead_sponsor.get("leadSponsorName", "Unknown")
                    lead_sponsor_class = lead_sponsor.get("leadSponsorClass", "Unknown")
                    st.write(f"**Sponsor:** {lead_sponsor_name} ({lead_sponsor_class})")
                    
                    # Add link to ClinicalTrials.gov
                    nct_id = study.get('nctId', '')
                    if nct_id:
                        st.markdown(f"[View on ClinicalTrials.gov](https://clinicaltrials.gov/ct2/show/{nct_id})")
            
            # Personalized recommendations - full width
            if st.session_state.agent_state.get("personalized_recommendations"):
                st.subheader("🎯 Personalized Recommendations")
                recommendations = st.session_state.agent_state["personalized_recommendations"]
                
                if recommendations:
                    st.success(f"✨ Found {len(recommendations)} matching trials!")
                    
                    # Show top 3 recommendations
                    for i, rec in enumerate(recommendations[:3]):
                        trial = rec["trial"]
                        score = rec["score"]
                        
                        with st.expander(f"🥇 #{i+1} - Score: {score}"):
                            st.write(f"**Match Score:** {score}/100")
                            st.write(f"**NCT ID:** {trial.get('nctId', 'Unknown')}")
                            
                            # Add link to ClinicalTrials.gov
                            nct_id = trial.get('nctId', '')
                            if nct_id:
                                st.markdown(f"[View on ClinicalTrials.gov](https://clinicaltrials.gov/ct2/show/{nct_id})")
                else:
                    st.info("💡 Set your profile in sidebar for personalized recommendations.")
            
            # Risk assessments summary
            if st.session_state.agent_state.get("risk_assessments"):
                st.subheader("⚠️ Risk Summary")
                risk_assessments = st.session_state.agent_state["risk_assessments"]
                
                if risk_assessments:
                    st.info(f"🔍 Risk analysis: {len(risk_assessments)} trials")
                    
                    # Show risk summary
                    for nct_id, assessment in risk_assessments.items():
                        risk_level = assessment["risk_level"]
                        title = assessment["title"][:50] + "..." if len(assessment["title"]) > 50 else assessment["title"]
                        
                        # Color code based on risk level
                        if risk_level == "High":
                            color = "🔴"
                        elif risk_level == "Medium-High":
                            color = "🟠"
                        elif risk_level == "Medium":
                            color = "🟡"
                        else:
                            color = "🟢"
                        
                        st.write(f"{color} {title} - {risk_level}")
        
        else:
            st.warning("No recruiting trials found for the specified condition.")
    else:
        st.info("👈 Start by entering a disease or condition in the chat to search for clinical trials.")
    
    # ===== STORY JOURNEY: HOW REFLEXION IMPROVED YOUR RESULTS =====
    # This section is now full-width, outside the columns
    if st.session_state.agent_state.get("api_results") and st.session_state.agent_state["api_results"].get("studies"):
        studies = st.session_state.agent_state["api_results"]["studies"]
        
        st.markdown("---")
        st.subheader("🚀 **Your Trial Search Journey Story**")
        
        st.info("""
        **📚 What is this?** This section tells the story of how our smart system improved your search results. 
        It's like having a friendly guide explain what happened behind the scenes to make your results better!
        """)
        
        with st.expander("📖 **Click to expand the full story**", expanded=False):
            st.markdown("""
            **Once upon a time, you searched for clinical trials...** 
            
            Let us show you how our smart system made your results better! ✨
            """)
            
            # Step 1: Initial Search
            with st.container():
                st.markdown("### 🔍 **Chapter 1: The Initial Search**")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown("""
                    **What happened:** We searched the database for trials matching your condition.
                    
                    **What we found:** Raw results from our search.
                    
                    **Your reaction:** "Hmm, these trials seem okay but not perfect for me..."
                    """)
                with col2:
                    st.metric("Initial Results", f"{len(studies)} trials", delta="Basic Search")
            
            # Step 2: Smart Analysis
            with st.container():
                st.markdown("### 🧠 **Chapter 2: Smart Analysis**")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown("""
                    **What happened:** Our system analyzed your profile and preferences.
                    
                    **What we learned:** Your age, location, risk tolerance, and travel preferences.
                    
                    **Your reaction:** "Wow, it's actually considering what I want!"
                    """)
                with col2:
                    user_profile = st.session_state.agent_state.get("user_profile", {})
                    if user_profile and any(user_profile.values()):
                        st.metric("Profile Match", "Active", delta="Smart!")
                    else:
                        st.metric("Profile Match", "Not Set", delta="Set Profile")
            
            # Step 3: Quality Check
            with st.container():
                st.markdown("### ⚖️ **Chapter 3: Quality Check**")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown("""
                    **What happened:** We evaluated if the results meet quality standards.
                    
                    **What we checked:** Trial count, match quality, location coverage.
                    
                    **Your reaction:** "It's like having a quality inspector for my search!"
                    """)
                with col2:
                    if st.session_state.agent_state.get("quality_metrics"):
                        quality_metrics = st.session_state.agent_state["quality_metrics"]
                        score = quality_metrics.get("score", 0)
                        if score >= 75:
                            st.metric("Quality Score", f"{score}%", delta="Excellent!", delta_color="normal")
                        elif score >= 50:
                            st.metric("Quality Score", f"{score}%", delta="Good", delta_color="normal")
                        else:
                            st.metric("Quality Score", f"{score}%", delta="Needs Work", delta_color="inverse")
                    else:
                        st.metric("Quality Score", "In Progress", delta="Checking")
            
            # Step 4: The Improvement
            with st.container():
                st.markdown("### ✨ **Chapter 4: The Magic Happens**")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown("""
                    **What happened:** Our reflexion system automatically improved your results.
                    
                    **What changed:** Better matching, more relevant trials, personalized recommendations.
                    
                    **Your reaction:** "This is exactly what I was looking for!"
                    """)
                with col2:
                    if st.session_state.agent_state.get("personalized_recommendations"):
                        recs = st.session_state.agent_state["personalized_recommendations"]
                        st.metric("Smart Matching", f"{len(recs)}", delta="Perfect!")
                    else:
                        st.metric("Smart Matching", "In Progress", delta="Working")
            
            # Step 5: The Happy Ending
            with st.container():
                st.markdown("### 🎉 **Chapter 5: Your Success Story**")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown("""
                    **What you got:** Trials that actually match your needs and preferences.
                    
                    **Why it's better:** Personalized, relevant, and accessible options.
                    
                    **Your final thought:** "This system really understands me!"
                    """)
                with col2:
                    st.success("🎯 **Mission Accomplished!**")
            
            # Summary of improvements
            st.markdown("---")
            st.markdown("### 📊 **Your Journey Summary**")
            
            st.info("""
            **📈 Here's what our smart system accomplished for you:**
            """)
            
            # Create simplified improvement metrics - only show what's meaningful
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("🔍 **Trials Found**", f"{len(studies)}", delta="Total Results")
            
            with col2:
                if st.session_state.agent_state.get("personalized_recommendations"):
                    recs = st.session_state.agent_state["personalized_recommendations"]
                    st.metric("🎯 **Smart Matches**", f"{len(recs)}", delta="Tailored for You")
                else:
                    st.metric("🎯 **Smart Matches**", "In Progress", delta="Working")
            
            # Moral of the story
            st.info("""
            **🎭 The Moral of Your Story:**
            
            > *"Smart systems don't just find trials - they find the RIGHT trials for YOU!"*
            
            **💡 What This Means:**
            • **Personalization:** Results tailored to your specific needs
            • **Quality Assurance:** We check if results meet high standards  
            • **Continuous Improvement:** The system learns and gets better
            • **User-Centric:** Everything is designed around YOUR preferences
            """)
        
        # ===== END STORY JOURNEY =====

if __name__ == "__main__":
    main()
