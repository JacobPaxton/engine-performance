import pandas as pd
import re
from sklearn.model_selection import train_test_split

# --------------------- Main Functions --------------------- #

def prep_explore():
    """ 
        Ingest car_info.csv and dyno_runs.csv,
        Clean both files while preserving shared key 'Run',
        Split files into train (50%), validate (30%), and test (20%) splits,
        Return train split of both files.
    """
    # car_info.csv
    info = prep_car_info()

    # dyno_runs.csv
    runs = prep_dyno_runs()

    # feature engineering
    info['has_keyword'] = False
    info = keyword_features(info)

    # split car_info.csv into train (50%), validate (30%), and test (20%)
    info_train, runs_train, _, _, _, _ = split_runs_and_info(info, runs)

    # return only the train split for exploration
    return info_train, runs_train

# --------------------- Assist Functions --------------------- #

def prep_car_info():
    """ 
        Ingest car_info.csv, 
        Drop several hundred runs that we drop when cleaning dyno_runs.csv,
        Drop 'Date' column,
        Move values from 'Car' column into car year, make, and model columns,
        Drop 'AFR' column,
        Convert column names to lowercase,
        Return cleaned data.
    """
    # ingest data
    info = pd.read_csv('car_info.csv')
    # drop runs (around 10% of values) to equalize with dyno_runs cleaning
    drop_list = runs_to_drop()
    info = info[~info.Run.isin(drop_list)].reset_index(drop=True)
    # drop Date column
    info = info.drop(columns='Date')
    # splitting the rest of the string into make and model
    year_make_model = info.Car.str.extract(r'^(.*?)\W(.*?)\W(.*?)$')
    # using the second word as the make
    info['car_make'] = year_make_model[1]
    # using the last portion as the model
    info['car_model'] = year_make_model[0] + ' ' + year_make_model[2]
    # drop redundant Car column
    info = info.drop(columns='Car')
    # convert remaining columns to lowercase
    info = info.rename(columns={'Run':'run',
                         'Name':'name',
                         'Specs':'specs'})
    
    return info

def prep_dyno_runs():
    """         
        Ingest dyno_runs.csv,
        Drop 'AFR' column in dyno_runs.csv,
        Drop rows in dyno_runs.csv with nulls in 'RPM' or 'Boost' columns,
        Convert column names to lowercase,
        Return cleaned data.
    """
    # ingest dyno_runs.csv
    runs = pd.read_csv('dyno_runs.csv', index_col=0)
    # drop AFR column
    runs = runs.drop(columns='AFR')
    # drop remaining rows having nulls in RPM and Boost columns
    runs = runs.dropna().reset_index(drop=True)
    # drop a few runs that had data but incorrect information
    runs = runs[~runs.Run.isin([91, 92, 93, 2491, 2492])]
    # convert column names to lowercase
    runs = runs.rename(columns={'Run':'run', 
                                'RPM':'rpm', 
                                'HP':'hp', 
                                'Torque':'torque', 
                                'Boost':'boost'})

    return runs

def split_runs_and_info(info, runs):
    """ 
        Split car_info into train, validate, and test,
        Store each split's run numbers to separate lists,
        Use lists to split dyno_runs,
        Return all six splits.
    """
    # split car_info.csv into train (50%), validate (30%), and test (20%)
    info_train_validate, info_test = train_test_split(info, test_size=.2, random_state=1)
    info_train, info_validate = train_test_split(info_train_validate, test_size=.375, random_state=1)

    # figure out run numbers in info splits
    run_list_train = info_train.run.tolist()
    run_list_validate = info_validate.run.tolist()
    run_list_test = info_test.run.tolist()
    # use run numbers to split dyno_runs.csv
    runs_train = runs[runs.run.isin(run_list_train)]
    runs_validate = runs[runs.run.isin(run_list_validate)]
    runs_test = runs[runs.run.isin(run_list_test)]

    # return only the train split for exploration
    return info_train, runs_train, info_validate, runs_validate, info_test, runs_test

# --------------------- Feature Engineering --------------------- #

def keyword_features(info):
    """ Create several features for keywords in the 'specs' column, return dataframe """
    # psi
    info = psi(info)
    # octane
    info = octane(info)

    return info

