import numpy as np
import pandas as pd

#Remove unnamed and Name_y colums from the dataset
df = pd.read_csv(r".\Data\final_dataset.csv")
df.drop(columns=["Unnamed: 0", "Name_y"], inplace=True)
print(df.dtypes)

#Remove rows were Name_x field is empty
initial_rows = len(df)
df = df.dropna(subset=["Name_x"])

final_rows = len(df)

deleted_rows = initial_rows - final_rows

print(f"{deleted_rows} rows were removed.")

#Resave the file
df.to_csv(r".\Data\final_dataset.csv", index=False)