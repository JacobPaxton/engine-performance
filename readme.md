# Engine Performance

![This is an image](https://i.imgur.com/H7sLgNy.png)

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

# Tableau Visualizations
- Boost PSI and horsepower correlate: https://public.tableau.com/app/profile/jacob.paxton/viz/CarsBoostPSICorrelateswithHorsepower/PSIandHP
- Fuel octane and horsepower correlate: https://public.tableau.com/app/profile/jacob.paxton/viz/CarsFuelOctaneCorrelateswithHorsepower/OctaneandHP

# Findings
## 1. As boost PSI is increased, max horsepower increases.
## 2. As fuel octane is increased, max horsepower increases.
## 3. Including the stock hosepower as a feature dramatically increases model performance.
The dataset includes various cars with different stock horsepower. Cars have varying performance at stock and that needs to be controlled-for in our model.
## 4. For unknown reasons, cars with engine computer tuning do not have higher horsepower than cars without it.

# Future Work
1. Use algorithmic clustering techniques to group keywords against changes in horsepower

# Recreate My Work
1. Read this README
2. Download wrangle.py, model.py, and final_notebook.ipynb
3. Run final_notebook.ipynb in a Jupyter notebook Python3 session
4. Execute all cells in final_notebook.ipynb