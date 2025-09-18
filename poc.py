import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
import time
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="SĀGARA - Marine Data & Analytics Portal",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for marine theme
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a1428 0%, #1a2744 50%, #0d1b2a 100%);
    }
    
    .css-1d391kg {
        background: rgba(13, 27, 42, 0.95);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 123, 191, 0.1), rgba(0, 212, 255, 0.05));
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(0, 212, 255, 0.2);
        margin-bottom: 1rem;
    }
    
    .main-header {
        background: linear-gradient(135deg, #007bbf, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #a0c4d4;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .team-badge {
        background: linear-gradient(135deg, #ff6b35, #f7931e);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .stSelectbox > div > div {
        background-color: rgba(26, 39, 68, 0.8);
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(26, 39, 68, 0.8);
        color: #e8f4f8;
        border: 1px solid rgba(0, 212, 255, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #007bbf, #00d4ff);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 212, 255, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "🌊 Welcome to SĀGARA! I'm your Oceanic Copilot. I can help analyze marine data, generate insights, and create visualizations. How can I assist you today?"}
    ]

if 'data_quality_score' not in st.session_state:
    st.session_state.data_quality_score = 98.7

# Generate sample data
@st.cache_data
def generate_marine_data():
    # Oceanographic data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    oceanographic_data = pd.DataFrame({
        'Date': dates,
        'Temperature': 25 + 3 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 1, len(dates)),
        'Salinity': 35 + 0.5 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 0.2, len(dates)),
        'pH': 8.1 + 0.1 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 0.05, len(dates)),
        'Dissolved_Oxygen': 6.5 + 0.5 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 0.3, len(dates))
    })
    
    # Species data
    species_data = pd.DataFrame({
        'Species': ['Tuna', 'Sardine', 'Mackerel', 'Anchovy', 'Pomfret', 'Kingfish'],
        'Count': [1250, 3400, 2100, 4500, 850, 1100],
        'Biomass_kg': [15000, 8500, 6300, 4500, 12000, 9800],
        'Habitat_Depth': [50, 20, 30, 15, 40, 35]
    })
    
    # Location data
    locations_data = pd.DataFrame({
        'Latitude': [19.0760, 18.5204, 20.1809, 19.2183, 18.9388],
        'Longitude': [72.8777, 73.8567, 70.1647, 72.9781, 72.8305],
        'Location': ['Mumbai Coast', 'Pune Region', 'Kutch Coast', 'Thane Creek', 'Navi Mumbai'],
        'Temperature': [26.5, 24.8, 27.2, 25.9, 26.1],
        'Species_Count': [45, 32, 38, 41, 36]
    })
    
    return oceanographic_data, species_data, locations_data

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="main-header">🌊 SĀGARA</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Smart Agentic Gateway for Aquatic Data, Marine Analytics and Research</div>', unsafe_allow_html=True)
    st.markdown('<div class="team-badge">Team DOMinators x SIH 2025</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image(r"./DOMinators_logo_V1.png", width=300)
    
    st.markdown("### 🎯 Navigation")
    page = st.selectbox(
        "Select Dashboard Section",
        ["🏠 Overview", "📊 Data Portal", "🗺️ Marine Digital Twin", "🧠 AI Analytics", "🤖 Oceanic Copilot", "📈 Ecosystem Modeling"]
    )
    
    st.markdown("### ⚙️ System Status")
    st.success("🟢 All Systems Online")
    st.info("🔄 Real-time Data Streaming")
    st.warning("⚠️ 3 Data Quality Alerts")
    
    st.markdown("### 📊 Quick Stats")
    st.metric("Active Sensors", "847", "12")
    st.metric("Data Quality", f"{st.session_state.data_quality_score:.1f}%", "0.3")
    st.metric("Species Tracked", "156", "4")

# Load data
oceanographic_data, species_data, locations_data = generate_marine_data()

# Main content based on selected page
if page == "🏠 Overview":
    st.markdown("## 🌊 Platform Overview")
    
    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Oceanographic Records", "2.3M+", "150K")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Fisheries Data Points", "45K+", "2.1K")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("eDNA Sequences", "12,847", "234")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("AI Model Accuracy", "94.2%", "1.5%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col5:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Active Monitoring", "24/7", "100%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌡️ Ocean Temperature Trends")
        fig = px.line(
            oceanographic_data.tail(90), 
            x='Date', 
            y='Temperature',
            title='90-Day Temperature Trend',
            color_discrete_sequence=['#00d4ff']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8f4f8'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🐟 Species Distribution")
        fig = px.pie(
            species_data, 
            values='Count', 
            names='Species',
            title='Current Species Count Distribution',
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8f4f8'
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "📊 Data Portal":
    st.markdown("## 📊 Unified Data Portal")
    
    # Data source selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        data_source = st.selectbox(
            "Select Data Source",
            ["Oceanographic", "Fisheries", "eDNA", "Satellite Imagery"]
        )
    
    with col2:
        time_range = st.selectbox(
            "Time Range",
            ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Last Year"]
        )
    
    with col3:
        quality_filter = st.selectbox(
            "Quality Filter",
            ["All Data", "High Quality Only", "Validated Only"]
        )
    
    # Data table
    if data_source == "Oceanographic":
        st.markdown("### 🌊 Oceanographic Data")
        filtered_data = oceanographic_data.tail(100)
        st.dataframe(filtered_data, use_container_width=True)
        
        # Download button
        csv = filtered_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Data",
            data=csv,
            file_name=f'oceanographic_data_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv'
        )
    
    # Data quality metrics
    st.markdown("### ✅ Data Quality Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Completeness", "98.5%", "0.2%")
    with col2:
        st.metric("Accuracy", "97.8%", "-0.1%")
    with col3:
        st.metric("Consistency", "99.1%", "0.3%")
    with col4:
        st.metric("Timeliness", "95.4%", "1.2%")

