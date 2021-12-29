import pandas as pd
import re
import tabula
import os

def fix_pdfs(folder_path):
    """ Takes in folder path for Cobb tuning PDFs, 
        Converts all PDFs into proper dataframes,
        Returns list of dataframes. """
    # Get filepaths of PDFs in given folder
    pdf_filepath_list = iterate_pdfs(folder_path)
    # Initialize empty df dict
    df_dict = {}
    # Read each filepath
    for filepath in pdf_filepath_list:
        # Get file name from file path
        head, filename = os.path.split(filepath)
        # Convert from PDF to df using tabula, fix rows, 
        # assign df to dict using file name as key
        df_dict[filename] = fix_dyno_pdf(pdf_to_df(filepath))

    return df_dict

def fix_dyno_pdf(df):
    """ Reformats a dyno.cobbtuning.com performance data PDF from 
        the raw tabula-py read_pdf function into a proper dataframe.
        The issue comes from not having column names on each page,
        causing the values for each column to concatenate into one 
        column. Using regex, this function splits this concatenation 
        back out into the proper columns, sets the df dtypes to float, 
        and returns the fixed dataframe. It works because each column
        after RPM has two decimal places of precision. """
        
    # iterate each row in the column that has concatenated values
    for i, item in enumerate(df['RPM']):
        # check for concatenation
        if len(item) > 5:
            # assign RPM using first four characters
            RPM = item[:4]
            # delete RPM from string
            item = item[4:]

            # grab all characters through two decimal places of precision
            HP = re.findall(r'.*?\.\w\w', item)[0]
            # except: HP = re.findall(r'..\.\w\w', item)[0]
            # delete HP from string
            item = item[len(HP):]

            # grab all characters through two decimal places of precision
            Torque = re.findall(r'.*?\.\w\w', item)[0]
            # except: Torque = re.findall(r'..\.\w\w', item)[0]
            # delete Torque from string
            item = item[len(Torque):]

            # grab all characters through two decimal places of precision
            AFR = re.findall(r'.*?\.\w\w', item)[0]
            # except: AFR = re.findall(r'.\.\w\w', item)[0]
            # delete AFR from string
            item = item[len(AFR):]
            
            # grab all characters through two decimal places of precision
            Boost = re.findall(r'.*?\.\w\w', item)[0]

            # assign each value back to the row in their proper columns
            df.loc[i] = {'RPM':RPM, 'HP':HP, 'Torque':Torque, 'AFR':AFR, 'Boost':Boost}
        else:
            continue

    # fix dataframe dtype
    df = df.astype('float')

    return df

def pdf_to_df(filepath):
    """ Uses tabula-py to read a PDF into a df, returns df """
    # Grab all pages of pdf into one dataframe
    df = tabula.read_pdf(filepath, # location of pdf
                         pages='all', # pull all pages of pdf
                         multiple_tables=False # into one df
                         )[0] # df located at list index 0
    
    return df

def iterate_pdfs(folder_path):
    """ Returns filepath list of all PDFs in given directory """
    # Initialize empty list
    pdf_filepath_list = []
    # Iterate all files
    for entry in os.scandir(folder_path):
        # Identify PDFs
        if entry.path.endswith(".pdf") and entry.is_file():
            # Add PDF filepath to list
            pdf_filepath_list.append(entry.path)
    
    return pdf_filepath_list