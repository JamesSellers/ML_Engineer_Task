"""
main.py

This serves as the main file for running the machine learning app.
We connect to both data_preprocessing.py and model_training.py to access the required functions

We create the following endpoint:
    predict - where we can issue JSON files and generate the predicted claim_status.

We create allow also arguments to be parsed which will retrain the model, including the option to cross validate.
    Use --train to retrain the model using existing CV parameters, or the default
    Use --cv to redo the cross validation, and save the best parameters
"""

__date__ = "2024-07-07"
__author__ = "James Sellers"


# %% --------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import pandas as pd

from model_training.data_preprocessing import process_data

import joblib
from flask import Flask, request, jsonify
                        
# %% --------------------------------------------------------------------------
# Training the model, or creating the required endpoint
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    app = Flask(__name__)

    @app.route("/")
    def home():
        """
        Creating a basic landing page for the application
        """
        return """Welcome to the Insurance Claim Predictor. 
                    To predict claim status, send your claim information as a JSON to the /predict endpoint"""


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
    app.run(host="0.0.0.0", port=80, debug=False)