elif page == "🗺️ Marine Digital Twin":
    st.markdown("## 🗺️ Marine Digital Twin Visualization")
    
    # Map controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        layer_select = st.multiselect(
            "Map Layers",
            ["Temperature", "Salinity", "Species Distribution", "Current Flow"],
            default=["Temperature", "Species Distribution"]
        )
    
    with col2:
        depth_range = st.slider("Depth Range (m)", 0, 200, (0, 50))
    
    with col3:
        time_slider = st.slider("Time", 0, 23, 12, format="%d:00")
    
  
    # Real-time data simulation
    col1, col2, col3 = st.columns(3)
    with col2:
          # Create map
        m = folium.Map(
            location=[19.0760, 72.8777],
            zoom_start=8,
            tiles='CartoDB dark_matter'
        )
        
        # Add markers for each location
        for idx, row in locations_data.iterrows():
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=row['Species_Count']/2,
                popup=f"<b>{row['Location']}</b><br>Temp: {row['Temperature']}°C<br>Species: {row['Species_Count']}",
                color='#00d4ff',
                fill=True,
                fillOpacity=0.7
            ).add_to(m)
        
        # Display map
        map_data = st_folium(m, width=800, height=500)
        
    with col1:
        st.markdown("### 📡 Real-time Sensors")
        sensor_data = pd.DataFrame({
            'Sensor_ID': [f'S{i:03d}' for i in range(1, 11)],
            'Status': ['Online'] * 8 + ['Offline'] * 2,
            'Last_Update': ['2 min ago'] * 8 + ['1 hour ago'] * 2,
            'Battery': np.random.randint(20, 100, 10)
        })
        st.dataframe(sensor_data, use_container_width=True)
    
    with col3:
        st.markdown("### 🌊 Current Conditions")
        current_conditions = {
            'Sea Surface Temp': '26.3°C',
            'Wave Height': '1.2 m',
            'Wind Speed': '15 km/h',
            'Visibility': '8.5 km',
            'Tide': 'High (+1.8m)'
        }
        
        for condition, value in current_conditions.items():
            st.metric(condition, value)

