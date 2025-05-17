import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import logging
import sys
import ast
import json
from sklearn.preprocessing import MultiLabelBinarizer


def load_data(file_path: Path) -> pd.DataFrame:
    try:
        print(f"Loading data from {file_path}")
        df = pd.read_csv(file_path)
        print(f"Loaded data with shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        raise


def clean_carpet_super_bulit_area(x):
    if not isinstance(x, str):
        return x  # Return as is if not a string (handles NaN)
    
    # Remove sq.ft and strip spaces
    x = x.replace(' sq.ft', '').strip()
    
    # Remove any trailing periods
    if x.endswith('.'):
        x = x[:-1]
    
    # Handle ranges with hyphen
    if '-' in x:
        try:
            first = (x.split('-')[0].strip())
            second = (x.split('-')[1].strip())
            return round((float(first) + float(second)) / 2)
        except:
            return None  
    
    # Convert single value
    try:
        return float(x)
    except:
        return None




def clean_price(x):
    # Handle NaN or non-string values
    if pd.isna(x) or not isinstance(x, str):
        return None
        
    # List of special non-numeric values to handle
    special_cases = [
        'Available on Request', 'On Request', 'Price on Request'
    ]
    
    # Check for special cases first
    for case in special_cases:
        if case.lower() in x.lower():
            return None  # or any other default value you prefer
    
    # Make a copy of x to avoid modifying the original
    original_x = x
    processed_x = x
    
    # Determine the unit type first (to apply conversion later)
    is_lakh = any(unit in original_x for unit in ['Lac', 'L', 'L+', 'Lakh', 'Lakhs'])
    
    # Remove all currency indicators
    indicators = ['Cr+ Charges', 'L+ Charges', 'Lac', 'Cr', 'L', 'Lakh', 'Lakhs', 'Crore', 'Crores']
    for indicator in indicators:
        if indicator in processed_x:
            processed_x = processed_x.replace(indicator, '')
    
    processed_x = processed_x.strip()
    
    # Handle range values
    if '-' in processed_x:
        try:
            parts = processed_x.split('-')
            min_val = float(parts[0].strip())
            max_val = float(parts[1].strip())
            value = round((min_val + max_val) / 2, 2)
        except ValueError:
            return None
    else:
        try:
            value = float(processed_x)
        except ValueError:
            return None
    
    # Convert to Crores based on the original unit
    if is_lakh:
        # Convert from Lakhs to Crores (1 Crore = 100 Lakhs)
        return round(value / 100, 2)
    else:
        # Already in Crores or no unit specified
        return round(value, 2)


def categorize_age_possession(value):
    # Handle NaN/None values
    if pd.isna(value):
        return "undefined"
    
    # Convert to string if value is not already a string
    if not isinstance(value, str):
        return "undefined"
    
    # Lists for categorization
    new_prop_list = ['New Launch', 'Ready To Move', 'Within 3 months', 'Within 6 months', '0 to 1 Year Old', 'Partially Ready To Move']
    under_const_list = ['Partially Ready To Move', 'Under Construction']
    
    # Check if value is in new property list
    if value in new_prop_list:
        return 'New Property'
    
    # Check specific age ranges
    if "1 to 5 Year Old" == value:
        return "Relatively New"
    if "5 to 10 Year Old" == value:
        return "Moderatly Old"
    if "10+ Year Old" == value:
        return "Old"
    
    # Check if under construction
    if value in under_const_list or 'By' in value:
        return "Under Construction"
    
    # Try to check numeric values for under construction properties
    try:
        if value.split('-')[0].strip().isnumeric():
            return "Under Construction"
    except (AttributeError, IndexError):
        pass
    
    # Default case
    return "undefined"


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned_data = df.assign(
        # Clean apartment name by removing 'in' and keeping only the part before the comma
        apartment_name=df['apartment_name'].str.replace('in', '').str.split(',').str[0],
        appartment_loc=df['appartment_loc'].apply(lambda x: x.split(',')[0].strip() if isinstance(x, str) and ',' in x else x.strip() if isinstance(x, str) else x),
        carpet_area=df['carpet_area'].apply(clean_carpet_super_bulit_area),
        bulit_area=df['bulit_area'].apply(clean_carpet_super_bulit_area),
        super_bulit_area=df['super_bulit_area'].apply(clean_carpet_super_bulit_area),
        price_value=df['price_value'].apply(clean_price),
        construction_status=df['construction_status'].apply(categorize_age_possession),
        bhk_type=df['bhk_type'].astype('category')
    )
    
    # Apply apartment name rectification to remove location from name if contained
    def apartment_rectification(row):
        if isinstance(row['appartment_loc'], str) and isinstance(row['apartment_name'], str):
            if row['appartment_loc'].lower() in row['apartment_name'].lower():
                return row['apartment_name'].lower().replace(row['appartment_loc'].lower(), '').strip()
            else:
                return row['apartment_name'].lower().strip()
        return row['apartment_name']
    
    cleaned_data['apartment_name'] = cleaned_data.apply(apartment_rectification, axis=1)
    
    # Drop unnecessary rows
    rows_to_drop = df[(df['carpet_area'].isnull()) & (df['bulit_area'].isnull()) & (df['super_bulit_area'].isnull())].index
    cleaned_data.drop(rows_to_drop, inplace=True)
    return cleaned_data


def load_luxury_facility_scores(lux_scores_path):
    # Load the JSON file
    with open(lux_scores_path, 'r') as file:
        luxury_facility_scores = json.load(file)
    print("Luxury facility scores loaded successfully.")
    return luxury_facility_scores


def facility_to_lux_score(facility_column, lux_scores_path=None):
    try:
        # Convert the string representation of lists to actual lists
        facility_list = facility_column.apply(
            lambda x: ast.literal_eval(x) if pd.notnull(x) and isinstance(x, str) and x.startswith('[') else []
        )
        
        # Use MultiLabelBinarizer to convert the features list into a binary matrix
        mlb = MultiLabelBinarizer()
        features_binary_matrix = mlb.fit_transform(facility_list)
        
        # Convert the binary matrix into a DataFrame
        features_binary_df = pd.DataFrame(features_binary_matrix, columns=mlb.classes_)
        
        # Load luxury facility scores if not provided
  
        luxury_facility_scores = load_luxury_facility_scores(lux_scores_path)
 
        
        # Get the intersection of available features and luxury score keys
        available_features = set(features_binary_df.columns).intersection(set(luxury_facility_scores.keys()))
        
        # Calculate luxury score by multiplying binary features with their scores
        luxury_score = features_binary_df[list(available_features)].multiply(
            [luxury_facility_scores[feature] for feature in available_features]
        ).sum(axis=1)
        
        return luxury_score
        
    except Exception as e:
        print(f"Error calculating luxury facility scores: {e}")

def categorize_luxury(score):
    if 0 <= score < 50:
        return 'low'
    elif 50 <= score < 150:
        return 'medium'
    else:
        return 'high'



if __name__ == "__main__":
    try:
        # root path
        root_path = Path(__file__).parent.parent.parent

        # data save directory
        cleaned_data_save_dir = root_path / "data" / "cleaned"
        # make directory if not exits
        cleaned_data_save_dir.mkdir(exist_ok=True, parents=True)

        # cleaned data file name
        cleaned_data_filename = "appartment_cleaned.csv"
        # data save path
        cleaned_data_save_path = cleaned_data_save_dir / cleaned_data_filename

        # data load path
        data_load_path = root_path / "data" / "raw" / "appartment.csv"

        # JSON file path
        lux_scores_path = root_path / "data" / "raw" / "lux_scores.json"
        
        # Main data processing flow
        df = load_data(data_load_path)
        cleaned_df = clean_data(df)
        
        # Calculate luxury scores
        cleaned_df['luxury_facility_scores'] = facility_to_lux_score(cleaned_df['facility'], lux_scores_path)

        cleaned_df['luxury_category'] = cleaned_df['luxury_facility_scores'].apply(categorize_luxury)
        
        # Save cleaned data
        cleaned_df.to_csv(cleaned_data_save_path, index=False)
        print(f"Cleaned data saved to {cleaned_data_save_path}")

    except Exception as e:
        print(f"An error occurred in the data cleaning script: {e}")
        sys.exit(1)