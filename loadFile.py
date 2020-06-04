import numpy as np
import pandas as pd
import os 
import xlrd

def read_excel(fname):
    
    df=pd.read_excel(fname, 
                    header=1,
                    usecols="C:F",
                    convert_float=True)
    
    arr=df.to_numpy()
    return arr


