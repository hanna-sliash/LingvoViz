import numpy as np
import pandas as pd



def clean_and_merge(input_files:list[str]):
      
    # Step 1. Loading CSV into a dataframe, row 1 is the header in both tables
    df1 = pd.read_csv(input_files[0], header=0)
    df2 = pd.read_csv("./Data/Glottolog_languages.csv", header=0)
# Step 1. Loading CSV into a dataframe, row 1 is the header in both tables

df1 = pd.read_csv("./Data/UNESCO_languages.csv", header=0)
df2 = pd.read_csv("./Data/Glottolog_languages.csv", header=0)

    
# Checking datatypes
print(f"The UNESCO table data types are: \n{df1.dtypes}")
print(f"The Glottolog table data types are: \n{df2.dtypes}")


# Step 2. Replace missing values with NaN and remove duplicates
def clean_data(df):
    # the function replaces the missing values with NaN and removes duplicates
    df.replace(["N/A", "<NA>"], np.nan, inplace=True)
    df.drop_duplicates(inplace=True)
    return df


df1 = clean_data(df1)
df2 = clean_data(df2)

# Step 3. Remove the column with numbering
df1.drop(columns=["Unnamed: 0"], inplace=True)
df2.drop(columns=["Unnamed: 0"], inplace=True)

# Step 4. Correct the datatype object to string
columns_to_convert1 = ["Name", "Status", "Link", "Glottocode", "Country"]
columns_to_convert2 = [
    "Name",
    "Top-level family",
    "ISO-639-3",
    "Glottocode",
    "Macroarea",
]
df1[columns_to_convert1] = df1[columns_to_convert1].astype("string")
df2[columns_to_convert2] = df2[columns_to_convert2].astype("string")
print(f"The updated UNESCO table data types are: \n{df1.dtypes}")
print(f"The updated Glottolog table data types are: \n{df2.dtypes}")

# Step 5. Remove empty rows
initial_rows1 = len(df1)
initial_rows2 = len(df2)
df1 = df1.dropna(subset=["Status", "Glottocode", "Country"], how="all")
df2 = df2.dropna(subset=["Name", "Glottocode"], how="all")
final_rows1 = len(df1)
final_rows2 = len(df2)

rows_removed1 = initial_rows1 - final_rows1
print(f"{rows_removed1} empty rows were removed from UNESCO dataset")
rows_removed2 = initial_rows2 - final_rows2
print(f"{rows_removed2} empty rows were removed from Glottolog dataset")

# Step 6. Merge the two datasets into one and save as a new CSV
df_final = pd.merge(
    df1, df2, how="right", on="Glottocode", sort=False, validate="many_to_one"
)
df_final.to_csv(r".\Data\final_dataset.csv")

# Step 8. Exploratory analysis
df_final.info()
df_final.describe(include="all")
