"""
    Title: Mini Project 2
    Author: Itaru Kishikawa
    Date: Mar 5, 2018
    Class: Adv Python Prog CS122 Sec 02
"""

import pandas as pd


def main():
    """
    Return a list of tuples of the form in result.txt file:
    (zipcode, mean score, number of restaurants)
    for each of the 92 zipcodes in NYC with over 100 restaurants.

    If there are multiple inspection reports for one restaurant,
    use the latest inspection date only. Sort the list in descending order by mean score.

    :return:Return a list of tuples of the form:
    (zipcode, mean score, number of restaurants)
    """

    df = pd.read_csv('data/data.txt', encoding='cp1252')

    # Drop duplicates and keep most recent inspection date -----------------------------------------------------
    df = df.sort_values(by=["CAMIS", 'INSPDATE'], ascending=False)
    df = df.drop_duplicates(subset=["CAMIS"], keep='first')
    # ----------------------------------------------------------------------------------------------------------

    # Clean up ZIPCODE -----------------------------------------------------------------------------------------
    df = df.dropna(subset=['ZIPCODE'])                               # Drop the null values from the zipcode column.
    df = df[(df['ZIPCODE'] >= 10001) & (df['ZIPCODE'] <= 11697)]     # Drop outside of range in NYC (10001 ~ 11697)
    # ----------------------------------------------------------------------------------------------------------

    # Drop if the number of element in each ZIPCODE is less than 100
    df = df.groupby('ZIPCODE').filter(lambda x: len(x) > 100)

    # Get the mean score and the number of restaurants for each zipcodes
    result_df = df.groupby('ZIPCODE')['SCORE'].agg(['mean', 'size'])

    # Transferring data to tuple
    result = [tuple(x) for x in result_df.to_records(index=True)]

    # Write tuple to text file --------------------------------------------------------------------------------
    with open('result.txt', 'w') as file:
        file.write('\n' + 'ZIPCODE           Mean Score     Number of Restaurants' + '\n' + '\n')
        for t in result:
            line = '%7s  %20s  %12s' % (str(t[0]), str(t[1]), str(t[2]))
            file.write(line + '\n')
    # ---------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    main()
