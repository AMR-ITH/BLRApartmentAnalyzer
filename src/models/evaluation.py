import pandas as pd
import joblib
import logging
import mlflow
import dagshub
from pathlib import Path
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn import set_config
import json
import sys
import os

def dagshub_init():
    dagshub.init(repo_owner='AMR-ITH', repo_name='RealEstateInsights', mlflow=True)
    # set the tracking server
    mlflow.set_tracking_uri("https://dagshub.com/AMR-ITH/RealEstateInsights.mlflow")
    # mlflow experiment name
    mlflow.set_experiment("DVC-Pipeline")


def load_data(data_path: Path) -> pd.DataFrame:
    try:
        df = pd.read_csv(data_path)
        print(f"Data loaded successfully from {data_path}")
        return df
    except Exception as e:
        print(f"Failed to load data from {data_path}: {e}")
        sys.exit(1)  # Exit if data loading fails
    
def load_model(model_path: Path):
    try:
        if not os.path.exists(model_path):
            print(f"ERROR: Model file does not exist at {model_path}")
            sys.exit(1)
            
        model = joblib.load(model_path)
        print(f"Model loaded successfully from {model_path}")
        return model
    except Exception as e:
        print(f"ERROR: Failed to load model from {model_path}: {e}")
        sys.exit(1)  # Exit if model loading fails

def train_model(model, X_train: pd.DataFrame, y_train):
    try:
        # fit on the data
        model.fit(X_train, y_train)
        print("Model trained successfully")
        return model
    except Exception as e:
        print(f"Failed to train model: {e}")
        return None

def save_model_info(save_json_path, run_id, artifact_path, model_name):
    info_dict = {
        "run_id": run_id,
        "artifact_path": artifact_path,
        "model_name": model_name
    }
    with open(save_json_path, 'w') as f:
        json.dump(info_dict, f, indent=4)
    print(f"Model info saved to {save_json_path}")

if __name__ == "__main__":

    # Define the root path
    root_path = Path(__file__).parent.parent.parent
    print(f"Root path: {root_path}")

    # train data load path 
    train_data_path = root_path / "data" / "processed" / "train_trans.csv"
    test_data_path = root_path / "data" / "processed" / "test_trans.csv"

    # model path
    model_path = root_path / "models" / "model.joblib"
    print(f"Looking for model at: {model_path}")
    
    # Check if model file exists
    if not os.path.exists(model_path):
        print(f"ERROR: Model file does not exist at {model_path}")
        sys.exit(1)

    # Load the training data
    train_df = load_data(train_data_path)
    test_df = load_data(test_data_path)

    # split the train and test data 
    X_train, y_train = train_df.drop(columns=['price_value']), train_df['price_value']
    X_test, y_test = test_df.drop(columns=['price_value']), test_df['price_value']

    # load the model with better error handling
    model = load_model(model_path)
    
    # Verify model is not None before proceeding
    if model is None:
        print("ERROR: Model failed to load properly. Exiting.")
        sys.exit(1)

    # get the train and test predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # calculate the train and test mae
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    print(f"Train MAE: {train_mae}, Test MAE: {test_mae}")

    # calculate the r2 scores
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    print(f"Train R2: {train_r2}, Test R2: {test_r2}")

    # calculate cross val scores
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="neg_mean_absolute_error", n_jobs=-1)
    print(f"Cross-validation scores: {cv_scores}")
    # mean cross val error
    mean_cv_error = -(cv_scores.mean())
    print(f"Mean cross-validation error: {mean_cv_error}")

    # dagshub init
    try:
        dagshub_init()
    except Exception as e:
        print(f"Warning: DagsHub initialization failed: {e}")
        print("Continuing without MLflow tracking...")
        sys.exit(0)  # Exit gracefully without MLflow tracking

    with mlflow.start_run() as run:
        # set tags
        mlflow.set_tag("model", "Real Estate Insights")

        # log parameters
        mlflow.log_params(model.get_params())

        # log metrics
        mlflow.log_metric("train_mae", train_mae)
        mlflow.log_metric("test_mae", test_mae)
        mlflow.log_metric("train_r2", train_r2)
        mlflow.log_metric("test_r2", test_r2)
        mlflow.log_metric("cv_score", mean_cv_error)
        mlflow.log_metrics({f"CV_{num}": -score for num, score in enumerate(cv_scores)})

        # mlflow dataset input datatype
        train_data_input = mlflow.data.from_pandas(train_df, targets="price_value")
        test_data_input = mlflow.data.from_pandas(test_df, targets="price_value")

        # log datasets
        mlflow.log_input(context="training", dataset=train_data_input)
        mlflow.log_input(context="validation", dataset=test_data_input)

        # model signature
        model_signature = mlflow.models.infer_signature(
            model_input=X_train.sample(20, random_state=42),
            model_output=model.predict(X_train.sample(20, random_state=42))
        )

        # log the final model
        mlflow.sklearn.log_model(model, "real_estate_insights", signature=model_signature)

        # get the current run artifact uri
        artifact_uri = mlflow.get_artifact_uri()

        # get the run id
        run_id = run.info.run_id
        model_name = "real_estate_insights"

        # save the model info
        save_json_path = root_path / "run_information.json"
        save_model_info(save_json_path=save_json_path,
                        run_id=run_id,
                        artifact_path=artifact_uri,
                        model_name=model_name)
        print(f"Model info saved to {save_json_path}")