def psi(info):
    """ Add new column for specs including the boost PSI """
    # psi
    info['psi'] = info.specs.str.extract(r'^.*\s(\d+\.*\d*)\s?[Pp][Ss][Ii].*$')
    # programmatic fix for '17.5 Peak PSI' issue
    newthing = info.specs.str.extract(r'^.*\b(\d\d\.\d) Peak PSI.*$')
    indices = newthing[newthing[0].notna()].index
    for ind in indices:
        info.loc[ind, 'psi'] = newthing[0][ind]

    return info

def octane(info):
    """ Add new column for specs including the fuel octane """
    # octane overall capture
    info['octane'] = info.specs.str.extract(r'^.*\b(\d+)[,\s]?\s?[Oo][Cc][Tt].*$')
    # 93 octane fuel
    octane_93_indices = info[info.specs.str.contains(' 93 ')].index
    for ind in octane_93_indices:
        info.loc[ind, 'octane'] = 93
    # 91 octane fuel
    octane_91_indices = info[info.specs.str.contains('ACN91|ANC91|91 CA| 91 ')].index
    for ind in octane_91_indices:
        info.loc[ind, 'octane'] = 91
    # 104 octane fuel
    octane_104_indices = info[info.specs.str.contains('104')].index
    for ind in octane_104_indices:
        info.loc[ind, 'octane'] = 104
    # e85 fuel
    e85_indices = info[info.specs.str.contains('E85|E-85')].index
    for ind in e85_indices:
        info.loc[ind, 'octane'] = 105
    # MS109 fuel
    ms109_indices = info[info.specs.str.contains('MS109')].index
    for ind in ms109_indices:
        info.loc[ind, 'octane'] = 109

    return info

# --------------------- Data-On-Demand Functions --------------------- #

def runs_to_drop():
    """ 
        Return a list of runs dropped when cleaning dyno_runs.csv.
        This list is needed for when we clean car_info.csv.
    """
    run_list = [91, 92, 93, 2491, 2492,
                94, 101, 209, 210, 211, 266, 267, 268, 270, 271, 272, 273, 274, 275, 276, 278, 
                279, 280, 354, 357, 425, 490, 546, 585, 607, 634, 635, 696, 727, 728, 916, 917, 
                980, 1044, 1186, 1236, 1237, 1238, 1239, 1240, 1241, 1242, 1243, 1244, 1245, 1246, 
                1278, 1279, 1280, 1375, 1376, 1405, 1417, 1418, 1419, 1420, 1421, 1422, 1423, 1427, 
                1428, 1429, 1444, 1445, 1448, 1449, 1450, 1460, 1461, 1462, 1463, 1464, 1465, 1466, 
                1467, 1468, 1469, 1612, 1613, 1614, 1641, 1642, 1643, 1661, 1665, 1666, 1694, 1695, 
                1697, 1721, 1722, 1723, 1724, 1725, 1726, 1727, 1728, 1731, 1861, 1862, 1863, 1869, 
                1870, 1967, 1999, 2000, 2029, 2030, 2031, 2049, 2050, 2076, 2077, 2078, 2079, 2080, 
                2081, 2196, 2197, 2243, 2244, 2245, 2246, 2247, 2279, 2353, 2502, 2503, 2550, 2551, 
                2552, 2554, 2698, 2699, 2700, 2753, 2872, 2971, 3198, 3199, 3238, 3239, 3240, 3247, 
                3248, 3249, 3254, 3256, 3327, 3328, 3329, 3403, 3404, 3405, 3406, 3407, 3408, 3409, 
                3465, 3466, 3669, 3682, 3880, 3881, 3951, 3952, 3953, 4133, 4134, 4135, 4136, 4148, 
                4149, 4150, 4191, 4192, 4214, 4215, 4216, 4239, 4240, 4291, 4342, 4343, 4358, 4359, 
                4360, 4436, 4437, 4438, 4444, 4571, 4660, 4663, 4664, 4665, 4668, 4692, 4693, 4705, 
                4706, 4710, 4711, 4742, 4743, 4747, 4760, 4761, 4762, 4763, 4791, 4793, 4817, 4874, 
                4900, 4953, 4954, 4955, 4956, 4957, 4958, 4959, 4960, 4961, 4962, 4963, 4964, 4965, 
                4966, 4967, 4969, 4970, 4971, 4972, 4973, 4974, 4975, 4986, 5005, 5008, 5009, 5010, 
                5011, 5019, 5020, 5021, 5040, 5052, 5053, 5054, 5056, 5057, 5058, 5059, 5067, 5068, 
                5069, 5080, 5088, 5089, 5090, 5091, 5092, 5148, 5199, 5200, 5201, 5202, 5203, 5204, 
                5205, 5206, 5229, 5230, 5231, 5232, 5233, 5234, 5235, 5236, 5237, 5238, 5239, 5245, 
                5246, 5247, 5253, 5280, 5281, 5288, 5293, 5294, 5307, 5308, 5309, 5332, 5333, 5337, 
                5338, 5342, 5348, 5350, 5383, 5413, 5420, 5421, 5422, 5423, 5425, 5428, 5430, 5431, 
                5437, 5438, 5439, 5442, 5443, 5444, 5445, 5446, 5447, 5448, 5449, 5450, 5453, 5460, 
                5461, 5462, 5463, 5465, 5469, 5471, 5473, 5507, 5508, 5517, 5518, 5524, 5525, 5527, 
                5528, 5532, 5538, 5546, 5552, 5558, 5559, 5560, 5561, 5562, 5570, 5571, 5572, 5576, 
                5582, 5583, 5592, 5594, 5596, 5597, 5603, 5604, 5619, 5621, 5622, 5629, 5630, 5634, 
                5644, 5656, 5660, 5665, 5670, 5671, 5673, 5682, 5702, 5703, 5704, 5712, 5713, 5714, 
                5715, 5716, 5717, 5719, 5720, 5723, 5725, 5734, 5736, 5737, 5743, 5744, 5745, 5800, 
                5801, 5803, 5804, 5805, 5806, 5807, 5808, 5816, 5818, 5819, 5820, 5825, 5831, 5832, 
                5833, 5834, 5835, 5836, 5837, 5838, 5839, 5844, 5845, 5846, 5848, 5849, 5851, 5852, 
                5853, 5854, 5860, 5861, 5864, 5866, 5867, 5868, 5869, 5872, 5874, 5875, 5876, 5877, 
                5878, 5879, 5881, 5883, 5884, 5885, 5889, 5890, 5891, 5892, 5906, 5907, 5908, 5909, 
                5910, 5911, 5920, 5921, 5922, 5923, 5924, 5926, 5933]

    return run_list

