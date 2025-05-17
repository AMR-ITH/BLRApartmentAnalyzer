import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(page_title="Recommend Apartments", page_icon="🏢")

# Load data
location_df = pickle.load(open('datasets/location_distance.pkl','rb'))
cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl','rb'))
cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl','rb'))
cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl','rb'))

# Add comments to explain what each similarity matrix represents
# We can assume these are based on your original code's purpose
st.title("Recommend Apartments")
st.write("""
This tool helps you find apartments in Bangalore based on similarity to other properties 
or by location proximity. You can also customize the recommendation algorithm!
""")

# Create tabs for different recommendation types
tab1, tab2 = st.tabs(["Similar Apartments", "Nearby Locations"])

# Function to recommend properties based on similarity
def recommend_properties_with_scores(property_name, top_n=5, weights=[0.5, 0.8, 1.0]):
    # Create combined similarity matrix with user-defined weights
    cosine_sim_matrix = weights[0] * cosine_sim1 + weights[1] * cosine_sim2 + weights[2] * cosine_sim3
    
    # Get the similarity scores for the property
    property_idx = location_df.index.get_loc(property_name)
    sim_scores = list(enumerate(cosine_sim_matrix[property_idx]))
    
    # Sort properties based on similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
    
    # Retrieve the names of the top properties
    top_properties = location_df.index[top_indices].tolist()
    
    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'Property Name': top_properties,
        'Similarity Score': top_scores
    })
    
    return recommendations_df

# Tab 1: Similar Apartments
with tab1:
    st.header("Find Similar Apartments")
    
    # Create a selectbox with property names
    sorted_properties = sorted(location_df.index.tolist())
    selected_apartment = st.selectbox("Select an apartment", sorted_properties)
    
    # Add a number input for recommendations
    num_recommendations = st.number_input("Number of recommendations", min_value=1, max_value=10, value=5)
    
    # Add sliders for customizing weights
    st.subheader("Customize Recommendation Weights")
    st.write("Adjust the importance of different similarity factors:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        weight1 = st.slider("Location Weight", 0.0, 1.0, 0.5, 0.1, help="Weight for location-based similarity")
    
    with col2:
        weight2 = st.slider("Amenities Weight", 0.0, 1.0, 0.8, 0.1, help="Weight for amenities-based similarity")
    
    with col3:
        weight3 = st.slider("Price Weight", 0.0, 1.0, 1.0, 0.1, help="Weight for price-based similarity")
    
    if st.button("Recommend"):
        # Get recommendations with custom weights
        recommendation_df = recommend_properties_with_scores(selected_apartment, num_recommendations, 
                                                           weights=[weight1, weight2, weight3])
        
        # Display results
        st.write(f"Apartments similar to {selected_apartment}:")
        st.dataframe(recommendation_df)

# Tab 2: Nearby Locations
with tab2:
    st.header("Find Nearby Apartments")
    
    # Create a selectbox with location names
    sorted_locations = sorted(location_df.columns.tolist())
    selected_location = st.selectbox("Select a location", sorted_locations)
    
    # Add a number input for radius
    radius = st.number_input("Radius in km", min_value=1, max_value=20, value=5)
    
    if st.button("Search"):
        # Convert km to meters
        radius_m = radius * 1000
        
        # Get properties within radius
        nearby = location_df[location_df[selected_location] < radius_m][selected_location].sort_values()
        
        # Create a dataframe with the results
        result_df = pd.DataFrame({
            'Property Name': nearby.index,
            'Distance (km)': nearby.values / 1000  # Convert meters to km
        })
        
        # Display results
        st.write(f"Apartments within {radius} km of {selected_location}:")
        st.dataframe(result_df)