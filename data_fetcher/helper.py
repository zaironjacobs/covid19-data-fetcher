import pandas as pd

from . import constants


def clean_data(file_name):
    """
    Convert negative numbers to positive numbers and remove unwanted columns
    """

    df = pd.read_csv(constants.data_dir + file_name)

    # Remove all .0
    df.fillna(0, inplace=True, downcast='infer')

    # Convert all negative numbers to positive numbers
    for column in constants.cases_columns:
        df[column] = df[column].abs()

    # Drop all unwanted columns
    df = df.drop(columns=constants.unwanted_columns)

    df.to_csv(constants.data_dir + file_name, index=False)
