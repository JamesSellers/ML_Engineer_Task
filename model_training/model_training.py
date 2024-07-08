"""
model_training.py

This file contains the following functions:
parameter_search: for a given training and test set, perform cross validation on the model.
                    The resulting parameters will be saved to 'parameters.json', and if available used to train the model in future.
train_model: for a given training set, fit the model and save the results to 'config/model.joblib'
evaluate_model:
"""

__date__ = "2024-07-08"
__author__ = "James Sellers"


# %% --------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import numpy as np
from scipy import stats
import json
import os

import xgboost as xgb
import joblib
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    log_loss,
)

# %% --------------------------------------------------------------------------
# Set Random State
# -----------------------------------------------------------------------------
rng = np.random.RandomState(1889)

# %% --------------------------------------------------------------------------
# Defining our functions
# -----------------------------------------------------------------------------
def parameter_search(X_train, X_test, y_train, y_test):
    """
    For a given training set, perform cross validation and return the best parameters. 
    Save these also to file, where they can be accessed in future.
    """
    parameter_gridSearch = RandomizedSearchCV(
        estimator=xgb.XGBClassifier(
            objective="binary:logistic",
            eval_metric=["auc", "rmse", "logloss"],
            early_stopping_rounds=15,
            enable_categorical=True,
        ),
        param_distributions={
            "n_estimators": stats.randint(50, 500),
            "learning_rate": stats.uniform(0.01, 0.75),
            "subsample": stats.uniform(0.25, 0.75),
            "max_depth": stats.randint(1, 8),
            "colsample_bytree": stats.uniform(0.1, 0.75),
            "min_child_weight": [1, 3, 5, 7, 9],
        },
        cv=5,
        n_iter=100,
        verbose=False,
        scoring="roc_auc",
    )

    parameter_gridSearch.fit(
        X_train, y_train, eval_set=[(X_test, y_test)], verbose=True
    )
    best_params = parameter_gridSearch.best_params_
    with open("config/parameters.json", "w") as f:
        json.dump(best_params, f)

    return best_params


def train_model(X_train, y_train):
    if os.path.isfile("config/parameters.json") and os.access(
        "config/parameters.json", os.R_OK
    ):
        with open("config/parameters.json", "r") as f:
            best_params = json.load(f)
        model = xgb.XGBClassifier(
            objective="binary:logistic", enable_categorical=True, **best_params
        )
    else:
        model = xgb.XGBClassifier(objective="binary:logistic", enable_categorical=True)

    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    y_pred_proba = model.predict(X_test)
    y_pred = (y_pred_proba > 0.5).astype(int)

    metrics = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1 Score": f1_score(y_test, y_pred),
        "ROC AUC Score": roc_auc_score(y_test, y_pred_proba),
        "Log Loss": log_loss(y_test, y_pred_proba),
    }
    return metrics

def save_model(model):
    joblib.dump(model, "config/model.joblib")
    return("Model successfuly saved")
    
