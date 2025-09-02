#!/usr/bin/env python3
"""
LangGraph Workflow Visualizer using LangGraph's built-in visualization
Creates visual representations of the clinical trials app workflow
"""

import streamlit as st
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Dict, Any, List
from langchain_core.messages import HumanMessage, AIMessage
import matplotlib.pyplot as plt
import networkx as nx

# Define the state structure (same as in app.py)
class AgentState(TypedDict):
    messages: List
    disease_name: str
    api_results: Dict[str, Any]
    simplified_criteria: str
    visualization_data: Dict[str, Any]
    needs_clarification: bool
    clarification_question: str
    selected_model: str
    user_profile: Dict[str, Any]
    risk_assessments: Dict[str, Any]
    personalized_recommendations: List[Dict[str, Any]]

def create_workflow_graph():
    """Create the LangGraph workflow and visualize it"""
    
    # Create the workflow (same as in app.py)
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("clarify_disease", lambda x: x)
    workflow.add_node("search_clinical_trials", lambda x: x)
    workflow.add_node("summarize_eligibility", lambda x: x)
    workflow.add_node("prepare_visualizations", lambda x: x)
    workflow.add_node("patient_profile_matcher", lambda x: x)
    workflow.add_node("risk_analyzer", lambda x: x)
    
    # Add edges
    workflow.add_edge(START, "clarify_disease")
    workflow.add_edge("clarify_disease", "search_clinical_trials")
    workflow.add_edge("search_clinical_trials", "summarize_eligibility")
    workflow.add_edge("summarize_eligibility", "prepare_visualizations")
    workflow.add_edge("prepare_visualizations", "patient_profile_matcher")
    workflow.add_edge("patient_profile_matcher", "risk_analyzer")
    workflow.add_edge("risk_analyzer", END)
    
    return workflow

