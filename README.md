# Instructions are as below: #

## Training the model ##

To train the model run "train.py"
This will take the latest data, and retrain the model.
If cross validation parameters exist, then these will be used.
The model will then be saved to config/model.joblib

## Performing Cross-Validation ##

To perform cross validation run "cross_validate.py"
This will take the latest data, and perform cross validation.
The best parameters will be stored to config/parameters.json

## Loading the endpoint ##

To load the endpoint, we run "app.py" as part of a docker container.
