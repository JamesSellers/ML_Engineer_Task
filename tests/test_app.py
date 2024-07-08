import pytest
import json
import random
from model_training.data_preprocessing import collect_from_database
import requests

# Currently hosting is done locally, so GitHub will not get a result from this
def test_predict():
    """Test the prediction endpoint."""

    sample_data = collect_from_database("query")
    index = random.randint(0,5000)

    json_str = sample_data.drop(columns = "claim_status").loc[index].to_json()
    print(f"True claim status is {sample_data.loc[index]["claim_status"]}")

    json_obj = json.loads(json_str)

    # Define the URL of the Flask endpoint
    url = 'http://localhost:80/predict'

    response = requests.post(url, json=json_obj)

    assert response.status_code == 200
    response_json = response.json()
    assert 'prediction' in response_json
    assert response.json()["prediction"][0] in [0,1]
