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
![image](https://github.com/user-attachments/assets/40ff8904-5be9-4173-ab80-c14dc60a380c)


### Model Development
Systematic experimentation was conducted to build a robust price prediction model, with results tracked using **MLflow**[https://dagshub.com/AMR-ITH/RealEstateInsights](https://dagshub.com/AMR-ITH/RealEstateInsights):
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


## 🔄 CI/CD Pipeline

![image](https://github.com/user-attachments/assets/5fe21c6d-9f4c-45c5-9b71-18775c96d9dc)


CI/CD pipeline automates the entire deployment process:

1. **GitHub Actions**: Automates CI/CD pipeline triggering tests and builds upon code changes
2. **Docker**: Containerizes the application for consistent deployment
3. **AWS ECR**: Stores Docker images securely in the cloud
4. **AWS EC2/ECS**: Hosts the deployed application in a scalable environment
5. **AWS CodeDeploy**: Manages the application deployment process
6. **Auto Scaling Groups**: Ensures scalability and zero-downtime updates as traffic demands


## 🔗 Live Demo & Access

Explore the application through the following links:

- **Production App**: [http://65.0.11.187/](http://65.0.11.187/) ,[https://apprealestateapp-ampnarww3zvyfodus39uf2.streamlit.app](https://apprealestateapp-ampnarww3zvyfodus39uf2.streamlit.app)


## 📊 Technical Stack

### Backend
- **Language**: Python 3.x
- **ML Framework**: Scikit-learn, Random Forest
- **Data Processing**: Pandas, NumPy

### Frontend
- **Framework**: Streamlit
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Interactive Maps**: Plotly Mapbox

### Web Scraping
- **HTTP Client**: HTTPX (async HTTP requests)
- **HTML Parsing**: Selectolax (fast HTML parser)
- **Data Export**: CSV module
- **Request Management**: Time delays and random intervals for respectful scraping


