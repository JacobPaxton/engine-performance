# Engine Performance

# Overview
Collect engine performance data from disparate sources. Create features based on displacement and parts. Predict horsepower using regression. 

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

# Work to do soon
## Data Acquisition and Preparation
- Need to handle/add other data portions (car specs/modifications) that are outside tabula.read_pdf purview
- Need to download all PDFs for the 2013 Subaru model I chose
- Need to import all PDFs
- Need to concat everything together somehow (logic not yet determined)
- Need to output data to a CSV
- Need to upload data to Kaggle and Google Docs