import pandas as pd
import yaml
import joblib
import logging
from sklearn.ensemble import RandomForestRegressor
from pathlib import Path
import sys



def load_params(params_path: Path) -> dict:
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
            print(f"Parameters loaded successfully from {params_path}")
        return params
    except Exception as e:
        print(f"Failed to load parameters from {params_path}: {e}")
        return {}

def load_data(data_path: Path) -> pd.DataFrame:
    try:
        df = pd.read_csv(data_path)

       

        print(f"Data loaded successfully from {data_path}")
        return df
    except Exception as e:
        print(f"Failed to load data from {data_path}: {e}")
        return pd.DataFrame()
    
def train_model(model, X_train: pd.DataFrame, y_train):
    try:
        # fit on the data
        model.fit(X_train, y_train)
        print("Model trained successfully")
        return model
    except Exception as e:
        print(f"Failed to train model: {e}")
        return None

def save_model(model: object, save_dir: Path, model_name: str):
    try:
        file_path = save_dir / model_name
        joblib.dump(model, file_path)
        print(f"Model {model_name} saved successfully to {save_dir}")
    except Exception as e:
        print(f"Failed to save model {model_name} to {save_dir}: {e}")


if __name__ == "__main__":

    try:
        # root path
        root_path = Path(__file__).parent.parent.parent
        print(f"Root path: {root_path}")

        # load parameters
        params_path = root_path / "params.yaml"
        params = load_params(params_path)

        # load the preprocessed data
        train_data_path = root_path / "data" / "processed" / "train_trans.csv"

        train_df = load_data(train_data_path)
        

        # split the data into X and y
        X_train, y_train = train_df.drop(columns=['price_value']), train_df['price_value']

        # build the best models
        rf_params = params["Train"]["Random_Forest"]

        best_rf = RandomForestRegressor(**rf_params)

        trained_model = train_model(best_rf, X_train, y_train)

        # model name
        model_filename = "model.joblib"

        # directory to save model
        model_save_dir = root_path / "models"
        model_save_dir.mkdir(exist_ok=True)

        # Save the model
        save_model(trained_model, model_save_dir, model_filename)

        print(f"Model training and saving completed successfully")

    except Exception as e:
        print(f"An error occurred in the model training script: {e}")
        sys.exit(1)
        