###In this script I combined the raw features of colone and humanbonmarrow to run with Height GWAS summary statistics
#importing the imprtant maduals
import pandas as pd
import numpy as np
import os
from pathlib import Path

arr = os.listdir('combine')

out_dir = Path("combine")

for file in arr:
    new_name = prefix + file
    # First rename the files
    os.rename(out_dir / file, out_dir / new_name)
    
    # Read in the data
    df = pd.read_csv(out_dir / new_name, sep="\t", header=0)
    
    # Get the name without extension
    base_name = Path(out_dir / new_name).stem
    print(base_name)
    # Add the file name to the columns
    new_cols = [base_name + "." + column for column in df.columns[1:].values]
    df.columns.values[1:] = new_cols
    
    # Overwrite the existing files with the new data frame
    df.to_csv(out_dir / new_name, sep="\t", index=False, mode="w+")
    