elif page == "🧠 AI Analytics":
    st.markdown("## 🧠 AI Analytics Engine")
    
    # Model performance metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🔍 Otolith Classification")
        accuracy = 94.2
        st.metric("Accuracy", f"{accuracy}%")
        progress_bar = st.progress(accuracy/100)
        
        st.markdown("**Recent Classifications:**")
        classifications = pd.DataFrame({
            'Image_ID': [f'OTO_{i:03d}' for i in range(1, 6)],
            'Species': ['Tuna', 'Sardine', 'Mackerel', 'Anchovy', 'Pomfret'],
            'Confidence': [0.94, 0.89, 0.96, 0.87, 0.91]
        })
        st.dataframe(classifications, use_container_width=True)
    
    with col2:
        st.markdown("### 🧬 eDNA Analysis")
        accuracy = 87.5
        st.metric("Match Rate", f"{accuracy}%")
        progress_bar = st.progress(accuracy/100)
        
        st.markdown("**Recent Matches:**")
        edna_matches = pd.DataFrame({
            'Sample_ID': [f'DNA_{i:03d}' for i in range(1, 6)],
            'Species_Match': ['Pomfret', 'Kingfish', 'Tuna', 'Sardine', 'Mackerel'],
            'Match_Score': [0.92, 0.85, 0.94, 0.81, 0.88]
        })
        st.dataframe(edna_matches, use_container_width=True)
    
    with col3:
        st.markdown("### 🏠 Habitat Prediction")
        accuracy = 91.3
        st.metric("Accuracy", f"{accuracy}%")
        progress_bar = st.progress(accuracy/100)
        
        st.markdown("**Habitat Suitability:**")
        habitat_data = pd.DataFrame({
            'Region': ['Mumbai Coast', 'Kutch Coast', 'Thane Creek', 'Navi Mumbai', 'Pune Region'],
            'Suitability': [0.89, 0.76, 0.93, 0.85, 0.72]
        })
        st.dataframe(habitat_data, use_container_width=True)
    
    # Model training status
    st.markdown("### 🔄 Model Training Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        training_progress = st.progress(0)
        status_text = st.empty()
        
        if st.button("🚀 Start Training"):
            for i in range(101):
                training_progress.progress(i)
                status_text.text(f'Training Progress: {i}%')
                time.sleep(0.05)
            st.success("✅ Model training completed successfully!")
    
    with col2:
        st.markdown("**Training Metrics:**")
        metrics_data = pd.DataFrame({
            'Epoch': list(range(1, 11)),
            'Loss': np.random.uniform(0.1, 0.8, 10),
            'Accuracy': np.random.uniform(0.8, 0.95, 10)
        })
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=metrics_data['Epoch'], y=metrics_data['Loss'], name="Loss"),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=metrics_data['Epoch'], y=metrics_data['Accuracy'], name="Accuracy"),
            secondary_y=True,
        )
        
        fig.update_yaxes(title_text="Loss", secondary_y=False)
        fig.update_yaxes(title_text="Accuracy", secondary_y=True)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8f4f8'
        )
        
        st.plotly_chart(fig, use_container_width=True)

elif page == "🤖 Oceanic Copilot":
    st.markdown("## 🤖 Oceanic Copilot - AI Assistant")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Chat with Oceanic Copilot")
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_history:
                if message["role"] == "assistant":
                    st.markdown(f"🌊 **Oceanic Copilot:** {message['content']}")
                else:
                    st.markdown(f"👤 **You:** {message['content']}")
        
        # Chat input
        user_input = st.text_input("Ask about marine data, analysis, or insights...")
        
        if st.button("Send") and user_input:
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Generate AI response
            responses = [
                f"Based on the current oceanographic data, I can see that {user_input.lower()} relates to our marine ecosystem patterns. Let me analyze the latest sensor data...",
                f"Great question about {user_input.lower()}! Our AI models show interesting correlations in the recent data. I'll generate a detailed analysis for you.",
                f"I'm processing your query about {user_input.lower()} through our marine analytics pipeline. Here are the key insights from our database...",
                f"Analyzing marine patterns related to {user_input.lower()}... Our ecosystem models indicate several important trends you should know about."
            ]
            
            ai_response = random.choice(responses)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            
            st.rerun()
    
    with col2:
        st.markdown("### 🎯 Quick Actions")
        
        if st.button("📊 Generate Species Report"):
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": "Generating comprehensive species distribution report based on latest eDNA analysis and fisheries data. Report includes population trends, habitat preferences, and seasonal patterns."
            })
            st.rerun()
        
        if st.button("🌡️ Temperature Analysis"):
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": "Analyzing ocean temperature data from the past 90 days. I've identified a 0.3°C warming trend with seasonal variations. This may impact fish migration patterns in the next quarter."
            })
            st.rerun()
        
        if st.button("🗺️ Create Habitat Map"):
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": "Creating habitat suitability map using latest environmental parameters. The map shows optimal zones for different species based on temperature, salinity, and depth preferences."
            })
            st.rerun()
        
        st.markdown("### 📈 AI Capabilities")
        st.info("✅ Natural Language Processing")
        st.info("✅ Data Query & Analysis")
        st.info("✅ Visualization Generation")
        st.info("✅ Report Creation")
        st.info("✅ Predictive Modeling")