def horsepower_dict():
    """ Return the results of manually checking car year+make max horsepower """

    hp_dict = {
    # subaru impreza WRX STI
    '2004 Impreza WRX STI':300, '2005 Impreza WRX STI':300, '2005 Impreza WRX STI Sedan':300, 
    '2006 Impreza WRX STI':300, '2007 Impreza WRX STI':300, '2008 Impreza WRX STI':305, 
    '2008 Impreza WRX STI Hatch':305, '2009 Impreza WRX STI':305, '2010 Impreza WRX STI':305, 
    '2011 Impreza WRX STI':305, '2011 Impreza WRX STI Hatch':305, '2011 Impreza WRX STI Sedan':305, 
    '2012 Impreza WRX STI':305, '2012 Impreza WRX STI Hatch':305, '2012 Impreza WRX STI Sedan':305, 
    '2013 Impreza WRX STI':305, '2013 Impreza WRX STI Hatch':305, '2013 Impreza WRX STI Sedan':305, 
    '2014 Impreza WRX STI':305, '2014 Impreza WRX STI Hatch':305, '2014 Impreza WRX STI Sedan':305, 
    '2015 Impreza WRX STI':305, '2015 WRX STI':305, '2016 WRX STI':305,
    # subaru impreza WRX
    '2002 Impreza WRX':227, '2003 Impreza WRX':227, '2004 Impreza WRX':227, '2005 Impreza WRX':300,
    '2006 Impreza WRX':230, '2007 Impreza WRX':300, '2008 Impreza WRX':305, '2009 Impreza WRX':265,
    '2010 Impreza WRX':265, '2011 Impreza WRX':305, '2012 Impreza WRX':265, '2013 Impreza WRX':265,
    '2014 Impreza WRX':265, '2015 WRX':268, '2015 Impreza WRX':268, '2016 WRX':268,
    # subaru impreza RS
    '1993 Impreza RS':110, '1994 Impreza RS':110, '1995 Impreza RS':135, '1997 Impreza RS':137,
    '1998 Impreza RS':165, '1999 Impreza RS':165, '2000 Impreza RS':165, '2001 Impreza RS':165,
    '2002 Impreza RS':165, '2006 Impreza 2.5i':173,
    # subaru legacy 2.5GT
    '2005 Legacy 2.5GT':250, '2006 Legacy 2.5GT':250, '2007 Legacy 2.5GT':245,
    '2007 Legacy 2.5 spec.B':243, '2008 Legacy 2.5GT':243, '2008 Legacy 2.5 spec.B':243,
    '2009 Legacy 2.5GT':245, '2009 Legacy 2.5 spec.B':243, '2010 Legacy 2.5GT':265, '2012 Legacy 2.5GT':265,
    # subaru legacy
    '1996 Legacy':137, '1998 Legacy':137,
    # subaru forester XT
    '2015 Forester XT':250, '2007 Forester XT':224, '2005 Forester XT':210, '2004 Forester XT':210,
    '2014 Forester XT':250,
    # subaru forester
    '2004 Forester':165, '2005 Forester':165, '2006 Forester':173, '2007 Forester':173, '2008 Forester':173, 
    '2009 Forester':170, '2010 Forester':170, '2012 Forester':170, '2013 Forester':170,
    # subaru outback
    '2002 Outback Sport':165, '2005 Outback XT':250, '2007 Outback XT':243,
    '2008 Outback XT':243, '2009 Outback XT':243,
    # mitsubishi EVO
    '2003 EVO VIII':271, '2006 EVO VIII':405, '2005 EVO IX':276, '2006 EVO IX':286, '2008 EVO X':291,
    '2008 EVO X MR':291, '2008 EVO X GSR':291, '2009 EVO IX':291, '2010 EVO X':291, '2010 EVO X SE':291,
    '2010 EVO X MR':291, '2010 EVO X GSR':291, '2011 EVO X':291, '2011 EVO X MR':291, '2011 EVO X GSR':291,
    '2012 EVO X':291, '2012 EVO X MR':291, '2012 EVO X GSR':291, '2013 EVO X':291, '2013 EVO X MR':291,
    '2013 EVO X GSR':291, '2014 EVO X MR':291, '2014 EVO X GSR':291, '2015 EVO X GSR':291,
    # mitsubishi lancer ralliart
    '2009 Lancer Ralliart':237, '2010 Lancer Ralliart':237, '2011 Lancer Ralliart':237,
    '2013 Lancer Ralliart':237, '2014 Lancer Ralliart':237,
    # mitsubishi eclipse
    '1995 Eclipse GSX':210, '1997 Eclipse GSX':210,
    # nissan GT-R
    '1995 Skyline GTS-T':247, '1995 Skyline R33':280, '2009 GT-R':480, '2010 GT-R':485, '2011 GT-R':485,
    '2012 GT-R':530, '2012 R35':530, '2013 GT-R':545, '2014 GT-R':545, '2015 GT-R':545,
    # nissan Z-variants
    '1976 280Z':171, '1990 300ZX':222, '1991 240SX':155, '1993 300ZX':300, '2006 350Z':287,
    # mazda speed variants
    '2006 Mazdaspeed6':274, '2007 Mazdaspeed3':263, '2007 Mazdaspeed6':215, '2008 Mazdaspeed3':263,
    '2009 Mazdaspeed3':263, '2010 Mazdaspeed3':263, '2011 Mazdaspeed3':263, '2012 Mazdaspeed3':263,
    '2013 Mazdaspeed3':263,
    # mazda miata
    '1991 MX-5/Miata':116, '2005 MX-5/Miata':142,
    # porsche
    '2010 997.2':345, '2010 997.2TT':500, '2011 997.2':500, '2014 991 Turbo S':560, '2015 991 Turbo S':560,
    'Macan 2.0L':261,
    # bmw 1m
    '2011 1M':335, '2012 1M':335,
    # bmw i-variants
    '2007 335i':300, '2008 335i':300, '2008 335xi':300, '2008 535Xi':300, '2008 135i':300,
    '2009 335i':300, '2010 335i':300, '2011 335i':300, '2015 335i':300,
    # volkswagon
    '1997 Golf':117, '2016 Golf R':292, '2012 GTI':200, '2016 GTI':210,
    # infiniti
    '2003 G35':260, '2008 G37':330,
    # ford focus st
    '2013 Focus ST':252, '2014 Focus ST':252,
    # other
    '1997 Supra':320, # toyota
    '2015 Mustang Ecoboost':310, # ford
    '1986 C10 Pickup':165, # chevy
    '2003 SMART':65, # smart
    '1974 914':85, # porsche
    '2005 9-2x':165, # saab
    '2009 Civic Si':197, # honda
    }