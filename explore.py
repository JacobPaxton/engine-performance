import pandas as pd

def check_non_keywords(df):
    """ Check value counts of words I did not designate as keywords in car specs column """
    # check all rows without keywords for each unique word's value counts in entire list
    print(
        pd.Series( # make a Series of each instance of each word
            ' '.join(
                    df[~df.has_keyword]    # look at rows we haven't caught with a keyword yet
                    .specs.tolist()        # put all 'specs' cells in a list
                    ).split()        # join all lists into one string, then split the string into a list of each word
        ).value_counts()        # calculate the value counts of each word in the series
        .head(25)         # display the top 25 keywords
    )