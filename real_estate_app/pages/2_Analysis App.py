import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
# import seaborn as sns
# from PIL import Image
# import base64
from pathlib import Path



# root path
root_path = Path(__file__).parent.parent

# 
print("Root path:", root_path)
df_path = root_path /"datasets"/"appartment_cleaned_final.csv"



# Page configuration
st.set_page_config(
    page_title="Bangalore Apartment Analysis",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #1E3A8A;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .card {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background-color: #EFF6FF;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1E40AF;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6B7280;
    }
</style>
""", unsafe_allow_html=True)


# Load data
df = pd.read_csv(df_path)

# Header
st.markdown("<h1 class='main-header'>Bangalore Apartment Analysis Dashboard</h1>", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("Filters")

# Zone filter
selected_zones = st.sidebar.multiselect(
    "Select Zones", 
    options=sorted(df['zone'].unique()),
    default=sorted(df['zone'].unique())
)

# BHK filter
selected_bhk = st.sidebar.multiselect(
    "Select BHK Type", 
    options=sorted(df['bhk_type'].unique()),
    default=sorted(df['bhk_type'].unique())
)

# Construction status filter
selected_status = st.sidebar.multiselect(
    "Select Construction Status", 
    options=sorted(df['construction_status'].unique()),
    default=sorted(df['construction_status'].unique())
)

# Price range filter
selected_price_range = st.sidebar.multiselect(
    "Select Price Range", 
    options=sorted(df['price_range'].unique()),
    default=sorted(df['price_range'].unique())
)



# Apply filters
filtered_df = df[
    df['zone'].isin(selected_zones) &
    df['bhk_type'].isin(selected_bhk) &
    df['construction_status'].isin(selected_status) &
    df['price_range'].isin(selected_price_range) 
]

# Create tabs for different sections
tab1, tab2 = st.tabs(["Overview", "Price Analysis"])

with tab1:
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<p class='metric-value'>{len(filtered_df)}</p>", unsafe_allow_html=True)
        st.markdown("<p class='metric-label'>Total Properties</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        avg_price = f"₹{filtered_df['price_value'].mean():.2f} Cr"
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<p class='metric-value'>{avg_price}</p>", unsafe_allow_html=True)
        st.markdown("<p class='metric-label'>Average Price</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        avg_price_sqft = f"₹{filtered_df['price_per_sqft'].mean():.0f}"
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<p class='metric-value'>{avg_price_sqft}</p>", unsafe_allow_html=True)
        st.markdown("<p class='metric-label'>Avg Price/sqft</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        avg_area = f"{filtered_df['bulit_area'].mean():.0f} sqft"
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<p class='metric-value'>{avg_area}</p>", unsafe_allow_html=True)
        st.markdown("<p class='metric-label'>Average Area</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h2 class='sub-header'>Distribution by Zone and BHK Type</h2>", unsafe_allow_html=True)
    
    # Distribution charts row
    col1, col2 = st.columns(2)
    
    with col1:
        zone_counts = filtered_df['zone'].value_counts().reset_index()
        zone_counts.columns = ['Zone', 'Count']
        
        fig = px.pie(
            zone_counts, 
            values='Count', 
            names='Zone',
            title='Properties by Zone',
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        bhk_counts = filtered_df['bhk_type'].value_counts().reset_index()
        bhk_counts.columns = ['BHK Type', 'Count']
        
        fig = px.bar(
            bhk_counts,
            x='BHK Type',
            y='Count',
            title='Properties by BHK Type',
            color='BHK Type',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Status 
    # col1, col2 = st.columns(2)
    
    # with col1:
    status_counts = filtered_df['construction_status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    
    fig = px.pie(
        status_counts, 
        values='Count', 
        names='Status',
        title='Properties by Construction Status',
        color_discrete_sequence=px.colors.qualitative.Pastel1
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


with tab2:
    st.markdown("<h2 class='sub-header'>Price Analysis</h2>", unsafe_allow_html=True)
    
    # Price distribution by zone
    fig = px.box(
        filtered_df, 
        x='zone', 
        y='price_value',
        color='zone',
        title='Price Distribution by Zone',
    )
    fig.update_layout(
        yaxis_title='Price (₹Cr)',
        xaxis_title='Zone',
        height=500
    )
    fig.update_yaxes(tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True)
    
    # Price vs area scatter
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(
            filtered_df,
            x='bulit_area',
            y='price_value',
            color='zone',
            size='price_per_sqft',
            hover_name='apartment_loc',
            title='Price vs Built Area by Zone',
            labels={'bulit_area': 'Built Area (sqft)', 'price_value': 'Price (₹)'},
        )
        fig.update_layout(height=500)
        fig.update_yaxes(tickformat=",.0f")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            filtered_df,
            x='bhk_type',
            y='price_per_sqft',
            color='zone',
            size='bulit_area',
            hover_name='apartment_loc',
            title='Price per sqft by BHK Type and Zone',
            labels={'price_per_sqft': 'Price per sqft (₹)'},
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Price heatmap
    st.markdown("<h3 class='sub-header'>Price Heatmap: Zone vs BHK Type</h3>", unsafe_allow_html=True)
    
    pivot_data = filtered_df.pivot_table(
        values='price_value', 
        index='zone',
        columns='bhk_type',
        aggfunc='mean'
    )
    
    fig = px.imshow(
        pivot_data,
        text_auto='.2s',
        aspect='auto',
        color_continuous_scale='Viridis',
        title='Average Price by Zone and BHK Type'
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # # Price trend over area ranges
    price_by_area = filtered_df.groupby('area_range')['price_per_sqft'].mean().reset_index()

    # Define the desired order for area_range
    area_order = ['< 1000 sqft', '1000-1500 sqft', '1500-2000 sqft', '2000-2500 sqft', '> 2500 sqft']

    # Convert area_range to a categorical type with the specified order
    price_by_area['area_range'] = pd.Categorical(price_by_area['area_range'], categories=area_order, ordered=True)

    # Sort the dataframe by the ordered area_range for correct plotting
    price_by_area = price_by_area.sort_values('area_range')

    
    fig = px.line(
        price_by_area, 
        x='area_range', 
        y='price_per_sqft',
        markers=True,
        title='Average Price per sqft by Area Range',
        labels={'price_per_sqft': 'Avg Price per sqft (₹)', 'area_range': 'Area Range'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


        # Map visualization
    st.markdown("<h3 class='sub-header'>Property Map with Price and Area Visualization</h3>", unsafe_allow_html=True)
    
    # Create figure
    fig = go.Figure()
    
    # Add scatter points for properties
    fig.add_trace(go.Scattermapbox(
        lat=filtered_df['Latitude'],
        lon=filtered_df['Longitude'],
        mode='markers',
        marker=dict(
            size=filtered_df['bulit_area'] / 100,
            sizemode='area',
            sizeref=0.1,
            color=filtered_df['price_per_sqft'],
            colorscale='IceFire',
            showscale=True,
            colorbar=dict(title="Price per sqft")
        ),
        opacity=0.8,
        text=[f"Location: {loc}<br>Price: ₹{price:,.2f}Cr<br>Area: {area} sqft<br>Price/sqft: ₹{ppsqft:,.2f}" 
              for loc, price, area, ppsqft in zip(
                  filtered_df['apartment_loc'], 
                  filtered_df['price_value'], 
                  filtered_df['bulit_area'], 
                  filtered_df['price_per_sqft'])],
        hoverinfo='text',
        hoverlabel=dict(
            bgcolor="white"
        ),
        name='Properties'
    ))
    
    # Define zone boundaries with proper formatting
    zones = [
        {
            'name': 'North Bangalore',
            'coords': [[77.50, 13.17], [77.66, 13.14], [77.66, 13.03], [77.50, 13.03], [77.50, 13.17]],
            'color': 'rgba(25, 118, 210, 0.9)',  # More vibrant blue
            'fill': 'rgba(25, 118, 210, 0.15)',
            'center': [13.10, 77.58]
        }, 
        {
            'name': 'South Bangalore',
            'coords': [[77.52, 12.93], [77.68, 12.93], [77.68, 12.87], [77.52, 12.87], [77.52, 12.93]],
            'color': 'rgba(255, 145, 0, 0.9)',  # More vibrant orange
            'fill': 'rgba(255, 145, 0, 0.15)',
            'center': [12.90, 77.60]
        }, 
        {
            'name': 'East Bangalore',
            'coords': [[77.60, 13.02], [77.75, 13.02], [77.75, 12.92], [77.60, 12.92], [77.60, 13.02]],
            'color': 'rgba(142, 36, 170, 0.9)',  # More vibrant purple
            'fill': 'rgba(142, 36, 170, 0.15)',
            'center': [12.97, 77.67]
        }, 
        {
            'name': 'West Bangalore',
            'coords': [[77.45, 13.02], [77.60, 13.02], [77.60, 12.92], [77.45, 12.92], [77.45, 13.02]],
            'color': 'rgba(0, 150, 136, 0.9)',  # Teal instead of another blue shade
            'fill': 'rgba(0, 150, 136, 0.15)',
            'center': [12.96, 77.53]
        }
    ]
    
    # Add zone boundaries to map
    for zone in zones:
        # Ensure coordinates are properly formatted for plotting a polygon
        lons = [coord[0] for coord in zone['coords']]
        lats = [coord[1] for coord in zone['coords']]
        
        # Close the polygon by adding the first point at the end
        lons.append(lons[0])
        lats.append(lats[0])
        
        fig.add_trace(go.Scattermapbox(
            lat=lats,
            lon=lons,
            mode='lines',
            fill='toself',
            fillcolor=zone['fill'],
            line=dict(color=zone['color'], width=2.5),  # Slightly thicker line
            name=zone['name']
        ))
        
        # Add zone labels
        fig.add_trace(go.Scattermapbox(
            lat=[zone['center'][0]],
            lon=[zone['center'][1]],
            mode='text',
            text=[zone['name']],
            textfont=dict(size=14, color='black', family="Arial Black"),
            textposition="middle center",
            showlegend=False
        ))
    
    # Update layout with improved styling
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",  # A cleaner map style
            center=dict(lat=12.97, lon=77.58),  # Better centered on Bangalore
            zoom=11
        ),
        height=700,
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0.8)"
        )
    )
    
    # Display the map
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True,
        'scrollZoom': True,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d']
    })

