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

</style>
""", unsafe_allow_html=True)

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
        "Tucson": {"lat": 32.2226, "lon": -110.9747},
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
        "clarification_question": ""
    }

# Mock LLM function (replace with actual LLM integration)
def mock_llm(prompt: str) -> str:
    """Mock LLM function - replace with actual LLM integration"""
    # Simple rule-based responses for demonstration
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
    
    # Simple rules for ambiguous terms
    ambiguous_terms = ["cancer", "tumor", "disease", "condition", "illness"]
    
    if any(term in disease for term in ambiguous_terms) and len(disease.split()) <= 2:
        state["needs_clarification"] = True
        state["clarification_question"] = "Could you please specify the type? For example: 'breast cancer', 'lung cancer', 'melanoma', etc."
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
    
    # Use mock LLM to simplify criteria
    prompt = f"Simplify these clinical trial eligibility criteria into plain language: {criteria_text}"
    simplified = mock_llm(prompt)
    
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
                    "trial_title": study.get("briefTitle", "")[:50] + "...",
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

# Create LangGraph
def create_agent_graph():
    """Create the LangGraph workflow"""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("clarify_disease", clarify_disease)
    workflow.add_node("search_clinical_trials", search_clinical_trials)
    workflow.add_node("summarize_eligibility", summarize_eligibility)
    workflow.add_node("prepare_visualizations", prepare_visualizations)
    
    # Add edges with proper START and END constants
    workflow.add_edge(START, "clarify_disease")
    workflow.add_edge("clarify_disease", "search_clinical_trials")
    workflow.add_edge("search_clinical_trials", "summarize_eligibility")
    workflow.add_edge("summarize_eligibility", "prepare_visualizations")
    workflow.add_edge("prepare_visualizations", END)
    
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
    
    # Create two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h2 class="sub-header">💬 Chat with Trial Navigator</h2>', unsafe_allow_html=True)
        
        # Chat interface
        for message in st.session_state.messages:
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.write(message.content)
            else:
                with st.chat_message("assistant"):
                    st.write(message.content)
        
        # Chat input
        if prompt := st.chat_input("Enter a disease or condition (e.g., 'breast cancer', 'diabetes')"):
            # Add user message
            st.session_state.messages.append(HumanMessage(content=prompt))
            st.session_state.agent_state["messages"].append(HumanMessage(content=prompt))
            
            # Update disease name
            st.session_state.agent_state["disease_name"] = prompt
            
            # Run the agent
            with st.spinner("Searching for clinical trials..."):
                agent = get_agent()
                final_state = agent.invoke(st.session_state.agent_state)
                st.session_state.agent_state = final_state
            
            # Rerun to show new messages
            st.rerun()
    
    with col2:
        st.markdown('<h2 class="sub-header">📊 Trial Analysis & Visualizations</h2>', unsafe_allow_html=True)
        
        # Show results if available
        if st.session_state.agent_state.get("api_results"):
            api_results = st.session_state.agent_state["api_results"]
            studies = api_results.get("studies", [])
            
            if studies:
                total_count = api_results.get("totalCount", len(studies))
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
                        st_folium(m, width=700, height=500)
                        
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
                
                # Simplified eligibility criteria
                if st.session_state.agent_state.get("simplified_criteria"):
                    st.subheader("✅ Simplified Eligibility Criteria")
                    st.write(st.session_state.agent_state["simplified_criteria"])
                
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
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Total Enrollment", f"{stats['Total Enrollment']:,}")
                            with col2:
                                st.metric("Average Study Size", f"{stats['Average Enrollment']:,}")
                            with col3:
                                st.metric("Largest Study", f"{stats['Largest Study']:,}")
                            with col4:
                                st.metric("Smallest Study", f"{stats['Smallest Study']:,}")
                
                # Sample trials list
                st.subheader("📋 Sample Trials")
                for i, study in enumerate(studies[:5]):  # Show first 5 trials
                    with st.expander(f"{study.get('briefTitle', 'Unknown Trial')} (NCT: {study.get('nctId', 'Unknown')})"):
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
                        
                        # Show location information
                        locations_module = study.get("locationsModule", {})
                        locations = locations_module.get("locations", [])
                        if locations:
                            location_info = []
                            for loc in locations[:3]:  # Show first 3 locations
                                facility = loc.get("facility", "")
                                city = loc.get("city", "")
                                country = loc.get("country", "")
                                if city and country:
                                    location_info.append(f"{facility}, {city}, {country}")
                            if location_info:
                                st.write(f"**Locations:** {'; '.join(location_info)}")
                        
                        # Add link to ClinicalTrials.gov
                        nct_id = study.get('nctId', '')
                        if nct_id:
                            st.markdown(f"[View on ClinicalTrials.gov](https://clinicaltrials.gov/ct2/show/{nct_id})")
            else:
                st.warning("No recruiting trials found for the specified condition.")
        else:
            st.info("👈 Start by entering a disease or condition in the chat to search for clinical trials.")

if __name__ == "__main__":
    main()