elif page == "📈 Ecosystem Modeling":
    st.markdown("## 📈 Ecosystem Graph Modeling")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🕸️ Species Interaction Network")
        
        # Network statistics
        network_stats = {
            'Total Species': 156,
            'Predator-Prey Links': 1203,
            'Competition Links': 847,
            'Symbiotic Links': 234,
            'Network Density': 0.68,
            'Average Clustering': 0.45
        }
        
        for stat, value in network_stats.items():
            st.metric(stat, value)
    
    with col2:
        st.markdown("### 📊 Ecosystem Health Index")
        
        # Create radar chart for ecosystem health
        categories = ['Biodiversity', 'Productivity', 'Stability', 'Resilience', 'Connectivity']
        values = [85, 78, 92, 73, 89]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Ecosystem Health',
            line_color='#00d4ff'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8f4f8'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Food web analysis
    st.markdown("### 🔗 Food Web Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Primary Producers**")
        producers = pd.DataFrame({
            'Species': ['Phytoplankton', 'Seaweed', 'Marine Plants'],
            'Biomass': [12500, 8900, 6700],
            'Growth_Rate': [0.12, 0.08, 0.05]
        })
        st.dataframe(producers, use_container_width=True)
    
    with col2:
        st.markdown("**Primary Consumers**")
        consumers = pd.DataFrame({
            'Species': ['Zooplankton', 'Small Fish', 'Crustaceans'],
            'Population': [450000, 85000, 67000],
            'Feeding_Rate': [0.25, 0.18, 0.15]
        })
        st.dataframe(consumers, use_container_width=True)
    
    with col3:
        st.markdown("**Top Predators**")
        predators = pd.DataFrame({
            'Species': ['Tuna', 'Shark', 'Large Fish'],
            'Population': [1250, 340, 890],
            'Hunt_Success': [0.68, 0.72, 0.61]
        })
        st.dataframe(predators, use_container_width=True)
    
    # Scenario modeling
    st.markdown("### 🎯 Scenario Modeling")
    
    scenario = st.selectbox(
        "Select Climate Scenario",
        ["Current Baseline", "+1°C Warming", "+2°C Warming", "Acidification Impact", "Overfishing Scenario"]
    )
    
    if scenario != "Current Baseline":
        st.warning(f"⚠️ Analyzing impact of: {scenario}")
        
        # Show impact predictions
        impact_data = pd.DataFrame({
            'Species_Group': ['Fish', 'Crustaceans', 'Mollusks', 'Plankton'],
            'Population_Change': [-15, -25, -35, +8],
            'Range_Shift_km': [45, 32, 28, 67],
            'Adaptation_Risk': ['Medium', 'High', 'Very High', 'Low']
        })
        
        st.dataframe(impact_data, use_container_width=True)
        
        # Impact visualization
        fig = px.bar(
            impact_data, 
            x='Species_Group', 
            y='Population_Change',
            title=f'Predicted Population Changes - {scenario}',
            color='Population_Change',
            color_continuous_scale=['red', 'yellow', 'green']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8f4f8'
        )
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🏢 Team DOMinators**")
    st.markdown("Advanced Marine Analytics Platform")

with col2:
    st.markdown("**📞 Support**")
    st.markdown("24/7 Technical Support Available")

with col3:
    st.markdown("**🔗 Integration**")
    st.markdown("API Documentation Available")

# Real-time updates simulation
if st.button("🔄 Refresh Real-time Data"):
    st.session_state.data_quality_score = round(random.uniform(95, 99), 1)
    st.success("✅ Data refreshed successfully!")
    st.rerun()
