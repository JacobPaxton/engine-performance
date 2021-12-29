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

# Work Done So Far
- Scraped data from dyno.cobbtuning.com
- Organized data into two files
- Uploaded the two files to Kaggle
- Cleaned the data while preserving shared key between the two files
- Split the data while preserving shared key
- Moved acquisition and cleaning work to wrangle.py