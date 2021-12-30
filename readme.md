# Engine Performance

# Overview
This project analyzes scraped engine performance data from COBB Tuning's public dyno run database. The goal is to use keywords in the 'Specs' column to determine what factors influence a car's horsepower, then use regression to predict the horsepower of a car given its year, make, model, boost, and any relevant keywords.

# The Data
Here is the dataset: https://www.kaggle.com/paxtonjacob/cobb-tuning-dyno-data

I scraped this data from the dyno database at https://dyno.cobbtuning.com and uploaded it to Kaggle in two files:
- Dyno data
    * Engine RPM and the horsepower, torque, air-fuel ratio, and boost at that RPM
- Car information for the run
    * Date, car's year make and model, name of driver, and information about the car's setup

# Objectives
From a practical perspective, this project should do two things:
1. Determine which factors increase max horsepower for any given car
2. Predict expected horsepower accurately given some information about the car

# Plan
Based on our objectives, I will lay out what needs to be done.

## 1. Determine which factors increase horsepower the most
To determine which parts packages and setups increase horsepower overall, we need to do the following things:
1. Limit cars to one overall make and model with same horsepower number
2. Create new version of car_info df for single make+model+horsepower combination
3. Get the stock performance of the single combination
4. Create features for parts, fuel, and more based on 'specs' values
    * Simplify dyno run data to max horsepower, max torque, and max boost
    * Append run's max horsepower, torque, and boost to car_info dataframe
    * Append stock max horsepower, torque, and boost to car_info dataframe
5. Use correlation heatmap to visually identify drivers

## 2. Predict expected horsepower accurately given some information about the car
Once we've identified features that drive horsepower, we will build regression models to predict the max horsepower and incorporate our best model in a horsepower calculator.
1. Isolate target column max_hp
2. Scale and encode features
3. Get baseline RMSE and R2
4. Build models using scaled and encoded data
5. Evaluate RMSE and R2 for each model on validate
    * Show results in a plot
6. Choose best-performing algorithm and hyperparameters
7. Evaluate RMSE and R2 for best model on test
8. Build horsepower calculator using best model

# Work Done So Far
- Scraped data from dyno.cobbtuning.com
- Organized data into two files
- Uploaded the two files to Kaggle
- Cleaned the data while preserving shared key between the two files
- Split the data while preserving shared key
- Moved acquisition and cleaning work to wrangle.py
- Choose Subaru Impreza WRX STI as our single engineering baseline