def visualize_with_networkx():
    """Create a NetworkX visualization of the reflexion workflow"""
    
    # Create directed graph
    G = nx.DiGraph()
    
    # Add nodes with attributes for the reflexion structure
    nodes = [
        ("START", {"color": "#e3f2fd", "shape": "ellipse", "type": "start_end"}),
        ("clarify_disease", {"color": "#fff3e0", "shape": "rectangle", "type": "core"}),
        ("search_clinical_trials", {"color": "#fff3e0", "shape": "rectangle", "type": "core"}),
        ("summarize_eligibility", {"color": "#fff3e0", "shape": "rectangle", "type": "core"}),
        ("prepare_visualizations", {"color": "#fff3e0", "shape": "rectangle", "type": "core"}),
        ("patient_profile_matcher", {"color": "#e8f5e8", "shape": "rectangle", "type": "personalization"}),
        ("risk_analyzer", {"color": "#fff8e1", "shape": "rectangle", "type": "analysis"}),
        ("quality_evaluator", {"color": "#f3e5f5", "shape": "rectangle", "type": "reflexion"}),
        ("search_refiner", {"color": "#f3e5f5", "shape": "rectangle", "type": "reflexion"}),
        ("profile_refiner", {"color": "#f3e5f5", "shape": "rectangle", "type": "reflexion"}),
        ("END", {"color": "#e8f5e8", "shape": "ellipse", "type": "start_end"})
    ]
    
    for node, attrs in nodes:
        G.add_node(node, **attrs)
    
    # Add edges including reflexion feedback loops
    edges = [
        ("START", "clarify_disease"),
        ("clarify_disease", "search_clinical_trials"),
        ("search_clinical_trials", "summarize_eligibility"),
        ("summarize_eligibility", "prepare_visualizations"),
        ("prepare_visualizations", "patient_profile_matcher"),
        ("patient_profile_matcher", "risk_analyzer"),
        ("risk_analyzer", "quality_evaluator"),
        ("quality_evaluator", "search_refiner"),
        ("search_refiner", "profile_refiner"),
        ("profile_refiner", "END"),
        # Reflexion feedback loops
        ("search_refiner", "search_clinical_trials"),
        ("profile_refiner", "patient_profile_matcher")
    ]
    
    G.add_edges_from(edges)
    
    # Create the visualization
    plt.figure(figsize=(18, 12))
    
    # Adjust positions for better centered layout and intuitive reflexion flow
    pos = {
        "START": (0, 5),
        "clarify_disease": (2, 5),
        "search_clinical_trials": (4, 5),
        "summarize_eligibility": (6, 5),
        "prepare_visualizations": (8, 5),
        "patient_profile_matcher": (10, 5),
        "risk_analyzer": (12, 5),
        "quality_evaluator": (14, 5),
        "search_refiner": (10, 2.5),
        "profile_refiner": (6, 2.5),
        "END": (16, 5)
    }
    
    # Draw nodes with different colors and shapes
    node_colors = [G.nodes[node]["color"] for node in G.nodes()]
    node_sizes = [2000 if G.nodes[node]["type"] == "start_end" else 3500 for node in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, 
                          node_color=node_colors,
                          node_size=node_sizes,
                          edgecolors='#333',
                          linewidths=2)
    
    # Draw edges with different styles for feedback loops
    regular_edges = [edge for edge in G.edges() if edge not in [("search_refiner", "search_clinical_trials"), ("profile_refiner", "patient_profile_matcher")]]
    feedback_edges = [("search_refiner", "search_clinical_trials"), ("profile_refiner", "patient_profile_matcher")]
    
    # Draw regular edges
    nx.draw_networkx_edges(G, pos, 
                          edgelist=regular_edges,
                          edge_color='#666',
                          arrows=True,
                          arrowsize=20,
                          arrowstyle='->',
                          width=2)
    
    # Draw feedback edges with different style - more intuitive curved paths
    nx.draw_networkx_edges(G, pos, 
                          edgelist=feedback_edges,
                          edge_color='#ff6b6b',
                          arrows=True,
                          arrowsize=20,
                          arrowstyle='->',
                          width=3,
                          style='dashed',
                          connectionstyle="arc3,rad=0.4")
    
    # Draw labels
    labels = {node: node.replace('_', '\n') for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=9, font_weight='bold')
    
    # Add title
    plt.title('Clinical Trials App - LangGraph Reflexion Workflow', fontsize=20, fontweight='bold', pad=20)
    
    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#e3f2fd', 
                  markersize=15, label='Start/End Points'),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#fff3e0', 
                  markersize=15, label='Core Processing Nodes'),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#e8f5e8', 
                  markersize=15, label='Personalization Nodes'),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#fff8e1', 
                  markersize=15, label='Risk Analysis Node'),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#f3e5f5', 
                  markersize=15, label='Reflexion Nodes'),
        plt.Line2D([0], [0], color='#666', linewidth=2, label='Forward Flow'),
        plt.Line2D([0], [0], color='#ff6b6b', linewidth=3, linestyle='--', label='Feedback Loops')
    ]
    
    plt.legend(handles=legend_elements, loc='lower left', bbox_to_anchor=(0, 0.05), fontsize=10)
    
    # Add flow indicators with better positioning
    plt.text(8, 6.5, 'Forward Data Flow →', ha='center', va='center', fontsize=14, 
             fontweight='bold', color='#666', style='italic')
    plt.text(8, 1.5, 'Reflexion Feedback Loops', ha='center', va='center', fontsize=14, 
             fontweight='bold', color='#ff6b6b', style='italic')
    
    # Remove unnecessary text boxes and incorrect arrows
    
    plt.axis('off')
    plt.tight_layout()
    
    return plt.gcf()

if __name__ == "__main__":
    print("🎨 Creating LangGraph workflow visualization...")
    
    # Test the workflow creation
    try:
        workflow = create_workflow_graph()
        print("✅ LangGraph workflow created successfully")
        print(f"📊 Workflow has {len(workflow.nodes)} nodes")
        print(f"🔗 Workflow has {len(workflow.edges)} edges")
    except Exception as e:
        print(f"❌ Error creating workflow: {e}")
    
    # Create NetworkX visualization
    print("🎨 Creating NetworkX visualization...")
    fig1 = visualize_with_networkx()
    fig1.savefig('langgraph_workflow.png', dpi=300, bbox_inches='tight')
    print("✅ Saved langgraph_workflow.png")
    
    print("🎉 LangGraph workflow visualization complete!")
    print("📁 Generated files:")
    print("   - langgraph_workflow.png (LangGraph workflow)")
    
    # Show plots
    plt.show()
