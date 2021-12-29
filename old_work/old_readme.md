# Engine Performance

# Overview
Collect engine performance data from disparate sources. Create features based on displacement and parts. Predict horsepower using regression. 

# Kaggle Upload Link
https://www.kaggle.com/paxtonjacob/cobb-tuning-dyno-data

# Potential Leads
0. OEM data, specifically camshaft tests and otherwise for engines
1. https://apidocs.marketcheck.com - Excellent resource for OEM car data including engines, requires an account and API key, 20k requests and 30 days free accessx
2. https://dyno.cobbtuning.com - Manually scrape dyno tests by car
3. https://tuning-shop.com/downloads/ - A few PDFs with relevant car information
4. https://www.dyno-chiptuningfiles.com/tuning-file/ - Search by make/model/engine, get engine specifications and BHP/Torque, see improvements before and after chiptuning
5. Google Images - search Google images for more potential leads in case what you've found so far isn't sufficient

# Decision Points
1. Decided to use Cobb tuning dyno data for initial analysis
2. Chose 2013 Subaru Impreza WRX STI for initial analysis
    * It had a lot of different owners and dyno runs
3. Installed tabula-py through pip to read the Cobb tuning PDFs
4. Chose to convert PDFs programatically
5. Stored programatic conversion functions to prepare.py
6. Downloaded all 2013 Subaru Impreza WRX STI dyno runs to directory
7. Converted PDFs to CSVs
8. Added specified drivetrain characteristics to analysis.ipynb
9. Chose to focus on max horsepower
10. Revisited programmatic web scraping, found solution
11. Uploaded *all* dyno runs to Kaggle

# Work to do soon
## Data Acquisition and Preparation
- Project on hold for the meantime; data uploaded to Kaggle, next steps are to analyze the data