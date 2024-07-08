import pytest
import numpy as np
from model_training.model_training import train_model, parameter_search, evaluate_model

def test_model_training():
    """
    Test that the model can correctly train on data and save a model in config
    """
    # Create dummy data
    # Load data into model functions
    # Check that model fits properly
    assert True

def test_model_prediction():
    """
    Test that the model can be used for predictions
    """
    # Load saved model
    # Create dummy data for prediction
    # Test that model can be used for prediction
    assert True

def test_model_evaluation():
    """
    Test models can be evaluated
    Assert False to test what is delivered
    """
    # Load saved model
    # Create available test data
    # Check output of evaluated model

    model_output = {"Accuracy" : 0.5, "F1-Score" : 0.6}
    assert "Recall" in model_output