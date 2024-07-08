"""
Train

When run, this script will retrain the model using the loaded data.
If available, parameters stored in config/parameters.json will be used.
The model will be saved to model.joblib, which can be hosted with app.py
"""

__date__ = "2024-07-08"
__author__ = "James Sellers"



# %% --------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import numpy as np

from model_training.data_preprocessing import load_data, process_data, split_data
from model_training.model_training import train_model, evaluate_model, save_model

# %% --------------------------------------------------------------------------
# Set Random State
# -----------------------------------------------------------------------------
rng = np.random.RandomState(123)

# %% --------------------------------------------------------------------------
# Training the model
# -----------------------------------------------------------------------------

if __name__ == "__main__":

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
    save_model()
