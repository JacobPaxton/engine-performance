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
    # using first-4 characters as year
    info['car_year'] = info.Car.str[:4]
    # splitting the rest of the string into make and model
    make_model = info.Car.str.extract(r'\W(.*?)\W(.*?)$')
    # using the second word as the make
    info['car_make'] = make_model[0]
    # using the last portion as the model
    info['car_model'] = make_model[1]
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

def runs_to_drop():
    """ 
        Return a list of runs dropped when cleaning dyno_runs.csv.
        This list is needed for when we clean car_info.csv.
    """
    run_list = [94, 101, 209, 210, 211, 266, 267, 268, 270, 271, 272, 273, 274, 275, 276, 278, 
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