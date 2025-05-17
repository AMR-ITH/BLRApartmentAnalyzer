import streamlit as st
import pandas as pd
import numpy as np
import dagshub
import json
import joblib
from pathlib import Path
import mlflow

st.set_page_config(page_title="Bangalore Flats Price Prediction", page_icon="🏢")

def load_model_information(file_path):
    with open(file_path) as f:
        run_info = json.load(f)
    return run_info

def load_trasformer(transformer_path):
    transformer = joblib.load(transformer_path)
    return transformer

# Set title with some styling
st.title("Bangalore Real Estate Price Predictor")
st.markdown("### Get estimated prices for flats in Bangalore")

# Initialize DagsHub connection
try:
    dagshub.init(repo_owner='AMR-ITH', repo_name='RealEstateInsights', mlflow=True)
    st.success("Successfully connected to DagsHub repository")
except Exception as e:
    st.error(f"Failed to connect to DagsHub: {e}")
    st.stop()

# root path
root_path = Path(__file__).parent.parent.parent


# load the model info to get the model name
try:
    model_name = load_model_information(root_path/"run_information.json")['model_name']
except Exception as e:
    st.error(f"Error loading model information: {e}")
    st.stop()

# Create two columns for the form inputs
col1, col2 = st.columns(2)

with col1:
    # sector
    zone = st.selectbox('Zone/Sector', ['east', 'west', 'north', 'south'])
    
    # construction status
    construction_status = st.selectbox('Construction Status', 
                                      ['New Property', 'Under Construction', 
                                       'Relatively New', 'Moderatly Old', 
                                       'Old', 'undefined'])
    
    # bhk
    bhk = float(st.selectbox('Number of Bedrooms', ['1', '2', '3', '4', '5', '6', '7']))

with col2:
    # built_up_area
    built_up_area = float(st.number_input('Built Up Area (sq.ft.)', 
                                         min_value=100.0, value=1000.0, step=100.0))
    
    # facility_category
    facility_category = st.selectbox('Facility Category', ['low', 'medium', 'high'])

# Add a divider
st.markdown("---")

# Create a prediction button
predict_button = st.button("Predict Price", type="primary")

if predict_button:
    # Show a spinner while predicting
    with st.spinner("Predicting price..."):
        try:
            # stage of the model
            alias_name = "staging_latest"
            
            # Construct the model URI using the alias
            model_uri = f"models:/{model_name}@{alias_name}"
            
            # Load the model using the alias
            model = mlflow.pyfunc.load_model(model_uri)
            
            # Get the run ID associated with this model version
            model_info = mlflow.models.get_model_info(model_uri)
            run_id = model_info.run_id
            
            # Fetch metrics from the run
            client = mlflow.tracking.MlflowClient()
            run = client.get_run(run_id)
            test_mae = run.data.metrics.get("test_mae", 0.5307577857825541)  # Default if not found
            
            # load the preprocessor
            preprocessor_path = root_path/"models"/"preprocessor.joblib"
            preprocessor = load_trasformer(preprocessor_path)
            
            # Create input dataframe for prediction
            input_data = pd.DataFrame({
                'zone': [zone],
                'construction_status': [construction_status],
                'bhk_type': [bhk],
                'bulit_area': [built_up_area],
                'luxury_category': [facility_category]
            })
            
            # Preprocess the input
            preprocessed_input = preprocessor.transform(input_data)
            
            # Make prediction
            prediction = model.predict(preprocessed_input)
            
            # Display the prediction
            st.success("Prediction Complete!")
            
            # Get metrics for the confidence interval
            # Now using the test_mae we retrieved from MLflow
            
            # Since you mentioned prices are in actual values, not log scale
            predicted_price = prediction[0]
            
            # Calculate the lower and upper bounds based on the test MAE
            # Using an absolute range since we're dealing with actual prices
            lower_bound = max(0, predicted_price - test_mae)  # Ensure non-negative
            upper_bound = predicted_price + test_mae
            
            # Display the prediction with range
            st.markdown(f"## Estimated Price: ₹{predicted_price:,.2f}")
            st.markdown(f"### Price Range: ₹{lower_bound:,.2f} - ₹{upper_bound:,.2f}")
            

            
        except Exception as e:
            st.error(f"Error during prediction: {e}")
            st.write("Please check if all the model dependencies are correctly installed.")
