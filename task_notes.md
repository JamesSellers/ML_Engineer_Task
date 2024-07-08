# Notes #

## File Structure ##

There are 3 main files that are used in this project:
 - app.py
    - Creating a docker container for app.py will host the endpoint required to make predictions with this model.
    - Predictions can be made to the /predict endpoint, provided they contain the correct information
 - train.py
    - Running train.py will retrain the model and save the updated model in the config folder.
    - When we load the prediction endpoint it will use the model saved in config.
 - cross_validate.py
    - Running cross_validate.py will rerun cross_validation and save the updated parameters in the config folder.
    - These parameters will be used the next time the model is trained.

These files take functions from two further files:
    - data_preprocessing.py: where data is loaded and preprocessed
    - model_training.py: where model training and evaluation takes place

## Loading the Model Locally ##

To load locally, simply build and run a docker container in the main directory.\
When running the app, make sure to open port 80.\
We can then post jsons to the /predict endpoint to receive back the model's prediction.

The file 'endpoint_testing.ipynb' can be used to create some sample data and send this post request.

## Testing ##

Testing has been set up in the /tests folder\
- This is fairly minimal currently, with just a handful of tests\
- More tests should be made for all aspects of the model including: 
    - Ingestion
    - Preprocessing
    - Training
    - Evaluation
    - Prediction

### Testing Locally ###

To test locally, use 'poetry run pytest --cov= tests/'\
One test is set to fail, this is "tests/test_model.py::test_model_evaluation"

### Github Automated Testing ###

A GitHub workflow has been set up such that these tests will be run each time a file is pushed to the main branch.
Current the 'prediction' test uses the local endpoint. This will work when tests are performed locally, but will fail in GitHub.

# Next Steps #

## Data Ingestion ##

Currently we are only using dummy data, we want to confirm that the model can work with real data.

Within \config I have included a .toml file to store credentials. Certain secret credentials should be split into a more secure format, but this will serve as the storage place to retrieve most credentials.
I have included also the file 'utils.py' this currently only includes one function, which allows us to retrieve these credentials.

Within 'data_preprocessing.py' there is a function 'load_data'. Here I have started outlining the code that could be used to retrieve data and transform it into the correct format. This is for an AWS Relation Database, but similar fetching code could be used for Snowflake, Azure, etc.


## Automated Retraining ##

Within the brief it is stated that we want the model to incorporate new data each month. This would mean that the we would need to retrain the model at least monthly. \
This can be easily achieved by running 'train.py', with the optional choice of reconducting cross validation with 'cross_validate.py'.

Before updating the model used in live predictions, we should have extensive automated testing confirm that everything is still working correctly, and that performance has not significantly deviated. \
If these tests fail, the model should not update and the relevant individuals should be contacted.

## Making the endpoint discoverable over a cloud resource ##

Using this set-up, we should be able to load our endpoint into a cloud resource such as Azure or AWS.

For Azure, we would complete the following steps:
- Create a resource group. This is a container which can hold related resources.
- Create an Azure Container Registery (ACR). This will store our docker image.
- Build the Docker image and push it to our ACR.
- Create an App Service Plan. This sets up the infrastructure for our app.
- Create and Configure the Web App. Need to allow our Web App to use ACR.


## Workspace Clean-Up ##

Some elements of this workspace should be cleaned, especially as functionality increases. \
Type hinting should be used to a much larger degree for clarity.

# Specified Questions #

## What are the assumptions you have made for this service and why? ##
- Data is being batch-loaded into our data storage at the end of each day as specified
    - If we are going to retrain the model each month on stored data, this data need to be correctly updated
    - If data does not get updated, retraining the model will serve no use
- Input data is of a consistent format
    - While we have updated the model to replace null values, it has little in the way of managing general data changes
    - For instance if gender is 'male' instead of a binary number, the model will create an error
    - Further tests and error messages should be developed for these situations
    - If the feature set is to change, the model may also encounter issues, especially with categorical columns, which are currently hard coded.

## What considerations are there to ensure the business can leverage this service? ##
- The model will need to meet compliance and reliability standards
- We will need to confirm claim data can be input in large batches to avoid having to send post requests for claims individually.
- Endpoint uptime must be very consistent, likely available at all times during work hours.
- Endpoint model must stay accurate and reliable, if the model experiences drift or becomes hard to use it will lose usefulness.
- Requests must be able to input in a simple way, we do not want only those with more advanced technical knowledge to leverage it. 
- Evaluation should be performed and logged continously, such that we can highlight positive results to key stakeholders.
- We will also want model logging to be saved, both during testing and post requests made to the live model.
- Data security and privacy should be paramount, with thorough and frequent checks that all data is being handled correctly.
 
## Which traditional teams within the business would you need to talk to and why? ##
- Data Engineering / IT
    - We will need to ensure that we can collect the data we need from where it is currently stored, and that whatever keys we are using to access this do not need constant manual updating.
- Data Science / ML
    - The team in which this will be made and deployed, will need to confirm what work has already been done, and what resources are available.
- Underwriting
    - It seems that underwriters will be the primary team that will use this tool, and therefore we should target their input on how they would like the model to operate.
    - We want to make sure what we make integrates will into existing business practices.
- Compliance
    - Want to ensure that the model meets regulatory standards; there may be concerns in PII leakage, or bias towards certain groups.

## What is in and out of scope for your responsibility? ##

# In Scope #
- Data Ingestion
    - While not handling the entire data ingestion pipeline, we will need to be able to access where claim data is stored to train our model.
- Data Preprocessing
    - The data we receive should be of a consistent format, however some preprocessing can still be done.
    - This may include the handling of null values where they appear.
    - It also includes setting the appropriate columns as 'categorical' for the model to interprate.
- Model Training
    - We will manage the model itself being trained.
    - We will also have the model retrained each month, as requested.
- CI / CD Pipeline setup
    - We will create the systems to continously work on this tool without interrupting other business workflow.
    - Tests will be done manually and automatically to ensure the models continues to work.
    - Model performance will be watched and actions will be taken if we begin to experience model drift.
- Endpoint Deployment
    - We will manage an endpoint being deployed for this service
    - We will ensure endpoint uptime
- Model Evaluation
    - All model results will be logged
    - This will serve useful to show model performance, and confirm model compliance.

# Out of Scope #
- Extensive Hyperparamater Testing
    - Cross Validation takes place, but we are not extensively checking for the best results.
- Performing continous EDA
    - Some EDA will be done during model development, but once an endpoint is created we will not closely monitor items like feature correlation.
- Building a complete full production-ready UI
    - An endpoint can be created, but currently we are not looking to develop an entire user interface for this single function.

# Workspace Notes #

This project has been created in WSL 2, allowing for Linux to be operated within Windows.

In lieu of pip, I have opted for poetry, my prefered choice for dependency management.
