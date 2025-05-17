import pandas as pd
import logging
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    OneHotEncoder,
    MinMaxScaler,
    OrdinalEncoder)
import joblib
from sklearn import set_config
import sys
from sklearn.model_selection import train_test_split
import yaml


def load_data(file_path: Path) -> pd.DataFrame:
    try:
        print(f"Loading data from {file_path}")
        df = pd.read_csv(file_path)
        print(f"Loaded data with shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")

def drop_cols(df: pd.DataFrame) -> pd.DataFrame:
    df =df.drop(columns=['carpet_area','super_bulit_area','nearbylocation','facility','apartment_name','appartment_loc','luxury_facility_scores'])
    return df

def preprocessor_pipeline() -> ColumnTransformer:
    num_cols = ['bulit_area']
    nomial_cols = ['zone']
    ordinal_cols = ['construction_status','bhk_type','luxury_category']

    bhk_type_order = ['1','2','3','4','5','6','7','8','9','10']
    construction_status_order = ['New Property','Under Construction', 'Relatively New', 'Moderatly Old', 'Old','undefined']
    luxury_facility_scores_order = ['low','medium','high']

    # build a preprocessor

    prepocessor = ColumnTransformer(transformers=[
        ("scale", MinMaxScaler(), num_cols),
            ("nominal_encode", OneHotEncoder(handle_unknown="ignore",sparse_output=False), nomial_cols),
        ("ordinal_encode", OrdinalEncoder(categories=[construction_status_order,bhk_type_order,luxury_facility_scores_order]), ordinal_cols)
    ],remainder="passthrough",n_jobs=-1,force_int_remainder_cols=False,verbose_feature_names_out=False)

    prepocessor.set_output(transform="pandas")
    return prepocessor

def save_transformer(transformer: ColumnTransformer, save_dir: Path, transformer_name: str):
    try:
        file_path = save_dir / transformer_name
        joblib.dump(transformer, file_path)
        print("Transformer saved successfully")
    except Exception as e:
        print(f"Failed to save transformer: {e}")

def load_params(params_path: Path) -> dict:
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
            print(f"Parameters loaded successfully from {params_path}")
        return params
    except Exception as e:
        print(f"Failed to load parameters from {params_path}: {e}")
        return {}

if __name__ == "__main__":
    try:
        # root path
        root_path = Path(__file__).parent.parent.parent

        # data path for inter
        data_path = root_path / "data" / "interim"
        file_name = "appartment_cleaned_interim.csv"
        # folder path
        folder_path = data_path / file_name
        # load the data
        df = load_data(folder_path)
        print(df.columns)
        

        necessary_df = drop_cols(df)

        # train test split
        X = necessary_df.drop(columns=['price_value'])
        y = necessary_df['price_value']

        # load parameters
        params_path = root_path / "params.yaml"
        params = load_params(params_path)

        # model params
        test_size = params["Data_Preparation"]["test_size"]
        random_state = params["Data_Preparation"]["random_state"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

        # preprocessor object
        preprocessor = preprocessor_pipeline()
        # fit the preprocessor
        X_train_trans = preprocessor.fit_transform(X_train)
        X_test_trans = preprocessor.transform(X_test)
        # join X and y
        df_train_trans = pd.concat([X_train_trans, y_train], axis=1)
        df_test_trans = pd.concat([X_test_trans, y_test], axis=1)


        # save the preprocessed data
        saved_data_path = root_path / "data" / "processed"
        saved_data_path.mkdir(exist_ok=True, parents=True)
        df_train_trans.to_csv(saved_data_path / "train_trans.csv", index=False)
        df_test_trans.to_csv(saved_data_path / "test_trans.csv", index=False)


                # save the preprocessor to location
        transformer_filename = "preprocessor.joblib"
        transformer_save_dir = root_path / "models"
        transformer_save_dir.mkdir(exist_ok=True)
        save_transformer(transformer=preprocessor,
                         save_dir=transformer_save_dir,
                         transformer_name=transformer_filename)

    except Exception as e:
        print(f"An error occurred in the data cleaning script: {e}")
        sys.exit(1)