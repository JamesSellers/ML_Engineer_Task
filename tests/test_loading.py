import pytest
import pandas as pd
from model_training.data_preprocessing import collect_from_database, process_data

def test_database_collection():
    """
    Test that we collect our data successfully
    """
    query = "SELECT * FROM DATABASE"
    result = collect_from_database(query)
    assert type(result) == pd.core.frame.DataFrame

def test_process_data():
    """
    Test that columns are correctly becoming categories
    """
    sample_data = collect_from_database("query")

    processed_data = process_data(sample_data)
    assert type(processed_data["income_level"].dtype) == pd.core.dtypes.dtypes.CategoricalDtype