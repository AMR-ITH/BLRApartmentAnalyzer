import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import logging
import sys
import ast

def load_data(file_path: Path) -> pd.DataFrame:
    try:
        print(f"Loading data from {file_path}")
        df = pd.read_csv(file_path)
        print(f"Loaded data with shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        raise

def impute_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    # Step 1: Calculate ratios from fully available rows
    all_present_df = df[
        df['super_bulit_area'].notnull() &
        df['bulit_area'].notnull() &
        df['carpet_area'].notnull()
    ]
    
    super_to_built_up_ratio = (
        all_present_df['super_bulit_area'] / all_present_df['bulit_area']
    ).mean()
    
    carpet_to_built_up_ratio = (
        all_present_df['carpet_area'] / all_present_df['bulit_area']
    ).mean()

    # Step 2: Case: super and carpet present, built up missing
    sc_df = df[
        df['super_bulit_area'].notnull() &
        df['bulit_area'].isnull() &
        df['carpet_area'].notnull()
    ]
    sc_df.loc[:, 'bulit_area'] = round((
        sc_df['super_bulit_area'] / super_to_built_up_ratio +
        sc_df['carpet_area'] / carpet_to_built_up_ratio
    ) / 2)

    df.update(sc_df)

    # Step 3: Case: only super present
    s_df = df[
        df['super_bulit_area'].notnull() &
        df['bulit_area'].isnull() &
        df['carpet_area'].isnull()
    ]
    s_df.loc[:, 'bulit_area'] = round(
        s_df['super_bulit_area'] / super_to_built_up_ratio
    )

    df.update(s_df)

    # Step 4: Case: only carpet present
    c_df = df[
        df['super_bulit_area'].isnull() &
        df['bulit_area'].isnull() &
        df['carpet_area'].notnull()
    ]
    c_df.loc[:, 'bulit_area'] = round(
        c_df['carpet_area'] / carpet_to_built_up_ratio
    )

    df.update(c_df)

    # Step 5: Drop cools not needed
    df.dropna(subset=['apartment_name', 'appartment_loc', 'price_value'], inplace=True)

    # Step 6: Outlier removal
    df = df[~(df['price_value'] > 14)]
    df = df[~((df['price_value'] > 0.7) & (df['bulit_area'] < 900))]
    df = df[~((df['price_value'] < 4) & (df['bulit_area'] > 4200))]

    return df


if __name__ == "__main__":
    try:
        # root path
        root_path = Path(__file__).parent.parent.parent

        # data directory
        cleaned_data_root = root_path / "data" / "cleaned"
        cleaned_data_filename = "appartment_cleaned.csv"
        # data save path
        cleaned_data_save_path = cleaned_data_root / cleaned_data_filename


        # save the cleaned data in interim directory
        cleaned_data_save_dir = root_path / "data" / "interim"
        # make directory if not exits
        cleaned_data_save_dir.mkdir(exist_ok=True, parents=True)
        # cleaned data file name
        cleaned_data_filename = "appartment_cleaned_interim.csv"
        


        # load the data
        df = load_data(cleaned_data_save_path)
        # impute missing values
        cleaned_data = impute_missing_values(df)
        # save the cleaned data
        cleaned_data.to_csv(cleaned_data_save_dir / cleaned_data_filename, index=False)
        print(f"Cleaned data saved to {cleaned_data_save_dir / cleaned_data_filename}")



    except Exception as e:
        print(f"An error occurred in the data cleaning script: {e}")
        sys.exit(1)