🏢 Bangalore Apartment Finder & Analysis
==============================

## About This App

This application empowers users to navigate Bangalore's real estate market with data-driven insights. Whether you're buying, renting, or researching, our tools provide valuable information to make informed decisions about properties across Bangalore. The app leverages machine learning, data visualization, and recommendation algorithms to deliver a seamless experience.

## Key Features

The application consists of three main tabs:

1. **Price Predictor**: Estimate apartment prices based on key property features.
2. **Analysis App**: Visualize market trends and property distributions through an interactive dashboard.
3. **Recommend Apartments**: Discover apartments tailored to your preferences using a customizable recommendation system.

## Data Source

The data for this project was scraped from [99acres.com](https://www.99acres.com/), covering apartments in Bangalore's **East, West, North, and South** zones.

## Project Components

### Data Pipeline
- **Data Collection**: Scraped apartment data from 99acres.com.
- **Data Cleaning**: Handled missing values, outliers, and inconsistencies.
- **Feature Engineering**: Created relevant features for modeling and analysis.
- **Preprocessing**: Standardized and transformed data for machine learning.
- **Training Pipeline**: Automated pipeline for model training and evaluation.

## 🔄 Workflow Architecture
![image](https://github.com/user-attachments/assets/5d625152-9924-4f22-851f-5cda4c4f88ef)

### Model Development
Systematic experimentation was conducted to build a robust price prediction model, with results tracked using **MLflow**[DagsHub](https://dagshub.com/AMR-ITH/RealEstateInsights):
- **Experiment 1**: Simple model with and without target transformation.
- **Experiment 2**: Model selection across various algorithms.
- **Experiment 3**: Hyperparameter tuning for Random Forest (RF-HP Tuning).
- **Experiment 4**: Final best model selection.

### MLflow Integration
- **Experiment Tracking**: All experiments, parameters, and metrics logged in MLflow.
- **Model Registry**: Best-performing model registered for deployment.

### DVC Pipeline
- **Data Versioning**: Tracked dataset changes using DVC.
- **Pipeline Automation**: Automated data processing and model training with `dvc repro`.
- **Storage**: Data and models pushed to an **S3** bucket for versioning and reproducibility.
- **Model Storage**: Final model stored and registered via DVC.

### CI/CD Deployment
- **Automated Testing**: Ensured code quality and model performance.
- **Deployment**: Streamlined deployment of the application for production use.


