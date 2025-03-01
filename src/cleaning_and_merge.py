import dataclasses

import numpy as np
import pandas as pd


@dataclasses.dataclass
class Dataset:
    """This class holds file and the corresponding columns that are contained in this file."""

    filename: str
    """Name of the file"""
    columns_to_convert: list[str]
    """All columns in the file"""
    columns_subset: list[str]
    """Columns that need to be cleaned up"""


# Step 2. Replace missing values with NaN and remove duplicates
def clean_data(df):
    # the function replaces the missing values with NaN and removes duplicates
    df.replace(["N/A", "<NA>"], np.nan, inplace=True)
    df.drop_duplicates(inplace=True)
    return df


def clean_data_in_file(input_data: Dataset) -> pd.DataFrame:
    # Step 1. Loading CSV into a dataframe, row 1 is the header
    df = pd.read_csv(input_data.filename, header=0)

    # Checking datatypes
    print(f"table data types are: \n{df.dtypes}")

    df = clean_data(df)

    # Step 3. Remove the column with numbering
    df.drop(columns=["Unnamed: 0"], inplace=True)

    # Step 4. Correct the datatype object to string
    df[input_data.columns_to_convert] = df[input_data.columns_to_convert].astype(
        "string"
    )
    print(f"The updated table data types are: \n{df.dtypes}")

    # Step 5. Remove empty rows
    initial_rows = len(df)
    df = df.dropna(subset=input_data.columns_subset, how="all")
    final_rows1 = len(df)

    rows_removed1 = initial_rows - final_rows1
    print(f"{rows_removed1} empty rows were removed from the dataset")
    return df


def clean_and_merge(input_data1: Dataset, input_data2: Dataset) -> pd.DataFrame:
    """Cleans and merges two datasets, returns the merged dataframe"""
    df1 = clean_data_in_file(input_data=input_data1)
    df2 = clean_data_in_file(input_data=input_data2)

    # Step 6. Merge the two datasets into one and save as a new CSV
    df_final = pd.merge(
        df1, df2, how="right", on="Glottocode", sort=False, validate="many_to_one"
    )
    return df_final


input_data1 = Dataset(
    filename="./Data/UNESCO_languages.csv",
    columns_to_convert=["Name", "Status", "Link", "Glottocode", "Country"],
    columns_subset=["Status", "Glottocode", "Country"],
)
input_data2 = Dataset(
    filename="./Data/Glottolog_languages.csv",
    columns_to_convert=[
        "Name",
        "Top-level family",
        "ISO-639-3",
        "Glottocode",
        "Macroarea",
    ],
    columns_subset=["Name", "Glottocode"],
)

df_final = clean_and_merge(input_data1=input_data1, input_data2=input_data2)

df_final.to_csv(r".\Data\final_dataset.csv")

# Step 8. Exploratory analysis
df_final.info()
df_final.describe(include="all")
