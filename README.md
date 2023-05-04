# Bike Sharing Prediction and Operation

## DESCRIPTION:

The product is deployed by Python, with the following packages:

Pandas and Numpy: The latest version of pandas and numpy is used for preprocessing data, assisting to build machine learning models, and the calculation for rebalancing strategy.  
Keras: Keras is a deep learning Python library to deploy artificial neural networks. This package supports our experiment for LSTM bike usage prediction.  
Scikit-learn: Scikit-learn is a machine learning Python library. This package supports our experiment for machine learning bike usage prediction.  
Plotly: Plotly is a graphing library which supports our visualization, such as the heatmap. It is also the foundation for Streamlit to build the web app.  
Streamlit: From its introduction page, “Streamlit is an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science.” It lessens the effort to program all the JavaScript details and allows us to focus more on the analysis.  
Streamlit_plotly_events: This is an add-on for Streamlit based on Plotly, which enables the “click” event interaction.

## INSTALLATION:

Install all mentioned Python packages above.

Data Preprocessing (Reference Only, No need for demo):  
Download Citi Bike data from https://ride.citibikenyc.com/system-data  
Download weather data from http://www.ncdc.noaa.gov/cdo-web/  
Download COVID data from https://github.com/nychealth/coronavirus-data  
Run /CODE/Preprocess (Reference Only)/preprocess_citibike.ipynb to preprocess Citi Bike data.  
Run /CODE/Preprocess (Reference Only)/dataset_join.ipynb to merge preprocessed Citi Bike data, weather data and COVID data. Output “data.csv”.  
Run /CODE/Preprocess (Reference Only)/heatmap.ipynb for heatmap visualization. Output “heatmap.csv”.  

Analysis (Reference Only, No need for demo):  
Run /CODE/Analysis (Reference Only)/lstm.py to get LSTM prediction. Output “LSTM.csv”  
Run /CODE/Analysis (Reference Only)/location-based_prediction.ipynb to get ML prediction. Output “pickup_dropoff_pred.csv”.
Run /CODE/Analysis (Reference Only)/rebalancing.py to get rebalancing results based on LSTM prediction. Output “rebalancing0.csv” and “rebalancing1.csv” for before 12PM and after 12PM.

Demo preparation:
Download /CODE folder.

## EXECUTION:

Open a Python command environment and change directory to /CODE

Run “streamlit run main.py” command.

## Features:
A heatmap on the left for selected month’s Citi Bike usage summing pickup and dropoff for all days. Details will be shown when hovering the mouse on the station. A selection dropdown to interact with the heatmap.  
Click on the station will update the ML prediction charts on the top part on the right, which will show the prediction for that station for that month.  
Scroll down on the right, a LSTM prediction will be shown for future usage prediction for the clicked-on station. Since the latest data is until 9/30/2021, the prediction is for 10/1/2021.  
Bottom right is the suggestion for rebalancing the bikes for the clicked-on station, based on the LSTM prediction and nearest distance between stations.
