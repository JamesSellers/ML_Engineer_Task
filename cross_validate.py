"""
Cross Validate

When run, this script will perform cross validation on the XGBoost model.
The parameters will then be saved in config/parameters.json
"""

__date__ = "2024-07-08"
__author__ = "James Sellers"



# %% --------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import numpy as np

from model_training.data_preprocessing import load_data, process_data, split_data
from model_training.model_training import parameter_search

# %% --------------------------------------------------------------------------
# Set Random State
# -----------------------------------------------------------------------------
rng = np.random.RandomState(1889)

# %% --------------------------------------------------------------------------
# Running Cross Validation
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    print("Performing cross validation and updating the best parameters")

    # Load and preprocess data
    data = load_data()
    processed_data = process_data(data)

    # Split the data and perform parameter search
    X_train, X_test, y_train, y_test = split_data(processed_data)
    parameter_search(X_train, X_test, y_train, y_test)
    print(parameter_search)