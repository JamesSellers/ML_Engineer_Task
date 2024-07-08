"""
main.py

This serves as the main file for running the machine learning app.
We connect to both data_preprocessing.py and model_training.py to access the required functions

We create the following endpoint:
    \predict - where we can issue JSON files and generate the predicted claim_status.

We create allow also arguments to be parsed which will retrain the model, including the option to cross validate.
    Use --train to retrain the model using existing CV parameters, or the default
    Use --cv to redo the cross validation, and save the best parameters
"""

__date__ = "2024-07-07"
__author__ = "James Sellers"


# %% --------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import numpy as np
import pandas as pd

from data_preprocessing import load_data, process_data, split_data
from model_training import train_model, evaluate_model, parameter_search

import joblib
from flask import Flask, request, jsonify
import argparse

# %% --------------------------------------------------------------------------
# Set Random State
# -----------------------------------------------------------------------------
rng = np.random.RandomState(123)

# %% --------------------------------------------------------------------------
# Setting up additional arguments that can be parsed when we want to train the model
# -----------------------------------------------------------------------------

def parse_args():
    """
    This will allow us to add optional arguments, so that we can customise what this main files does when run
    """
    parser = argparse.ArgumentParser(description="Run main or specific functions based on provided arguments.")
    parser.add_argument('--t', action='store_true', help="Train the model using existing/default parameters")
    parser.add_argument('--cv', action='store_true', help="""Perform cross validation and update the saved parameters""")
    return parser.parse_args()
                        
# %% --------------------------------------------------------------------------
# Training the model, or creating the required endpoint
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    # Check for parsed arugments
    args = parse_args()

    # Train the model if --t has been passed
    if args.t:
            print("Retraining the model")

            # Load and preprocess data
            data = load_data()
            processed_data = process_data(data)

            # Split the data and fit the model
            X_train, X_test, y_train, y_test = split_data(processed_data)
            model = train_model(X_train, y_train)

            # Evaluate the model and return the results
            evaluation_metrics = evaluate_model(model, X_test, y_test)
            print(evaluation_metrics)
    
    # Perform cross validation if --cv has been passed
    elif args.cv:
            print("Performing cross validation and updating the best parameters")

            # Load and preprocess data
            data = load_data()
            processed_data = process_data(data)

            # Split the data and perform parameter search
            X_train, X_test, y_train, y_test = split_data(processed_data)
            parameter_search(X_train, X_test, y_train, y_test)
            print(parameter_search)
    
    # Host the application if neither arguments have been passed
    else:
        app = Flask(__name__)

        @app.route("/")
        def home():
            """
            Creating a basic landing page for the application
            """
            return """Welcome to the Insurance Claim Predictor. 
                        To predict claim status, send your claim information as a JSON to the /predict endpoint \n
                        To retrain the model, you can use the /train endpoint \n
                            - send {"action" : "train"} to train the model with existing/default parameters \n
                            - send {"action" : "train_cv"} to train using cross validation \n
                                this will take longer, but will save the best results - which will be used by default in the future."""

        @app.route("/predict", methods=["POST"])
        def predict():
            """
            Using the saved model, predict claim_status for an inputted JSON
            """
            
            # Check that a model exists, if not raise an error
            try:
                model = joblib.load("config/model.joblib")

            except:
                raise (
                    "Failed to load model, check that a model has been trained previously"
                )
            
            # Collect the data from the endpoint, assume data is JSON
            data = request.get_json()

            # Convert input data to DataFrame
            input_df = pd.DataFrame([data])

            # Process the input json (set the required columns to 'categories')
            processed_input = process_data(input_df)

            # Predict and return claim_status
            prediction = model.predict(processed_input)
            return jsonify({"prediction": prediction.tolist()})

        # Host the app
        app.run(host="0.0.0.0", port=80, debug=True)
